# Quy cách năm ảnh nộp bài

Bài được chấm theo thứ tự `01` → `05`. Ảnh phải thấy đúng tài nguyên của repository
và không chứa credential.

## `01-mlflow-ui.png` — MLflow

Chụp danh sách runs tại <http://localhost:5000> sau khi sắp xếp F1 giảm dần. Ảnh cần
thấy:

- ít nhất ba runs;
- `f1_score` và `accuracy`;
- `n_estimators`, `learning_rate`, `max_depth`;
- URL trình duyệt.

Tham chiếu: [Bước 1](../../tasks/buoc-1.md).

## `02-actions-buoc-2.png` — Pipeline CI/CD

Chụp trang chi tiết GitHub Actions của Bước 2. Ảnh cần thấy:

- Unit Test, Train, Quality Gate và Release đều xanh;
- tiêu đề/commit của run;
- URL repository.

Tham chiếu: [Bước 2](../../tasks/buoc-2.md).

## `03-actions-buoc-3.png` — Continuous training

Chụp run do commit cập nhật `data/train_batch1.csv.dvc` tự kích hoạt. Ảnh cần thấy:

- event là **push**, không hiện “Manually triggered”;
- commit message `data: bổ sung 22361 mẫu dữ liệu mới (train_batch2)`;
- cả bốn jobs đều xanh;
- URL repository.

> Ảnh hiện tại là run #7 (ID `37611571848`), event `push`, commit `a6480b7`; cả
> bốn jobs đều xanh và đáp ứng tiêu chí tự động hóa.

Tham chiếu: [Bước 3](../../tasks/buoc-3.md).

## `04-curl-api.png` — FastAPI trên EC2

Chụp terminal có IP EC2, lệnh và kết quả của cả hai endpoint:

```bash
curl http://SERVER_IP:8080/healthz
curl -X POST http://SERVER_IP:8080/score \
  -H "Content-Type: application/json" \
  -d '{"features":[28,2,14,2,11,0,1,0,0,45]}'
```

Kết quả cần thấy `{"status":"ok"}` và prediction hợp lệ. Không dùng `localhost`
trong ảnh nộp.

## `05-cloud-storage.png` — Amazon S3

Chụp AWS Console, thấy rõ:

- tên bucket `income-lab-415150458684-us-east-1`;
- prefix `dvc/` có DVC objects;
- object `artifacts/current/model.joblib`;
- URL AWS Console.

Nếu không thể hiện hai prefix trong cùng một khung hình, dùng thêm
`05a-storage-dvc.png` và `05b-storage-model.png`, nhưng vẫn giữ ảnh `05` chính.

## Kiểm tra trước khi commit

- Đúng tên và định dạng PNG.
- Mỗi ảnh nhỏ hơn 1 MB.
- Không chứa AWS access key, SSH private key, token hoặc GitHub Secret.
- Không chỉnh sửa nội dung ảnh để tạo bằng chứng giả; nếu thiếu, chạy lại quy trình và
  chụp lại.
