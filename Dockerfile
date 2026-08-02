FROM python:3.11-slim

# 镜像源可配置,国内服务器可使用清华源
ARG PIP_INDEX_URL=https://pypi.org/simple
ENV PYTHONPATH=/app/src

WORKDIR /app

# 安装 curl 供健康检查使用(slim 镜像默认不带)
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# 先装依赖,利用镜像层缓存
COPY requirements.txt .
RUN pip install --no-cache-dir --timeout 120 -i "${PIP_INDEX_URL}" -r requirements.txt

# 复制源码与数据,并在构建时离线训练模型(模型默认不进 Git)
COPY src/ /app/src/
COPY data/ /app/data/
RUN python -m banksys_sy_liujunyan.train

EXPOSE 8888

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD curl -fsS http://localhost:8888/_stcore/health || exit 1

CMD ["streamlit", "run", "src/banksys_sy_liujunyan/app.py", "--server.port=8888", "--server.address=0.0.0.0"]
