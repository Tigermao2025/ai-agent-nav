# 使用官方 Python 镜像
FROM python:3.12-slim

WORKDIR /app

# 安装依赖
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# 复制项目文件
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# 修改 app.py 支持环境变量设置数据库路径
RUN sed -i 's|DB_PATH = os.path.join(BASE_DIR, .nav.db.*)|DB_PATH = os.environ.get("DB_PATH", "/app/data/nav.db")|' /app/backend/app.py

# 初始化数据库目录
RUN mkdir -p /app/data

# 暴露端口
EXPOSE 5000

# 启动前初始化数据库，然后启动服务
CMD if [ ! -f "$DB_PATH" ] || [ "$(ls -A $DB_PATH 2>/dev/null)" = "" ]; then \
      cd /app/backend && python seed.py; \
    fi && \
    python /app/backend/app.py
