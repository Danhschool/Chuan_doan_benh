import os
import streamlit as st

# 🔹 Hàm đọc danh sách tài khoản từ file (định dạng: username password)
def read_accounts(filename):
    accounts = {}
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 2:
                    username, password = parts
                    accounts[username] = password
    return accounts


def DangNhap_UI():
    # ⚙️ Cấu hình giao diện
    st.set_page_config(page_title="Đăng nhập hệ thống", page_icon="🔐", layout="centered")
    st.markdown("<h2 style='text-align:center;'>🔐 Đăng nhập hệ thống</h2>", unsafe_allow_html=True)
    st.write("")

    # 🧾 Form đăng nhập
    with st.form("login_form"):
        username = st.text_input("👤 Tên đăng nhập:")
        password = st.text_input("🔑 Mật khẩu:", type="password")
        submitted = st.form_submit_button("Đăng nhập")

        if submitted:
            # 🔍 Đọc dữ liệu từ file admin và user
            admin_path = "./TaiKhoan/admin.txt"
            user_path = "./TaiKhoan/users.txt"

            admin_accounts = read_accounts(admin_path)
            user_accounts = read_accounts(user_path)

            role = None

            # ✅ Kiểm tra tài khoản
            if username in admin_accounts and password == admin_accounts[username]:
                role = "admin"
            elif username in user_accounts and password == user_accounts[username]:
                role = "user"

            # 🟢 Xử lý đăng nhập thành công
            if role:
                st.success(f"✅ Đăng nhập thành công ({role.upper()})!")

                # Lưu trạng thái đăng nhập
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["role"] = role
                st.session_state["page"] = "MainMenu"  # 👈 sửa lại đúng tên trang

                st.rerun()
            else:
                st.error("❌ Sai tên đăng nhập hoặc mật khẩu!")

    # 🔄 Nút chuyển sang trang đăng ký
    if st.button("📝 Chưa có tài khoản? Đăng ký ngay"):
        st.session_state["page"] = "DangKy"
        st.rerun()
