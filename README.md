# 📧 Email Pitch Tool

一款轻量级的邮件营销自动化工具，帮助您发送个性化邮件、设置多步骤跟进序列、追踪邮件打开和回复情况。

---

## ✨ 核心功能

- 🔐 **Gmail 账号安全绑定** - 通过 Google OAuth 官方授权
- 📊 **批量导入联系人** - 支持 CSV、Excel、手动输入、批量粘贴
- 🎨 **个性化邮件模板** - 使用变量自动填充（如 `{{name}}`、`{{company}}`）
- 🔄 **多步骤自动跟进** - 设置邮件序列，自动按时间发送
- 📈 **邮件数据追踪** - 追踪打开率、点击率、回复率
- ⚙️ **灵活发送控制** - 自定义发送间隔和频率
- 🔄 **自动数据同步** - 每10分钟自动从追踪服务同步数据

---

## 🚀 快速开始

### 本地运行

```bash
# 1. 克隆仓库
git clone https://github.com/yourusername/email-pitch-tool.git
cd email-pitch-tool

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置 Google OAuth（见下方）

# 4. 运行应用
python app.py

# 5. 访问 http://localhost:8000
```

### 追踪服务部署（可选但推荐）⭐

为了追踪邮件打开率，需要部署追踪服务到公网。推荐使用 Render（完全免费）：

```bash
# 1. 进入追踪服务目录
cd tracker-render

# 2. 创建 GitHub 仓库并推送
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/你的用户名/email-tracker.git
git push -u origin main

# 3. 在 Render 部署
# 访问 https://render.com/
# New + → Web Service
# 连接你的 GitHub 仓库
# 配置:
#   - Build Command: pip install -r requirements.txt
#   - Start Command: gunicorn tracker:app
#   - 添加 Disk (持久化存储):
#     - Mount Path: /opt/render/project/src
#     - Size: 1GB (免费)

# 4. 配置本地应用
# 将 Render URL 添加到 .env 文件
echo TRACKER_URL=https://your-app.onrender.com >> .env
```

**📖 详细部署指南**: [tracker-render/RENDER_DEPLOY.md](tracker-render/RENDER_DEPLOY.md)

---

## ⚙️ 配置说明

### Google OAuth 设置

**方式1: 使用环境变量（推荐用于部署）**

```bash
# 设置环境变量
export GOOGLE_CLIENT_ID="your_client_id"
export GOOGLE_CLIENT_SECRET="your_client_secret"
export BASE_URL="https://your-app.com"
```

**方式2: 使用 credentials.json（本地开发）**

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 创建项目并启用 Gmail API
3. 创建 OAuth 2.0 凭据
4. 下载 `credentials.json` 到项目根目录
5. 添加授权回调 URI：
   - 本地：`http://localhost:8000/oauth/callback`
   - 云端：`https://your-app.com/oauth/callback`

**📖 详细步骤**: [原 README 中的详细步骤](docs/DEPLOYMENT.md#google-oauth-设置)

---

## 📁 项目结构

```
email-pitch-tool/
├── app.py                      # FastAPI 主应用
├── index.html                  # 前端界面
├── requirements.txt            # Python 依赖
├── data.db                     # SQLite 数据库
├── credentials.json            # Google OAuth 凭据
├── README.md                   # 项目说明（本文件）
│
├── tracker-render/             # 📡 追踪服务 (部署到 Render)
│   ├── tracker.py              # Flask 追踪服务
│   ├── requirements.txt        # 依赖
│   ├── README.md               # 服务说明
│   └── RENDER_DEPLOY.md        # 部署指南
│
├── docs/                       # 📚 文档目录
│   └── prd.md                  # 产品需求文档
│
└── examples/                   # 📋 示例文件
    └── example_leads.csv       # CSV 导入示例
```

---

## 🎯 使用流程

### 1. 绑定 Gmail 账号
- 点击"绑定Gmail账号"
- 授权 Google 账号

### 2. 创建 Campaign
- 输入 Campaign 名称
- 点击"创建"

### 3. 添加邮件模板
```html
主题: Hi {{first_name}}, quick question about {{company}}

内容:
<p>Hi {{first_name}},</p>
<p>I noticed {{company}} is doing great work in...</p>
<p>Would love to chat!</p>
```

### 4. 导入联系人
支持三种方式：
- 📁 上传 CSV/Excel
- ✍️ 手动输入
- 📋 批量粘贴

CSV 格式示例：
```csv
email,first_name,company
john@example.com,John,Acme Inc
jane@example.com,Jane,Tech Corp
```

### 5. 启动发送
- 选择发件账号
- 设置发送间隔
- 点击"启动"

### 6. 查看统计
- 打开率
- 点击率
- 回复率

---

## 🔧 环境变量

| 变量 | 说明 | 必需 | 默认值 |
|------|------|------|--------|
| `TRACKER_URL` | 追踪服务地址 | 推荐 | - |
| `GOOGLE_CLIENT_ID` | Google OAuth ID | 是* | - |
| `GOOGLE_CLIENT_SECRET` | Google OAuth Secret | 是* | - |
| `PORT` | 应用端口 | 否 | `8000` |

*如果有 `credentials.json` 文件则不需要

**示例 .env 文件:**
```bash
TRACKER_URL=https://your-app.onrender.com
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
```

---

## 📊 技术栈

### 主应用 (本地运行)
- **后端**: Python + FastAPI
- **前端**: Vanilla JS + HTML/CSS
- **数据库**: SQLite (WAL 模式)
- **邮件**: Gmail API
- **任务调度**: APScheduler

### 追踪服务 (Render 部署)
- **后端**: Flask + Gunicorn
- **数据库**: SQLite (持久化存储)
- **同步**: HTTP REST API (每10分钟自动同步)

---

## 🐛 故障排除

### 数据库锁定错误
已优化，使用 WAL 模式和超时配置

### 打开率显示为 0
1. 确保已部署追踪服务到 Render 并设置了 `TRACKER_URL`
2. 检查追踪服务状态：访问 `https://your-app.onrender.com/health`
3. 邮件客户端可能阻止图片加载（Gmail、Outlook 等）
4. 数据每10分钟自动同步一次

### 回复检测不工作
1. 确保已授权 Gmail API 读取权限
2. 检查 Gmail 账号的"已发送"文件夹
3. 回复检测每5分钟运行一次

### OAuth 回调失败
确保 Google Console 中的回调 URL 配置正确：
- 本地: `http://localhost:8000/oauth/callback`

---

## 📖 文档

- [📡 追踪服务部署指南](tracker-render/RENDER_DEPLOY.md)
- [📝 产品需求文档](docs/prd.md)

---

## 🧪 测试

```bash
# 查看数据库
sqlite3 data.db "SELECT * FROM leads"

# 测试追踪服务（部署后）
curl https://your-app.onrender.com/health
curl https://your-app.onrender.com/api/stats
```

---

## ⚠️ 注意事项

### Gmail 发送限制
- 个人账号：500封/天
- Google Workspace：2000封/天

### 垃圾邮件预防
- 控制发送频率（建议每5-10分钟一封）
- 配置 SPF、DKIM、DMARC
- 提供取消订阅选项
- 发送有价值的内容

### 隐私和合规
- 遵守 GDPR / CAN-SPAM
- 获得收件人同意
- 提供退订机制
- 保护用户数据安全

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License

---

## 💬 联系方式

- GitHub Issues: [提交问题](https://github.com/yourusername/email-pitch-tool/issues)
- 文档: [完整文档](docs/)

---

**🎉 开始使用**: [快速部署指南](docs/QUICKSTART_DEPLOY.md)
