import os
import re

DATA_PATH = "./DuLieuLuat/benh4tang.txt"

# --- Kiểm tra file tồn tại khi import ---
if not os.path.exists(DATA_PATH):
    print(f"❌ Không tìm thấy file dữ liệu: {DATA_PATH}")
else:
    print(f"✅ Đã phát hiện file dữ liệu: {DATA_PATH}")

def DocLuat():
    """Đọc danh sách luật từ file, bỏ qua dòng trống."""
    rules = []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        # chỉ lấy dòng hợp lệ (có -> và :)
        lines = [line.strip() for line in f if line.strip() and "->" in line and ":" in line]

    for idx, line in enumerate(lines, 1):
        left_part, right_part = line.split("->", 1)
        right_side, expression = right_part.split(":", 1)
        left_vars = [x.strip() for x in left_part.split("^")]
        right_var = right_side.strip()
        CongThuc = expression.strip()
        rules.append({
            "inputs": left_vars,
            "output": right_var,
            "CongThuc": CongThuc,
            "line": idx
        })
    return rules

def ChuanHoaLuat(Luat: str) -> str:
    Luat = Luat.strip()
    Luat = re.sub(r"\s+", "", Luat)
    Luat = Luat.replace("->", " -> ").replace("^", " ^ ")
    Luat = re.sub(r"\s+", " ", Luat).strip()
    return Luat

def KiemTraLuat(Luat: str) -> bool:
    if "->" not in Luat:
        print("Luật không có dấu '->'")
        return False

    ve_trai, ve_phai = Luat.split("->", 1)
    ve_trai = ve_trai.strip()
    ve_phai = ve_phai.strip()

    if not ve_trai or not ve_phai:
        print("Luật thiếu vế trái hoặc vế phải.")
        return False

    if not re.fullmatch(r"[A-Za-z0-9\s\^]+", ve_trai):
        print("Vế trái chứa ký tự không hợp lệ.")
        return False

    if not re.fullmatch(r"[A-Za-z0-9]+", ve_phai):
        print("Vế phải phải là một ký hiệu duy nhất (không có ^ hoặc dấu khác).")
        return False

    return True

def ThemLuat(Luat: str, CongThuc="") -> bool:
    if not os.path.exists(DATA_PATH):
        print("Không tìm thấy file:", DATA_PATH)
        return False

    if not Luat or not isinstance(Luat, str):
        print("Luật không hợp lệ hoặc rỗng.")
        return False

    Luat = ChuanHoaLuat(Luat)

    if not KiemTraLuat(Luat):
        return False

    CongThuc = CongThuc.strip() if CongThuc.strip() else ""
    rule_line = f"{Luat} : {CongThuc}"

    # --- Đọc danh sách luật hiện có, bỏ dòng trống ---
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    existing_titles = [line.split(":")[0].strip() for line in lines]

    if Luat in existing_titles:
        print(f"Luật '{Luat}' đã tồn tại (trùng tiêu đề-kết luận).")
        return False

    # --- Ghi thêm vào file ---
    with open(DATA_PATH, "a", encoding="utf-8") as f:
        if os.path.getsize(DATA_PATH) > 0:
            f.write("\n")  # thêm dòng mới nếu file chưa trống
        f.write(rule_line)

    print(f"Đã thêm luật: {rule_line}")
    return True

def XoaLuat(Luat: str) -> bool:
    """
    Xóa một luật khỏi file luật (xóa hoàn toàn dòng chứa luật đó, không để trống).
    """
    if not Luat or not isinstance(Luat, str):
        print("Chuỗi luật không hợp lệ hoặc rỗng.")
        return False

    # --- Chuẩn hóa luật nhập vào ---
    Luat = ChuanHoaLuat(Luat)

    # --- Đọc toàn bộ luật, bỏ qua dòng trống ---
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    found = False
    new_lines = []

    for line in lines:
        title = line.split(":")[0].strip()
        if title == Luat:
            found = True
            continue  # bỏ qua dòng cần xóa
        new_lines.append(line)

    if not found:
        print(f"Không tìm thấy luật '{Luat}' để xóa.")
        return False

    # --- Ghi lại file, đảm bảo không có dòng trống ---
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        # chỉ ghi nếu còn luật, mỗi luật nằm trên 1 dòng
        if new_lines:
            f.write("\n".join(new_lines))

    print(f"Đã xóa luật: {Luat}")
    return True

