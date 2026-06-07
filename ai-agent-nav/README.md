# 🤖 国内 AI & Agent 导航站

> 收录国内主流人工智能平台 · AI Agent · 开发工具 · 创作工具  
> 前后端分离 | 数据持久化 | 管理后台 | 深色/浅色主题

---

## 📋 项目概述

一个功能完整的国内 AI 资源导航网站，收录 **78 个国内 AI 站点**，分为 **11 个分类**，支持：

- **🏠 公开导航页** — 浏览所有 AI 站点，分类展示，点击直达
- **🔐 管理后台** — 登录后对分类和站点进行增删改查
- **🌙 主题切换** — 深色/浅色模式自由切换，自动保存偏好
- **📊 数据持久化** — 使用 SQLite 数据库存储，重启不丢失

---

## 📁 项目结构

```
F:\ai-agent-nav\
├── backend\
│   ├── app.py         ← Flask 后端 API 服务（端口 5000）
│   ├── seed.py        ← 数据库初始化（创建表 + 导入 78 个站点）
│   └── nav.db         ← SQLite 数据库文件
├── frontend\
│   ├── index.html     ← 公开导航页（API 驱动渲染）
│   └── admin.html     ← 管理后台（登录 + CRUD）
└── README.md          ← 本文件
```

---

## 🚀 快速启动

### 环境要求

- Python 3.8+
- Flask + flask-cors（首次运行会自动安装）

### 启动步骤

```bash
# 1. 进入项目目录
cd /ai-agent-nav/backend

# 2. 安装依赖（首次运行）
pip install flask flask-cors

# 3. 初始化数据库（首次运行，或重置数据）
python seed.py

# 4. 启动服务
python app.py
```

启动后访问：

| 地址 | 说明 |
|:---|:---|
| `http://localhost:5000` | 🏠 公开导航首页 |
| `http://localhost:5000/admin` | 🔐 管理后台 |
| `http://localhost:5000/api/categories` | 📡 API - 获取分类及站点 |

---
当前端口在 app.py 最底部第 267 行，默认是 5000：

python
复制
app.run(host='0.0.0.0', port=5000, debug=True)

改端口有 3 种方法：

方法 1️⃣ 直接改代码（最简单）
打开 F:\ai-agent-nav\backend\app.py，找到最后一行，把 port=5000 改成你想要的端口，比如改成 8080：

python
复制
app.run(host='0.0.0.0', port=8080, debug=True)
然后重启服务就行了。

方法 2️⃣ 用命令行参数（不改文件）
启动时指定端口：

bash
复制
cd /f/ai-agent-nav/backend
python -c "from app import app; app.run(host='0.0.0.0', port=8080, debug=True)"
方法 3️⃣ 通过环境变量
bash
复制
cd /f/ai-agent-nav/backend
env FLASK_RUN_PORT=8080 python app.py
注意： 改端口后，浏览器访问地址也要跟着变，比如改成 http://localhost:8080。
## 🔧 功能详情

### 🏠 公开导航页

- 页面加载时通过 `fetch()` 调用后端 API 获取数据
- 分类卡片式布局，展示站点名称、描述、标签、域名
- 点击卡片直接跳转到目标站点
- 左上角主题切换按钮（深色/浅色，自动记忆）
- 右上角「管理」入口链接
- 统计栏实时显示站点总数和分类数

### 🔐 管理后台

**登录信息：** 用户名 `admin` / 密码 `admin123`

**功能模块：**

| 模块 | 功能 |
|:---|:---|
| 📊 **仪表盘** | 站点/分类总数统计，各分类站点分布表 |
| 📂 **分类管理** | 新增、编辑、删除分类（删除级联删除站点） |
| 🔗 **站点管理** | 按分类筛选、新增、编辑、删除站点 |

- 所有操作实时写入 SQLite 数据库
- 登录 Token 保存在 localStorage，刷新不丢失
- 退出登录自动跳转首页

### 🌙 主题切换

