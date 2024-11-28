import streamlit as st
from simpleai.search import CspProblem, backtrack
import matplotlib.pyplot as plt

# Hàm kiểm tra ràng buộc giữa hai vùng
def constraint_func(names, values):
    return values[0] != values[1]

def draw_map(solution):
    fig, ax = plt.subplots(figsize=(8, 6))

    # Tọa độ các vùng
    coordinates = {
        'WA': (1, 3),
        'NT': (2, 4),
        'Q': (3, 4),
        'SA': (2, 3),
        'NSW': (3, 3),
        'V': (3, 2),
        'T': (3, 1.2),  # Di chuyển Tasmania gần hơn
    }

    # Kết nối các vùng liền kề
    connections = [
        ('SA', 'WA'), ('SA', 'NT'), ('SA', 'Q'), ('SA', 'NSW'), ('SA', 'V'),
        ('WA', 'NT'), ('NT', 'Q'), ('Q', 'NSW'), ('NSW', 'V'),
        ('V', 'T'),  # Thêm kết nối Tasmania
    ]

    # Ánh xạ màu từ ký hiệu
    color_map = {
        'R': 'red',
        'G': 'green',
        'B': 'blue'
    }

    # Vẽ các kết nối giữa các vùng
    for region1, region2 in connections:
        x1, y1 = coordinates[region1]
        x2, y2 = coordinates[region2]
        ax.plot([x1, x2], [y1, y2], color='black', zorder=1)

    # Vẽ và tô màu các vùng
    for region, (x, y) in coordinates.items():
        # Lấy màu từ kết quả, nếu không có thì mặc định là 'white'
        color = color_map.get(solution.get(region, 'white'), 'white')
        ax.scatter(x, y, s=2000, color=color, edgecolors='black', zorder=2)
        ax.text(x, y, region, color='black', ha='center', va='center', fontsize=12)

    # Cài đặt giao diện đồ thị
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 5)
    ax.axis('off')
    st.pyplot(fig)


# Tạo giao diện Streamlit
st.title("Tô màu bản đồ miền Tây nước Úc")
st.write("Sử dụng CSP để giải bài toán tô màu bản đồ.")

# Định nghĩa bài toán
names = ('WA', 'NT', 'Q', 'NSW', 'V', 'SA', 'T')
domain = {
    'WA':  ['R', 'G', 'B'],
    'NT':  ['R', 'G', 'B'],
    'Q':   ['R', 'G', 'B'],
    'NSW': ['R', 'G', 'B'],
    'V':   ['R', 'G', 'B'],
    'SA':  ['R', 'G', 'B'],
    'T':   ['R', 'G', 'B'],
}

constraints = [
    (('SA', 'WA'), constraint_func),
    (('SA', 'NT'), constraint_func),
    (('SA', 'Q'), constraint_func),
    (('SA', 'NSW'), constraint_func),
    (('SA', 'V'), constraint_func),
    (('WA', 'NT'), constraint_func),
    (('NT', 'Q'), constraint_func),
    (('Q', 'NSW'), constraint_func),
    (('NSW', 'V'), constraint_func),
    (('V', 'T'), constraint_func),  # Thêm ràng buộc kết nối Tasmania
]

# Giải bài toán
if st.button("Giải bài toán"):
    problem = CspProblem(names, domain, constraints)
    solution = backtrack(problem)

    if solution:
        st.success("Tìm được giải pháp!")
        st.json(solution)
        st.subheader("Bản đồ tô màu:")
        draw_map(solution)
    else:
        st.error("Không tìm được giải pháp.")