"""Local Facebook session opener. Never stores or logs entered cookies."""
import queue
import re
import threading


def parse_cookies(raw):
    raw = raw.strip()
    if not raw or len(raw) > 65536 or any(ord(c) < 32 or ord(c) == 127 for c in raw):
        raise ValueError("Cookie trống, quá dài hoặc chứa ký tự điều khiển.")
    if raw.lower().startswith("cookie:"):
        raw = raw[7:].strip()
    result = {}
    for item in raw.split(";"):
        if not item.strip():
            continue
        name, sep, value = item.strip().partition("=")
        name, value = name.strip(), value.strip()
        if not sep or not re.fullmatch(r"[!#$%&'*+.^_`|~0-9A-Za-z-]+", name):
            raise ValueError("Dùng định dạng tên=giá_trị; tên_khác=giá_trị.")
        if name in result:
            raise ValueError("Cookie chứa tên bị lặp; hãy dùng một phiên duy nhất.")
        result[name] = value
    if not result.get("c_user") or not result.get("xs"):
        raise ValueError("Thiếu cookie phiên c_user hoặc xs.")
    return [dict(name=n, value=v, domain=".facebook.com", path="/", secure=True)
            for n, v in result.items()]


def open_session(cookies, events, stop):
    try:
        from playwright.sync_api import sync_playwright, TimeoutError
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            try:
                context = browser.new_context(accept_downloads=False)
                context.add_cookies(cookies)
                cookies.clear()
                page = context.new_page()
                try:
                    page.goto("https://www.facebook.com/", wait_until="domcontentloaded", timeout=30000)
                    events.put("Đã mở Facebook. Kiểm tra tài khoản trên trình duyệt; có thể cần xác minh.")
                except TimeoutError:
                    events.put("Trang tải chậm. Kiểm tra mạng hoặc tải lại trong trình duyệt.")
                while browser.is_connected() and context.pages and not stop.is_set():
                    context.pages[0].wait_for_timeout(200)
            finally:
                browser.close()
    except ImportError:
        events.put("Chưa cài Playwright. Xem các lệnh cài đặt trong README.md.")
    except Exception:
        # Raw automation errors may include cookie values; do not log them.
        events.put("Phiên đã đóng hoặc không mở được. Kiểm tra cài đặt Chromium và kết nối mạng.")
    finally:
        cookies.clear()
        events.put(None)


def main():
    import tkinter as tk
    from tkinter import ttk, messagebox
    root = tk.Tk()
    root.title("Facebook — mở phiên cá nhân")
    root.geometry("620x300")
    root.minsize(540, 300)
    panel = ttk.Frame(root, padding=20)
    panel.pack(fill="both", expand=True)
    ttk.Label(panel, text="Mở Facebook bằng cookie của bạn", font=("Arial", 16, "bold")).pack(anchor="w")
    ttk.Label(panel, text="Chỉ nhập cookie của tài khoản bạn sở hữu hoặc được phép sử dụng.", wraplength=550).pack(anchor="w", pady=(10, 6))
    entry = ttk.Entry(panel, show="•")
    entry.pack(fill="x", pady=8)
    entry.focus_set()
    ttk.Label(panel, text="Định dạng: c_user=…; xs=…; …  •  Không lưu cookie thành tệp.").pack(anchor="w")
    status = tk.StringVar(value="Sẵn sàng. Cookie hết hạn có thể không đăng nhập được.")
    events, stop = queue.Queue(), threading.Event()
    worker = None
    closing = False

    def start():
        nonlocal worker
        try:
            cookies = parse_cookies(entry.get())
        except ValueError as exc:
            messagebox.showerror("Kiểm tra cookie", str(exc))
            return
        entry.delete(0, "end")
        stop.clear()
        button.config(state="disabled")
        status.set("Đang mở trình duyệt…")
        worker = threading.Thread(target=open_session, args=(cookies, events, stop))
        worker.start()

    def close():
        nonlocal closing
        closing = True
        entry.delete(0, "end")
        button.config(state="disabled")
        status.set("Đang đóng phiên…")
        stop.set()

    def poll():
        while not events.empty():
            event = events.get_nowait()
            if event is None:
                if not closing:
                    button.config(state="normal")
            else:
                status.set(event)
        if closing and (worker is None or not worker.is_alive()):
            root.destroy()
            return
        root.after(100, poll)

    button = ttk.Button(panel, text="Mở Facebook", command=start)
    button.pack(anchor="w", pady=14)
    ttk.Label(panel, textvariable=status, wraplength=550).pack(anchor="w")
    root.protocol("WM_DELETE_WINDOW", close)
    root.after(100, poll)
    root.mainloop()


if __name__ == "__main__":
    main()
