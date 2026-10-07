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

Chọn `n_estimators=200`, `learning_rate=0.1`, `max_depth=5`: F1 cao nhất và vượt
gate `0.65`. Lần 1 nhỉnh hơn về accuracy nhưng kém F1; lần 2 có ít cây, tốc độ học
thấp và cây nông nên chưa bù đủ sai số.

## 2. Vì sao Quality Gate dùng F1

Lớp thu nhập cao chỉ chiếm 24,77%; đoán toàn lớp thấp vẫn đạt 75,23% accuracy nhưng
bỏ sót mọi mẫu dương. F1 kết hợp precision và recall nên phản ánh cả gán nhầm lẫn bỏ
sót. Pipeline dùng `f1_score(y_eval, preds)` riêng cho `target=1`, không dùng macro hay
weighted average vì lớp đa số có thể che lấp hiệu quả trên lớp thiểu số.

## 3. Khó khăn và cách giải quyết

| Khó khăn | Nguyên nhân | Cách giải quyết |
|---|---|---|
| GitHub OIDC bị AWS từ chối | Trust policy chưa khớp claim repository/branch | Khóa `aud`, `sub` đúng repo và nhánh `main` |
| SSH deploy cần mở cổng 22 | IP GitHub runner thay đổi | Chỉ mở `/32` của runner và luôn thu hồi bằng `if: always()` |
| DVC/CI cần AWS credential | Không được lưu access key dài hạn | Dùng OIDC cho runner và instance role cho EC2 |

## 4. So sánh Bước 2 và Bước 3

| Chỉ số | Bước 2 — 22.361 mẫu | Bước 3 — 44.722 mẫu | Chênh lệch |
|---|---:|---:|---:|
| `f1_score` | 0.7149321267 | 0.7354260090 | +0.0204938823 |
| `accuracy` | 0.8740 | 0.8820 | +0.0080 |

F1 tăng 0,0205 và accuracy tăng 0,0080. Biên tăng nhỏ vì hai batch cùng nguồn và
phân phối tương tự. Bước 3 xác nhận chuỗi DVC → GitHub Actions → Quality Gate → S3 →
EC2 chạy tự động, tái lập được từ một commit dữ liệu.

## 5. Phần Bonus đã thực hiện

- [ ] Bonus 1 — Workflow đã hỗ trợ DagsHub; còn thiếu secret `DAGSHUB_USER_TOKEN` và run từ xa.
- [x] Bonus 2 — Quét 17 ngưỡng 0,10–0,90; F1 tăng từ 0,7354 lên 0,7537 tại ngưỡng 0,30.
- [x] Bonus 3 — `detail.txt` chứa matrix, precision/recall từng lớp; ưu tiên giảm false negative thu nhập cao.
- [x] Bonus 4 — Gate so F1 mới/cũ từ S3; chỉ publish khi `new_f1 >= current_f1`.
- [x] Bonus 5 — Trước train, tỷ lệ dương 0,2478 lệch dưới 5 điểm %, nên không cảnh báo.
