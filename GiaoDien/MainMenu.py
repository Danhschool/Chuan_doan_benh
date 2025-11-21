import streamlit as st

def Main_UI():
    st.set_page_config(page_title="Main Menu", page_icon="🧠", layout="centered")

    # Chào người dùng
    st.markdown(f"<h2 style='text-align:center;'>👋 Xin chào, {st.session_state['username']}</h2>", unsafe_allow_html=True)
    st.markdown("---")

    st.subheader("🔧 Chọn chức năng:")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📘 Tập luật"):
            st.session_state["page"] = "TapLuat"
            st.rerun()

        if st.button("⚙️ Suy diễn tiến"):
            st.session_state["page"] = "SuyDienTien"
            st.rerun()

    with col2:
        if st.button("🔄 Suy diễn lùi"):
            st.session_state["page"] = "SuyDienLui"
            st.rerun()

        if st.button("📊 Vẽ đồ thị"):
            st.session_state["page"] = "VeDoThi"
            st.rerun()

    st.markdown("---")
    if st.button("🚪 Đăng xuất"):
        st.session_state.clear()
        st.session_state["page"] = "DangNhap"
        st.rerun()
