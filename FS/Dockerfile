FROM python:3.9-slim
WORKDIR /app
# 安裝 Flask
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# 聲明 FS 使用的 Port
EXPOSE 9090
CMD ["python", "fs.py"]