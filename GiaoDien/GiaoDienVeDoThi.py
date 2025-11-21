import streamlit as st
import networkx as nx
from pyvis.network import Network
from XuLyLogic import TapLuat, FPG_RPG
import tempfile
import os

def VeDoThi_UI():
    st.title("📊 Vẽ Đồ Thị Suy Diễn (FPG & RPG)")
    st.markdown("---")

    # 1️⃣ Đọc tập luật
    DanhSachLuat = TapLuat.DocLuat()
    if not DanhSachLuat:
        st.warning("⚠️ Không có luật nào trong cơ sở tri thức để vẽ đồ thị.")
        if st.button("🏠 Trở về giao diện chính", use_container_width=True):
            st.session_state["page"] = "MainMenu"
            st.rerun()
        return

    # 2️⃣ Lựa chọn loại đồ thị
    st.subheader("🧭 Chọn loại đồ thị cần hiển thị:")
    loai_do_thi = st.radio(
        "Chọn loại đồ thị:",
        ("FPG (Fact Precedence Graph)", "RPG (Rule Precedence Graph)"),
        index=None
    )

    # ✅ Cho phép quay lại ngay cả khi chưa chọn loại đồ thị
    if not loai_do_thi:
        st.info("👆 Hãy chọn một loại đồ thị để hiển thị.")
        if st.button("🏠 Trở về giao diện chính", use_container_width=True):
            st.session_state["page"] = "MainMenu"
            st.rerun()
        return

    # 3️⃣ Tạo đồ thị
    if "FPG" in loai_do_thi:
        st.markdown("### 📘 Đồ thị FPG")
        G = FPG_RPG.FPG(DanhSachLuat)
        mau_node = "#89CFF0"
    else:
        st.markdown("### 📙 Đồ thị RPG")
        G = FPG_RPG.RPG(DanhSachLuat)
        mau_node = "#FFD580"

    if len(G.nodes) == 0:
        st.warning("⚠️ Không thể tạo đồ thị vì danh sách luật rỗng hoặc không hợp lệ.")
        if st.button("🏠 Trở về giao diện chính", use_container_width=True):
            st.session_state["page"] = "MainMenu"
            st.rerun()
        return

    # 4️⃣ Dùng PyVis để tạo đồ thị tương tác
    net = Network(height="750px", width="100%", directed=True, notebook=False)
    net.from_nx(G)

    # ⚙️ Cấu hình layout vật lý giúp kéo thả mượt và các node cách xa nhau
    net.repulsion(
        node_distance=250,
        central_gravity=0.25,
        spring_length=200,
        spring_strength=0.03,
        damping=0.85
    )

    # 🧩 Tùy chỉnh giao diện node & cạnh
    for node in net.nodes:
        node["color"] = mau_node
        node["size"] = 10
        node["font"] = {"size": 10, "color": "black", "face": "Arial"}

    for edge in net.edges:
        edge["color"] = "gray"
        edge.pop("label", None)

    # ⚙️ Bật kéo thả node và zoom có giới hạn
    net.set_options("""
    {
      "physics": {
        "enabled": true
      },
      "interaction": {
        "dragNodes": true,
        "dragView": true,
        "zoomView": true,
        "minZoom": 0.4,
        "maxZoom": 1.8
      },
      "edges": {
        "smooth": {
          "enabled": true,
          "type": "dynamic"
        },
        "arrows": {
          "to": { "enabled": true, "scaleFactor": 1.2 }
        }
      }
    }
    """)

    # 5️⃣ Xuất file HTML và hiển thị trong Streamlit
    tmp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".html").name
    net.write_html(tmp_path)

    with open(tmp_path, "r", encoding="utf-8") as f:
        html_code = f.read()
    st.components.v1.html(html_code, height=780, scrolling=True)

    os.remove(tmp_path)

    st.info("🖱️ Bạn có thể **kéo thả các node** và **phóng to/thu nhỏ vừa phải** để quan sát rõ các quan hệ.")

    # 6️⃣ Nút quay lại luôn có mặt
    st.markdown("---")
    if st.button("🏠 Trở về giao diện chính", use_container_width=True):
        st.session_state["page"] = "MainMenu"
        st.rerun()
