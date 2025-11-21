import streamlit as st
import pandas as pd
import networkx as nx
from XuLyLogic import SuyDienLui, FPG_RPG, TapLuat
from queue import Queue

def SuyDienLui_UI():
    st.title("🔙 Suy Diễn Lùi (Backward Chaining)")
    st.markdown("---")

    # 1️⃣ Đọc tập luật
    DanhSachLuat = TapLuat.DocLuat()
    if not DanhSachLuat:
        st.warning("⚠️ Không có luật nào trong cơ sở tri thức.")
        if st.button("🏠 Trở về giao diện chính"):
            st.session_state["page"] = "MainMenu"
            st.rerun()
        return

    # 2️⃣ Lấy danh sách sự kiện từ các luật
    TapGiaThiet = set()
    TapKetLuan = set()
    for rule in DanhSachLuat:
        for inp in rule['inputs']:
            TapGiaThiet.add(inp)
        if isinstance(rule['output'], list):
            for out in rule['output']:
                TapKetLuan.add(out)
        else:
            TapKetLuan.add(rule['output'])

    # 3️⃣ Giao diện chọn giả thiết và kết luận
    st.subheader("🧮 Chọn giả thiết và kết luận")
    GiaThiet = st.multiselect(
        "🧩 Chọn tập giả thiết:",
        options=sorted(TapGiaThiet),
        help="Chọn một hoặc nhiều sự kiện có trong cơ sở tri thức."
    )

    KetLuan = st.selectbox(
        "🎯 Chọn kết luận cần chứng minh:",
        options=sorted(TapKetLuan),
        help="Chọn một sự kiện kết luận có trong cơ sở tri thức."
    )

    st.markdown("---")
    st.subheader("⚙️ Chọn hướng suy diễn")
    huong = st.radio("Chọn phương pháp suy diễn:", ["Theo Min/Max", "Theo FPG"])
    min_max = st.radio("Chọn hướng:", ["Min", "Max"])

    st.markdown("---")
    if st.button("🚀 Thực hiện suy diễn"):
        if not GiaThiet or not KetLuan:
            st.warning("⚠️ Vui lòng chọn đầy đủ Giả thiết và Kết luận!")
            return

        # Tạo đồ thị FPG nếu cần
        G = nx.DiGraph()
        for rule in DanhSachLuat:
            for inp in rule['inputs']:
                G.add_edge(inp, rule['output'])

        try:
            if huong == "Theo Min/Max":
                ketqua, vet, bangqt = SuyDienLui.ChonLuatMinMax(GiaThiet, KetLuan, DanhSachLuat, min_max)
            else:  # Theo FPG
                G_FPG = FPG_RPG.FPG(DanhSachLuat)
                ketqua, vet, bangqt = SuyDienLui.ChonLuatFPG(GiaThiet, KetLuan, min_max, G_FPG, DanhSachLuat)

            # Hiển thị bảng quy trình
            st.markdown("### 📋 Bảng Quy Trình")
            if bangqt:
                st.dataframe(pd.DataFrame(bangqt), use_container_width=True)

            st.markdown("---")
            # Hiển thị kết quả suy diễn
            if ketqua:
                st.success(f"✅ Kết luận **{KetLuan}** được SUY DIỄN THÀNH CÔNG từ tập giả thiết {GiaThiet}.")
            else:
                st.error(f"❌ Không thể suy diễn ra **{KetLuan}** từ tập giả thiết {GiaThiet}.")

            # ===== HIỂN THỊ VẾT SUY DIỄN DẠNG ĐẦY ĐỦ (CHO SUY DIỄN LÙI – ĐẢO NGƯỢC) =====
            if ketqua and vet:
                st.markdown("### 🧠 Vết Suy Diễn (Vector đánh giá thứ tự)")

                # Lấy danh sách ID luật
                if isinstance(vet, dict):
                    ds_luat = list(vet.keys())
                else:
                    ds_luat = vet

                # ĐẢO NGƯỢC THỨ TỰ cho suy diễn lùi
                ds_luat = list(reversed(ds_luat))

                vet_rows = []
                for idx, r in enumerate(ds_luat, 1):
                    rule = DanhSachLuat[r - 1]

                    # Lấy vế trái + phải
                    inputs = " ^ ".join(rule["inputs"])
                    output = rule["output"]

                    # Tạo dạng "r11: a ^ b ^ c → mc"
                    rule_full = f"r{r}: {inputs} → {output}"

                    # Công thức
                    congthuc = rule.get("CongThuc", "")

                    vet_rows.append({
                        "Thứ tự": idx,
                        "Luật được áp dụng": rule_full,
                        "Công thức": congthuc
                    })

                df_vet = pd.DataFrame(vet_rows)
                st.dataframe(df_vet, use_container_width=True)

                # Chuỗi suy diễn dạng r16 → r14 → r10 → r11
                st.markdown(f"➡️ Chuỗi suy diễn: {' → '.join([f'r{r}' for r in ds_luat])}")

        except Exception as e:
            st.error(f"🚨 Đã xảy ra lỗi khi suy diễn: {e}")

    st.markdown("---")
    if st.button("🏠 Trở về giao diện chính"):
        st.session_state["page"] = "MainMenu"
        st.rerun()
