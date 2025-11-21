import streamlit as st
from GiaoDien import DangNhap, DangKy, MainMenu, GiaoDienTapLuat, GiaoDienVeDoThi, GiaoDienSuyDienTien, GiaoDienSuyDienLui
from XuLyLogic import TapLuat

# from GiaoDien.GiaoDienTapLuat import GiaoDienTapLuat_UI
# from GiaoDien.GiaoDienSuyDienTien import GiaoDienSuyDienTien_UI
# from GiaoDien.GiaoDienSuyDienLui import GiaoDienSuyDienLui_UI
# from GiaoDien.GiaoDienVeDoThi import GiaoDienVeDoThi_UI

if "page" not in st.session_state:
    st.session_state["page"] = "DangNhap"

if st.session_state["page"] == "DangNhap":
    DangNhap.DangNhap_UI()
elif st.session_state["page"] == "DangKy":
    DangKy.DangKy_UI()
elif st.session_state["page"] == "MainMenu":
    MainMenu.Main_UI()
elif st.session_state["page"] == "TapLuat":
    GiaoDienTapLuat.TapLuat_UI()
elif st.session_state["page"] == "VeDoThi":
    GiaoDienVeDoThi.VeDoThi_UI()
elif st.session_state["page"] == "SuyDienTien":
    GiaoDienSuyDienTien.SuyDienTien_UI()
elif st.session_state["page"] == "SuyDienLui":
    GiaoDienSuyDienLui.SuyDienLui_UI()