- 首页和管理后台均支持深色/浅色切换
- 主题偏好存储在 `localStorage`，跨页面共享
- 深色：暗紫黑背景 + 霓虹紫色调
- 浅色：柔白灰背景 + 紫色强调

---

## 📡 API 接口文档

### 公开接口（无需认证）

| 方法 | 路径 | 说明 |
|:---:|:---|:---|
| GET | `/api/categories` | 获取所有分类及下属站点 |
| GET | `/api/sites` | 获取站点列表（可选 `?category_id=N` 筛选） |
| GET | `/api/sites?category_id=1` | 获取指定分类的站点 |
| GET | `/api/stats` | 获取统计数据（站点数、分类数） |

### 管理接口（需 Bearer Token）

| 方法 | 路径 | 说明 |
|:---:|:---|:---|
| POST | `/api/admin/login` | 登录，返回 Token |
| GET | `/api/admin/verify` | 验证 Token 是否有效 |
| GET | `/api/admin/categories` | 获取全部分类（含站点数） |
| POST | `/api/admin/categories` | 新增分类 |
| PUT | `/api/admin/categories/:id` | 编辑分类 |
| DELETE | `/api/admin/categories/:id` | 删除分类（级联删除站点） |
| GET | `/api/admin/sites` | 获取全部站点 |
| POST | `/api/admin/sites` | 新增站点 |
| PUT | `/api/admin/sites/:id` | 编辑站点 |
| DELETE | `/api/admin/sites/:id` | 删除站点 |

**登录示例：**

```bash
curl -X POST http://localhost:5000/api/admin/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

---

## 🗄️ 数据库结构

使用 **SQLite** 轻量级数据库，共 3 张表：

```sql
-- 分类表
CREATE TABLE categories (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,       -- 分类名
    icon        TEXT DEFAULT '📁',   -- Emoji 图标
    sort_order  INTEGER DEFAULT 0   -- 排序顺序
);

-- 站点表
CREATE TABLE sites (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id  INTEGER NOT NULL,   -- 外键 → categories.id
    name         TEXT NOT NULL,      -- 站点名称
    url          TEXT NOT NULL,      -- 链接地址
    description  TEXT DEFAULT '',    -- 描述
    badge        TEXT DEFAULT '',    -- 角标（🔥/API/国内）
    domain       TEXT DEFAULT '',    -- 显示域名
    sort_order   INTEGER DEFAULT 0,  -- 排序顺序
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

-- 管理员表
CREATE TABLE admins (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT NOT NULL UNIQUE,     -- 登录名
    password_hash TEXT NOT NULL             -- SHA256 密码哈希
);
```

---

## 🗺️ 站点分类一览

| # | 分类 | 站点数 |
|:---:|:---|:---:|
| 1 | 💬 大语言模型 / 对话AI | 15 |
| 2 | 🛠️ AI Agent 平台 | 8 |
| 3 | 🎨 AI 图像 / 视频生成 | 9 |
| 4 | ⌨️ AI 编程助手 | 6 |
| 5 | 🔍 AI 搜索 & 效率工具 | 8 |
| 6 | 🎵 AI 音频 / 语音 | 5 |
| 7 | 📦 AI 开源社区 & 模型 | 7 |
| 8 | 📰 AI 资讯 & 社区 | 5 |
| 9 | 📄 AI 办公效率 | 6 |
| 10 | 🔌 AI API 聚合平台 | 5 |
| 11 | 🎯 AI 设计工具 | 4 |
| | **合计** | **78** |

---

## 🛠️ 技术栈

| 技术 | 用途 |
|:---|:---|
| **Python Flask** | 后端 RESTful API 框架 |
| **SQLite** | 轻量级嵌入式数据库 |
| **HTML + CSS + JavaScript** | 前端页面（无框架，纯原生） |
| **localStorage** | 前端持久化（主题/Token） |
| **SHA256** | 密码加密存储 |
| **CSS Variables** | 主题切换系统 |

---

## 📝 许可证

本项目仅供学习和参考使用，如有转发请注明出处。
