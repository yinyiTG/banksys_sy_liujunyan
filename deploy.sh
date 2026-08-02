#!/usr/bin/env bash
# CD 部署脚本:在服务器上构建镜像并启动容器。
# 前置:仓库文件已由 CI 上传到当前目录(DEPLOY_DIR)。
set -e

APP=banksys_sy_liujunyan
PORT=8888
PORT_MAX=8897
CONTAINER_PORT=8888

echo ">> 开始部署 $APP 到 $(pwd)"

# 构建镜像(国内服务器用清华源)
docker build --build-arg PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple -t "$APP":latest .

# 端口:容器内端口固定;主机端口优先 8888,被占用就在预留区间自动找空闲端口
port_in_use() {
  ss -ltnH 2>/dev/null | grep -q ":$1 " && return 0
  docker ps --format "{{.Ports}}" 2>/dev/null | grep -q ":$1->" && return 0
  return 1
}
HOST_PORT=""
for p in $(seq "$PORT" "$PORT_MAX"); do
  if ! port_in_use "$p"; then HOST_PORT="$p"; break; fi
done
[ -z "$HOST_PORT" ] && { echo "预留端口区间已全部占用,部署中止"; exit 1; }
echo ">> 部署到主机端口 $HOST_PORT"

# 一步停删自身旧容器,幂等可重跑
docker rm -f "$APP" 2>/dev/null || true
docker run -d --name "$APP" --restart unless-stopped -p "${HOST_PORT}:${CONTAINER_PORT}" "$APP":latest
echo ">> 部署成功:容器 $APP 已启动,主机端口 ${HOST_PORT} -> 容器内 ${CONTAINER_PORT}"
