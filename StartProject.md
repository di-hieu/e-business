# Start Project

Hướng dẫn khởi động project trên Windows (PowerShell).

## 1. Tạo môi trường ảo (.venv)

```powershell
python -m venv .venv
```

## 2. Kích hoạt môi trường ảo

```powershell
.venv\Scripts\activate
```

## 3. Cài đặt dependencies

```powershell
pip install -r requirements.txt
```
## 4. Seed dữ liệu demo *(chỉ chạy 1 lần)*
```powershell
python seed_data.py
```

## 5. Chạy ứng dụng

```powershell
python run.py
```

## Tất cả lệnh trong một lần chạy

```powershell
python -m venv .venv; .venv\Scripts\activate; pip install -r requirements.txt; python run.py
```
