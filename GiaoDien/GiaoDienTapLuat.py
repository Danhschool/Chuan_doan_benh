import streamlit as st
import pandas as pd
from XuLyLogic import TapLuat

def TapLuat_UI():
    st.title("📘 Quản lý Tập Luật")
    st.markdown("---")

    # 🧩 1. Đọc dữ liệu
    rules = TapLuat.DocLuat()
    if not rules:
        st.warning("⚠️ Hiện chưa có luật nào trong file dữ liệu.")
        if st.button("🏠 Trở về giao diện chính", use_container_width=True):
            st.session_state["page"] = "MainMenu"
            st.rerun()
        return

    # 🧾 2. Hiển thị bảng luật
    df = pd.DataFrame(rules)
    df_display = df[["line", "inputs", "output", "CongThuc"]]
    df_display.columns = ["STT", "Vế trái (inputs)", "Vế phải (output)", "Công thức"]
    st.dataframe(df_display, use_container_width=True, hide_index=True)

    st.markdown("---")

    # 👤 3. Phân quyền
    username = st.session_state.get("username", "")
    is_admin = (username.lower() == "admin")

    if not is_admin:
        st.info("🔒 Bạn chỉ có quyền xem tập luật. Chỉ admin mới có thể thêm / sửa / xóa.")
        if st.button("🏠 Trở về giao diện chính", use_container_width=True):
            st.session_state["page"] = "MainMenu"
            st.rerun()
        return

    # ⚙️ 4. Chức năng dành cho admin
    st.subheader("🧠 Thao tác quản lý (Admin only)")

    tab1, tab2 = st.tabs(["➕ Thêm luật", "🗑️ Xóa luật"])

    # =====================================
    # ➕ TAB 1: Thêm luật (có xác nhận)
    # =====================================
    with tab1:
        col1, col2 = st.columns([2, 1])
        with col1:
            luat_moi = st.text_input("Nhập luật mới (vd: A ^ B -> C):")
        with col2:
            cong_thuc = st.text_input("Công thức (tuỳ chọn):")

        if "confirm_add" not in st.session_state:
            st.session_state.confirm_add = False

        if st.button("✅ Thêm luật", use_container_width=True):
            if not luat_moi.strip():
                st.warning("⚠️ Bạn chưa nhập luật.")
            else:
                st.session_state.confirm_add = True
                st.session_state.pending_rule = (luat_moi, cong_thuc)

        if st.session_state.confirm_add:
            luat_txt, congthuc_txt = st.session_state.pending_rule
            st.warning(f"❓ Bạn có chắc chắn muốn thêm luật sau không?\n\n👉 **{luat_txt} : {congthuc_txt}**")

            colA, colB = st.columns(2)
            with colA:
                if st.button("✔️ Có, thêm vào file"):
                    if TapLuat.ThemLuat(luat_txt, congthuc_txt):
                        st.success("🎉 Đã thêm luật thành công!")
                        st.session_state.confirm_add = False
                        st.session_state.pop("pending_rule", None)
                        st.rerun()
                    else:
                        st.error("❌ Không thể thêm luật. Kiểm tra định dạng hoặc trùng lặp.")
                        st.session_state.confirm_add = False
            with colB:
                if st.button("❌ Không, hủy thao tác"):
                    st.info("🛑 Đã hủy thêm luật.")
                    st.session_state.confirm_add = False
                    st.session_state.pop("pending_rule", None)

    # =====================================
    # 🗑️ TAB 2: Xóa luật (có xác nhận)
    # =====================================
    with tab2:
        st.write("Chọn dòng luật cần xóa:")

        # Hiển thị đúng dạng a ^ b -> c
        luat_list = [f"{' ^ '.join(r['inputs'])} -> {r['output']}" for r in rules]
        luat_chon = st.selectbox("📜 Chọn luật để xóa:", ["-- Chọn --"] + luat_list)

        if "confirm_delete" not in st.session_state:
            st.session_state.confirm_delete = False

        if luat_chon != "-- Chọn --" and st.button("🗑️ Xóa luật này", type="primary", use_container_width=True):
            st.session_state.confirm_delete = True
            st.session_state.rule_to_delete = luat_chon

        if st.session_state.confirm_delete:
            luat_del = st.session_state.rule_to_delete
            st.warning(f"❓ Bạn có chắc chắn muốn **xóa luật** sau không?\n\n🗑️ `{luat_del}`")

            colA, colB = st.columns(2)
            with colA:
                if st.button("✔️ Có, xóa luôn"):
                    if TapLuat.XoaLuat(luat_del):
                        st.success(f"✅ Đã xóa luật: {luat_del}")
                        st.session_state.confirm_delete = False
                        st.session_state.pop("rule_to_delete", None)
                        st.rerun()
                    else:
                        st.error("❌ Không tìm thấy luật cần xóa. Kiểm tra định dạng trong file.")
                        st.session_state.confirm_delete = False
            with colB:
                if st.button("❌ Không, hủy xóa"):
                    st.info("🛑 Đã hủy thao tác xóa.")
                    st.session_state.confirm_delete = False
                    st.session_state.pop("rule_to_delete", None)

    # =====================================
    # 🔙 Nút quay lại giao diện chính (luôn hiển thị cuối)
    # =====================================
    st.markdown("---")
    if st.button("🏠 Trở về giao diện chính", use_container_width=True):
        st.session_state["page"] = "MainMenu"
        st.rerun()
