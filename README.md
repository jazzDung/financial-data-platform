# Project 3

### Workflow
- Mọi người set up Postgresql, TimescaleDB, Docker
- Dùng script Create Table để tạo bảng
- Dùng các lệnh trong script Import csv to table để import file csv vào bảng
- Build file docker-compose trên Docker để bắt đầu xử dụng Airflow
- Mở remote access cho database, kết nối Airflow với database tại mục Admin/Connections
- Viết thử 1 vài file DAG để thực hiện các tác vụ tính toán hoặc tác động lên database

### API
Chứa code python phục vụ các công việc sau:

- Lấy dữ liệu từ API TCBS, lưu dưới dạng file CSV
- Viết lệnh SQL tạo bảng Postgres
- Các file trong này chỉ dùng để vọc vạch chứ không chạy cũng được vì file CSV đã có sẵn

### Formatted Data

- Chứa các file CSV dữ liệu từ API, đã sửa format để sẵn sàng nhập vào bảng Postgres

### Sample Data

- Một số dữ liệu mẫu có được khi sử dụng thư viện vnStock

### SQL Script

- Create Table.sql: Lệnh SQL tạo bảng
- Hypertable and testing: Lệnh biến các bảng có time-series thành TimescaleDB hypertable
- Hình ảnh biểu diễn schema bảng
- Import csv to table: Các lệnh import record từ file CSV vào bảng, chạy trên psql terminal0

### Airflow

- docker-compose.yaml: File docker compose, chạy file này trên terminal để build các container cần thiết để sử dụng airflow
- dags: Folder chứa các file dag, dùng để thiết lập các task sẽ chạy trên Airflow
