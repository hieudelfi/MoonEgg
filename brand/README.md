# Nhận diện — tên và biểu tượng

## Tên
**Trứng Trăng** · khẩu hiệu: *Mỗi ngày nở một từ* · tên kỹ thuật (package/domain): `trungtrang`

Vì sao: gắn thẳng với nhân vật phi hành gia nở từ vỏ trứng trên Mặt Trăng; hai tiếng, cùng vần "tr", dễ nhớ và dễ đọc với người Việt; ẩn dụ "nở" khớp thông điệp sản phẩm (mỗi ngày mở ra một từ) và khớp cơ chế cột mốc (nhân vật ra khỏi trứng).

Tên tiếng Anh khi cần: **MoonEgg** (App Store/Play có thể để "Trứng Trăng — MoonEgg").

Trước khi chốt (task 4.1): kiểm trùng trên Google Play, App Store, tra nhãn hiệu tại noip.gov.vn, kiểm tên miền trungtrang.com / .vn / .app.

## Tên dự phòng (nếu trùng)
| Tên | Nghĩa | Ghi chú |
| --- | --- | --- |
| Nở Từ | mỗi ngày một từ "nở" ra | ngắn, hơi lạ tai |
| Vỏ Trứng | ẩn dụ bước ra khỏi vùng an toàn | kém vui hơn |
| Mochi Trăng | thân thiện | dễ nhầm MochiMochi — tránh |
| WordHatch | tiếng Anh, "nở từ" | dùng cho bản quốc tế |

## Biểu tượng
`app-icon.svg` (nguồn vector, 512 viewBox) · `app-icon-1024.png` (nộp store).

Thiết kế: mũ phi hành gia kính vàng nhô lên từ vỏ trứng nứt, trên nền trời đêm và bề mặt Mặt Trăng. Kính vàng đọc được như lòng đỏ trứng ở cỡ nhỏ — đó là điểm nhận diện.

Kiểm tra đã làm: đọc được ở 64 px; không chữ; không giống linh vật app khác; nguyên bản (vẽ vector, không dùng ảnh AI).

Bảng màu (khớp docs/06-thiet-ke-ui-ux.md):
- Trời đêm `#1F2A44` → `#162038`
- Vỏ trứng `#FFF3E0`, viền `#E3D2B8`
- Kính vàng `#FFD98A` → `#E8A33C` → `#C97A1A`
- Mực `#2B2622`, Mặt Trăng `#8D93A8`/`#6F7590`
- San hô nhấn `#E8735A` (ngôi sao nhỏ)

Còn phải làm (task 2.1 và 4.1):
- Xuất bộ kích thước: iOS 1024 + các cỡ; Android adaptive icon (foreground vỏ trứng + mũ, background nền đêm), maskable 512, favicon 32/180, splash.
- Bản đơn sắc cho notification Android (trắng trên trong suốt).
- Kiểm hiển thị trên nền sáng/tối và trong thư mục app thật.
