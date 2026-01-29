# Email Pitch Tool - 邮件营销自动化工具

一款轻量级的邮件营销工具，帮助您自动发送个性化邮件、设置多步骤跟进序列、追踪邮件打开和点击情况。

---

## 目录

- [功能介绍](#功能介绍)
- [系统要求](#系统要求)
- [安装步骤](#安装步骤)
  - [第一步：安装 Python](#第一步安装-python)
  - [第二步：下载项目](#第二步下载项目)
  - [第三步：安装依赖](#第三步安装依赖)
  - [第四步：创建 Google Cloud 凭据](#第四步创建-google-cloud-凭据credentials)
- [启动程序](#启动程序)
- [使用教程](#使用教程)
- [CSV 文件格式说明](#csv-文件格式说明)
- [邮件模板语法](#邮件模板语法)
- [常见问题](#常见问题)
- [注意事项](#注意事项)

---

## 功能介绍

- **Gmail 账号绑定**：通过 Google 官方授权方式安全连接您的 Gmail 账号
- **批量导入联系人**：支持 CSV、Excel 文件导入，也可以手动输入或粘贴
- **个性化模板**：使用变量（如 `{{姓名}}`）自动填充每封邮件的个性化内容
- **多步骤自动跟进**：设置多封跟进邮件，系统自动按计划发送
- **邮件追踪**：追踪邮件是否被打开、链接是否被点击、是否收到回复
- **发送频率控制**：自定义发送间隔，避免触发垃圾邮件过滤

---

## 系统要求

- 操作系统：Windows 10/11、macOS 或 Linux
- Python 3.8 或更高版本
- 网络连接
- 一个 Gmail 账号
- 一个 Google Cloud 账号（免费）

---

## 安装步骤

### 第一步：安装 Python

#### Windows 用户

1. 打开浏览器，访问 Python 官网：https://www.python.org/downloads/
2. 点击黄色的 **"Download Python 3.x.x"** 按钮下载安装程序
3. 运行下载的安装程序
4. **重要**：在安装界面底部，**勾选 "Add Python to PATH"**（将 Python 添加到环境变量）
5. 点击 **"Install Now"** 开始安装
6. 安装完成后，点击 **"Close"** 关闭安装程序

**验证安装是否成功：**
1. 按 `Win + R` 键，输入 `cmd`，按回车打开命令提示符
2. 输入 `python --version`，按回车
3. 如果显示 `Python 3.x.x` 则安装成功

#### macOS 用户

1. 打开 **"终端"** 应用（在"应用程序" → "实用工具"中）
2. 输入以下命令检查是否已安装 Python：
   ```bash
   python3 --version
   ```
3. 如果没有安装，访问 https://www.python.org/downloads/macos/ 下载安装

---

### 第二步：下载项目

将整个 `email-pitch-tool-main` 文件夹放到您方便找到的位置，例如：
- Windows：`C:\Users\您的用户名\Documents\email-pitch-tool-main`
- macOS：`/Users/您的用户名/Documents/email-pitch-tool-main`

---

### 第三步：安装依赖

#### Windows 用户

1. 打开 **"命令提示符"**（按 `Win + R`，输入 `cmd`，按回车）
2. 使用 `cd` 命令进入项目文件夹，例如：
   ```bash
   cd C:\Users\您的用户名\Documents\email-pitch-tool-main
   ```
3. 运行以下命令安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
4. 等待安装完成（可能需要几分钟）

#### macOS 用户

1. 打开 **"终端"** 应用
2. 使用 `cd` 命令进入项目文件夹，例如：
   ```bash
   cd /Users/您的用户名/Documents/email-pitch-tool-main
   ```
3. 运行以下命令安装依赖：
   ```bash
   pip3 install -r requirements.txt
   ```
4. 等待安装完成

---

### 第四步：创建 Google Cloud 凭据（credentials）

这是最重要的一步，请仔细按照以下步骤操作：

#### 4.1 登录 Google Cloud Console

1. 打开浏览器，访问：https://console.cloud.google.com/
2. 使用您的 Google 账号登录
3. 如果是第一次使用，需要同意服务条款

#### 4.2 创建新项目

1. 在页面顶部，点击项目选择器（显示 **"Select a project"** 或当前项目名称的下拉菜单）
2. 在弹出的窗口中，点击右上角的 **"NEW PROJECT"**
3. 填写项目信息：
   - **Project name**（项目名称）：输入一个名称，例如 `email-pitch-tool`
   - **Location**（位置）：保持默认即可
4. 点击 **"CREATE"** 按钮
5. 等待几秒钟，项目创建完成后会自动跳转

#### 4.3 启用 Gmail API

1. 在左侧菜单中，点击 **"APIs & Services"** → **"Library"**
   （如果找不到左侧菜单，点击左上角的 ☰ 汉堡菜单图标）
2. 在搜索框中输入 **"Gmail API"**
3. 点击搜索结果中的 **"Gmail API"**
4. 在 Gmail API 页面，点击蓝色的 **"ENABLE"** 按钮
5. 等待启用完成

#### 4.4 配置 OAuth 同意屏幕

1. 在左侧菜单中，点击 **"APIs & Services"** → **"OAuth consent screen"**
2. 选择用户类型（User Type）：
   - 如果您只是个人使用，选择 **"External"**
   - 点击 **"CREATE"**
3. 填写应用信息（OAuth consent screen 页面）：
   - **App name**（应用名称）：输入 `Email Pitch Tool`
   - **User support email**（用户支持电子邮件）：选择您的邮箱
   - 滚动到页面底部
   - **Developer contact information**（开发者联系信息）：输入您的邮箱
   - 其他字段可以留空
4. 点击 **"SAVE AND CONTINUE"**
5. **Scopes 页面**（范围）：直接点击 **"SAVE AND CONTINUE"**（无需添加任何范围）
6. **Test users 页面**（测试用户）：
   - 点击 **"+ ADD USERS"**
   - 输入您要使用的 Gmail 邮箱地址
   - 点击 **"ADD"**
   - 点击 **"SAVE AND CONTINUE"**
7. **Summary 页面**（摘要）：点击 **"BACK TO DASHBOARD"** 返回

#### 4.5 创建 OAuth 凭据

1. 在左侧菜单中，点击 **"APIs & Services"** → **"Credentials"**
2. 点击顶部的 **"+ CREATE CREDENTIALS"**
3. 在下拉菜单中选择 **"OAuth client ID"**
4. 配置 OAuth 客户端：
   - **Application type**（应用类型）：选择 **"Desktop app"**
   - **Name**（名称）：输入 `Email Pitch Tool Desktop`
5. 点击 **"CREATE"**

#### 4.6 下载凭据文件

1. 创建成功后，会弹出一个窗口显示 "OAuth client created"
2. 点击 **"DOWNLOAD JSON"** 按钮下载凭据文件
3. 将下载的文件 **重命名** 为 `credentials.json`
   - 下载的文件名通常是 `client_secret_xxxxx.json`，需要改成 `credentials.json`
4. 将 `credentials.json` 文件 **移动到** 项目文件夹中（与 `app.py` 在同一目录）

**文件夹结构应该是这样的：**
```
email-pitch-tool-main/
├── app.py
├── index.html
├── requirements.txt
├── credentials.json  ← 您刚下载并重命名的文件
└── ...
```

---

## 启动程序

#### Windows 用户

1. 打开 **"命令提示符"**
2. 进入项目文件夹：
   ```bash
   cd C:\Users\您的用户名\Documents\email-pitch-tool-main
   ```
3. 运行程序：
   ```bash
   python app.py
   ```
4. 看到类似以下信息表示启动成功：
   ```
   INFO:     Uvicorn running on http://0.0.0.0:8000
   ```

#### macOS 用户

1. 打开 **"终端"**
2. 进入项目文件夹：
   ```bash
   cd /Users/您的用户名/Documents/email-pitch-tool-main
   ```
3. 运行程序：
   ```bash
   python3 app.py
   ```

#### 访问程序

1. 打开浏览器
2. 在地址栏输入：**http://localhost:8000**
3. 按回车，即可看到程序界面

**注意**：命令行窗口要保持打开状态，关闭窗口程序会停止运行。

---

## 使用教程

### 1. 绑定 Gmail 账号

1. 在页面顶部，点击 **"绑定 Gmail 账号"** 按钮
2. 浏览器会跳转到 Google 登录页面
3. 选择您要使用的 Gmail 账号登录
4. 如果看到 "此应用未经 Google 验证" 的警告：
   - 点击 **"高级"**
   - 点击 **"转至 Email Pitch Tool（不安全）"**
   - 这是正常的，因为这是您自己创建的应用
5. 点击 **"继续"** 授予权限
6. 授权成功后会自动返回程序页面

### 2. 创建营销活动

1. 在 **"营销活动"** 区域，点击 **"+ 新建活动"**
2. 输入活动名称（例如："产品推广-1月"）
3. 点击 **"创建"**

### 3. 设置邮件模板

1. 点击刚创建的活动，进入详情页
2. 切换到 **"模板"** 标签页
3. 点击 **"+ 添加模板"**
4. 填写模板信息：
   - **步骤**：第几封邮件（1 = 首次发送，2 = 第一次跟进，以此类推）
   - **主题**：邮件主题，可以使用变量如 `{{first_name}}`
   - **正文**：邮件内容，支持 HTML 格式和变量
   - **延迟天数**：发送这封邮件前等待的天数（首封邮件通常设为 0）
5. 点击 **"保存"**

### 4. 导入联系人

1. 切换到 **"联系人"** 标签页
2. 选择导入方式：
   - **上传文件**：点击 "选择文件"，选择 CSV 或 Excel 文件
   - **粘贴数据**：从 Excel 复制数据（包含表头），粘贴到文本框
   - **手动添加**：逐个输入联系人信息

### 5. 启动活动

1. 切换到 **"发送"** 标签页
2. 选择要使用的 Gmail 账号
3. 设置发送间隔（例如：每 5 分钟发送一封）
4. 点击 **"启动活动"**

### 6. 查看统计数据

1. 切换到 **"统计"** 标签页
2. 可以查看：
   - 总联系人数
   - 已发送数量
   - 打开次数和打开率
   - 点击次数和点击率
   - 回复数量和回复率

---

## CSV 文件格式说明

CSV 文件是一种简单的表格格式，可以用 Excel 创建。

### 创建 CSV 文件的方法

1. 打开 Excel
2. 在第一行输入列标题（字段名）
3. 从第二行开始输入数据
4. 点击 "文件" → "另存为"
5. 在 "保存类型" 中选择 **"CSV UTF-8（逗号分隔）"**
6. 保存文件

### 示例格式

| email | first_name | last_name | company | title |
|-------|------------|-----------|---------|-------|
| john@example.com | John | Doe | Acme Inc | CEO |
| jane@example.com | Jane | Smith | Tech Corp | CTO |
| bob@example.com | Bob | Johnson | StartupXYZ | Founder |

**必须包含的列**：`email`（收件人邮箱地址）

**可选列**：您可以添加任意列，如 `first_name`、`company`、`phone` 等，这些都可以在邮件模板中作为变量使用。

---

## 邮件模板语法

### 基本变量

使用双花括号包裹变量名：

```
Hi {{first_name}},

我注意到 {{company}} 最近发展得很好...
```

### 带默认值的变量

如果某个联系人没有填写该字段，可以设置默认值：

```
Hi {{first_name|朋友}},
```

如果联系人有 `first_name`，显示其名字；如果没有，显示 "朋友"。

### 完整示例

**主题**：
```
Hi {{first_name|there}}, 有个问题想请教
```

**正文**：
```html
<p>Hi {{first_name|there}},</p>

<p>我是张三，来自 ABC 公司。</p>

<p>我注意到 {{company|贵公司}} 在 {{industry|行业}} 领域做得很出色，
想和您探讨一下合作的可能性。</p>

<p>方便的话，这周能否安排 15 分钟的电话交流？</p>

<p>期待您的回复！</p>

<p>张三<br>
ABC 公司<br>
电话：123-4567-8900</p>
```

---

## 常见问题

### Q1: 启动时提示 "找不到 credentials.json"

**原因**：凭据文件未放置在正确位置或文件名不对。

**解决方法**：
1. 确认 `credentials.json` 文件在项目文件夹中
2. 确认文件名是 `credentials.json`（注意大小写）
3. 确认文件和 `app.py` 在同一个文件夹内

### Q2: Google 授权时提示 "此应用未经验证"

**原因**：这是正常的，因为这是您个人创建的应用。

**解决方法**：
1. 点击 "高级"
2. 点击 "转至 Email Pitch Tool（不安全）"
3. 继续授权流程

### Q3: 邮件发送失败

**可能原因及解决方法**：
1. **Gmail 账号未授权**：重新绑定 Gmail 账号
2. **网络问题**：检查网络连接
3. **发送频率过高**：增加发送间隔时间
4. **Gmail 每日限额**：Gmail 每天有发送限制（约 500 封），等待次日重试

### Q4: 如何停止正在运行的活动？

1. 进入活动详情页
2. 切换到 "发送" 标签页
3. 点击 "停止活动" 按钮

### Q5: 为什么打开率显示 0%？

**可能原因**：
1. 邮件被归类到垃圾邮件
2. 收件人的邮箱客户端屏蔽了追踪图片
3. 收件人尚未打开邮件

### Q6: 如何关闭程序？

在运行程序的命令行窗口中，按 `Ctrl + C` 键停止程序。

### Q7: 如何在另一台电脑上使用？

1. 复制整个项目文件夹到新电脑
2. 在新电脑上安装 Python
3. 运行 `pip install -r requirements.txt` 安装依赖
4. `credentials.json` 可以直接复制使用
5. 但需要重新绑定 Gmail 账号

---

## 注意事项

### 关于发送频率

- Gmail 个人账号每天发送上限约 **500 封**
- Google Workspace 账号每天发送上限约 **2000 封**
- 建议设置发送间隔至少 **3-5 分钟**，避免被识别为垃圾邮件

### 关于邮件送达率

为了提高邮件送达率，建议：
1. 使用个性化内容，避免完全相同的邮件
2. 避免使用过多营销词汇（如 "免费"、"优惠"、"限时"）
3. 保持合理的发送频率
4. 在邮件底部提供退订链接

### 关于数据安全

- 所有数据存储在本地 `data.db` 文件中
- Gmail 授权信息也存储在本地
- 不会上传任何数据到外部服务器
- 建议定期备份 `data.db` 文件

### 关于黑名单

如果某个收件人要求不再接收邮件：
1. 在界面中找到该联系人
2. 将其添加到黑名单
3. 系统将不再向该邮箱发送任何邮件

---

## 技术支持

如果遇到问题，请检查：
1. Python 是否正确安装
2. 依赖是否完整安装
3. `credentials.json` 是否在正确位置
4. Gmail 账号是否已正确授权

---

## 许可证

本项目仅供学习和个人使用。请遵守相关法律法规，不要发送垃圾邮件。
