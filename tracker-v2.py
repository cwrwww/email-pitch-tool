"""
轻量级邮件追踪服务 V2
- 移除Google Sheet依赖
- 使用SQLite存储
- 提供API供本地应用拉取数据
"""

from flask import Flask, request, send_file, jsonify
import datetime
import io
import os
import sqlite3

app = Flask(__name__)

# 数据库文件（Render会持久化）
DB_FILE = "tracker.db"

def init_db():
    """初始化数据库"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS opens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uid INTEGER,
            timestamp TEXT,
            ip TEXT,
            user_agent TEXT,
            synced INTEGER DEFAULT 0
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clicks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uid INTEGER,
            url TEXT,
            timestamp TEXT,
            ip TEXT,
            synced INTEGER DEFAULT 0
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_opens_uid ON opens(uid)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_opens_synced ON opens(synced)")
    conn.commit()
    conn.close()

# 启动时初始化数据库
init_db()

@app.route("/")
def home():
    """服务状态"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    opens_count = cursor.execute("SELECT COUNT(*) FROM opens").fetchone()[0]
    clicks_count = cursor.execute("SELECT COUNT(*) FROM clicks").fetchone()[0]
    unsynced = cursor.execute("SELECT COUNT(*) FROM opens WHERE synced=0").fetchone()[0]
    conn.close()

    return jsonify({
        "service": "Email Tracker V2",
        "status": "running",
        "total_opens": opens_count,
        "total_clicks": clicks_count,
        "unsynced_opens": unsynced
    })

@app.route("/health")
def health():
    """健康检查"""
    return jsonify({"status": "ok"})

@app.route("/open")
def open_tracker():
    """追踪邮件打开"""
    uid = request.args.get("uid", "unknown")
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ua = request.headers.get("User-Agent", "")
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 记录到数据库
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO opens (uid, timestamp, ip, user_agent) VALUES (?, ?, ?, ?)",
            (uid, ts, ip, ua)
        )
        conn.commit()
        conn.close()
        print(f"📩 Open recorded: uid={uid}, ip={ip}")
    except Exception as e:
        print(f"Error recording open: {e}")

    # 返回1x1透明GIF
    gif_bytes = (
        b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00"
        b"\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,"
        b"\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02"
        b"D\x01\x00;"
    )
    return send_file(io.BytesIO(gif_bytes), mimetype="image/gif")

@app.route("/click")
def click_tracker():
    """追踪链接点击"""
    uid = request.args.get("uid", "unknown")
    url = request.args.get("url", "")
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 记录到数据库
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO clicks (uid, url, timestamp, ip) VALUES (?, ?, ?, ?)",
            (uid, url, ts, ip)
        )
        conn.commit()
        conn.close()
        print(f"🔗 Click recorded: uid={uid}, url={url}")
    except Exception as e:
        print(f"Error recording click: {e}")

    # 重定向到目标URL
    from flask import redirect
    return redirect(url) if url else "No URL provided"

# ============================================
# API端点 - 供本地应用拉取数据
# ============================================

@app.route("/api/opens")
def get_opens():
    """获取打开记录（未同步的）"""
    limit = request.args.get("limit", 1000, type=int)
    all_records = request.args.get("all", "false").lower() == "true"

    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if all_records:
        # 获取所有记录
        opens = cursor.execute(
            "SELECT * FROM opens ORDER BY id DESC LIMIT ?",
            (limit,)
        ).fetchall()
    else:
        # 只获取未同步的
        opens = cursor.execute(
            "SELECT * FROM opens WHERE synced=0 ORDER BY id DESC LIMIT ?",
            (limit,)
        ).fetchall()

    result = [dict(row) for row in opens]
    conn.close()

    return jsonify({
        "count": len(result),
        "opens": result
    })

@app.route("/api/clicks")
def get_clicks():
    """获取点击记录（未同步的）"""
    limit = request.args.get("limit", 1000, type=int)
    all_records = request.args.get("all", "false").lower() == "true"

    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if all_records:
        clicks = cursor.execute(
            "SELECT * FROM clicks ORDER BY id DESC LIMIT ?",
            (limit,)
        ).fetchall()
    else:
        clicks = cursor.execute(
            "SELECT * FROM clicks WHERE synced=0 ORDER BY id DESC LIMIT ?",
            (limit,)
        ).fetchall()

    result = [dict(row) for row in clicks]
    conn.close()

    return jsonify({
        "count": len(result),
        "clicks": result
    })

@app.route("/api/mark_synced", methods=["POST"])
def mark_synced():
    """标记记录为已同步"""
    data = request.get_json()
    open_ids = data.get("open_ids", [])
    click_ids = data.get("click_ids", [])

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    marked = 0
    for oid in open_ids:
        cursor.execute("UPDATE opens SET synced=1 WHERE id=?", (oid,))
        marked += cursor.rowcount

    for cid in click_ids:
        cursor.execute("UPDATE clicks SET synced=1 WHERE id=?", (cid,))
        marked += cursor.rowcount

    conn.commit()
    conn.close()

    return jsonify({
        "status": "ok",
        "marked": marked
    })

@app.route("/api/stats")
def get_stats():
    """统计信息"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    total_opens = cursor.execute("SELECT COUNT(*) FROM opens").fetchone()[0]
    total_clicks = cursor.execute("SELECT COUNT(*) FROM clicks").fetchone()[0]
    unsynced_opens = cursor.execute("SELECT COUNT(*) FROM opens WHERE synced=0").fetchone()[0]
    unsynced_clicks = cursor.execute("SELECT COUNT(*) FROM clicks WHERE synced=0").fetchone()[0]

    # 最近24小时
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    recent_opens = cursor.execute(
        "SELECT COUNT(*) FROM opens WHERE timestamp > ?",
        (yesterday,)
    ).fetchone()[0]

    conn.close()

    return jsonify({
        "total_opens": total_opens,
        "total_clicks": total_clicks,
        "unsynced_opens": unsynced_opens,
        "unsynced_clicks": unsynced_clicks,
        "recent_opens_24h": recent_opens
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
