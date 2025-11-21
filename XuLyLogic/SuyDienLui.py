from queue import Queue
import networkx as nx
import math
from queue import PriorityQueue
def LOC(TG, DanhSachLuat, R):
    """
    Lọc ra tập luật có toàn bộ input nằm trong tập giả thiết TG
    và vẫn còn trong tập luật R.
    """
    Temp = []
    for i in range(1, len(DanhSachLuat) + 1):
        rule = DanhSachLuat[i - 1]
        if set(rule['inputs']).issubset(TG) and i in R:
            Temp.append(i)
    return Temp


from queue import PriorityQueue

def ChonLuatMinMax(GiaThiet, KetLuan, DanhSachLuat, MinMax):
    """
    Thuật toán chọn luật theo Min/Max với Max-Priority Queue.
    """

    # Khởi tạo Max-Priority Queue (giá trị âm để giả lập max-queue)
    KL = PriorityQueue()
    KL.put((0, KetLuan, -1))        # (priority, Node, parent_rule)

    VET = []                        # Danh sách các luật đã chọn
    BangQuyTrinh = []               # Ghi lại toàn bộ quá trình suy diễn
    Parent = {}                     # Lưu quan hệ cha của từng node trong queue
    Check = {}                      # Luật đã được dùng rồi sẽ không xét lại

    # Ghi lại bước đầu tiên
    BangQuyTrinh.append({
        'Xet': '',
        'r': '',
        'Queue': ', '.join([str(v) for p, v, l in KL.queue]),
        'THOA': '',
        'TrangThai': '',
        'VET': ''
    })

    # ================== Vòng lặp chính =======================
    while not KL.empty():

        THOA = []
        GiaTri, TenXet, luat_cha = KL.get()

        # Tìm tất cả luật kết luận ra TenXet
        for luat in DanhSachLuat:
            if luat['output'] == TenXet:
                THOA.append(luat['line'])

        # Bỏ các luật đã xét rồi
        THOA = [i for i in THOA if not Check.get(i, False)]

        # Ghi bước xét node
        BangQuyTrinh.append({
            'Xet': TenXet,
            'r': '',
            'Queue': ', '.join([str(v) for p, v, l in KL.queue]),
            'THOA': ','.join(map(str, THOA)),
            'TrangThai': '' if THOA else 'QuayLui',
            'VET': ','.join(map(str, VET)) or ''
        })

        # ==================== Không có luật thỏa → Quay lùi ====================
        if not THOA:

            # đánh dấu luật cha của node này là đã xét để không duyệt lại
            if luat_cha != -1:
                Check[luat_cha] = True

            # Loại bỏ các node con yếu hơn
            temp = []
            while not KL.empty():
                temp.append(KL.get())
            for p, v, l in temp:
                if abs(p) >= abs(GiaTri):
                    KL.put((p, v, l))

            # Quay lùi VET đến đúng luật cha
            while VET:
                x = VET.pop()
                if x == luat_cha:
                    break

            # Đẩy lại node cha nếu tồn tại
            key_parent = (GiaTri, TenXet, luat_cha)
            try:
                print(Parent[key_parent])
            except KeyError:
                print(f"Key {key_parent} không tồn tại")
                return False, VET, BangQuyTrinh
            if key_parent in Parent:
                KL.put(Parent[key_parent])
            else:
                break

            BangQuyTrinh.append({
                'Xet': '',
                'r': '',
                'Queue': ', '.join([str(v) for p, v, l in KL.queue]),
                'THOA': '',
                'TrangThai': '',
                'VET': ','.join(map(str, VET))
            })
            continue

        # ==================== Có luật thỏa → Chọn Min/Max ====================
        r_chon = min(THOA) if MinMax == "Min" else max(THOA)
        VET.append(r_chon)

        # Expand các input của luật vào queue
        for i in DanhSachLuat[r_chon - 1]['inputs']:
            if i not in GiaThiet:
                new_priority = -(abs(GiaTri) + 1)
                print(i, new_priority)
                KL.put((new_priority, i, r_chon))
                Parent[(new_priority, i, r_chon)] = (GiaTri, TenXet, luat_cha)

        # Ghi bảng quy trình
        BangQuyTrinh.append({
            'Xet': '',
            'r': r_chon,
            'Queue': ', '.join([str(v) for p, v, l in KL.queue]),
            'THOA': '',
            'TrangThai': '',
            'VET': ','.join(map(str, VET))
        })

    # ==================== Kết thúc ====================
    return True, VET, BangQuyTrinh




