# Sử dụng Python 3.10.11-slim làm base image
# Phiên bản slim giúp giảm kích thước image cuối cùng.
FROM python:3.10.11-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

#############################################################
# BƯỚC 01: CÀI ĐẶT THƯ VIỆN CẦN THIẾT
#############################################################
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

#############################################################
# BƯỚC 02: CONFIGURE CƠ SỞ DỮ LIỆU, PRE-TRAINED MODEL
#############################################################


