import streamlit as st

# Thêm CSS đổi màu nền thành xanh đen
st.markdown(
    """
    <style>
        body, .stApp {
            background-color: #0a192f !important;
            color: #f8fafc !important;
        }
        .block-container {
            background-color: #0a192f !important;
            color: #f8fafc !important;
        }
        .css-18e3th9, .css-1d391kg, .css-1dp5vir, .css-1v0mbdj, .css-1cpxqw2 {
            background-color: #0a192f !important;
            color: #f8fafc !important;
        }
        .stMarkdown, .stHeader, .stText, .stTitle, .stSubtitle, .stDataFrame, .stTable, .stExpander, .stButton, .stSidebar, .stSidebarContent {
            background-color: transparent !important;
            color: #f8fafc !important;
        }
        h1, h2, h3, h4, h5, h6, p, li, span, div {
            color: #f8fafc !important;
        }
        /* Đổi màu chữ sidebar */
        .css-1v0mbdj, .css-1cpxqw2, .css-1d391kg, .css-18e3th9 {
            color: #f8fafc !important;
        }
        /* Đổi màu placeholder input nếu có */
        ::placeholder {
            color: #cbd5e1 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)
# ===============================
# TITLE + TỔNG QUAN ĐỀ TÀI
# ===============================
st.markdown('<h1 class="tongquan-title">TỔNG QUAN ĐỀ TÀI</h1>', unsafe_allow_html=True)
# CSS căn giữa tiêu đề và tăng khoảng cách dưới
st.markdown(
    """
    <style>
        .tongquan-title {
            text-align: center;
            margin-bottom: 1.2rem;
            margin-top: 0.5rem;
            letter-spacing: 2px;
        }
        /* Nếu có hr hoặc st.write('---') thì margin-top vừa phải */
        hr, .stHorizontalRule {
            margin-top: 1.2rem !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)
st.write("---")

# ===============================
# SECTION 1
# ===============================
st.header("1. Giới thiệu đề tài")

st.markdown("""
Đề tài hướng đến việc xây dựng một khung phân tích định lượng nhằm đánh giá sức khỏe tài chính
của doanh nghiệp phi tài chính tại Việt Nam. Thay vì sử dụng trực tiếp các mô hình xếp hạng tín nhiệm
truyền thống, nghiên cứu khai thác cấu trúc nội tại của dữ liệu tài chính để nhận diện các nhóm doanh nghiệp
có đặc điểm tương đồng.

Cách tiếp cận này giúp giảm phụ thuộc vào giả định chủ quan, đồng thời cho phép mở rộng mô hình
theo thời gian và theo ngành.
""")

# ===============================
# SECTION 2
# ===============================
st.header("2. Dữ liệu và chỉ tiêu tài chính")

st.markdown("""
Dữ liệu nghiên cứu được tổng hợp từ báo cáo tài chính năm của doanh nghiệp, bao gồm các nhóm chỉ tiêu chính:
""")

st.markdown("""
- **Khả năng sinh lời**: ROA, ROE, biên lợi nhuận, EBIT trên tổng tài sản  
- **Cơ cấu vốn**: Nợ trên tổng tài sản, nợ trên vốn chủ sở hữu, tỷ lệ vốn chủ sở hữu  
- **Khả năng thanh khoản**: Current Ratio, Cash Ratio, khả năng thanh toán lãi vay  
- **Hiệu quả hoạt động**: Vòng quay tổng tài sản, vòng quay phải thu  
- **Dòng tiền và tăng trưởng**: Dòng tiền trên doanh thu, tăng trưởng doanh thu, lợi nhuận và tài sản  

Toàn bộ biến số được chuẩn hóa nhằm đảm bảo khả năng so sánh giữa các doanh nghiệp có quy mô khác nhau.
""")

# ===============================
# SECTION 3
# ===============================
st.header("3. Phương pháp phân cụm K-Means")

st.markdown("""
Thuật toán K-Means được sử dụng để phân chia doanh nghiệp thành các nhóm dựa trên mức độ tương đồng
của các chỉ tiêu tài chính. Thuật toán tối ưu bằng cách cực tiểu hóa khoảng cách nội cụm,
giúp các doanh nghiệp trong cùng một nhóm có cấu trúc tài chính gần nhau hơn.

Sau quá trình thử nghiệm nhiều cấu hình khác nhau, mô hình được lựa chọn với **6 cụm**,
đảm bảo cân bằng giữa tính ổn định thống kê và khả năng diễn giải kinh tế.
""")

# ===============================
# SECTION 4
# ===============================
st.header("4. Diễn giải kết quả phân cụm")

st.markdown("""
Kết quả phân cụm cho thấy dữ liệu doanh nghiệp hình thành 6 nhóm với đặc trưng tài chính rõ ràng:

- **AAA**: Nền tảng tài chính vượt trội, sinh lời cao, đòn bẩy thấp, thanh khoản mạnh  
- **AA**: Cơ cấu vốn an toàn, rủi ro thấp, hiệu quả hoạt động ổn định  
- **A**: Tình hình tài chính trung bình, hoạt động bình thường  
- **BBB**: Hiệu quả trung bình, sử dụng đòn bẩy cao, nhạy cảm với biến động vĩ mô  
- **BB**: Tăng trưởng nhanh, chấp nhận rủi ro tài chính cao  
- **B**: Sức khỏe tài chính yếu, áp lực lớn về lợi nhuận và thanh khoản  
""")

# ===============================
# SECTION 5
# ===============================
st.header("5. Quy đổi tín nhiệm và nhóm sức khỏe tài chính")

st.markdown("""
Trên cơ sở thứ bậc tương đối của các cụm, nghiên cứu tiến hành quy đổi thành các mức tín nhiệm
từ AAA đến B nhằm tăng khả năng diễn giải. Việc gán nhãn mang tính so sánh nội bộ trong mẫu nghiên cứu.

Tiếp theo, các mức tín nhiệm được gộp thành **bốn nhóm sức khỏe tài chính tổng quát** gồm:
sức khỏe tốt, khá, trung bình và yếu để phù hợp với nhu cầu phân tích và ra quyết định trong thực tiễn đầu tư và quản trị rủi ro.
""")

# ===============================
# FOOTER
# ===============================
st.write("---")
st.markdown(
    """
<center>
<span style='font-size:14px;color:#6b7280;'>
Trang Home cung cấp tổng quan dữ liệu, phương pháp và logic phân tích của hệ thống đánh giá sức khỏe tài chính doanh nghiệp.
</span>
</center>
""",
    unsafe_allow_html=True
)
