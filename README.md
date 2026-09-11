# Facebook — mở phiên cá nhân

Ứng dụng Python có giao diện nhập cookie, mở Chromium với phiên riêng.
Dùng trên máy tính Windows/macOS/Linux có Python 3.10 trở lên và Tkinter.
Không chạy trực tiếp trên iPhone/iPad. Đây là mã nguồn, chưa phải tệp .exe.

## Cài đặt

Giải nén, mở terminal trong thư mục dự án:

```sh
python -m venv .venv
```

Windows:

```bat
.venv\Scripts\activate
```

macOS/Linux (dùng `python3` nếu máy không có lệnh `python`):

```sh
source .venv/bin/activate
```

Sau đó:

```sh
python -m pip install -r requirements.txt
python -m playwright install chromium
python app.py
```

Nếu thiếu Tkinter trên Ubuntu/Debian: cài gói `python3-tk` của hệ điều hành.
Nếu Chromium báo thiếu thư viện trên Linux, chạy `python -m playwright install --with-deps chromium` (có thể cần quyền quản trị).

## Sử dụng

1. Nhập chuỗi cookie phiên của chính bạn theo dạng `c_user=…; xs=…; …`.
   Hỗ trợ chuỗi Cookie header một dòng, không hỗ trợ JSON hoặc Netscape cookie file.
2. Bấm **Mở Facebook**; nội dung ô nhập sẽ được xóa.
3. Kiểm tra trực tiếp tài khoản trong cửa sổ Chromium. Việc mở trang không chứng minh đăng nhập thành công.
4. Đóng cửa sổ ứng dụng để đóng phiên Chromium, hoặc đóng tất cả các tab Chromium.

Cookie là thông tin đăng nhập nhạy cảm: không gửi vào chat, chia sẻ hoặc commit lên GitHub.
Ứng dụng không thu thập cookie từ trình duyệt khác, không lưu tệp cookie, không in cookie vào log.
Cookie được nạp vào ngữ cảnh trình duyệt tạm thời và gửi cho miền Facebook để khôi phục phiên.
Nội dung clipboard bạn đã sao chép không được ứng dụng xóa tự động.
Cookie hết hạn, bị thu hồi hoặc phiên bị Facebook yêu cầu xác minh sẽ cần đăng nhập/xác minh theo giao diện Facebook; ứng dụng không vượt qua các bước đó.
Đóng phiên cục bộ không thu hồi cookie trên máy chủ; dùng phần quản lý phiên của Facebook nếu cần thu hồi.

## Kiểm tra

```sh
python -m unittest discover -s tests -v
```

Kiểm thử dùng dữ liệu giả để xác minh bộ đọc cookie. Chưa xác minh đăng nhập bằng tài khoản Facebook thật hoặc chạy giao diện trên từng hệ điều hành.

API tham khảo: https://playwright.dev/python/docs/api/class-browsercontext#browser-context-add-cookies
