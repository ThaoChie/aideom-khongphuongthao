# AIDEOM-VN Dashboard

**AIDEOM-VN** (Artificial Intelligence and Digital Economy Optimization Models for Vietnam) là một hệ thống hỗ trợ ra quyết định đa mô hình, được xây dựng để đánh giá tác động của Chuyển đổi số và Trí tuệ Nhân tạo (AI) lên nền kinh tế, thị trường lao động và chiến lược phân bổ ngân sách của Việt Nam. Hệ thống bao gồm 12 bài toán mô phỏng tối ưu hóa từ quy mô vĩ mô đến vi mô, được tích hợp vào một Dashboard trực quan.

## Cấu trúc thư mục

- `Application/`: Chứa mã nguồn của giao diện Dashboard xây dựng bằng Streamlit (`app.py`).
- `src/`: Mã nguồn Python lõi chứa các hàm tối ưu hóa (`optimization.py`, `rl_env.py`, `data_loader.py`).
- `notebooks/`: Các file Jupyter Notebook giải thích chi tiết thuật toán và biểu diễn dữ liệu của từng bài toán.
- `data/`: Dữ liệu đầu vào ở định dạng CSV (Macro 2020-2025, Sectors 2024, Regions 2024).

---

## Hướng dẫn cài đặt và chạy trên Local (macOS & Windows)

### Yêu cầu hệ thống
- **Python:** Phiên bản 3.9 trở lên (Khuyến nghị 3.11 hoặc 3.12).
- Các thư viện cần thiết đã được liệt kê trong file `requirements.txt`.

### Bước 1: Clone hoặc tải mã nguồn về máy
Mở Terminal (macOS) hoặc Command Prompt / PowerShell (Windows) và di chuyển vào thư mục dự án:
```bash
cd du-an-aideom-vn
```

### Bước 2: Tạo và kích hoạt môi trường ảo (Virtual Environment)
Việc sử dụng môi trường ảo giúp tránh xung đột thư viện giữa các dự án trên máy.

**Trên macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Trên Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

### Bước 3: Cài đặt các thư viện cần thiết
Đảm bảo bạn đang ở trong môi trường ảo (có chữ `(.venv)` ở đầu dòng lệnh), sau đó chạy lệnh cài đặt:
```bash
pip install -r requirements.txt
```
*Lưu ý: Quá trình này có thể mất vài phút để tải các gói như `numpy`, `pandas`, `streamlit`, `stable-baselines3`, `pulp`, `cvxpy`,...*

### Bước 4: Khởi chạy Dashboard
Chạy lệnh sau để khởi động ứng dụng Streamlit:
```bash
streamlit run Application/app.py
```

Sau khi chạy lệnh, trình duyệt web mặc định của bạn sẽ tự động mở lên địa chỉ:
👉 **http://localhost:8501**

Từ đây, bạn có thể tương tác với giao diện của cả 12 Bài toán thông qua menu điều hướng bên trái.

---

## Khắc phục sự cố thường gặp (Troubleshooting)
- **Lỗi không tìm thấy module (`ModuleNotFoundError`)**: Chắc chắn rằng bạn đã kích hoạt môi trường ảo `.venv` và đã chạy lệnh `pip install -r requirements.txt`.
- **Lỗi cổng (Port already in use)**: Nếu cổng 8501 đã bị sử dụng, Streamlit sẽ tự động tìm cổng 8502, 8503... Bạn cũng có thể tự định nghĩa cổng chạy bằng tham số `--server.port`, ví dụ: `streamlit run Application/app.py --server.port 8080`.
