# 🤖 国内 AI & Agent 导航站 / China AI & Agent Navigation

> 收录国内主流人工智能平台 · AI Agent · 开发工具 · 创作工具  
> Frontend-Backend Separation | Data Persistence | Admin Panel | Dark/Light Theme

---

## 📋 项目概述 / Project Overview

一个功能完整的国内 AI 资源导航网站，收录 **78 个国内 AI 站点**，分为 **11 个分类**，支持：  
A comprehensive China AI resource navigation website featuring **78 Chinese AI sites** across **11 categories**, with support for:

- **🏠 公开导航页** — 浏览所有 AI 站点，分类展示，点击直达  
  **Public Navigation** — Browse all AI sites with categorized display, click to visit
- **🔐 管理后台** — 登录后对分类和站点进行增删改查  
  **Admin Panel** — CRUD operations for categories and sites after login
- **🌙 主题切换** — 深色/浅色模式自由切换，自动保存偏好  
  **Theme Switch** — Dark/light mode toggle with auto-save preference
- **📊 数据持久化** — 使用 SQLite 数据库存储，重启不丢失  
  **Data Persistence** — SQLite database storage, data survives restarts

---

## 📁 项目结构 / Project Structure

```
F:\ai-agent-nav\
├── backend\
│   ├── app.py         ← Flask 后端 API 服务（端口 5000）/ Flask Backend API (Port 5000)
│   ├── seed.py        ← 数据库初始化（创建表 + 导入 78 个站点）/ DB Initialization
│   └── nav.db         ← SQLite 数据库文件 / SQLite Database
├── frontend\
│   ├── index.html     ← 公开导航页（API 驱动渲染）/ Public Navigation Page
│   └── admin.html     ← 管理后台（登录 + CRUD）/ Admin Panel
└── README.md          ← 本文件 / This File
```

---

## 🚀 快速启动 / Quick Start

### 环境要求 / Requirements

- Python 3.8+
- Flask + flask-cors（首次运行会自动安装 / Auto-installed on first run）

### 启动步骤 / Getting Started

```bash
# 1. 进入项目目录 / Enter project directory
cd ai-agent-nav/backend

# 2. 安装依赖（首次运行）/ Install dependencies (first run）
pip install flask flask-cors

# 3. 初始化数据库（首次运行，或重置数据）/ Initialize database (first run）
python seed.py

# 4. 启动服务 / Start server
python app.py
```

启动后访问 / After starting, visit:

| 地址 / URL | 说明 / Description |
|:---|:---|
| `http://localhost:5000` | 🏠 公开导航首页 / Public Navigation |
| `http://localhost:5000/admin` | 🔐 管理后台 / Admin Panel |
| `http://localhost:5000/api/categories` | 📡 API - 获取分类及站点 / API - Get Categories & Sites |

### 🔌 修改端口 / Change Port

当前端口默认为 **5000**，如需修改有 3 种方式：  
Default port is **5000**. Three ways to change it:

**方法 1️⃣ 直接改代码 / Method 1: Modify code**

打开 `backend/app.py`，找到最后一行，修改 `port` 参数：  
Open `backend/app.py`, find the last line, modify `port`:

```python
app.run(host='0.0.0.0', port=8080, debug=True)  # 将 5000 改为你想要的端口 / Change 5000 to desired port
```

**方法 2️⃣ 命令行指定（不改文件） / Method 2: CLI argument**

```bash
cd ai-agent-nav/backend
python -c "from app import app; app.run(host='0.0.0.0', port=8080, debug=True)"
```

**方法 3️⃣ 环境变量 / Method 3: Environment variable**

```bash
cd ai-agent-nav/backend
env FLASK_RUN_PORT=8080 python app.py
```

> ⚠️ 修改端口后，浏览器访问地址也要相应调整，例如改为 `http://localhost:8080`  
> ⚠️ After changing port, update browser URL accordingly, e.g., `http://localhost:8080`

---

## 🔧 功能详情 / Features

### 🏠 公开导航页 / Public Navigation

- 页面加载时通过 `fetch()` 调用后端 API 获取数据  
  Fetch data from backend API on page load
- 分类卡片式布局，展示站点名称、描述、标签、域名  
  Category-based card layout showing site name, description, badge, domain
- 点击卡片直接跳转到目标站点  
  Click card to navigate to target site
- 左上角主题切换按钮（深色/浅色，自动记忆）  
  Theme toggle button (dark/light, auto-save)
- 右上角「管理」入口链接  
  Admin entry link at top-right
- 统计栏实时显示站点总数和分类数  
  Statistics bar showing total sites and categories

### 🔐 管理后台 / Admin Panel

**登录信息 / Login Credentials:** 用户名 `admin` / 密码 `admin123` | Username `admin` / Password `admin123`

**功能模块 / Modules:**

| 模块 / Module | 功能 / Function |
|:---|:---|
| 📊 **仪表盘 / Dashboard** | 站点/分类总数统计，各分类站点分布表 / Site & category statistics |
| 📂 **分类管理 / Category Management** | 新增、编辑、删除分类（删除级联删除站点） / Create, edit, delete categories (cascade deletes sites) |
| 🔗 **站点管理 / Site Management** | 按分类筛选、新增、编辑、删除站点 / Filter by category, create, edit, delete sites |

- 所有操作实时写入 SQLite 数据库  
  All operations written to SQLite in real-time
- 登录 Token 保存在 localStorage，刷新不丢失  
  Login token stored in localStorage, persists on refresh
- 退出登录自动跳转首页  
  Auto redirect to homepage after logout

### 🌙 主题切换 / Theme Switch

- 首页和管理后台均支持深色/浅色切换  
  Dark/light mode support for both pages
