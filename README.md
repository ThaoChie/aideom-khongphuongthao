# AIDEOM-VN eLearning Decision Lab v5

Bản thiết kế lại theo change request:

- Chuyển từ dashboard tổng hợp sang mô hình **eLearning 11 bài học**.
- Sidebar trái hiển thị đầy đủ **Bài 1 → Bài 11**.
- Mỗi bài có **file Python độc lập** tại `backend/core/lessons/lessonXX_*.py`.
- Hệ số/tham số đề xuất của từng mô hình có thể **tinh chỉnh bằng slider/input** trên web.
- Mỗi bài có dashboard tối thiểu 4 tab:
  1. Tổng quan
  2. Phân bổ
  3. Kịch bản so sánh
  4. Cảnh báo rủi ro
- Giữ phong cách UI/UX hiện tại: light futuristic minimalism, card bo góc lớn, gradient xanh, dashboard SaaS.

## Chạy nhanh bằng Docker

```bash
cp .env.example .env
docker compose up --build --force-recreate
```

Truy cập:

- Frontend: http://localhost:5173
- Backend API: http://localhost:8001/api
- MySQL host port: 3307

> Bản này dùng port `8001` và `3307` để tránh xung đột với các container cũ đang dùng `8000`/`3306`.

## API chính

```text
GET  /api/health/
GET  /api/lessons/
GET  /api/lessons/<lesson_id>/
POST /api/lessons/<lesson_id>/run/
POST /api/pipeline/run/
```

Ví dụ:

```bash
curl http://localhost:8001/api/lessons/

curl -X POST http://localhost:8001/api/lessons/lesson01/run/   -H 'Content-Type: application/json'   -d '{"params":{"alpha":0.33,"beta":0.42,"gamma":0.10,"delta":0.08,"theta":0.07}}'
```

## Chạy local backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

## Chạy local frontend

```bash
cd frontend
npm install
VITE_API_BASE_URL=http://localhost:8000/api npm run dev
```

## Cấu trúc chính

```text
backend/core/lessons/
  lesson01_cobb_douglas.py
  lesson02_simple_lp.py
  lesson03_priority_index.py
  lesson04_region_lp.py
  lesson05_mip_projects.py
  lesson06_topsis.py
  lesson07_nsga_pareto.py
  lesson08_dynamic_optimization.py
  lesson09_labor_ai.py
  lesson10_stochastic.py
  lesson11_q_learning.py
frontend/src/
  App.jsx
  style.css
```

## Lưu ý triển khai

Đây là bản prototype sạch để demo đồ án/eLearning. Các solver nặng như NSGA-II/Pyomo/DQN được mô phỏng gọn bằng NumPy/SciPy để chạy ổn định trên máy cá nhân và Docker. Có thể thay từng `lessonXX_*.py` bằng implementation học thuật đầy đủ sau này mà không đổi giao diện.
