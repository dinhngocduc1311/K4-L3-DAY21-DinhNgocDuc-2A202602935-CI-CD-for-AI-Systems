# Báo cáo Lab Day 21 — CI/CD cho AI Systems

| | |
|---|---|
| Họ và tên | Đinh Ngọc Đức |
| MSSV | 2A202602935 |
| Lớp / Khóa | K4 |
| Repo GitHub | <https://github.com/dinhngocduc1311/K4-L3-DAY21-DinhNgocDuc-2A202602935-CI-CD-for-AI-Systems> |
| Cloud | AWS — S3, EC2, IAM/OIDC |
| Ngày nộp | 07/10/2026 |

## 1. Bộ siêu tham số đã chọn

| Lần | `n_estimators` | `learning_rate` | `max_depth` | `f1_score` | `accuracy` |
|---:|---:|---:|---:|---:|---:|
| 1 | 100 | 0.1 | 3 | 0.7109 | 0.8780 |
| 2 | 50 | 0.05 | 2 | 0.6051 | 0.8460 |
| 3 | 200 | 0.1 | 5 | **0.7149** | 0.8740 |

Chọn `n_estimators=200`, `learning_rate=0.1`, `max_depth=5` vì lần 3 có F1 cao
nhất và vượt Quality Gate `0.65`. Lần 1 có accuracy cao nhất nhưng F1 thấp hơn. Lần
2 có learning rate thấp, ít cây và cây nông nên chưa bù đủ sai số.

## 2. Vì sao Quality Gate dùng F1

Chỉ 24,77% dữ liệu ban đầu thuộc lớp thu nhập cao. Mô hình luôn dự đoán thu nhập
thấp vẫn đạt khoảng 75,23% accuracy nhưng không nhận diện được mẫu dương nào. F1 kết
hợp precision và recall nên phản ánh cả dự đoán dương sai lẫn mẫu dương bị bỏ sót.
Pipeline dùng `f1_score(y_eval, preds)` cho `target=1`; không dùng weighted average vì
lớp đa số sẽ kéo điểm lên, và không dùng macro average vì mục tiêu là đánh giá trực
tiếp lớp thiểu số.

## 3. Khó khăn và cách giải quyết

| Khó khăn | Nguyên nhân | Cách giải quyết |
|---|---|---|
| MLflow lỗi metadata khi test | Test dùng chung tracking state cục bộ | Dùng SQLite và `tmp_path` riêng cho từng test |
| GitHub OIDC bị AWS từ chối | Trust policy chưa khớp claim repository/branch | Khóa `aud`, `sub` đúng repo và nhánh `main` |
| SSH deploy cần mở cổng 22 | IP GitHub runner thay đổi | Chỉ mở `/32` của runner và luôn thu hồi bằng `if: always()` |
| DVC/CI cần AWS credential | Không được lưu access key dài hạn | Dùng OIDC cho runner và instance role cho EC2 |
| Push không kích hoạt Actions trên fork | Trạng thái automation của fork chưa được khởi tạo đúng | Reset Actions, bật lại workflow và xác nhận run #5 có event `push` |

## 4. So sánh Bước 2 và Bước 3

| Chỉ số | Bước 2 — 22.361 mẫu | Bước 3 — 44.722 mẫu | Chênh lệch |
|---|---:|---:|---:|
| `f1_score` | 0.7149321267 | 0.7354260090 | +0.0204938823 |
| `accuracy` | 0.8740 | 0.8820 | +0.0080 |

Sau khi ghép batch 2, F1 tăng khoảng 0,0205 và accuracy tăng 0,0080. Mức tăng nhỏ vì
hai batch lấy từ cùng nguồn và có phân phối tương tự. Giá trị chính của Bước 3 là xác
minh dữ liệu được phiên bản hóa bằng DVC, huấn luyện trên GitHub Actions, vượt Quality
Gate, tải model lên S3 và cập nhật API trên EC2 theo cùng một pipeline tái lập được.
