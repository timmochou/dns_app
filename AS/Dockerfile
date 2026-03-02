FROM python:3.9-slim
WORKDIR /app
COPY . .
# 不需要安裝任何套件，因為沒用到 Flask
# 聲明 UDP Port
EXPOSE 53533/udp
CMD ["python", "as.py"]