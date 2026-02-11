# 🚀 Email Pitch Tool - 云端部署指南

## 快速开始：Railway 部署（推荐）

### 为什么选择 Railway？
- ✅ 部署超简单（3分钟）
- ✅ 每月 $5 免费额度
- ✅ 不会休眠
- ✅ 自动HTTPS
- ✅ 持久化存储支持

---

## 📋 部署前准备

### 1. 创建 Railway 账号
访问：https://railway.app/
- 使用 GitHub 账号登录（推荐）
- 绑定信用卡验证（不会扣费，只是验证）

### 2. 准备 Google OAuth 凭据
⚠️ **重要**: 部署前必须更新 Google Cloud Console 的回调URL

1. 访问：https://console.cloud.google.com/apis/credentials
2. 找到你的 OAuth 2.0 客户端ID
3. 在"已获授权的重定向 URI"中添加：
   ```
   https://your-app-name.up.railway.app/oauth/callback
   ```
   （部署后会得到实际URL，到时再更新）

---

## 🚂 Railway 部署步骤

### 方法1: GitHub 部署（推荐）⭐

#### 步骤1: 推送代码到 GitHub
```bash
cd D:\dev\vibecode\email-pitch-tool

# 如果还没初始化git
git init
git add .
git commit -m "Initial commit"

# 创建GitHub仓库后
git remote add origin https://github.com/your-username/email-pitch-tool.git
git branch -M main
git push -u origin main
```

#### 步骤2: 在 Railway 上部署
1. 访问 https://railway.app/new
2. 点击 "Deploy from GitHub repo"
3. 选择你的仓库 `email-pitch-tool`
4. Railway 会自动检测到是 Python 项目并开始构建

#### 步骤3: 配置环境变量
在 Railway 项目页面：
1. 点击项目 → Variables 标签
2. 添加以下环境变量：

```bash
# 必需
BASE_URL=https://your-app-name.up.railway.app

# 可选（如果需要测试模式）
TEST_MODE=false
```

3. 点击 "Deploy" 重新部署

#### 步骤4: 上传 credentials.json
⚠️ **重要**: credentials.json 不能提交到 GitHub（已在 .gitignore 中）

**选项A: 使用 Railway CLI**
```bash
# 安装 Railway CLI
npm i -g @railway/cli

# 登录
railway login

# 链接到项目
railway link

# 上传文件
railway run bash
# 然后在 Railway shell 中上传 credentials.json
# 或使用 railway volumes 功能
```

**选项B: 手动配置（推荐）**
在 Railway 项目中：
1. 添加环境变量 `GOOGLE_CLIENT_ID` 和 `GOOGLE_CLIENT_SECRET`
2. 修改 app.py 使用环境变量而不是 credentials.json

#### 步骤5: 更新 Google OAuth 回调URL
1. 获取 Railway 提供的 URL（如：`https://email-pitch-tool-production.up.railway.app`）
2. 回到 Google Cloud Console
3. 更新"已获授权的重定向 URI"为：
   ```
   https://your-actual-railway-url.up.railway.app/oauth/callback
   ```

### 方法2: Railway CLI 部署

```bash
# 安装 Railway CLI
npm i -g @railway/cli

# 登录
railway login

# 初始化项目
cd D:\dev\vibecode\email-pitch-tool
railway init

# 部署
railway up

# 设置环境变量
railway variables set BASE_URL=https://your-app.railway.app

# 查看日志
railway logs
```

---

## 🎨 Render 部署（免费但会休眠）

### 步骤1: 推送到 GitHub（同上）

### 步骤2: 在 Render 上创建服务
1. 访问：https://render.com/
2. 点击 "New +" → "Web Service"
3. 连接 GitHub 仓库
4. 配置：
   - **Name**: email-pitch-tool
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free

### 步骤3: 配置环境变量
在 Render Dashboard:
```
BASE_URL=https://your-app.onrender.com
```

