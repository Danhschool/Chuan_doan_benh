import matplotlib.pyplot as plt
from XuLyLogic import TapLuat
import networkx as nx
import matplotlib.pyplot as plt

def VeFPG():
    return

def FPG(DanhSachLuat):
    # Tạo đồ thị có hướng
    G = nx.DiGraph()

    # Thêm cạnh (edge)
    for rule in DanhSachLuat:
        for inp in rule['inputs']:
            G.add_edge(inp, rule['output'], label=f"{inp}→{rule['output']}")
    return G

def VeRPG():
    return

def RPG(DanhSachLuat):
    # Tạo đồ thị có hướng
    G = nx.DiGraph()

    # Tạo các đỉnh: r1, r2, ...
    for i in range(1, len(DanhSachLuat) + 1):
        G.add_node(f"r{i}")

    # Tạo các cạnh theo quan hệ phụ thuộc
    for i, rule_i in enumerate(DanhSachLuat, start=1):
        out_i = rule_i["output"]
        for j, rule_j in enumerate(DanhSachLuat, start=1):
            if out_i in rule_j["inputs"]:
                G.add_edge(f"r{i}", f"r{j}", label=f"{out_i}")

    return G
