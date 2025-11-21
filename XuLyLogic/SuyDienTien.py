from collections import deque
import networkx as nx
from queue import PriorityQueue
import math

# Hàm LOC
def LOC(TG, DanhSachLuat, R):
    Temp = []
    for i in range(1, len(DanhSachLuat) + 1):
        rule = DanhSachLuat[i - 1]
        if set(rule['inputs']).issubset(TG) and i in R:
            Temp.append(i)
    return Temp

# Suy diễn tiến không chọn luật theo stack or queue
def KhongChonLuat(GiaThiet, KetLuan, DanhSachLuat, LuaChon):
    if LuaChon == "Stack":
        Thoa = []
    else:
        Thoa = deque()

    TG = list(GiaThiet)
    KL = {KetLuan}
    VET = []
    R = list(range(1, len(DanhSachLuat) + 1))
    BangQuyTrinh = []
    BangQuyTrinh.append({
        'r': '',
        'THOA': ','.join(map(str, Thoa)) or '',
        'TG': ','.join(TG) or '',
        'R': ','.join(map(str, R)) or '',
        'VET': ','.join(map(str, VET)) or '∅'
    })

    for idx in LOC(TG, DanhSachLuat, R):
        if idx not in Thoa:
            Thoa.append(idx)

    while Thoa and not KL.issubset(TG):
        BangQuyTrinh.append({
            'r': '',
            'THOA': ','.join(map(str, Thoa)) or '',
            'TG': '',
            'R': '',
            'VET': ''
        })
        if LuaChon == "Stack":
            Temp = Thoa.pop()
        else:
            Temp = Thoa.popleft()

        VET.append(Temp)
        R.remove(Temp)
        output = DanhSachLuat[Temp - 1]['output']
        if output not in TG:
            TG.append(output)

        for idx in LOC(TG, DanhSachLuat, R):
            if idx not in Thoa:
                Thoa.append(idx)

        BangQuyTrinh.append({
            'r': Temp,
            'THOA': '',
            'TG': ','.join(TG) or '∅',
            'R': ','.join(map(str, R)) or '∅',
            'VET': ','.join(map(str, VET)) or '∅'
        })

    ket_qua = KL.issubset(TG)
    return ket_qua, VET, BangQuyTrinh

# Suy diễn tiến chọn luật theo max min
def ChonLuatMinMax(GiaThiet, KetLuan, DanhSachLuat, MinMax):
    TG = list(GiaThiet)
    KL = {KetLuan}
    R = list(range(1, len(DanhSachLuat) + 1))
    VET = []
    BangQuyTrinh = []
    Temp = PriorityQueue()

    # Bước 0: Ghi lại trạng thái ban đầu
    BangQuyTrinh.append({
        'r': '',
        'THOA': '',
        'TG': ','.join(TG) or '',
        'R': ','.join(map(str, R)) or '∅',
        'VET': ','.join(map(str, VET)) or '∅'
    })

    # Xác định các luật thỏa ngay từ đầu
    for idx in LOC(TG, DanhSachLuat, R):
        if idx not in [abs(x) for x in Temp.queue]:
            Temp.put(-idx if MinMax == "Max" else idx)

    BangQuyTrinh.append({
        'r': '',
        'THOA': ','.join(map(str, sorted([abs(x) for x in Temp.queue], reverse=(MinMax == "Max")))) or '',
        'TG': ','.join(TG) or '',
        'R': ','.join(map(str, R)) or '∅',
        'VET': ','.join(map(str, VET)) or '∅'
    })

    # Bắt đầu suy diễn
    while not Temp.empty() and not KL.issubset(TG):
        r = abs(Temp.get())
        if r not in R:
            continue  # bỏ qua nếu luật đã dùng rồi

        R.remove(r)
        VET.append(r)
        output = DanhSachLuat[r - 1]['output']

        if output not in TG:
            TG.append(output)

        # Ghi lại trạng thái sau khi áp dụng luật r
        BangQuyTrinh.append({
            'r': str(r),
            'THOA': '',
            'TG': ','.join(TG) or '',
            'R': ','.join(map(str, R)) or '∅',
            'VET': ','.join(map(str, VET)) or '∅'
        })

        # Cập nhật luật thỏa sau khi TG thay đổi
        for idx in LOC(TG, DanhSachLuat, R):
            if idx not in [abs(x) for x in Temp.queue]:
                Temp.put(-idx if MinMax == "Max" else idx)

        BangQuyTrinh.append({
            'r': '',
            'THOA': ','.join(map(str, sorted([abs(x) for x in Temp.queue], reverse=(MinMax == "Max")))) or '',
            'TG': ','.join(TG) or '',
            'R': ','.join(map(str, R)) or '∅',
            'VET': ','.join(map(str, VET)) or '∅'
        })
    ket_qua = KL.issubset(TG)
    return ket_qua, VET, BangQuyTrinh

