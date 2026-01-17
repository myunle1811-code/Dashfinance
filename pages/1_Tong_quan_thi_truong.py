import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# 1. CẤU HÌNH TRANG (GIỮ 1 LẦN)
# =====================================================
st.set_page_config(
    page_title="Tổng quan thị trường",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# 2. CSS – NỀN XANH ĐEN (FULL DARK THEME)
# =====================================================
st.markdown("""
<style>
/* OPTION BỊ DISABLED – HIỂN THỊ RÕ NHƯNG KHÔNG CHỌN */
div[data-baseweb="menu"] div[aria-disabled="true"] {
    color: #94a3b8 !important;        /* xám rõ */
    font-weight: 500 !important;
    background-color: #f8fafc !important;
    cursor: not-allowed !important;
    opacity: 1 !important;            /* QUAN TRỌNG */
    position: relative;
}
div[data-baseweb="menu"] div[aria-disabled="true"]:before {
    content: "\2713  "; /* Unicode tick ✓ */
    color: #22c55e;
    font-weight: bold;
    font-size: 1.1em;
    position: absolute;
    left: 10px;
    top: 50%;
    transform: translateY(-50%);
}
div[data-baseweb="menu"] div[aria-disabled="true"] span {
    margin-left: 22px !important;
}

/* OPTION ĐƯỢC CHỌN BÌNH THƯỜNG */
div[data-baseweb="menu"] div[aria-selected="true"] {
    background-color: #e0f2fe !important;
    color: #0f172a !important;
    font-weight: 600;
}
/* Nền chính */
body, .main, [data-testid="stAppViewContainer"], [data-testid="stVerticalBlock"] {
    background-color: #0b1320 !important;
    color: #e5e7eb !important;
}

/* Sidebar */
[data-testid="stSidebar"], .stSidebar {
    background-color: #000000 !important;
    color: #e5e7eb !important;
}

/* Header và text */
h1, h2, h3, h4, h5, h6, p, span, div {
    color: #e5e7eb !important;
}

h3 {
    font-size: 18px !important;
    margin-top: 5px !important;
    margin-bottom: 5px !important;
}

/* Block container */
.block-container {
    padding-top: 1rem;
    background-color: #0b1320 !important;
}

/* Metric cards */
.metric-card {
    background: linear-gradient(135deg,#0f172a,#020617) !important;
    border-radius: 16px;
    padding: 18px;
    border: 1px solid #1f2937;
    box-shadow: 0 0 25px rgba(0,0,0,0.3);
    color: #e5e7eb !important;
}
.metric-title { color: #9ca3af !important; font-size: 13px; }
.metric-value { color: #e5e7eb !important; font-size: 28px; font-weight: 700; }
.metric-sub { font-size: 12px; color: #22c55e !important; }

/* General cards */
.card {
    background-color: #020617 !important;
    border-radius: 16px;
    padding: 16px;
    border: 1px solid #1f2937;
    color: #e5e7eb !important;
}

/* Dataframe styling */
[data-testid="stDataFrame"] {
    background-color: #020617 !important;
}

/* Selectbox, multiselect, etc. */

.stSelectbox, .stMultiSelect, .stSlider, select, option, [data-baseweb="select"] input, [data-baseweb="select"] {
    box-shadow: none !important;
    outline: none !important;
    border: 2px solid #374151 !important;
    border-radius: 8px !important;
    background: #1e293b !important;
    color: #fff !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px;
}

[data-baseweb="select"] {
    box-shadow: none !important;
    outline: none !important;
    border: 2px solid #374151 !important;
    border-radius: 8px !important;
    background: #000 !important;
}

[data-baseweb="select"] input,
[data-baseweb="select"] [data-baseweb="placeholder"] {
    background: #000 !important;
    color: #fff !important;
    opacity: 1 !important;
    font-weight: bold !important;
    border: none !important;
    box-shadow: none !important;
}

[data-baseweb="select"] [data-baseweb="input-container"] {
    background: #000 !important;
    border: none !important;
    box-shadow: none !important;
}

[data-baseweb="select"] [data-baseweb="control-container"] {
    background: #000 !important;
    border: none !important;
    box-shadow: none !important;
}

.stSelectbox:focus, .stMultiSelect:focus, select:focus, [data-baseweb="select"] input:focus {
    outline: none !important;
    box-shadow: none !important;
    border-color: #60a5fa !important;
}


.stSelectbox input, .stSelectbox option, .stMultiSelect input, .stMultiSelect option {
    background-color: #1e293b !important;
    color: #fff !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    opacity: 1 !important;
    letter-spacing: 0.5px;
}


.stSelectbox input::placeholder, .stMultiSelect input::placeholder {
    color: #fff !important;
    opacity: 1 !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    letter-spacing: 0.5px;
}


select {
    background-color: #1e293b !important;
    color: #fff !important;
    border: 2px solid #374151 !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    opacity: 1 !important;
    letter-spacing: 0.5px;
}


option {
    background-color: #1e293b !important;
    color: #fff !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    opacity: 1 !important;
    letter-spacing: 0.5px;
}

[data-baseweb="select"] input,
[data-baseweb="select"] [data-baseweb="placeholder"] {
    background-color: #000 !important;
    color: #fff !important;
    opacity: 1 !important;
    font-weight: bold !important;
}

/* Dropdown menu */
[data-baseweb="select"] [data-baseweb="menu"] {
    background-color: #f8fafc !important;
    color: #0f172a !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
}

[data-baseweb="select"] [data-baseweb="option"] {
    background-color: #f8fafc !important;
    color: #0f172a !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
}

[data-baseweb="select"] [data-baseweb="option"]:hover {
    background-color: #dbeafe !important;
    color: #0f172a !important;
}

[data-baseweb="select"] [aria-selected="true"] {
    background-color: #bae6fd !important;
    color: #0f172a !important;
}

/* Multiselect chips */
[data-baseweb="tag"] {
    background-color: #000000 !important;
    color: #ffffff !important;
    border: 1px solid #374151 !important;
}

/* Buttons */
.stButton button {
    background-color: #1f2937 !important;
    color: #e5e7eb !important;
}

/* Divider */
hr {
    border-color: #1f2937 !important;
    margin: 5px 0 !important;
}

/* Columns */
.stColumn {
    padding: 0 5px !important;
}
/* Đổi màu radio đã chọn sang xanh mạnh, override cả ::after */
div[role="radiogroup"] > label > div:first-child {
    border-color: #22c55e !important;
}
div[role="radiogroup"] > label > div:first-child > div:after {
    background: #22c55e !important;
    border: 2px solid #22c55e !important;
}
/* Đổi màu tick checkbox đã chọn sang xanh mạnh, override cả ::before */
div[role="checkbox"] > div:first-child {
    border-color: #22c55e !important;
}
div[role="checkbox"][aria-checked="true"] > div:first-child {
    background: #22c55e !important;
    border-color: #22c55e !important;
}
div[role="checkbox"][aria-checked="true"] > div:first-child > svg {
    color: #fff !important;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# 3. LOAD DATA (ƯU TIÊN CODE 1)
# =====================================================
@st.cache_data
def load_data():
    df_health = pd.read_csv("data_suc_khoe.csv")
    df_mktcap = pd.read_parquet("Marketcap_2124.parquet")
    df_cluster = pd.read_excel("Cluster_Profile_KMeans_k6.xlsx")

    df_health["NĂM"] = df_health["NĂM"].astype(int)
    return df_health, df_mktcap, df_cluster

df_health, df_mktcap, df_cluster = load_data()

# Màu xanh đậm cho biểu đồ
blue_palette = ['#1e40af', '#3b82f6', '#2563eb', '#1d4ed8', '#1e3a8a', '#0f172a']

# =====================================================
# 4. SIDEBAR – BỘ LỌC (GIỮ CODE 1)
# =====================================================
st.sidebar.title("BỘ LỌC")

year = st.sidebar.radio(
    "Năm tài chính",
    sorted(df_health["NĂM"].unique()),
    index=len(df_health["NĂM"].unique()) - 1,
    horizontal=False
)


st.sidebar.write("")
st.sidebar.markdown("<b>Ngành (ICB cấp 2)</b>", unsafe_allow_html=True)
all_industries = sorted(df_health["NGÀNH"].dropna().unique())
industry_selected = []
select_all = st.sidebar.checkbox("Tất cả các ngành", value=True)
if select_all:
    industry_selected = all_industries
else:
    for ng in all_industries:
        if st.sidebar.checkbox(ng, value=False, key=f"nganh_{ng}"):
            industry_selected.append(ng)

rating_filter = st.sidebar.radio(
    "Mức tín nhiệm",
    ["Tất cả", "AAA", "AA", "A", "BBB", "BB", "B"],
    horizontal=False
)

# =====================================================
# 5. LỌC DATA
# =====================================================

df = df_health[df_health["NĂM"] == year].copy()
if industry_selected:
    df = df[df["NGÀNH"].isin(industry_selected)]

if rating_filter != "Tất cả":
    df = df[df["Credit_Rating"] == rating_filter]

# =====================================================
# 6. TIÊU ĐỀ (THEO YÊU CẦU – GIỮ CODE 1)
# =====================================================
st.markdown("""
<h2 style='text-align:center; font-weight:800; margin-top: 3.5rem;'>
TỔNG QUAN THỊ TRƯỜNG
</h2>
""", unsafe_allow_html=True)

st.divider()

# =====================================================
# 7. KPI TOÀN THỊ TRƯỜNG (KẾT HỢP 2 CODE)
# =====================================================
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Tổng số doanh nghiệp</div>
        <div class="metric-value">{df['MÃ'].nunique():,}</div>
        <div class="metric-sub">Năm {year}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">ROA trung bình</div>
        <div class="metric-value">{df['ROA'].mean()*100:.2f}%</div>
        <div class="metric-sub">Hiệu quả sử dụng tài sản</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    safe_ratio = (df["EQUITY / TỔNG TÀI SẢN"] > 0.5).mean() * 100
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Doanh nghiệp có VCSH &gt; 50%</div>
        <div class="metric-value">{safe_ratio:.1f}%</div>
        <div class="metric-sub">Cấu trúc vốn an toàn</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    high_debt = (df["NỢ / TỔNG TÀI SẢN"] > 0.7).mean() * 100
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Doanh nghiệp có đòn bẩy cao</div>
        <div class="metric-value">{high_debt:.1f}%</div>
        <div class="metric-sub">Rủi ro tài chính</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    num_good = (df['financial_health'] == 'Tốt').sum()
    percent_good = (num_good / len(df) * 100) if len(df) > 0 else 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Doanh nghiệp sức khỏe <b>Tốt</b></div>
        <div class="metric-value">{percent_good:.1f}%</div>
        <div class="metric-sub">Số lượng: {num_good}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()
# =====================================================
# 8. TREEMAP VỐN HÓA THỊ TRƯỜNG & PHÂN BỐ CỤM (CẠNH NHAU)
# =====================================================
col_tree, col_cluster = st.columns(2)

with col_tree:
    # st.subheader("BIỂU ĐỒ VỐN HÓA THỊ TRƯỜNG THEO NĂM")

    # --- Chuẩn hóa ngày & tạo cột năm ---
    df_mktcap["Ngày"] = pd.to_datetime(df_mktcap["Ngày"])
    df_mktcap["NĂM"] = df_mktcap["Ngày"].dt.year

    # --- Lấy MarketCap ngày cuối năm cho từng mã ---
    df_mktcap_year = (
        df_mktcap
        .sort_values("Ngày")
        .groupby(["Mã", "NĂM"], as_index=False)
        .tail(1)
    )

    # --- Lọc theo năm dashboard ---
    df_mktcap_year = df_mktcap_year[df_mktcap_year["NĂM"] == year]

    # --- Ghép ngành từ data tài chính ---
    df_treemap = df_mktcap_year.merge(
        df[["MÃ", "NGÀNH"]],
        left_on="Mã",
        right_on="MÃ",
        how="inner"
    )

    # --- Vẽ treemap ---
    fig_tree = px.treemap(
        df_treemap,
        path=["NGÀNH", "Mã"],
        values="MarketCap",
        template="plotly_dark",
        title=f"BẢN ĐỒ VỐN HÓA THỊ TRƯỜNG THEO NĂM – {year}",
        color_discrete_sequence=blue_palette
    )

    fig_tree.update_traces(
        hovertemplate=
        "<b>%{label}</b><br>" +
        "Vốn hóa: %{value:,.0f}<br>" +
        "Ngành: %{parent}<extra></extra>"
    )

    fig_tree.update_layout(
        paper_bgcolor='#0f172a',
        plot_bgcolor='#020617',
        font=dict(color='#e5e7eb'),
        title_font_color='#fff'
    )

    st.plotly_chart(fig_tree, use_container_width=True)

with col_cluster:
    # st.subheader("PHÂN BỐ DOANH NGHIỆP THEO NHÃN TÍN NHIỆM")

    fig_cluster = px.histogram(
        df,
        x="Credit_Rating",
        color="Credit_Rating",
        template="plotly_dark",
        title=f"PHÂN BỐ DOANH NGHIỆP THEO NHÃN TÍN NHIỆM – {year}",
        color_discrete_sequence=blue_palette
    )
    fig_cluster.update_layout(
        showlegend=False,
        paper_bgcolor='#0f172a',
        plot_bgcolor='#020617',
        font=dict(color='#e5e7eb'),
        title_font_color='#fff'
    )

    st.plotly_chart(fig_cluster, use_container_width=True)

st.divider()
# =====================================================
# 10. SỨC KHỎENH & BOXPLOT ROA (CẠNH NHAU)
# =====================================================
col_health, col_box = st.columns(2)

# ...existing code...

with col_health:
    # Biểu đồ stacked bar: Phân bố ngành với mức tín nhiệm
    industry_rating = (
        df.groupby(["NGÀNH", "Credit_Rating"]).size().reset_index(name="Số lượng doanh nghiệp")
    )
    fig_industry = px.bar(
        industry_rating,
        x="Số lượng doanh nghiệp",
        y="NGÀNH",
        color="Credit_Rating",
        orientation="h",
        template="plotly_dark",
        color_discrete_sequence=blue_palette,
        title=f"PHÂN BỐ NGÀNH VỚI MỨC TÍN NHIỆM – {year}"
    )
    fig_industry.update_layout(
        paper_bgcolor='#0f172a',
        plot_bgcolor='#020617',
        font=dict(color='#fff'),  # Chữ trắng
        title_font_color='#fff',
        legend_font_color='#fff',  # Chữ trắng cho chú thích
        xaxis=dict(color='#fff'),
        yaxis=dict(color='#fff')
    )

    st.plotly_chart(fig_industry, use_container_width=True)

with col_box:
    fig_box = px.box(
        df,
        x="NGÀNH",
        y="ROA",
        template="plotly_dark",
        title=f"PHÂN PHỐI ROA THEO NGÀNH – {year}",
        color_discrete_sequence=blue_palette
    )

    fig_box.update_layout(
        paper_bgcolor='#0f172a',
        plot_bgcolor='#020617',
        font=dict(color='#fff'),  # Chữ trắng
        title_font_color='#fff',
        legend_font_color='#fff',  # Chữ trắng cho chú thích
        xaxis=dict(color='#fff'),
        yaxis=dict(color='#fff')
    )

    st.plotly_chart(fig_box, use_container_width=True)


# =====================================================
# 11A. TOP 10 CÔNG TY DOANH THU THUẦN CAO NHẤT, TĂNG TRƯỞNG LNST, DOANH THU, TÀI SẢN
# =====================================================
st.subheader("TOP 10 CÔNG TY NỔI BẬT THEO CHỈ TIÊU")

# Đọc data_dash.csv
df_dash = pd.read_csv("data_dash.csv")
df_dash = df_dash[df_dash["NĂM"] == year]

top_doanh_thu = df_dash.sort_values("DOANH THU", ascending=False).head(10)[["MÃ", "TÊN CÔNG TY", "NGÀNH", "DOANH THU"]].reset_index(drop=True)
top_tangtruong_doanhthu = df_dash.sort_values("TĂNG TRƯỞNG DOANH THU", ascending=False).head(10)[["MÃ", "TÊN CÔNG TY", "NGÀNH", "TĂNG TRƯỞNG DOANH THU"]].reset_index(drop=True)

colA, colB = st.columns(2)
with colA:
    fig1 = px.bar(
        top_doanh_thu,
        x="TÊN CÔNG TY",
        y="DOANH THU",
        text="DOANH THU",
        color_discrete_sequence=["#e6007a"],
        title=f"Top 10 Công Ty Có Doanh Thu Thuần Cao Nhất {year}"
    )
    fig1.update_traces(
        texttemplate='%{y:,.0f}',
        textposition='outside',
        marker_line_width=0  # Xóa viền cột để không che số
    )
    fig1.update_layout(
        xaxis_tickangle=-30,
        paper_bgcolor='#0f172a',
        plot_bgcolor='#020617',
        font=dict(color='#e5e7eb'),
        title_font_color='#fff',
        yaxis_title=None,
        xaxis_title=None,
        margin=dict(t=60, b=60),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig1, use_container_width=True)

with colB:
    fig3 = px.bar(
        top_tangtruong_doanhthu,
        x="TÊN CÔNG TY",
        y="TĂNG TRƯỞNG DOANH THU",
        text="TĂNG TRƯỞNG DOANH THU",
        color_discrete_sequence=["#00e6b8"],
        title=f"Top 10 Công Ty Có Tăng Trưởng Doanh Thu Cao Nhất {year}"
    )
    fig3.update_traces(
        texttemplate='%{y:.2%}',
        textposition='outside',
        marker_line_width=0  # Xóa viền cột để không che số
    )
    fig3.update_layout(
        xaxis_tickangle=-30,
        paper_bgcolor='#0f172a',
        plot_bgcolor='#020617',
        font=dict(color='#e5e7eb'),
        title_font_color='#fff',
        yaxis_title=None,
        xaxis_title=None,
        margin=dict(t=60, b=60),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig3, use_container_width=True)



# =====================================================
# 11B. DÒNG TIỀN NHÀ ĐẦU TƯ NƯỚC NGOÀI THEO NGÀNH & NHÓM SỨC KHỎE (SỬA: DÙNG data_cff.parquet + data_suc_khoe.csv)
# =====================================================

import os
import warnings
warnings.filterwarnings("ignore")

# Đọc data_cff.parquet (dòng tiền theo năm, mã)
df_cff = None
if os.path.exists("data_cff.parquet"):
    df_cff = pd.read_parquet("data_cff.parquet")
else:
    st.warning("Không tìm thấy file data_cff.parquet để vẽ biểu đồ dòng tiền nhà đầu tư nước ngoài.")

# Đọc data_suc_khoe.csv để lấy ngành, tín nhiệm, nhóm sức khỏe
df_health_info = None
if os.path.exists("data_suc_khoe.csv"):
    df_health_info = pd.read_csv("data_suc_khoe.csv")
else:
    st.warning("Không tìm thấy file data_suc_khoe.csv để join thông tin ngành, sức khỏe.")

if df_cff is not None and df_health_info is not None:
    # Đảm bảo cột NĂM là int
    if "NĂM" in df_cff.columns:
        df_cff["NĂM"] = df_cff["NĂM"].astype(int)
    if "NĂM" in df_health_info.columns:
        df_health_info["NĂM"] = df_health_info["NĂM"].astype(int)

    # Lọc theo năm dashboard
    df_cff_year = df_cff[df_cff["NĂM"] == year].copy()
    df_health_info_year = df_health_info[df_health_info["NĂM"] == year].copy()

    # Join để lấy ngành, tín nhiệm, nhóm sức khỏe
    df_cff_joined = df_cff_year.merge(
        df_health_info_year[["MÃ", "NGÀNH", "Credit_Rating", "financial_health"]],
        left_on="Mã",
        right_on="MÃ",
        how="left"
    )

    # Biểu đồ 1: Dòng tiền nhà đầu tư nước ngoài vào mỗi ngành
    if "NGÀNH" in df_cff_joined.columns and "Net.F_Val" in df_cff_joined.columns:
        df_industry_flow = df_cff_joined.groupby("NGÀNH")["Net.F_Val"].sum().reset_index()
        fig_industry_flow = px.bar(
            df_industry_flow,
            x="NGÀNH",
            y="Net.F_Val",
            color="Net.F_Val",
            color_continuous_scale="Blues",
            title=f"Dòng tiền nhà đầu tư nước ngoài vào từng ngành năm {year}"
        )
        fig_industry_flow.update_layout(
            paper_bgcolor='#0f172a',
            plot_bgcolor='#020617',
            font=dict(color='#e5e7eb'),
            title_font_color='#fff',
            xaxis_tickangle=-30
        )
        st.plotly_chart(fig_industry_flow, use_container_width=True)
    else:
        st.info("Không đủ cột để vẽ biểu đồ dòng tiền theo ngành.")


st.divider()
# =====================================================
# 12. DOANH NGHIỆP TIÊU BIỂU
# =====================================================
st.subheader("DOANH NGHIỆP TIÊU BIỂU")

# Đảm bảo cột health_num tồn tại, nếu không thì tạo tạm
if "health_num" not in df.columns:
    health_map = {"Tốt": 4, "Khá": 3, "Trung bình": 2, "Yếu": 1}
    df["health_num"] = df["financial_health"].map(health_map)

# Chỉ lấy các cột có tồn tại trong df
cols = [c for c in ["MÃ", "TÊN CÔNG TY", "NGÀNH", "Credit_Rating", "financial_health"] if c in df.columns]

if len(df) > 0 and len(cols) > 0:
    top_table = (
        df.sort_values("health_num", ascending=False)
        [cols]
        .head(10)
        .reset_index(drop=True)
    )
    st.dataframe(top_table, use_container_width=True)
else:
    st.info("Không có dữ liệu doanh nghiệp tiêu biểu phù hợp.")

# =====================================================
# 13. FOOTER
# =====================================================
st.caption(
    "Dữ liệu được tổng hợp từ báo cáo tài chính doanh nghiệp niêm yết tại Việt Nam. "
    "Phân tích dựa trên mô hình K-Means (k = 6) và hệ thống chỉ tiêu tài chính chuẩn hóa."
)
