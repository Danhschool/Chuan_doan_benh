import streamlit as st
import os
import time

# 🔹 Đọc danh sách user hoặc admin
def read_accounts(file_path):
    accounts = {}
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 2:
                    username, password = parts[0], parts[1]
                    accounts[username] = password
    return accounts

# 🔹 Ghi thêm user mới (luôn xuống dòng đúng cách)
def save_user(username, password, file_path="./TaiKhoan/users.txt"):
    with open(file_path, "a", encoding="utf-8") as f:
        if os.path.getsize(file_path) > 0:  # nếu file không rỗng
            f.write("\n")
        f.write(f"{username} {password}")

# 🔹 Giao diện đăng ký
def DangKy_UI():
    st.set_page_config(page_title="Đăng ký tài khoản", page_icon="📝", layout="centered")
    st.markdown("<h2 style='text-align:center;'>📝 Đăng ký tài khoản mới</h2>", unsafe_allow_html=True)
    st.write("")

    with st.form("register_form"):
        username = st.text_input("👤 Tên đăng nhập:")
        password = st.text_input("🔑 Mật khẩu:", type="password")
        confirm_password = st.text_input("🔁 Nhập lại mật khẩu:", type="password")

        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("✅ Đăng ký")
        with col2:
            cancel = st.form_submit_button("⬅️ Trở về đăng nhập")

        # Nếu nhấn "Trở về"
        if cancel:
            st.session_state["page"] = "DangNhap"
            st.rerun()

        # Nếu nhấn "Đăng ký"
        if submitted:
            if not username or not password or not confirm_password:
                st.warning("⚠️ Vui lòng nhập đầy đủ thông tin!")
                return

            # 🔍 Đọc cả 2 file user & admin
            users = read_accounts("./TaiKhoan/users.txt")
            admins = read_accounts("./TaiKhoan/admin.txt")

            # 🔍 Kiểm tra trùng username ở cả 2 file
            if username in users or username in admins:
                st.error("❌ Tên đăng nhập đã tồn tại (trùng với người dùng hoặc admin)!")
                return

            # 🔑 Kiểm tra xác nhận mật khẩu
            if password != confirm_password:
                st.error("❌ Mật khẩu xác nhận không khớp!")
                return

            # ✅ Lưu thông tin user mới
            save_user(username, password)
            st.success("✅ Đăng ký thành công! Đang chuyển về trang đăng nhập...")

            # Chuyển về trang đăng nhập
            st.session_state["page"] = "DangNhap"
            time.sleep(1)
            st.rerun()
