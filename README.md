# Email Pitch Tool

轻量级邮件营销工具 MVP

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置 Gmail OAuth
# - 前往 https://console.cloud.google.com/
# - 创建项目 → 启用 Gmail API
# - 创建 OAuth 2.0 凭据 (桌面应用)
# - 下载 JSON 并保存为 credentials.json

# 3. 启动
python app.py
# 访问 http://localhost:8000
```

## 功能

- Gmail OAuth 绑定
- CSV/Excel 批量导入收件人
- Jinja2 模板变量 `{{name}}` `{{name|默认值}}`
- 多步骤自动化序列 (Follow-up)
- 打开/点击追踪
- 发送频率控制

## CSV 格式示例

```csv
email,first_name,company
john@example.com,John,Acme Inc
jane@example.com,Jane,Tech Corp
```

## 模板示例

主题: `Hi {{first_name|there}}, quick question`

内容:
```html
<p>Hi {{first_name|there}},</p>
<p>I noticed {{company}} is doing great work...</p>
```