⚠️ **注意**: Render 免费版会在15分钟无访问后休眠，首次访问需要30秒唤醒

---

## 🪁 Fly.io 部署（推荐进阶用户）

### 步骤1: 安装 Fly CLI
```bash
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex

# Mac/Linux
curl -L https://fly.io/install.sh | sh
```

### 步骤2: 创建 Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}
```

### 步骤3: 部署
```bash
cd D:\dev\vibecode\email-pitch-tool

# 登录
fly auth login

# 初始化
fly launch

# 设置环境变量
fly secrets set BASE_URL=https://your-app.fly.dev

# 部署
fly deploy
```

---

## 🔧 部署后配置

### 1. 测试应用
访问：`https://your-app-url.com`
应该看到应用界面

### 2. 绑定 Gmail 账号
1. 点击"绑定Gmail账号"
2. 授权 Google 账号
3. 检查是否成功绑定

### 3. 测试追踪功能
```bash
# 访问追踪端点
curl https://your-app-url.com/track/open/1

# 应该返回一个透明GIF
```

### 4. 设置持久化存储（重要！）

#### Railway:
```bash
# 添加 Volume
railway volume create data-volume
railway volume mount data-volume /app
```

#### Render:
1. 在 Dashboard 中添加 Persistent Disk
2. Mount path: `/app/data`
3. 修改 DB_PATH 为 `/app/data/data.db`

---

## 📊 监控和维护

### 查看日志
```bash
# Railway
railway logs

# Render
# 在 Dashboard 中查看 Logs 标签

# Fly.io
fly logs
```

### 重启服务
```bash
# Railway
railway restart

# Fly.io
fly apps restart your-app-name
```

---

## ⚠️ 常见问题

### 1. credentials.json 怎么上传？

**最佳实践**：使用环境变量
修改 `app.py`:
```python
# 如果有环境变量，使用环境变量创建凭据
if os.environ.get("GOOGLE_CLIENT_ID"):
    client_config = {
        "web": {
            "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
            "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [f"{BASE_URL}/oauth/callback"]
        }
    }
    flow = Flow.from_client_config(client_config, scopes=SCOPES)
else:
    flow = Flow.from_client_secrets_file(CREDENTIALS_FILE, scopes=SCOPES)
```

### 2. 数据库会丢失吗？
- Railway/Fly.io: 需要配置 Volume
- Render: 需要添加 Persistent Disk
- 或者使用 PostgreSQL

### 3. Gmail OAuth 回调失败？
检查：
1. Google Cloud Console 中的回调URL是否正确
2. BASE_URL 环境变量是否设置
3. credentials.json 是否上传

### 4. 应用休眠怎么办？
- Render 免费版会休眠：使用 UptimeRobot 定期 ping
- Railway/Fly.io 不会休眠（推荐）

---

## 🎯 推荐配置

### 小型使用（<1000封/月）
- **服务**: Render Free
- **成本**: $0
- **注意**: 会休眠

### 中型使用（<5000封/月）
- **服务**: Railway Hobby
- **成本**: ~$5/月
- **优势**: 稳定不休眠

### 大型使用（>5000封/月）
- **服务**: Fly.io 或自建服务器
- **成本**: ~$10-20/月
- **优势**: 性能好，可扩展

---

## 📝 部署检查清单

- [ ] 代码推送到 GitHub
- [ ] Railway/Render 项目创建完成
- [ ] BASE_URL 环境变量已设置
- [ ] credentials.json 已上传或配置环境变量
- [ ] Google OAuth 回调URL已更新
- [ ] 应用可以正常访问
- [ ] Gmail 账号绑定测试通过
- [ ] 追踪功能测试通过
- [ ] 持久化存储已配置

---

## 🆘 需要帮助？

1. **Railway 文档**: https://docs.railway.app/
2. **Render 文档**: https://render.com/docs
3. **Fly.io 文档**: https://fly.io/docs/

有问题请查看项目 Issues 或联系支持。
