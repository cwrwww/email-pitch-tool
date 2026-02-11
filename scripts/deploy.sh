#!/bin/bash
# 快速部署脚本

echo "🚀 Email Pitch Tool - 快速部署脚本"
echo "=================================="
echo ""

# 检查是否有未提交的更改
if [[ -n $(git status -s) ]]; then
    echo "📝 检测到未提交的更改，正在提交..."
    git add .
    git commit -m "Prepare for deployment"
fi

# 选择部署平台
echo "选择部署平台:"
echo "1) Railway (推荐)"
echo "2) Render"
echo "3) Fly.io"
read -p "请输入选项 (1-3): " choice

case $choice in
    1)
        echo ""
        echo "🚂 Railway 部署"
        echo "==============="

        # 检查是否安装了 railway CLI
        if ! command -v railway &> /dev/null; then
            echo "❌ 未安装 Railway CLI"
            echo "请运行: npm i -g @railway/cli"
            exit 1
        fi

        # 登录
        echo "正在登录 Railway..."
        railway login

        # 初始化或链接项目
        if [ ! -f ".railway" ]; then
            echo "正在初始化新项目..."
            railway init
        else
            echo "使用现有项目..."
        fi

        # 部署
        echo "正在部署..."
        railway up

        # 获取域名
        DOMAIN=$(railway domain)
        echo ""
        echo "✅ 部署成功！"
        echo "📍 应用地址: https://$DOMAIN"
        echo ""
        echo "⚠️  下一步操作:"
        echo "1. 设置环境变量:"
        echo "   railway variables set BASE_URL=https://$DOMAIN"
        echo "   railway variables set GOOGLE_CLIENT_ID=你的client_id"
        echo "   railway variables set GOOGLE_CLIENT_SECRET=你的client_secret"
        echo ""
        echo "2. 更新 Google OAuth 回调URL:"
        echo "   https://$DOMAIN/oauth/callback"
        ;;

    2)
        echo ""
        echo "🎨 Render 部署"
        echo "=============="
        echo ""
        echo "请按照以下步骤操作:"
        echo "1. 访问 https://render.com/"
        echo "2. 点击 'New +' -> 'Web Service'"
        echo "3. 连接你的 GitHub 仓库"
        echo "4. 配置:"
        echo "   - Build Command: pip install -r requirements.txt"
        echo "   - Start Command: uvicorn app:app --host 0.0.0.0 --port \$PORT"
        echo ""
        echo "5. 添加环境变量:"
        echo "   BASE_URL=https://your-app.onrender.com"
        echo "   GOOGLE_CLIENT_ID=你的client_id"
        echo "   GOOGLE_CLIENT_SECRET=你的client_secret"
        ;;

    3)
        echo ""
        echo "🪁 Fly.io 部署"
        echo "=============="

        # 检查是否安装了 fly CLI
        if ! command -v fly &> /dev/null; then
            echo "❌ 未安装 Fly CLI"
            echo "请访问: https://fly.io/docs/hands-on/install-flyctl/"
            exit 1
        fi

        # 登录
        echo "正在登录 Fly.io..."
        fly auth login

        # 初始化
        if [ ! -f "fly.toml" ]; then
            echo "正在初始化..."
            fly launch --no-deploy
        fi

        # 设置环境变量
        read -p "请输入你的应用域名 (如: your-app.fly.dev): " DOMAIN
        fly secrets set BASE_URL=https://$DOMAIN

        # 部署
        echo "正在部署..."
        fly deploy

        echo ""
        echo "✅ 部署成功！"
        echo "📍 应用地址: https://$DOMAIN"
        ;;

    *)
        echo "❌ 无效选项"
        exit 1
        ;;
esac

echo ""
echo "🎉 部署完成！"
echo ""
echo "📖 查看完整文档: DEPLOYMENT.md"