def KC(Luat, G, KL):
    """
    Tính khoảng cách ngắn nhất giữa hai nút trong đồ thị G.
    Nếu không tồn tại đường đi, trả về vô cực (math.inf).
    """
    try:
        return nx.shortest_path_length(G, source=Luat, target=KL)
    except nx.NetworkXNoPath:
        return math.inf
    except nx.NodeNotFound:
        return math.inf


def d(Luat, G, GT):
    """
    Tính khoảng cách nhỏ nhất giữa Luat và các giả thiết GT trong đồ thị G.
    """
    kc_min = math.inf
    for i in GT:
        kc = KC(i, G, Luat)
        if kc < kc_min:
            kc_min = kc
    return kc_min

def ChonLuatFPG(gia_thiet, ket_luan, min_max, G, danh_sach_luat):
    """
    Chọn luật phù hợp nhất theo thuật toán FPG (Forward Propagation Graph)

    Tham số:
        gia_thiet:    Tập giả thiết ban đầu (list hoặc set)
        ket_luan:     Kết luận cần suy diễn (string)
        min_max:      'Min' hoặc 'Max' để quyết định tiêu chí chọn luật
        G:            Đồ thị quan hệ giữa các luật (networkx.Graph)
        danh_sach_luat: Danh sách các luật, mỗi luật có dạng:
                        {'line': int, 'inputs': [str], 'output': str}

    Trả về:
        ket_qua: True nếu đạt được kết luận cuối cùng, False nếu không
        BangQuyTrinh: Danh sách chi tiết các bước thực hiện (list[dict])
    """

    GT = []
    KL = ket_luan
    R = list(range(1, len(danh_sach_luat) + 1))
    VET = []
    BangQuyTrinh = []
    queue = Queue()

    queue.put(KL)

    BangQuyTrinh.append({
        'Xet': '',
        'Queue': ','.join(list(queue.queue)),
        'r': '',
        'THOA': '',
        'GiaThiet': ','.join(GT),
        'KC': '',
        'R': ','.join(map(str, R)),
        'VET': ','.join(map(str, VET)) or '∅'
    })

    while not queue.empty():
        xet = queue.get()
        THOA = []

        for rule in danh_sach_luat:
            if rule['output'] == xet:
                THOA.append(rule['line'])

        if len(THOA) == 0:
            if queue.empty():
                break
            else:
                continue

        r_chon = None
        khoang_cach = []
        best_value = math.inf

        for i in THOA:
            i = int(i)
            chuoi = f"h(r{i}) = Max("
            kc_value = -math.inf

            for j in danh_sach_luat[i - 1]['inputs']:
                temp = d(j, G, gia_thiet)
                chuoi += f"d({j}, GT)={temp}, "
                kc_value = max(kc_value, temp)

            chuoi = chuoi.rstrip(', ') + f") = {kc_value}"
            khoang_cach.append(chuoi)

            if min_max == "Min":
                if kc_value < best_value:
                    r_chon = i
                    best_value = kc_value
            else:
                if kc_value <= best_value:
                    r_chon = i
                    best_value = kc_value

        if best_value == math.inf:
            break

        BangQuyTrinh.append({
            'Xet': xet,
            'Queue': ','.join(list(queue.queue)) or '',
            'r': f"r{r_chon}" if r_chon else '',
            'THOA': ','.join(map(str, THOA)) or '',
            'GiaThiet': ','.join(GT),
            'KC': '\n'.join(khoang_cach),
            'R': ','.join(map(str, R)),
            'VET': ','.join(map(str, VET)) or '∅'
        })

        if r_chon and r_chon in R:
            R.remove(r_chon)
        if r_chon:
            VET.append(r_chon)

        if r_chon:
            for j in danh_sach_luat[r_chon - 1]['inputs']:
                if j not in GT:
                    if j not in gia_thiet:
                        queue.put(j)
                    GT.append(j)
        BangQuyTrinh.append({
            'Xet': '',
            'Queue': ','.join(list(queue.queue)) or '',
            'r': '',
            'THOA': '',
            'GiaThiet': ','.join(GT),
            'KC': '',
            'R': ','.join(map(str, R)),
            'VET': ','.join(map(str, VET)) or '∅'
        })

    ket_qua = set(gia_thiet).issubset(set(GT))
    return ket_qua, VET, BangQuyTrinh
