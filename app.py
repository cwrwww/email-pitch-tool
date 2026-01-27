"""Email Pitch Tool - 轻量级邮件营销工具 MVP"""
import os
import io
import csv
import json
import sqlite3
import base64
from datetime import datetime, timedelta
from pathlib import Path
from contextlib import contextmanager
from typing import Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from jinja2 import Template
from openpyxl import load_workbook
from email_validator import validate_email, EmailNotValidError
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from apscheduler.schedulers.background import BackgroundScheduler
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

app = FastAPI(title="Email Pitch Tool")
scheduler = BackgroundScheduler()
scheduler.start()

# 配置
DB_PATH = "data.db"
CREDENTIALS_FILE = "credentials.json"  # 从Google Cloud Console下载
SCOPES = ['https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.readonly']
REDIRECT_URI = "http://localhost:8000/oauth/callback"
TEST_MODE = os.environ.get("TEST_MODE", "false").lower() == "true"  # 测试模式不发真邮件

# 数据库初始化
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY, email TEXT UNIQUE, token TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS campaigns (
                id INTEGER PRIMARY KEY, name TEXT, status TEXT DEFAULT 'draft',
                account_email TEXT, interval_minutes INTEGER DEFAULT 5,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS templates (
                id INTEGER PRIMARY KEY, campaign_id INTEGER, step INTEGER, subject TEXT, body TEXT,
                delay_days INTEGER DEFAULT 0, FOREIGN KEY(campaign_id) REFERENCES campaigns(id)
            );
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY, campaign_id INTEGER, email TEXT, data TEXT,
                status TEXT DEFAULT 'pending', current_step INTEGER DEFAULT 1,
                last_sent_at TIMESTAMP, opened INTEGER DEFAULT 0, clicked INTEGER DEFAULT 0, replied INTEGER DEFAULT 0,
                FOREIGN KEY(campaign_id) REFERENCES campaigns(id)
            );
            CREATE TABLE IF NOT EXISTS blacklist (email TEXT PRIMARY KEY);
        """)
init_db()

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try: yield conn
    finally: conn.close()

# Gmail OAuth
@app.get("/oauth/start")
def oauth_start():
    if not Path(CREDENTIALS_FILE).exists():
        return {"error": "请先下载credentials.json到项目根目录"}
    flow = Flow.from_client_secrets_file(CREDENTIALS_FILE, scopes=SCOPES, redirect_uri=REDIRECT_URI)
    auth_url, _ = flow.authorization_url(prompt='consent')
    return RedirectResponse(auth_url)

@app.get("/oauth/callback")
def oauth_callback(code: str):
    flow = Flow.from_client_secrets_file(CREDENTIALS_FILE, scopes=SCOPES, redirect_uri=REDIRECT_URI)
    flow.fetch_token(code=code)
    creds = flow.credentials
    service = build('gmail', 'v1', credentials=creds)
    profile = service.users().getProfile(userId='me').execute()
    email = profile['emailAddress']
    with get_db() as conn:
        conn.execute("INSERT OR REPLACE INTO accounts(email, token) VALUES(?, ?)",
                    (email, creds.to_json()))
        conn.commit()
    return RedirectResponse("/?msg=账号绑定成功: " + email)

# API 路由
@app.post("/api/campaigns")
def create_campaign(name: str = Form(...)):
    with get_db() as conn:
        cur = conn.execute("INSERT INTO campaigns(name) VALUES(?)", (name,))
        conn.commit()
        return {"id": cur.lastrowid, "name": name}

@app.get("/api/campaigns")
def list_campaigns():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM campaigns ORDER BY id DESC").fetchall()
        return [dict(r) for r in rows]

@app.post("/api/campaigns/{cid}/templates")
def add_template(cid: int, step: int = Form(...), subject: str = Form(...), body: str = Form(...), delay_days: int = Form(0)):
    with get_db() as conn:
        conn.execute("INSERT INTO templates(campaign_id, step, subject, body, delay_days) VALUES(?,?,?,?,?)",
                    (cid, step, subject, body, delay_days))
        conn.commit()
    return {"ok": True}

@app.get("/api/campaigns/{cid}/templates")
def get_templates(cid: int):
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM templates WHERE campaign_id=? ORDER BY step", (cid,)).fetchall()
        return [dict(r) for r in rows]

@app.post("/api/campaigns/{cid}/leads")
async def upload_leads(cid: int, file: UploadFile = File(...)):
    content = await file.read()
    rows = []

    if file.filename.endswith('.csv'):
        text = content.decode('utf-8-sig')
        reader = csv.DictReader(io.StringIO(text))
        rows = list(reader)
    else:
        wb = load_workbook(io.BytesIO(content), read_only=True)
        ws = wb.active
        headers = [cell.value for cell in next(ws.iter_rows(max_row=1))]
        for row in ws.iter_rows(min_row=2, values_only=True):
            rows.append(dict(zip(headers, row)))

    if not rows or 'email' not in rows[0]:
        raise HTTPException(400, "文件必须包含email列")

    added, skipped = 0, 0
    with get_db() as conn:
        blacklist = {r[0] for r in conn.execute("SELECT email FROM blacklist").fetchall()}
        existing = {r[0] for r in conn.execute("SELECT email FROM leads WHERE campaign_id=?", (cid,)).fetchall()}

        for row in rows:
            email = str(row.get('email', '')).strip().lower()
            try:
                validate_email(email)
                if email in blacklist or email in existing:
                    skipped += 1; continue
                data = {k: v for k, v in row.items() if k != 'email'}
                conn.execute("INSERT INTO leads(campaign_id, email, data) VALUES(?,?,?)",
                            (cid, email, json.dumps(data, default=str)))
                added += 1
            except EmailNotValidError:
                skipped += 1
        conn.commit()
    return {"added": added, "skipped": skipped}

@app.get("/api/campaigns/{cid}/leads")
def get_leads(cid: int):
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM leads WHERE campaign_id=?", (cid,)).fetchall()
        return [dict(r) for r in rows]

@app.post("/api/campaigns/{cid}/leads/json")
async def add_leads_json(cid: int, request: Request):
    """支持JSON格式批量导入leads"""
    rows = await request.json()

    added, skipped = 0, 0
    errors = []
    with get_db() as conn:
        blacklist = {r[0] for r in conn.execute("SELECT email FROM blacklist").fetchall()}
        existing = {r[0] for r in conn.execute("SELECT email FROM leads WHERE campaign_id=?", (cid,)).fetchall()}

        for row in rows:
            email = str(row.get('email', '')).strip().lower()
            if not email:
                errors.append("空邮箱")
                skipped += 1
                continue
            try:
                # 使用宽松模式验证邮箱
                validate_email(email, check_deliverability=False)
                if email in blacklist:
                    errors.append(f"{email}: 在黑名单中")
                    skipped += 1
                    continue
                if email in existing:
                    errors.append(f"{email}: 已存在")
                    skipped += 1
                    continue
                data = {k: v for k, v in row.items() if k != 'email'}
                conn.execute("INSERT INTO leads(campaign_id, email, data) VALUES(?,?,?)",
                            (cid, email, json.dumps(data, default=str)))
                existing.add(email)
                added += 1
            except EmailNotValidError as e:
                errors.append(f"{email}: {str(e)}")
                skipped += 1
        conn.commit()
    return {"added": added, "skipped": skipped, "errors": errors[:5]}

@app.get("/api/campaigns/{cid}/preview")
def preview_email(cid: int, lead_id: int, step: int = 1):
    with get_db() as conn:
        lead = conn.execute("SELECT * FROM leads WHERE id=?", (lead_id,)).fetchone()
        tpl = conn.execute("SELECT * FROM templates WHERE campaign_id=? AND step=?", (cid, step)).fetchone()
        if not lead or not tpl: raise HTTPException(404)
        data = json.loads(lead['data'])
        data['email'] = lead['email']
        return {
            "subject": Template(tpl['subject']).render(**data),
            "body": Template(tpl['body']).render(**data)
        }

@app.post("/api/campaigns/{cid}/launch")
def launch_campaign(cid: int, account_email: str = Form(...), interval_minutes: int = Form(5)):
    with get_db() as conn:
        conn.execute("UPDATE campaigns SET status='running', account_email=?, interval_minutes=? WHERE id=?",
                    (account_email, interval_minutes, cid))
        conn.commit()
    scheduler.add_job(process_campaign, 'interval', minutes=interval_minutes,
                      args=[cid, account_email], id=f"campaign_{cid}", replace_existing=True)
    return {"ok": True, "msg": f"已启动，每{interval_minutes}分钟发送一封"}

@app.get("/api/campaigns/{cid}")
def get_campaign(cid: int):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM campaigns WHERE id=?", (cid,)).fetchone()
        if not row: raise HTTPException(404)
        return dict(row)

@app.post("/api/campaigns/{cid}/stop")
def stop_campaign(cid: int):
    with get_db() as conn:
        conn.execute("UPDATE campaigns SET status='paused' WHERE id=?", (cid,))
        conn.commit()
    try: scheduler.remove_job(f"campaign_{cid}")
    except: pass
    return {"ok": True}

def send_gmail(account_email: str, to: str, subject: str, body: str) -> bool:
    if TEST_MODE:
        print(f"[TEST MODE] Would send email:")
        print(f"  From: {account_email}")
        print(f"  To: {to}")
        print(f"  Subject: {subject}")
        print(f"  Body: {body[:200]}...")
        return True

    with get_db() as conn:
        row = conn.execute("SELECT token FROM accounts WHERE email=?", (account_email,)).fetchone()
        if not row: return False
    creds = Credentials.from_authorized_user_info(json.loads(row['token']))
    service = build('gmail', 'v1', credentials=creds)
    msg = MIMEMultipart('alternative')
    msg['To'], msg['Subject'] = to, subject
    msg.attach(MIMEText(body, 'html'))
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    service.users().messages().send(userId='me', body={'raw': raw}).execute()
    return True

def check_replies(cid: int, account_email: str):
    """检查收件箱，标记已回复的leads"""
    if TEST_MODE:
        print(f"[TEST MODE] Skipping reply check for campaign {cid}")
        return

    with get_db() as conn:
        row = conn.execute("SELECT token FROM accounts WHERE email=?", (account_email,)).fetchone()
        if not row: return

        # 获取该campaign所有待处理的lead邮箱
        leads = conn.execute(
            "SELECT id, email FROM leads WHERE campaign_id=? AND replied=0 AND status='pending'", (cid,)
        ).fetchall()
        if not leads: return

        lead_emails = {l['email'].lower(): l['id'] for l in leads}

        try:
            creds = Credentials.from_authorized_user_info(json.loads(row['token']))
            service = build('gmail', 'v1', credentials=creds)

            # 查询最近7天的收件邮件
            results = service.users().messages().list(
                userId='me', q='in:inbox newer_than:7d', maxResults=100
            ).execute()

            messages = results.get('messages', [])
            for msg in messages:
                msg_detail = service.users().messages().get(
                    userId='me', id=msg['id'], format='metadata',
                    metadataHeaders=['From']
                ).execute()

                headers = msg_detail.get('payload', {}).get('headers', [])
                from_header = next((h['value'] for h in headers if h['name'] == 'From'), '')

                # 提取发件人邮箱
                import re
                match = re.search(r'<(.+?)>', from_header)
                sender = (match.group(1) if match else from_header).lower().strip()

                # 如果发件人在我们的leads列表中，标记为已回复
                if sender in lead_emails:
                    lead_id = lead_emails[sender]
                    conn.execute("UPDATE leads SET replied=1, status='replied' WHERE id=?", (lead_id,))
                    print(f"[Reply detected] Lead {lead_id} ({sender}) replied")

            conn.commit()
        except Exception as e:
            print(f"[Check replies error] {e}")

def process_campaign(cid: int, account_email: str):
    # 先检查回复
    check_replies(cid, account_email)

    with get_db() as conn:
        lead = conn.execute("""
            SELECT l.* FROM leads l WHERE l.campaign_id=? AND l.status='pending' AND l.replied=0
            AND (l.last_sent_at IS NULL OR datetime(l.last_sent_at, '+' ||
                (SELECT delay_days FROM templates WHERE campaign_id=? AND step=l.current_step) || ' days') <= datetime('now'))
            LIMIT 1
        """, (cid, cid)).fetchone()
        if not lead: return

        tpl = conn.execute("SELECT * FROM templates WHERE campaign_id=? AND step=?",
                          (cid, lead['current_step'])).fetchone()
        if not tpl:
            conn.execute("UPDATE leads SET status='completed' WHERE id=?", (lead['id'],))
            conn.commit(); return

        data = json.loads(lead['data'])
        data['email'] = lead['email']
        subject = Template(tpl['subject']).render(**data)
        body = Template(tpl['body']).render(**data)

        # 添加追踪像素
        track_pixel = f'<img src="http://localhost:8000/track/open/{lead["id"]}" width="1" height="1">'
        body += track_pixel

        if send_gmail(account_email, lead['email'], subject, body):
            next_tpl = conn.execute("SELECT * FROM templates WHERE campaign_id=? AND step=?",
                                   (cid, lead['current_step'] + 1)).fetchone()
            new_status = 'pending' if next_tpl else 'completed'
            conn.execute("UPDATE leads SET current_step=current_step+1, last_sent_at=?, status=? WHERE id=?",
                        (datetime.now(), new_status, lead['id']))
            conn.commit()

# 追踪
@app.get("/track/open/{lead_id}")
def track_open(lead_id: int):
    with get_db() as conn:
        conn.execute("UPDATE leads SET opened=1 WHERE id=?", (lead_id,))
        conn.commit()
    # 返回1x1透明GIF
    gif = base64.b64decode("R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7")
    return HTMLResponse(content=gif, media_type="image/gif")

@app.get("/track/click/{lead_id}")
def track_click(lead_id: int, url: str):
    with get_db() as conn:
        conn.execute("UPDATE leads SET clicked=1 WHERE id=?", (lead_id,))
        conn.commit()
    return RedirectResponse(url)

@app.get("/api/accounts")
def list_accounts():
    with get_db() as conn:
        rows = conn.execute("SELECT id, email, created_at FROM accounts").fetchall()
        accounts = [dict(r) for r in rows]
        # 测试模式下添加虚拟账号
        if TEST_MODE and not accounts:
            conn.execute("INSERT OR IGNORE INTO accounts(email, token) VALUES(?, ?)",
                        ("test@example.com", "{}"))
            conn.commit()
            accounts = [{"id": 1, "email": "test@example.com", "created_at": "test"}]
        return accounts

@app.get("/api/campaigns/{cid}/stats")
def campaign_stats(cid: int):
    with get_db() as conn:
        stats = conn.execute("""
            SELECT COUNT(*) as total, SUM(opened) as opens, SUM(clicked) as clicks, SUM(replied) as replies,
            SUM(CASE WHEN status IN ('completed', 'replied') OR current_step > 1 THEN 1 ELSE 0 END) as sent
            FROM leads WHERE campaign_id=?
        """, (cid,)).fetchone()
        return dict(stats)

@app.post("/api/campaigns/{cid}/check-replies")
def check_replies_now(cid: int):
    """手动触发检查回复"""
    with get_db() as conn:
        campaign = conn.execute("SELECT account_email FROM campaigns WHERE id=?", (cid,)).fetchone()
        if not campaign or not campaign['account_email']:
            return {"msg": "请先启动campaign以设置发件账号"}
    check_replies(cid, campaign['account_email'])
    return {"msg": "检查完成"}

@app.post("/api/leads/{lead_id}/mark")
def mark_lead(lead_id: int, field: str):
    """手动标记lead状态（用于测试）"""
    if field not in ('opened', 'clicked', 'replied'):
        raise HTTPException(400, "Invalid field")
    with get_db() as conn:
        if field == 'replied':
            conn.execute("UPDATE leads SET replied=1, status='replied' WHERE id=?", (lead_id,))
        else:
            conn.execute(f"UPDATE leads SET {field}=1 WHERE id=?", (lead_id,))
        conn.commit()
    return {"ok": True}

# 前端页面
@app.get("/", response_class=HTMLResponse)
def index():
    return Path("index.html").read_text(encoding='utf-8')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
