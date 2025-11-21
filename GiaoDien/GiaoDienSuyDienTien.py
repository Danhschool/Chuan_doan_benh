import streamlit as st
import pandas as pd
from XuLyLogic import SuyDienTien, TapLuat, FPG_RPG
import matplotlib.pyplot as plt

def SuyDienTien_UI():
    st.title("🔍 Suy Diễn Tiến (Forward Chaining)")
    st.markdown("---")

    # 1️⃣ Đọc tập luật
    DanhSachLuat = TapLuat.DocLuat()
    if not DanhSachLuat:
        st.warning("⚠️ Không có luật nào trong cơ sở tri thức.")
        if st.button("🏠 Trở về giao diện chính", use_container_width=True):
            st.session_state["page"] = "MainMenu"
            st.rerun()
        return

    # 2️⃣ Lấy danh sách sự kiện từ các luật
    TapGiaThiet = set()
    TapKetLuan = set()
    for i in range(len(DanhSachLuat)):
        for j in DanhSachLuat[i]['inputs']:
            TapGiaThiet.add(j)
        if isinstance(DanhSachLuat[i]['output'], list):
            for k in DanhSachLuat[i]['output']:
                TapKetLuan.add(k)
        else:
            TapKetLuan.add(DanhSachLuat[i]['output'])

    TatCaSuKien = sorted(TapGiaThiet.union(TapKetLuan))

    # 3️⃣ Giao diện chọn giả thiết và kết luận
    st.subheader("🧮 Chọn giả thiết và kết luận từ tập luật")

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

    # 4️⃣ Lựa chọn phương pháp suy diễn
    st.subheader("⚙️ Lựa chọn phương pháp suy diễn")

    huong = st.radio("Bạn có muốn **chọn hướng** suy diễn không?", ("Không chọn hướng", "Có chọn hướng"))
    phuong_phap = None
    do_thi = None
    minmax = None

    if huong == "Không chọn hướng":
        phuong_phap = st.radio("Chọn phương pháp:", ("Stack", "Queue"))

    else:
        loai_huong = st.radio("Chọn loại hướng:", ("Theo Max/Min trực tiếp", "Theo đồ thị (FPG/RPG)"))
        if loai_huong == "Theo Max/Min trực tiếp":
            minmax = st.radio("Chọn hướng:", ("Max", "Min"))
        elif loai_huong == "Theo đồ thị (FPG/RPG)":
            do_thi = st.radio("Chọn loại đồ thị:", ("FPG", "RPG"))
            minmax = st.radio("Chọn hướng:", ("Max", "Min"))

    st.markdown("---")

    # 5️⃣ Thực hiện suy diễn
    if st.button("🚀 Thực hiện suy diễn", use_container_width=True):
        if not GiaThiet or not KetLuan:
            st.warning("⚠️ Vui lòng chọn đầy đủ **Giả thiết** và **Kết luận**.")
            return

        GT = list(GiaThiet)
        KL = KetLuan

        try:
            # ====================== GỌI HÀM SUY DIỄN ======================
            if huong == "Không chọn hướng":
                if phuong_phap == "Stack":
                    ketqua, vet, bangqt = SuyDienTien.KhongChonLuat(GT, KL, DanhSachLuat, "Stack")
                else:
                    ketqua, vet, bangqt = SuyDienTien.KhongChonLuat(GT, KL, DanhSachLuat, "Queue")

            else:
                if minmax and not do_thi:
                    ketqua, vet, bangqt = SuyDienTien.ChonLuatMinMax(GT, KL, DanhSachLuat, minmax)
                elif do_thi and minmax:
                    if do_thi == "FPG":
                        G_FPG = FPG_RPG.FPG(DanhSachLuat)
                        ketqua, vet, bangqt = SuyDienTien.ChonLuatFPG(GT, KL, minmax, G_FPG, DanhSachLuat)
                    elif do_thi == "RPG":
                        G_RPG = FPG_RPG.RPG(DanhSachLuat)
                        ketqua, vet, bangqt = SuyDienTien.ChonLuatRPG(GT, KL, minmax, G_RPG, DanhSachLuat)
                else:
                    st.warning("⚠️ Hãy chọn đầy đủ loại đồ thị và hướng (Max/Min).")
                    return
            # =====================================================================

            # 6️⃣ Hiển thị bảng quy trình
            st.markdown("### 📋 Bảng Quy Trình Suy Diễn")
            if bangqt and isinstance(bangqt, list):
                df = pd.DataFrame(bangqt)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("Không có quy trình nào được tạo ra.")

            # 7️⃣ Hiển thị kết quả suy diễn
            st.markdown("---")
            if ketqua:
                st.success(f"✅ Kết luận **{KL}** được SUY DIỄN THÀNH CÔNG từ tập giả thiết {GT}.")
            else:
                st.error(f"❌ Không thể suy diễn ra **{KL}** từ tập giả thiết {GT}.")

            # ===== HIỂN THỊ VẾT SUY DIỄN DẠNG ĐẦY ĐỦ =====
            if ketqua and vet:
                st.markdown("### 🧠 Vết Suy Diễn (Vector đánh giá thứ tự)")

                # Lấy danh sách ID luật theo đúng thứ tự
                if isinstance(vet, dict):
                    ds_luat = list(vet.keys())
                else:
                    ds_luat = vet

                # Tạo bảng: rK : inputs → output + công thức
                vet_rows = []
                for idx, r in enumerate(ds_luat, 1):
                    rule = DanhSachLuat[r - 1]

                    # Lấy vế trái
                    inputs = " ^ ".join(rule["inputs"])

                    # Lấy vế phải
                    output = rule["output"]

                    # Tạo dạng “r11: a ^ b ^ c → mc”
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

                    # Chuỗi suy diễn dạng r11 → r10 → r14 → r16
                st.markdown(f"➡️ Chuỗi suy diễn: {' → '.join([f'r{r}' for r in ds_luat])}")
        except Exception as e:
            st.error(f"🚨 Đã xảy ra lỗi khi suy diễn: {e}")

    # 9️⃣ Nút quay lại
    st.markdown("---")
    if st.button("🏠 Trở về giao diện chính", use_container_width=True):
        st.session_state["page"] = "MainMenu"
        st.rerun()