# Khoảng cách trong đồ thị
def KC(Luat, G, KL):
    try:
        return nx.shortest_path_length(G, source=Luat, target=KL)
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return math.inf

def ChonLuatFPG(GiaThiet, KetLuan, MinMax, G, DanhSachLuat):
    """
    Thuật toán chọn luật FPG (Forward Production Graph)
    ----------------------------------------------
    GiaThiet   : tập giả thiết ban đầu (list)
    KetLuan    : kết luận cần đạt (string)
    MinMax     : 'Min' hoặc 'Max' – cách chọn luật
    G          : đồ thị biểu diễn quan hệ luật (nx.DiGraph)
    DanhSachLuat : danh sách các luật (list of dict)
    """

    TG = list(GiaThiet)       # Tập giả thiết hiện tại
    KL = KetLuan              # Kết luận (string)
    VET = []                  # Tập vết
    R = list(range(1, len(DanhSachLuat) + 1))  # Tập chỉ số luật
    BangQuyTrinh = []         # Bảng quy trình lưu các bước

    # Xác định tập luật thỏa điều kiện hiện tại
    THOA = LOC(TG, DanhSachLuat, R)

    # Ghi bước khởi tạo
    BangQuyTrinh.append({
        'r': '',
        'THOA': '',
        'TG': ','.join(TG),
        'KC': '',
        'R': ','.join(map(str, R)),
        'VET': ','.join(map(str, VET)) or '∅'
    })

    # Lặp cho đến khi KL xuất hiện trong TG
    while KL not in TG:
        # Ghi lại tập THỎA trước khi chọn luật
        BangQuyTrinh.append({
            'r': '',
            'THOA': ','.join(map(str, THOA)),
            'TG': '',
            'KC': '',
            'R': ','.join(map(str, R)),
            'VET': ','.join(map(str, VET)) or '∅'
        })

        # --- Tính khoảng cách & chọn luật phù hợp ---
        KhoangCach = []
        best_val = math.inf
        Chon = None

        for i in THOA:
            output = DanhSachLuat[i - 1]["output"]
            kc_value = KC(output, G, KL)  # tính KC(output, KL)

            # In công thức ĥ(rᵢ)
            temp = f"ĥ(r{i}) = KC({output}, {KL}) = {kc_value}"
            KhoangCach.append(temp)

            # Lựa chọn luật theo Min hoặc Max
            if MinMax == "Max":
                if kc_value <= best_val:
                    best_val = kc_value
                    Chon = i
            else:  # Min
                if kc_value < best_val:
                    best_val = kc_value
                    Chon = i

        # --- Cập nhật sau khi chọn luật ---
        if Chon is None:
            print("⚠️ Không còn luật thỏa mãn điều kiện.")
            break

        R.remove(Chon)
        TG.append(DanhSachLuat[Chon - 1]['output'])
        VET.append(Chon)
        THOA = LOC(TG, DanhSachLuat, R)

        # Ghi lại bước sau khi chọn luật
        BangQuyTrinh.append({
            'r': f"r{Chon}",
            'THOA': '',
            'TG': ','.join(TG),
            'KC': '\n'.join(KhoangCach),  # mỗi công thức 1 dòng
            'R': ','.join(map(str, R)),
            'VET': ','.join(map(str, VET)) or '∅'
        })

    # Kết quả cuối cùng
    ket_qua = KL in TG
    return ket_qua, VET, BangQuyTrinh

