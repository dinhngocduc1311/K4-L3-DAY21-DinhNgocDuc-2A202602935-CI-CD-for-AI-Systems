# Checklist nộp bài — Day 21

Thư mục này chứa toàn bộ bằng chứng được chấm trực tiếp trong repository.

```text
nop-bai/
├── README.md
├── bao-cao.md
└── anh-chup-man-hinh/
    ├── README.md
    ├── 01-mlflow-ui.png
    ├── 02-actions-buoc-2.png
    ├── 03-actions-buoc-3.png
    ├── 04-curl-api.png
    └── 05-cloud-storage.png
```

## Trạng thái

- [x] Repository GitHub ở chế độ public.
- [x] Đủ năm tệp ảnh đúng tên; mỗi ảnh nhỏ hơn 1 MB.
- [x] `bao-cao.md` có đủ bốn mục và không còn placeholder.
- [x] Báo cáo dùng số liệu thực tế của Bước 1, 2 và 3.
- [x] `03-actions-buoc-3.png` là run #7, event **push**, commit `a6480b7` và bốn jobs xanh.
- [x] Commit và push toàn bộ thay đổi cuối cùng; `vlearn.md` được giữ cục bộ và exclude khỏi Git.
- [x] Đã mở run bằng Chrome headless không đăng nhập, xác nhận repository và ảnh truy cập công khai.
- [ ] Dán URL repository vào bài nộp trên <https://vlearn.dev>.

## Đối chiếu rubric

| Bằng chứng | Nội dung chứng minh | Điểm chính |
|---|---|---:|
| `01-mlflow-ui.png` | Ít nhất ba runs, tham số, F1 và accuracy | 20 |
| `02-actions-buoc-2.png` | Bốn jobs CI/CD hoàn thành | 16 |
| `03-actions-buoc-3.png` | Commit dữ liệu tự kích hoạt pipeline | 12 |
| `04-curl-api.png` | FastAPI trên EC2 trả kết quả | 12 |
| `05-cloud-storage.png` | DVC objects và model artifact trên S3 | 12 |
| `bao-cao.md` | Lựa chọn tham số, F1 và phân tích kết quả | 8 |

## Trạng thái Bonus

- [x] Bonus 1: [DagsHub mirror](https://dagshub.com/dinhngocduc1311/K4-L3-DAY21-DinhNgocDuc-2A202602935-CI-CD-for-AI-Systems) + GitHub Secret hoạt động; MLflow run `d21216b` hoàn tất.
- [x] Bonus 2: quét threshold 0,10–0,90 và ghi F1/ngưỡng tối ưu vào report + MLflow.
- [x] Bonus 3: tạo `detail.txt` với confusion matrix, precision và recall từng lớp.
- [x] Bonus 4: so F1 với report hiện hành trên S3 trước khi cho phép release.
- [x] Bonus 5: kiểm tra tỷ lệ lớp dương trước train và cảnh báo khi lệch quá 5 điểm %.

## Quy ước bằng chứng

- Giữ nguyên tiền tố `01` đến `05` và định dạng PNG.
- Ảnh trình duyệt phải thấy URL, tên repo/bucket và phần nội dung cần chấm.
- Không che tên job, trạng thái, metrics, commit message hoặc đường dẫn object.
- Phải che email nếu muốn bảo mật; tuyệt đối không để lộ private key, access key,
  session token hay nội dung GitHub Secrets.
- Ảnh Bước 3 phải xuất phát từ event `push`, không dùng `workflow_dispatch`.
- Báo cáo tối đa một trang A4 và chỉ ghi kết quả đã kiểm chứng.

Chi tiết từng ảnh: [anh-chup-man-hinh/README.md](anh-chup-man-hinh/README.md).
