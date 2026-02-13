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

#### 第一步：访问 Google Cloud Console

1. 打开浏览器，访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 使用你的 Google 账号登录

#### 第二步：创建新项目

1. 点击顶部导航栏的项目下拉菜单
2. 点击"新建项目"（New Project）
3. 输入项目名称，例如 `email-pitch-tool`
4. 点击"创建"（Create）
5. 等待项目创建完成（约10-30秒）

#### 第三步：启用 Gmail API

1. 确保已选中刚创建的项目
2. 在左侧菜单中，点击"API 和服务" > "启用的 API 和服务"
3. 点击顶部的"+ 启用 API 和服务"按钮
4. 在搜索框中输入 `Gmail API`
5. 点击搜索结果中的 "Gmail API"
6. 点击"启用"（Enable）按钮
7. 等待 API 启用完成

#### 第四步：配置 OAuth 同意屏幕

1. 在左侧菜单中，点击"OAuth 同意屏幕"（OAuth consent screen）
2. 选择用户类型：
   - **外部**（External）：任何 Google 账号都可以授权
   - **内部**（Internal）：仅限你的 Google Workspace 组织内的用户
   - 推荐选择"外部"
3. 点击"创建"
4. 填写必填信息：
   - **应用名称**：`Email Pitch Tool` 或其他名称
   - **用户支持电子邮件**：选择你的邮箱
   - **开发者联系信息**：填写你的邮箱
5. 点击"保存并继续"
6. 在"范围"（Scopes）页面，点击"保存并继续"（暂时不需要添加）
7. 在"测试用户"页面，点击"+ ADD USERS"，添加你要用于测试的 Gmail 账号
8. 点击"保存并继续"
9. 检查摘要页面，点击"返回控制台"

#### 第五步：创建 OAuth 2.0 凭据

1. 在左侧菜单中，点击"凭据"（Credentials）
2. 点击顶部的"+ 创建凭据"（Create Credentials）
3. 选择"OAuth 客户端 ID"（OAuth client ID）
4. 在"应用类型"中选择"桌面应用"（Desktop app）
5. 输入名称，例如 `Email Pitch Desktop Client`
6. 点击"创建"
7. 弹出窗口会显示客户端 ID 和客户端密钥，点击"确定"

#### 第六步：配置授权重定向 URI（重要！）

1. 在凭据列表中，找到刚创建的 OAuth 2.0 客户端 ID
2. 点击右侧的编辑图标（铅笔图标）
3. 在"已获授权的重定向 URI"（Authorized redirect URIs）部分：
   - 点击"+ 添加 URI"
   - 本地开发添加：`http://localhost:8000/oauth/callback`
   - 如需云端部署，再添加：`https://your-app.com/oauth/callback`（替换为你的实际域名）
4. 点击底部的"保存"按钮

#### 第七步：下载 credentials.json

1. 返回"凭据"页面
2. 找到你创建的 OAuth 2.0 客户端
3. 点击右侧的下载图标（⬇️ 下载 JSON）
4. 文件会被下载为类似 `client_secret_xxx.json` 的名称
5. 将下载的文件重命名为 `credentials.json`
6. 将文件移动到项目根目录（与 `app.py` 同级）

#### 文件格式示例

你的 `credentials.json` 文件应该类似这样：

```json
{
  "installed": {
    "client_id": "你的客户端ID.apps.googleusercontent.com",
    "project_id": "你的项目ID",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "你的客户端密钥",
    "redirect_uris": ["http://localhost"]
  }
}
```

#### 验证配置

1. 确认文件路径：
   ```
   email-pitch-tool/
   ├── app.py
   ├── credentials.json  ← 应该在这里
   └── ...
   ```

2. 运行应用：
   ```bash
   python app.py
   ```

3. 访问 `http://localhost:8000`，点击"绑定 Gmail 账号"
4. 会跳转到 Google 授权页面
5. 选择你的 Google 账号并授权
6. 授权成功后会自动跳转回应用

#### 常见问题

**问题1: "redirect_uri_mismatch" 错误**
- 原因：OAuth 客户端配置中的重定向 URI 与应用使用的不一致
- 解决：确保 Google Console 中添加了 `http://localhost:8000/oauth/callback`

**问题2: "access_denied" 错误**
- 原因：应用处于测试模式，当前用户不在测试用户列表中
- 解决：在 OAuth 同意屏幕的"测试用户"中添加该 Gmail 账号

**问题3: credentials.json 找不到**
- 原因：文件路径不正确或文件名拼写错误
- 解决：确保文件名为 `credentials.json`（全小写）并放在项目根目录

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