def ChonLuatRPG(GiaThiet, KetLuan, MinMax, G, DanhSachLuat):
    """
    Chọn luật theo phương pháp RPG (Rule Path Graph)

    Tham số:
        GiaThiet   : Tập giả thiết ban đầu (list)
        KetLuan    : Kết luận cần suy ra (string)
        MinMax     : 'Min' hoặc 'Max' — cách chọn luật dựa vào khoảng cách
        G           : Đồ thị luật (networkx.DiGraph)
        DanhSachLuat: Danh sách luật [{inputs:[], output:'', line:int}, ...]

    Trả về:
        (ket_qua, BangQuyTrinh)
        - ket_qua: True nếu suy ra được KetLuan
        - BangQuyTrinh: danh sách dict lưu các bước thực hiện
    """

    TG = list(GiaThiet)  # Tập giả thiết hiện tại
    KL = [i["line"] for i in DanhSachLuat if i["output"] == KetLuan]  # Các luật có đầu ra = Kết luận
    VET = []  # Tập vết (các luật đã dùng)
    R = list(range(1, len(DanhSachLuat) + 1))  # Tập chỉ số luật
    BangQuyTrinh = []  # Lưu lại quá trình thực hiện

    # --- Bước khởi tạo ---
    THOA = LOC(TG, DanhSachLuat, R)  # Các luật thoả điều kiện hiện tại
    BangQuyTrinh.append({
        'r': '',
        'THOA': '',
        'TG': ','.join(TG),
        'KC': '',
        'R': ','.join(map(str, R)),
        'VET': ','.join(map(str, VET)) or '∅'
    })

    Chon = None

    # --- Lặp cho đến khi tìm được luật dẫn đến KL ---
    while Chon not in KL:
        # Ghi lại tập THỎA trước khi chọn luật
        BangQuyTrinh.append({
            'r': '',
            'THOA': ','.join(map(str, THOA)),
            'TG': '',
            'KC': '',
            'R': ','.join(map(str, R)),
            'VET': ','.join(map(str, VET)) or '∅'
        })

        # Nếu không còn luật thoả mãn, dừng
        if not THOA:
            print("⚠️ Không còn luật thỏa mãn điều kiện.")
            break

        # --- Tính khoảng cách và chọn luật ---
        KhoangCach = []
        best_val = math.inf
        Chon = None

        for i in THOA:
            Chuoi = f"ĥ(r{i}) = min("
            hmin = math.inf
            for j in KL:
                kc_value = KC(f"r{i}", G, f"r{j}")  # KC(ri, rj)
                Chuoi = Chuoi + f" KC(r{i}, r{j}) = {kc_value},"
                if MinMax == "Max":
                    if kc_value <= best_val:
                        best_val = kc_value
                        Chon = i
                else:  # Min
                    if kc_value < best_val:
                        best_val = kc_value
                        hmin = kc_value
                        Chon = i
                if kc_value < hmin:
                    hmin = kc_value
            Chuoi = Chuoi.rstrip(',') + ") = " + str(hmin)
            KhoangCach.append(Chuoi)
        # --- Cập nhật sau khi chọn luật ---
        if Chon is None:
            print("⚠️ Không tìm được luật để chọn.")
            break

        # Loại bỏ luật vừa chọn
        if Chon in R:
            R.remove(Chon)

        # Thêm kết luận của luật vào TG
        TG.append(DanhSachLuat[Chon - 1]['output'])
        VET.append(Chon)

        # Cập nhật tập luật thoả điều kiện
        THOA = LOC(TG, DanhSachLuat, R)

        # Lưu lại bước sau khi chọn
        BangQuyTrinh.append({
            'r': f"r{Chon}",
            'THOA': '',
            'TG': ','.join(TG),
            'KC': '\n'.join(KhoangCach),
            'R': ','.join(map(str, R)),
            'VET': ','.join(map(str, VET)) or '∅'
        })

    # --- Kết quả ---
    ket_qua = Chon in KL
    return ket_qua, VET, BangQuyTrinh