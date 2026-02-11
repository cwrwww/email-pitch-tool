# 📧 Email Pitch Tool

一款轻量级的邮件营销自动化工具，帮助您发送个性化邮件、设置多步骤跟进序列、追踪邮件打开和回复情况。

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/yourusername/email-pitch-tool)

---

## ✨ 核心功能

- 🔐 **Gmail 账号安全绑定** - 通过 Google OAuth 官方授权
- 📊 **批量导入联系人** - 支持 CSV、Excel、手动输入、批量粘贴
- 🎨 **个性化邮件模板** - 使用变量自动填充（如 `{{name}}`、`{{company}}`）
- 🔄 **多步骤自动跟进** - 设置邮件序列，自动按时间发送
- 📈 **邮件数据追踪** - 追踪打开率、点击率、回复率
- ⚙️ **灵活发送控制** - 自定义发送间隔和频率

---

## 🚀 快速开始

### 方式1: 云端部署（推荐）⭐

最快5分钟部署到云端：

```bash
# 1. 推送代码到 GitHub
git clone https://github.com/yourusername/email-pitch-tool.git
cd email-pitch-tool

# 2. 访问 Railway 一键部署
# https://railway.app/new
# 选择从 GitHub 部署

# 3. 配置环境变量（见下方）
```

**📖 详细部署指南**: [docs/QUICKSTART_DEPLOY.md](docs/QUICKSTART_DEPLOY.md)

### 方式2: 本地运行

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
├── README.md                   # 项目说明（本文件）
├── .gitignore                  # Git 忽略配置
│
├── Procfile                    # 部署配置
├── railway.json                # Railway 配置
├── runtime.txt                 # Python 版本
│
├── docs/                       # 📚 文档目录
│   ├── QUICKSTART_DEPLOY.md    # 5分钟快速部署
│   ├── DEPLOYMENT.md           # 完整部署指南
│   ├── setup_tracking.md       # 追踪功能设置
│   └── prd.md                  # 产品需求文档
│
├── scripts/                    # 🔧 脚本工具
│   ├── deploy.sh               # 自动部署脚本
│   ├── test_tracking.py        # 追踪功能测试
│   └── test_tracking_simple.py # 简化版测试
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
| `BASE_URL` | 应用公网地址 | 部署时必需 | `http://localhost:8000` |
| `GOOGLE_CLIENT_ID` | Google OAuth ID | 是* | - |
| `GOOGLE_CLIENT_SECRET` | Google OAuth Secret | 是* | - |
| `PORT` | 应用端口 | 否 | `8000` |
| `TEST_MODE` | 测试模式（不发真邮件） | 否 | `false` |

*如果有 `credentials.json` 文件则不需要

---

## 📊 技术栈

- **后端**: Python + FastAPI
- **前端**: Vanilla JS + HTML/CSS
- **数据库**: SQLite
- **邮件**: Gmail API
- **任务调度**: APScheduler
- **部署**: Railway / Render / Fly.io

---

## 🐛 故障排除

### 数据库锁定错误
已优化，使用 WAL 模式和连接池

### 打开率显示为 0
1. 检查 `BASE_URL` 是否设置为公网地址
2. 邮件客户端可能阻止图片加载
3. 建议关注回复率而非打开率

详见：[docs/setup_tracking.md](docs/setup_tracking.md)

### OAuth 回调失败
确保 Google Console 中的回调 URL 与 `BASE_URL` 匹配

---

## 📖 文档

- [🚀 5分钟快速部署](docs/QUICKSTART_DEPLOY.md)
- [📚 完整部署指南](docs/DEPLOYMENT.md)
- [📊 追踪功能设置](docs/setup_tracking.md)
- [📝 产品需求文档](docs/prd.md)

---

## 🧪 测试

```bash
# 测试追踪功能
python scripts/test_tracking_simple.py

# 查看数据库
sqlite3 data.db "SELECT * FROM leads"
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
