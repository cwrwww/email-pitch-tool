# 🚀 5分钟快速部署指南

## 最简单方案：Railway (推荐)

### 第1步: 准备 Google OAuth 凭据 (2分钟)

1. 打开 `credentials.json`，找到 `client_id` 和 `client_secret`
2. 保存这两个值，稍后要用

### 第2步: 推送代码到 GitHub (1分钟)

```bash
cd D:\dev\vibecode\email-pitch-tool

# 如果还没有 GitHub 仓库
git init
git add .
git commit -m "Ready for deployment"

# 在 GitHub 上创建新仓库，然后
git remote add origin https://github.com/你的用户名/email-pitch-tool.git
git branch -M main
git push -u origin main
```

### 第3步: 部署到 Railway (2分钟)

1. 访问 https://railway.app/new
2. 点击 **"Deploy from GitHub repo"**
3. 选择 `email-pitch-tool` 仓库
4. 等待部署完成（约1分钟）

### 第4步: 配置环境变量 (1分钟)

在 Railway 项目页面：

1. 点击项目名称
2. 点击 **"Variables"** 标签
3. 添加以下变量：

```bash
BASE_URL=https://your-app-name.up.railway.app  # 从 Railway 获取
GOOGLE_CLIENT_ID=你的client_id
GOOGLE_CLIENT_SECRET=你的client_secret
```

4. Railway 会自动重新部署

### 第5步: 更新 Google OAuth 设置 (1分钟)

1. 访问 https://console.cloud.google.com/apis/credentials
2. 点击你的 OAuth 2.0 客户端ID
3. 在 **"已获授权的重定向 URI"** 中添加：
   ```
   https://your-app-name.up.railway.app/oauth/callback
   ```
4. 点击保存

---

## ✅ 完成！

访问你的应用：`https://your-app-name.up.railway.app`

### 测试步骤：
1. 点击"绑定Gmail账号"
2. 授权 Google 账号
3. 创建 campaign 并测试

---

## 🎯 获取你的 Railway URL

部署完成后，在 Railway 项目页面：
1. 点击 **"Settings"** 标签
2. 找到 **"Domains"** 部分
3. 复制显示的 URL（如：`https://email-pitch-tool-production.up.railway.app`）

---

## 💡 提示

### 查看日志
```bash
# 安装 Railway CLI (可选)
npm i -g @railway/cli

# 查看日志
railway login
railway link
railway logs
```

### 常见问题

**Q: OAuth 回调失败？**
A: 确保 Google Cloud Console 中的回调URL与 Railway URL 完全匹配

**Q: 应用无法访问？**
A: 检查 Railway 部署日志，确认没有错误

**Q: 环境变量不生效？**
A: 修改环境变量后，Railway 会自动重新部署，等待1-2分钟

---

## 🔄 其他部署选项

### Render (免费但会休眠)
详见 `DEPLOYMENT.md` 的 Render 部署部分

### Fly.io (性能好)
详见 `DEPLOYMENT.md` 的 Fly.io 部署部分

---

## 📚 完整文档

- 详细部署指南: `DEPLOYMENT.md`
- 追踪功能设置: `setup_tracking.md`
- 使用说明: `README.md`

---

**需要帮助？** 查看 [DEPLOYMENT.md](DEPLOYMENT.md) 获取详细说明
