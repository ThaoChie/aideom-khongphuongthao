FROM python:3.10-slim

WORKDIR /app

# Cài đặt các thư viện hệ thống cần thiết cho các solver tối ưu hóa (GLPK, CBC)
RUN apt-get update && apt-get install -y \
    git \
    glpk-utils \
    coinor-cbc \
    && rm -rf /var/lib/apt/lists/*

# Copy file requirements.txt vào container
COPY requirements.txt .

# Cài đặt các thư viện Python
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ source code vào container
COPY . .

# Expose port cho Streamlit
EXPOSE 8501

# Chạy ứng dụng Streamlit
CMD ["streamlit", "run", "Application/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
