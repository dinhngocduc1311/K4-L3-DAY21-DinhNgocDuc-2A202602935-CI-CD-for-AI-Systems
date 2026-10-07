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
- [x] `03-actions-buoc-3.png` là run #5, event **push**, đúng commit dữ liệu và bốn jobs xanh.
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

## Quy ước bằng chứng

- Giữ nguyên tiền tố `01` đến `05` và định dạng PNG.
- Ảnh trình duyệt phải thấy URL, tên repo/bucket và phần nội dung cần chấm.
- Không che tên job, trạng thái, metrics, commit message hoặc đường dẫn object.
- Phải che email nếu muốn bảo mật; tuyệt đối không để lộ private key, access key,
  session token hay nội dung GitHub Secrets.
- Ảnh Bước 3 phải xuất phát từ event `push`, không dùng `workflow_dispatch`.
- Báo cáo tối đa một trang A4 và chỉ ghi kết quả đã kiểm chứng.

Chi tiết từng ảnh: [anh-chup-man-hinh/README.md](anh-chup-man-hinh/README.md).