- 主题偏好存储在 `localStorage`，跨页面共享  
  Theme preference stored in localStorage, shared across pages
- 深色：暗紫黑背景 + 霓虹紫色调  
  Dark: Dark purple background + neon purple accents
- 浅色：柔白灰背景 + 紫色强调  
  Light: Soft white-gray background + purple accents

---

## 📡 API 接口文档 / API Documentation

### 公开接口（无需认证） / Public APIs (No Auth Required)

| 方法 / Method | 路径 / Path | 说明 / Description |
|:---:|:---|:---|
| GET | `/api/categories` | 获取所有分类及下属站点 |
| | | Get all categories with sites |
| GET | `/api/sites` | 获取站点列表（可选 `?category_id=N` 筛选） |
| | | Get site list (filter with `?category_id=N`) |
| GET | `/api/sites?category_id=1` | 获取指定分类的站点 |
| | | Get sites by category |
| GET | `/api/stats` | 获取统计数据（站点数、分类数） |
| | | Get statistics (site count, category count) |

### 管理接口（需 Bearer Token） / Admin APIs (Bearer Token Required)

| 方法 / Method | 路径 / Path | 说明 / Description |
|:---:|:---|:---|
| POST | `/api/admin/login` | 登录，返回 Token |
| | | Login, return Token |
| GET | `/api/admin/verify` | 验证 Token 是否有效 |
| | | Verify Token validity |
| GET | `/api/admin/categories` | 获取全部分类（含站点数） |
| | | Get all categories (with site count) |
| POST | `/api/admin/categories` | 新增分类 |
| | | Create category |
| PUT | `/api/admin/categories/:id` | 编辑分类 |
| | | Update category |
| DELETE | `/api/admin/categories/:id` | 删除分类（级联删除站点） |
| | | Delete category (cascade delete sites) |
| GET | `/api/admin/sites` | 获取全部站点 |
| | | Get all sites |
| POST | `/api/admin/sites` | 新增站点 |
| | | Create site |
| PUT | `/api/admin/sites/:id` | 编辑站点 |
| | | Update site |
| DELETE | `/api/admin/sites/:id` | 删除站点 |
| | | Delete site |

**登录示例 / Login Example:**

```bash
curl -X POST http://localhost:5000/api/admin/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

---

## 🗄️ 数据库结构 / Database Structure

使用 **SQLite** 轻量级数据库，共 3 张表：  
Using **SQLite** lightweight database with 3 tables:

```sql
-- 分类表 / Categories Table
CREATE TABLE categories (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,       -- 分类名 / Category name
    icon        TEXT DEFAULT '📁',   -- Emoji 图标 / Emoji icon
    sort_order  INTEGER DEFAULT 0   -- 排序顺序 / Sort order
);

-- 站点表 / Sites Table
CREATE TABLE sites (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id  INTEGER NOT NULL,   -- 外键 → categories.id / Foreign key
    name         TEXT NOT NULL,      -- 站点名称 / Site name
    url          TEXT NOT NULL,      -- 链接地址 / URL
    description  TEXT DEFAULT '',    -- 描述 / Description
    badge        TEXT DEFAULT '',    -- 角标（🔥/API/国内）/ Badge
    domain       TEXT DEFAULT '',    -- 显示域名 / Display domain
    sort_order   INTEGER DEFAULT 0,  -- 排序顺序 / Sort order
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

-- 管理员表 / Admins Table
CREATE TABLE admins (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT NOT NULL UNIQUE,     -- 登录名 / Username
    password_hash TEXT NOT NULL             -- SHA256 密码哈希 / SHA256 password hash
);
```

---

## 🗺️ 站点分类一览 / Site Categories

| # | 分类 / Category | 站点数 / Count |
|:---:|:---|:---:|
| 1 | 💬 大语言模型 / 对话AI | 15 |
| | Large Language Models / Chat AI | |
| 2 | 🛠️ AI Agent 平台 | 8 |
| | AI Agent Platforms | |
| 3 | 🎨 AI 图像 / 视频生成 | 9 |
| | AI Image / Video Generation | |
| 4 | ⌨️ AI 编程助手 | 6 |
| | AI Coding Assistants | |
| 5 | 🔍 AI 搜索 & 效率工具 | 8 |
| | AI Search & Productivity | |
| 6 | 🎵 AI 音频 / 语音 | 5 |
| | AI Audio / Speech | |
| 7 | 📦 AI 开源社区 & 模型 | 7 |
| | AI Open Source & Models | |
| 8 | 📰 AI 资讯 & 社区 | 5 |
| | AI News & Community | |
| 9 | 📄 AI 办公效率 | 6 |
| | AI Office Productivity | |
| 10 | 🔌 AI API 聚合平台 | 5 |
| | AI API Aggregators | |
| 11 | 🎯 AI 设计工具 | 4 |
| | AI Design Tools | |
| | **合计 / Total** | **78** |

---

## 🛠️ 技术栈 / Tech Stack

| 技术 / Technology | 用途 / Usage |
|:---|:---|
| **Python Flask** | 后端 RESTful API 框架 / Backend RESTful API Framework |
| **SQLite** | 轻量级嵌入式数据库 / Lightweight Embedded Database |
| **HTML + CSS + JavaScript** | 前端页面（无框架，纯原生） / Frontend (Vanilla) |
| **localStorage** | 前端持久化（主题/Token） / Frontend Storage |
| **SHA256** | 密码加密存储 / Password Encryption |
| **CSS Variables** | 主题切换系统 / Theme Switch System |

---

## 📝 许可证 / License

本项目仅供学习和参考使用。  
This project is for learning and reference purposes only.
