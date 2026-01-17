"""
Dashboard Phân Tích Chi Tiết Doanh Nghiệp
Giao diện dark theme xanh đen với đầy đủ tính năng phân tích tài chính
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
import glob
from datetime import datetime as NgayGio, timedelta as KhoangThoiGian  # Đổi sang tiếng Việt
warnings.filterwarnings('ignore')

# ============================================================================
# CẤU HÌNH TRANG
# ============================================================================
st.set_page_config(
    page_title="Phân Tích Chi Tiết Doanh Nghiệp",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# CSS - GIAO DIỆN XANH ĐEN
# ============================================================================
st.markdown("""
<style>
    /* Nền chính - Xanh đen */
    .main {
        background: linear-gradient(135deg, #0a1628 0%, #020617 50%, #0a1628 100%) !important;
    }
    
    [data-testid="stAppViewContainer"], 
    [data-testid="stVerticalBlock"],
    .block-container {
        background: linear-gradient(135deg, #0a1628 0%, #020617 50%, #0a1628 100%) !important;
        color: #e5e7eb !important;
        padding-top: 1rem !important;
    }
    
    /* Sidebar - Đen đậm */
    [data-testid="stSidebar"] {
        background: #000000 !important;
        border-right: 1px solid #1e293b !important;
    }
    
    /* Typography - Màu xanh nhạt */
    h1, h2, h3, h4, h5, h6 {
        color: #22d3ee !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
    }
    
    h1 {
        font-size: 2.5rem !important;
        text-shadow: 0 2px 10px rgba(34, 211, 238, 0.3) !important;
        border-bottom: 3px solid #22d3ee !important;
        padding-bottom: 10px !important;
        margin-bottom: 20px !important;
    }
    
    h2 {
        font-size: 1.8rem !important;
        color: #06b6d4 !important;
        border-bottom: 2px solid #06b6d4 !important;
        padding-bottom: 8px !important;
        margin: 20px 0 15px 0 !important;
    }
    
    h3 {
        font-size: 1.4rem !important;
        color: #67e8f9 !important;
        margin: 15px 0 10px 0 !important;
    }
    
    p, span, div, label {
        color: #cbd5e1 !important;
    }
    
    /* Metric Cards - Nền xanh đen với border xanh */
    [data-testid="stMetricValue"], 
    [data-testid="stMetricLabel"],
    [data-testid="stMetricDelta"] {
        color: #e5e7eb !important;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important;
        border: 1px solid #22d3ee !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0 4px 15px rgba(34, 211, 238, 0.2) !important;
        transition: all 0.3s ease !important;
    }
    
    .metric-card:hover {
        box-shadow: 0 6px 25px rgba(34, 211, 238, 0.4) !important;
        border-color: #06b6d4 !important;
        transform: translateY(-2px) !important;
    }
    
    /* Health Score Gauge - Xanh cyan */
    .health-score-container {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important;
        border: 2px solid #22d3ee !important;
        border-radius: 20px !important;
        padding: 30px !important;
        text-align: center !important;
        box-shadow: 0 8px 30px rgba(34, 211, 238, 0.3) !important;
    }
    
    .health-score-value {
        font-size: 48px !important;
        font-weight: 900 !important;
        color: #22d3ee !important;
        text-shadow: 0 0 20px rgba(34, 211, 238, 0.8) !important;
    }
    
    .health-score-label {
        font-size: 18px !important;
        color: #67e8f9 !important;
        margin-top: 10px !important;
    }
    
    /* Company Info Card */
    .company-info-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important;
        border: 1px solid #06b6d4 !important;
        border-radius: 16px !important;
        padding: 25px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 6px 20px rgba(6, 182, 212, 0.2) !important;
    }
    
    .company-name {
        font-size: 32px !important;
        font-weight: 900 !important;
        color: #22d3ee !important;
        margin-bottom: 10px !important;
    }
    
    .company-code {
        display: inline-block !important;
        background: #06b6d4 !important;
        color: #020617 !important;
        padding: 5px 15px !important;
        border-radius: 20px !important;
        font-weight: 700 !important;
        font-size: 18px !important;
        margin-right: 10px !important;
    }
    
    .company-tag {
        display: inline-block !important;
        border: 1px solid #22d3ee !important;
        color: #22d3ee !important;
        padding: 5px 12px !important;
        border-radius: 15px !important;
        font-size: 13px !important;
        margin: 5px 5px 5px 0 !important;
        background: rgba(34, 211, 238, 0.1) !important;
    }
    
    /* Rating Badges */
    .rating-aaa { color: #10b981 !important; font-weight: 700 !important; }
    .rating-aa { color: #22d3ee !important; font-weight: 700 !important; }
    .rating-a { color: #fbbf24 !important; font-weight: 700 !important; }
    .rating-bbb { color: #f59e0b !important; font-weight: 700 !important; }
    .rating-b { color: #ef4444 !important; font-weight: 700 !important; }
    
    /* Selectbox, Dropdown */
    [data-baseweb="select"],
    .stSelectbox > div > div {
        background: #000000 !important;
        border: 2px solid #22d3ee !important;
        border-radius: 8px !important;
        color: #e5e7eb !important;
    }
    
    [data-baseweb="select"] input,
    [data-baseweb="select"] [data-baseweb="placeholder"] {
        background: #000000 !important;
        color: #22d3ee !important;
        font-weight: 600 !important;
    }
    
    [data-baseweb="select"] [data-baseweb="menu"] {
        background: #0f172a !important;
        border: 1px solid #22d3ee !important;
    }
    
    [data-baseweb="select"] [data-baseweb="option"]:hover {
        background: #1e293b !important;
        color: #22d3ee !important;
    }
    
    /* Input text */
    [data-testid="stTextInput"] input {
        background: #000000 !important;
        border: 2px solid #22d3ee !important;
        color: #e5e7eb !important;
        border-radius: 8px !important;
    }
    
    [data-testid="stTextInput"] input:focus {
        border-color: #06b6d4 !important;
        box-shadow: 0 0 10px rgba(34, 211, 238, 0.3) !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%) !important;
        color: #020617 !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        padding: 10px 20px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #22d3ee 0%, #06b6d4 100%) !important;
        box-shadow: 0 4px 15px rgba(34, 211, 238, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Dataframe */
    [data-testid="stDataFrame"] {
        background: #0f172a !important;
        border: 1px solid #1e293b !important;
        border-radius: 8px !important;
    }
    
    /* Tabs cho Financial Statements */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
        background: #0f172a !important;
        border-bottom: 2px solid #1e293b !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #1e293b !important;
        border: 1px solid #22d3ee !important;
        border-radius: 8px 8px 0 0 !important;
        color: #cbd5e1 !important;
        padding: 10px 20px !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: #06b6d4 !important;
        color: #020617 !important;
        font-weight: 700 !important;
        border-color: #06b6d4 !important;
    }
    
    /* AI Commentary Box */
    .ai-commentary-box {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
        border: 2px solid #22d3ee !important;
        border-radius: 12px !important;
        padding: 25px !important;
        margin: 20px 0 !important;
        box-shadow: 0 6px 25px rgba(34, 211, 238, 0.2) !important;
    }
    
    .ai-commentary-title {
        font-size: 24px !important;
        color: #22d3ee !important;
        font-weight: 700 !important;
        margin-bottom: 15px !important;
        border-bottom: 2px solid #06b6d4 !important;
        padding-bottom: 10px !important;
    }
    
    .ai-commentary-section {
        margin: 15px 0 !important;
    }
    
    .ai-commentary-section h4 {
        color: #06b6d4 !important;
        font-size: 18px !important;
        margin-bottom: 10px !important;
    }
    
    .ai-commentary-section p {
        color: #cbd5e1 !important;
        line-height: 1.8 !important;
        font-size: 15px !important;
    }
    
    /* Warning Box */
    .warning-box {
        background: linear-gradient(135deg, #7c2d12 0%, #431407 100%) !important;
        border: 2px solid #f59e0b !important;
        border-radius: 12px !important;
        padding: 20px !important;
        margin: 15px 0 !important;
    }
    
    .warning-title {
        color: #fbbf24 !important;
        font-weight: 700 !important;
        font-size: 18px !important;
    }
    
    .warning-text {
        color: #fcd34d !important;
    }
    
    /* Info Box */
    .info-box {
        background: linear-gradient(135deg, #164e63 0%, #0c4a6e 100%) !important;
        border: 2px solid #06b6d4 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        margin: 15px 0 !important;
    }
    
    /* Success Box */
    .success-box {
        background: linear-gradient(135deg, #064e3b 0%, #022c22 100%) !important;
        border: 2px solid #10b981 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        margin: 15px 0 !important;
    }
    
    /* Divider */
    hr {
        border-color: #1e293b !important;
        margin: 30px 0 !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0f172a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #22d3ee;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #06b6d4;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# LOAD DỮ LIỆU - TẤT CẢ FILE
# ============================================================================
@st.cache_data
def load_all_data():
    """Tải tất cả dữ liệu cần thiết"""
    data_dict = {}
    
    try:
        # 1. DATA_SUC_KHOE (chỉ tiêu tài chính)
        data_dict['health'] = pd.read_csv('data_suc_khoe.csv')
        data_dict['health']['NĂM'] = data_dict['health']['NĂM'].astype(int)
        
        # 2. DATA_FIN_FULL (báo cáo tài chính đầy đủ)
        try:
            if 'DATA_FIN_FULL.xlsx' in glob.glob('*.xlsx'):
                data_dict['fin_full'] = pd.read_excel('DATA_FIN_FULL.xlsx')
                data_dict['fin_full']['NĂM'] = data_dict['fin_full']['NĂM'].astype(int)
        except:
            data_dict['fin_full'] = None
            
        # 3. DATA_BCTC (bảng cân đối kế toán + KQKD + LCTT)
        try:
            if 'Data BCTC.xlsx' in glob.glob('*.xlsx'):
                data_dict['bctc'] = pd.read_excel('Data BCTC.xlsx')
                data_dict['bctc']['NĂM'] = data_dict['bctc']['NĂM'].astype(int)
        except:
            data_dict['bctc'] = None
        
        # 4. PRICE (giá cổ phiếu)
        try:
            import pyarrow
            if 'Price_2124.parquet' in glob.glob('*.parquet'):
                data_dict['price'] = pd.read_parquet('Price_2124.parquet')
                if 'Ngày' in data_dict['price'].columns:
                    data_dict['price']['Ngày'] = pd.to_datetime(data_dict['price']['Ngày'])  # Ngày
            else:
                data_dict['price'] = None
        except:
            data_dict['price'] = None
        
        # 5. VOLUME (khối lượng)
        try:
            if 'Volume_2124.parquet' in glob.glob('*.parquet'):
                data_dict['volume'] = pd.read_parquet('Volume_2124.parquet')
                if 'Ngày' in data_dict['volume'].columns:
                    data_dict['volume']['Ngày'] = pd.to_datetime(data_dict['volume']['Ngày'])  # Ngày
            else:
                data_dict['volume'] = None
        except:
            data_dict['volume'] = None
        
        # 6. MARKETCAP (vốn hóa)
        try:
            if 'Marketcap_2124.parquet' in glob.glob('*.parquet'):
                data_dict['marketcap'] = pd.read_parquet('Marketcap_2124.parquet')
                if 'Ngày' in data_dict['marketcap'].columns:
                    data_dict['marketcap']['Ngày'] = pd.to_datetime(data_dict['marketcap']['Ngày'])  # Ngày
            else:
                data_dict['marketcap'] = None
        except:
            data_dict['marketcap'] = None
        
        # 7. DF_FT (dữ liệu foreign flow)
        try:
            if 'df_ft_2124.parquet' in glob.glob('*.parquet'):
                data_dict['foreign'] = pd.read_parquet('df_ft_2124.parquet')
                if 'Ngày' in data_dict['foreign'].columns:
                    data_dict['foreign']['Ngày'] = pd.to_datetime(data_dict['foreign']['Ngày'])  # Ngày
            else:
                data_dict['foreign'] = None
        except:
            data_dict['foreign'] = None
        
        # 8. DATA_CFF (dòng tiền nước ngoài)
        try:
            if 'data_cff.parquet' in glob.glob('*.parquet'):
                data_dict['cff'] = pd.read_parquet('data_cff.parquet')
                data_dict['cff']['NĂM'] = data_dict['cff']['NĂM'].astype(int)
            else:
                data_dict['cff'] = None
        except:
            data_dict['cff'] = None
        
        # 9. DATA_DASH (tổng hợp)
        try:
            if 'data_dash.csv' in glob.glob('*.csv'):
                data_dict['dash'] = pd.read_csv('data_dash.csv')
                data_dict['dash']['NĂM'] = data_dict['dash']['NĂM'].astype(int)
            else:
                data_dict['dash'] = None
        except:
            data_dict['dash'] = None
            
    except Exception as e:
        st.error(f"Lỗi khi tải dữ liệu: {str(e)}")
        return None
    
    return data_dict

# Load dữ liệu
data = load_all_data()

if data is None or data.get('health') is None:
    st.error("❌ Không thể tải dữ liệu. Vui lòng kiểm tra file data_suc_khoe.csv")
    st.stop()

# ============================================================================
# HÀM TRỢ GIÚP - TÍNH TOÁN VÀ PHÂN TÍCH
# ============================================================================

def calculate_health_score(company_data):
    """
    Tính điểm sức khỏe tài chính dựa trên các chỉ tiêu
    Không phải health score phức tạp, chỉ là indicator đơn giản
    """
    if len(company_data) == 0:
        return 0, "Không có dữ liệu"
    
    latest = company_data.iloc[-1]
    
    score = 0
    max_score = 100
    
    # ROA (0-20 điểm)
    if pd.notna(latest.get('ROA')):
        roa = latest['ROA']
        if roa > 0.1:
            score += 20
        elif roa > 0.05:
            score += 15
        elif roa > 0:
            score += 10
        elif roa > -0.05:
            score += 5
    
    # ROE (0-20 điểm)
    if pd.notna(latest.get('ROE')):
        roe = latest['ROE']
        if roe > 0.2:
            score += 20
        elif roe > 0.15:
            score += 15
        elif roe > 0.1:
            score += 10
        elif roe > 0:
            score += 5
    
    # Current Ratio (0-15 điểm)
    if pd.notna(latest.get('CURRENT RATIO')):
        cr = latest['CURRENT RATIO']
        if 1.5 <= cr <= 3:
            score += 15
        elif 1 <= cr < 1.5:
            score += 10
        elif cr >= 3:
            score += 8
        else:
            score += 3
    
    # Nợ/Tổng tài sản (0-15 điểm) - càng thấp càng tốt
    if pd.notna(latest.get('NỢ / TỔNG TÀI SẢN')):
        debt_ratio = latest['NỢ / TỔNG TÀI SẢN']
        if debt_ratio < 0.3:
            score += 15
        elif debt_ratio < 0.5:
            score += 12
        elif debt_ratio < 0.7:
            score += 8
        else:
            score += 3
    
    # Dòng tiền (0-15 điểm)
    if pd.notna(latest.get('DÒNG TIỀN / DOANH THU')):
        cf_ratio = latest['DÒNG TIỀN / DOANH THU']
        if cf_ratio > 0.1:
            score += 15
        elif cf_ratio > 0:
            score += 10
        else:
            score += 3
    
    # Khả năng thanh toán lãi vay (0-15 điểm)
    if pd.notna(latest.get('KHẢ NĂNG THANH TOÁN LÃI VAY')):
        interest_coverage = latest['KHẢ NĂNG THANH TOÁN LÃI VAY']
        if interest_coverage > 3:
            score += 15
        elif interest_coverage > 1.5:
            score += 10
        elif interest_coverage > 0:
            score += 5
    
    # Xếp loại
    if score >= 80:
        rating = "Xuất sắc"
    elif score >= 65:
        rating = "Tốt"
    elif score >= 50:
        rating = "Khá"
    elif score >= 35:
        rating = "Trung bình"
    else:
        rating = "Yếu"
    
    return score, rating

def generate_ai_commentary(company_code, company_data, price_data, foreign_data, data_dict):
    """
    PROMPT CHUẨN CHO AI NHẬN XÉT TOÀN DIỆN DOANH NGHIỆP (DÀI, ĐA CHIỀU, CỤ THỂ):

    Hãy đóng vai chuyên gia phân tích đầu tư, nhận xét toàn diện về doanh nghiệp {company_code} dựa trên dữ liệu đầu vào. Nhận xét phải dài, chi tiết, đa chiều, có dẫn chứng số liệu cụ thể, giải thích rõ ràng, giúp nhà đầu tư phổ thông dễ hiểu và có thể ra quyết định.

    YÊU CẦU:
    - Đánh giá tổng quan hoạt động kinh doanh, tăng trưởng doanh thu, lợi nhuận, biên lợi nhuận, dòng tiền, rủi ro tài chính, cơ cấu nợ, khả năng thanh khoản, tín nhiệm, vị thế ngành, hành vi nhà đầu tư nước ngoài, biến động giá cổ phiếu, tiềm năng phát triển, các điểm mạnh/yếu nổi bật.
    - Nếu có dữ liệu so sánh ngành, hãy so sánh vị thế doanh nghiệp với trung bình ngành.
    - Đưa ra nhận xét từng khía cạnh, giải thích ý nghĩa các chỉ số tài chính quan trọng.
    - Đưa ra cảnh báo nếu có rủi ro (lợi nhuận giảm, dòng tiền âm, nợ cao, giá biến động mạnh, tín nhiệm thấp...).
    - Kết luận cuối cùng: tổng hợp ưu nhược điểm, đánh giá triển vọng, và khuyến nghị cụ thể (nên mua, nên theo dõi, nên tránh, trung lập), giải thích lý do.
    - Nếu thiếu dữ liệu ở khía cạnh nào, hãy ghi rõ "Không đủ dữ liệu để đánh giá ...".
    - Văn phong chuyên nghiệp, dễ hiểu, không dùng từ ngữ quá kỹ thuật.

    GỢI Ý CẤU TRÚC NHẬN XÉT:
    1. Tổng quan hoạt động kinh doanh và tăng trưởng
    2. Phân tích lợi nhuận, biên lợi nhuận, dòng tiền
    3. Rủi ro tài chính, cơ cấu nợ, thanh khoản
    4. Vị thế ngành, so sánh ngành (nếu có)
    5. Tín nhiệm, hành vi nhà đầu tư nước ngoài, biến động giá cổ phiếu
    6. Tiềm năng phát triển, các điểm mạnh/yếu nổi bật
    7. Kết luận & khuyến nghị đầu tư (nên mua, nên theo dõi, nên tránh, trung lập) kèm lý do

    Ví dụ đoạn kết luận:
    "Tổng hợp các yếu tố trên, doanh nghiệp có nền tảng tài chính ổn định, tăng trưởng tốt, dòng tiền lành mạnh và vị thế ngành vững chắc. Giá cổ phiếu đang ở vùng hấp dẫn so với trung bình. Khuyến nghị: NÊN MUA cho nhà đầu tư trung-dài hạn. Tuy nhiên, cần theo dõi thêm các yếu tố vĩ mô và diễn biến ngành."
    "Nếu doanh nghiệp có rủi ro lớn: ... Khuyến nghị: NÊN TRÁNH do rủi ro tài chính và tăng trưởng kém."
    "Nếu dữ liệu chưa đủ: ... Khuyến nghị: TRUNG LẬP, cần theo dõi thêm."

    """
    if len(company_data) == 0:
        return {"summary": "Không có dữ liệu để phân tích doanh nghiệp."}

    latest = company_data.iloc[-1]
    latest_year = latest.get('NĂM', 2024)
    summary = ""
    revs = None
    profits = None
    strong_growth = False
    weak_growth = False
    strong_profit = False
    weak_profit = False
    foreign_buy = False
    price_low = False
    price_high = False
    # Đánh giá tăng trưởng doanh thu/lợi nhuận nếu có tối thiểu 2 năm
    if revs is not None and len(revs) == 2:
        rev_growth = (revs.iloc[-1] - revs.iloc[0]) / abs(revs.iloc[0]) if revs.iloc[0] != 0 else 0
        summary += f"- Tăng trưởng doanh thu năm nay so với năm trước: {rev_growth*100:.1f}%. {'Tích cực' if rev_growth > 0 else 'Suy giảm'}. "
    elif revs is not None and len(revs) > 2:
        rev_growth = (revs.iloc[-1] - revs.iloc[0]) / abs(revs.iloc[0]) if revs.iloc[0] != 0 else 0
        summary += f"- Tăng trưởng doanh thu {rev_growth*100:.1f}% trong {len(revs)} năm gần nhất. {'Tích cực' if rev_growth > 0 else 'Suy giảm'}. "
    # Lợi nhuận
    if profits is not None and len(profits) == 2:
        profit_growth = (profits.iloc[-1] - profits.iloc[0]) / abs(profits.iloc[0]) if profits.iloc[0] != 0 else 0
        summary += f"Lợi nhuận sau thuế năm nay so với năm trước: {profit_growth*100:.1f}%. {'Tích cực' if profit_growth > 0 else 'Cần chú ý xu hướng giảm'}. "
    elif profits is not None and len(profits) > 2:
        profit_growth = (profits.iloc[-1] - profits.iloc[0]) / abs(profits.iloc[0]) if profits.iloc[0] != 0 else 0
        summary += f"Lợi nhuận sau thuế tăng trưởng {profit_growth*100:.1f}% trong {len(profits)} năm. {'Tích cực' if profit_growth > 0 else 'Cần chú ý xu hướng giảm'}. "
    # Nếu không đủ dữ liệu tăng trưởng, đánh giá bằng hiệu suất tài chính
    if ((revs is None or len(revs) < 2) and (profits is None or len(profits) < 2)):
        # Lấy các chỉ số hiệu suất tài chính từ latest
        perf = []
        if 'ROA' in latest and pd.notna(latest['ROA']):
            perf.append(f"ROA {latest['ROA']*100:.2f}%")
        if 'ROE' in latest and pd.notna(latest['ROE']):
            perf.append(f"ROE {latest['ROE']*100:.2f}%")
        if 'KQKD. LỢI NHUẬN GỘP VỀ BÁN HÀNG VÀ CUNG CẤP DỊCH VỤ' in latest and 'KQKD. DOANH THU THUẦN' in latest and pd.notna(latest['KQKD. LỢI NHUẬN GỘP VỀ BÁN HÀNG VÀ CUNG CẤP DỊCH VỤ']) and pd.notna(latest['KQKD. DOANH THU THUẦN']):
            gross_margin = latest['KQKD. LỢI NHUẬN GỘP VỀ BÁN HÀNG VÀ CUNG CẤP DỊCH VỤ'] / latest['KQKD. DOANH THU THUẦN']
            perf.append(f"Biên lợi nhuận gộp {gross_margin*100:.2f}%")
        if 'KQKD. LỢI NHUẬN SAU THUẾ THU NHẬP DOANH NGHIỆP' in latest and 'KQKD. DOANH THU THUẦN' in latest and pd.notna(latest['KQKD. LỢI NHUẬN SAU THUẾ THU NHẬP DOANH NGHIỆP']) and pd.notna(latest['KQKD. DOANH THU THUẦN']):
            net_margin = latest['KQKD. LỢI NHUẬN SAU THUẾ THU NHẬP DOANH NGHIỆP'] / latest['KQKD. DOANH THU THUẦN']
            perf.append(f"Biên lợi nhuận ròng {net_margin*100:.2f}%")
        if perf:
            summary += "- Đánh giá hiệu suất tài chính: " + ", ".join(perf) + ". "
        else:
            summary += "- Không đủ dữ liệu để đánh giá tăng trưởng doanh thu, lợi nhuận hoặc hiệu suất tài chính. "
    if 'ROA' in latest and pd.notna(latest['ROA']):
        roa = latest['ROA']
        summary += f"ROA {roa*100:.2f}%, {'hiệu quả sử dụng tài sản tốt' if roa > 0.1 else 'mức chấp nhận được' if roa > 0 else 'cần chú ý hiệu quả hoạt động'}. "
    if 'DÒNG TIỀN / DOANH THU' in latest and pd.notna(latest['DÒNG TIỀN / DOANH THU']):
        cf_ratio = latest['DÒNG TIỀN / DOANH THU']
        summary += f"Dòng tiền kinh doanh {'mạnh' if cf_ratio > 0.1 else 'yếu hoặc âm'}, chiếm {cf_ratio*100:.1f}% doanh thu. "

    # 3. Rủi ro tài chính, cơ cấu nợ, thanh khoản
    if 'CURRENT RATIO' in latest and pd.notna(latest['CURRENT RATIO']):
        cr = latest['CURRENT RATIO']
        summary += f"Current Ratio ({cr:.2f}x) {'an toàn' if 1 <= cr <= 3 else 'dư thừa vốn lưu động' if cr > 3 else 'rủi ro thanh khoản'}. "
    if 'NỢ / TỔNG TÀI SẢN' in latest and pd.notna(latest['NỢ / TỔNG TÀI SẢN']):
        debt_ratio = latest['NỢ / TỔNG TÀI SẢN']
        summary += f"Tỷ lệ nợ ({debt_ratio*100:.1f}%) {'thấp, cấu trúc tài chính an toàn' if debt_ratio <= 0.5 else 'trung bình' if debt_ratio <= 0.7 else 'rất cao, rủi ro tài chính lớn'}. "


    # 4. Vị thế ngành, so sánh ngành (nếu có)
    industry_compare = ""
    if data_dict and 'industry' in data_dict and company_code in data_dict['industry'].index:
        industry_rank = data_dict['industry'].loc[company_code, 'XẾP HẠNG NGÀNH']
        industry_row = data_dict['industry'].loc[company_code]
        compare_fields = [
            ('ROA', 'ROA (TTM)'),
            ('ROE', 'ROE (TTM)'),
            ('NỢ / VỐN CHỦ SỞ HỮU', 'Nợ / Vốn chủ sở hữu'),
            ('TỶ LỆ VỐN CHỦ SỞ HỮU', 'Tỷ lệ vốn chủ sở hữu'),
            ('TĂNG TRƯỞNG LNST', 'Tăng trưởng LNST'),
            ('EBIT/TỔNG TÀI SẢN', 'EBIT/Tổng tài sản'),
            ('KHẢ NĂNG THANH TOÁN LÃI VAY', 'Khả năng thanh toán lãi vay'),
            ('TĂNG TRƯỞNG DOANH THU', 'Tăng trưởng doanh thu'),
            ('LỢI NHUẬN BIÊN', 'Lợi nhuận biên'),
            ('CASH RATIO', 'Cash Ratio'),
            ('DÒNG TIỀN / DOANH THU', 'Dòng tiền / Doanh thu'),
            ('TĂNG TRƯỞNG TÀI SẢN', 'Tăng trưởng tài sản'),
        ]
        better = []
        worse = []
        for col, label in compare_fields:
            val = latest.get(label)
            ind = industry_row.get(f"Ngành: {label}")
            if val is not None and ind is not None and pd.notna(val) and pd.notna(ind):
                if col in ['NỢ / VỐN CHỦ SỞ HỮU']:
                    if val < ind:
                        better.append(label)
                    else:
                        worse.append(label)
                else:
                    if val > ind:
                        better.append(label)
                    else:
                        worse.append(label)
        summary += f"\nSo sánh với ngành: Xếp hạng vị thế {industry_rank} trong ngành. "
        if better:
            summary += f"Các chỉ số vượt trội ngành: {', '.join(better)}. "
        if worse:
            summary += f"Các chỉ số thấp hơn ngành: {', '.join(worse)}. "
        # Tổng kết vị thế
        if len(better) > len(worse):
            summary += "\nTổng thể: Doanh nghiệp có nhiều chỉ số vượt trội ngành, vị thế tốt trong ngành. "
        elif len(worse) > len(better):
            summary += "\nTổng thể: Nhiều chỉ số còn thấp hơn ngành, vị thế cần cải thiện hoặc chú ý. "
        else:
            summary += "\nTổng thể: Vị thế doanh nghiệp tương đương trung bình ngành. "
    else:
        summary += "\nKhông đủ dữ liệu để đánh giá vị thế ngành. "

    # 5. Tín nhiệm, hành vi nhà đầu tư nước ngoài, biến động giá cổ phiếu
    credit_rating = latest.get('Credit_Rating', 'N/A')
    if credit_rating and credit_rating != 'N/A':
        summary += f"Tín nhiệm {credit_rating}, {'độ tin cậy cao' if credit_rating in ['AAA','AA'] else 'mức tốt' if credit_rating=='A' else 'cần theo dõi'}. "
    if foreign_data is not None and len(foreign_data) > 0:
        foreign_filtered = foreign_data[foreign_data['Mã'] == company_code] if 'Mã' in foreign_data.columns else pd.DataFrame()
        if len(foreign_filtered) > 0:
            recent_foreign = foreign_filtered.tail(30)
            if 'Net.F_Val' in recent_foreign.columns:
                net_flow = recent_foreign['Net.F_Val'].sum()
                summary += f"Dòng tiền nước ngoài ròng {'dương' if net_flow > 0 else 'âm'} ({net_flow:,.0f} tỷ VND/30 ngày). "
    if price_data is not None and len(price_data) > 0:
        price_filtered = price_data[price_data['Mã'] == company_code] if 'Mã' in price_data.columns else pd.DataFrame()
        if len(price_filtered) > 0:
            latest_price = price_filtered.iloc[-1]['Giá'] if 'Giá' in price_filtered.columns else None
            ma_50 = price_filtered['Giá'].tail(50).mean() if len(price_filtered) >= 50 else None
            if pd.notna(latest_price) and pd.notna(ma_50):
                if latest_price > ma_50 * 1.1:
                    summary += f"Giá cổ phiếu hiện tại ({latest_price:,.0f}) cao hơn MA50 ({ma_50:,.0f}), có thể đang ở vùng quá mua. "
                elif latest_price < ma_50 * 0.9:
                    summary += f"Giá cổ phiếu hiện tại ({latest_price:,.0f}) thấp hơn MA50 ({ma_50:,.0f}), có thể là cơ hội mua nếu cơ bản tốt. "
                else:
                    summary += f"Giá cổ phiếu quanh MA50, vùng cân bằng. "

    # 6. Tiềm năng phát triển, điểm mạnh/yếu nổi bật (giản lược, vì không có dữ liệu định tính)
    # Nếu có dữ liệu định tính, có thể bổ sung thêm ở đây

    # 7. Kết luận & khuyến nghị đầu tư (chỉ trả về advice, không nối lại các chỉ số)
    try:
        # Ưu tiên tín nhiệm AAA
        if credit_rating == 'AAA':
            advice = "KHUYẾN NGHỊ: NÊN ĐẦU TƯ. Doanh nghiệp có tín nhiệm AAA, nền tảng tài chính rất vững chắc, rủi ro thấp, phù hợp cho đầu tư dài hạn."
        elif strong_growth and strong_profit and foreign_buy and price_low:
            advice = "NÊN MUA hoặc tích lũy nếu khẩu vị rủi ro phù hợp. Doanh nghiệp tăng trưởng tốt, dòng tiền nước ngoài tích cực và giá đang ở vùng hấp dẫn."
        elif weak_growth or weak_profit:
            advice = "NÊN TRÁNH hoặc bán ra, do doanh thu/lợi nhuận yếu hoặc suy giảm rõ rệt."
        elif price_high:
            advice = "THEO DÕI, giá cổ phiếu đang cao hơn trung bình, nên chờ nhịp điều chỉnh hoặc tích lũy thêm thông tin."
        else:
            advice = "TRUNG LẬP, nên theo dõi thêm các yếu tố vĩ mô, ngành và diễn biến thị trường."
    except Exception:
        advice = "TRUNG LẬP, nên theo dõi thêm các yếu tố vĩ mô, ngành và diễn biến thị trường."
    return {"summary": summary.strip(), "advice": advice}

    # 4. Quản trị & rủi ro (nếu có dữ liệu)
    if 'ROA' in latest and pd.notna(latest['ROA']):
        roa = latest['ROA']
        if roa > 0.1:
            summary += f"ROA {roa*100:.2f}%, hiệu quả sử dụng tài sản tốt. "
        elif roa > 0:
            summary += f"ROA {roa*100:.2f}%, mức chấp nhận được. "
        else:
            summary += f"ROA âm ({roa*100:.2f}%), cần chú ý hiệu quả hoạt động. "

    # 5. Tỷ lệ nợ, thanh khoản
    if 'CURRENT RATIO' in latest and pd.notna(latest['CURRENT RATIO']):
        cr = latest['CURRENT RATIO']
        if cr < 1:
            summary += f"⚠️ Current Ratio ({cr:.2f}x) dưới 1, rủi ro thanh khoản. "
        elif cr > 3:
            summary += f"Current Ratio ({cr:.2f}x) cao, vốn lưu động dư thừa. "
        else:
            summary += f"Current Ratio ({cr:.2f}x) an toàn. "
    if 'NỢ / TỔNG TÀI SẢN' in latest and pd.notna(latest['NỢ / TỔNG TÀI SẢN']):
        debt_ratio = latest['NỢ / TỔNG TÀI SẢN']
        if debt_ratio > 0.7:
            summary += f"⚠️ Tỷ lệ nợ ({debt_ratio*100:.1f}%) rất cao. "
        elif debt_ratio > 0.5:
            summary += f"Tỷ lệ nợ ({debt_ratio*100:.1f}%) trung bình. "
        else:
            summary += f"Tỷ lệ nợ ({debt_ratio*100:.1f}%) thấp. "

    # 6. Dòng tiền
    if 'DÒNG TIỀN / DOANH THU' in latest and pd.notna(latest['DÒNG TIỀN / DOANH THU']):
        cf_ratio = latest['DÒNG TIỀN / DOANH THU']
        if cf_ratio > 0.1:
            summary += f"Dòng tiền kinh doanh mạnh ({cf_ratio*100:.1f}% doanh thu). "
        elif cf_ratio <= 0:
            summary += f"⚠️ Dòng tiền kinh doanh âm hoặc yếu. "

    # 7. Tín nhiệm
    credit_rating = latest.get('Credit_Rating', 'N/A')
    if credit_rating and credit_rating != 'N/A':
        if credit_rating in ['AAA', 'AA']:
            summary += f"Tín nhiệm {credit_rating}, độ tin cậy cao. "
        elif credit_rating in ['A']:
            summary += f"Tín nhiệm {credit_rating}, mức tốt. "
        else:
            summary += f"⚠️ Tín nhiệm {credit_rating}, cần theo dõi. "

    # 8. Giá cổ phiếu và dòng tiền nước ngoài
    investor_analysis = ""
    if foreign_data is not None and len(foreign_data) > 0:
        foreign_filtered = foreign_data[foreign_data['Mã'] == company_code] if 'Mã' in foreign_data.columns else pd.DataFrame()
        if len(foreign_filtered) > 0:
            recent_foreign = foreign_filtered.tail(30)
            if 'Net.F_Val' in recent_foreign.columns:
                net_flow = recent_foreign['Net.F_Val'].sum()
                if net_flow > 0:
                    investor_analysis += f"Dòng tiền nước ngoài ròng dương ({net_flow:,.0f} tỷ VND/30 ngày). "
                    foreign_buy = True
                else:
                    investor_analysis += f"Dòng tiền nước ngoài ròng âm ({net_flow:,.0f} tỷ VND/30 ngày). "
                    foreign_buy = False
    if price_data is not None and len(price_data) > 0:
        price_filtered = price_data[price_data['Mã'] == company_code] if 'Mã' in price_data.columns else pd.DataFrame()
        if len(price_filtered) > 0:
            latest_price = price_filtered.iloc[-1]['Giá'] if 'Giá' in price_filtered.columns else None
            ma_50 = price_filtered['Giá'].tail(50).mean() if len(price_filtered) >= 50 else None
            if pd.notna(latest_price) and pd.notna(ma_50):
                if latest_price > ma_50 * 1.1:
                    investor_analysis += f" Giá hiện tại ({latest_price:,.0f}) cao hơn MA50 ({ma_50:,.0f}), có thể quá mua."
                    price_high = True
                elif latest_price < ma_50 * 0.9:
                    investor_analysis += f" Giá hiện tại ({latest_price:,.0f}) thấp hơn MA50 ({ma_50:,.0f}), có thể là cơ hội mua nếu cơ bản tốt."
                    price_low = True
                else:
                    investor_analysis += f" Giá quanh MA50, vùng cân bằng."
                    price_neutral = True
    if investor_analysis:
        summary += " " + investor_analysis

    # Đưa ra khuyến nghị cụ thể
    # Ưu tiên: mạnh toàn diện => nên mua; yếu rõ rệt => nên tránh; trung bình => theo dõi; còn lại => trung lập
    try:
        if ('strong_growth' in locals() and strong_growth) and ('strong_profit' in locals() and strong_profit) and ('foreign_buy' in locals() and foreign_buy) and ('price_low' in locals() and price_low):
            advice = "Khuyến nghị: NÊN MUA hoặc tích lũy nếu khẩu vị rủi ro phù hợp. Doanh nghiệp tăng trưởng tốt, dòng tiền nước ngoài tích cực và giá đang ở vùng hấp dẫn."
        elif ('weak_growth' in locals() and weak_growth) or ('weak_profit' in locals() and weak_profit):
            advice = "Khuyến nghị: NÊN TRÁNH hoặc bán ra, do doanh thu/lợi nhuận yếu hoặc suy giảm rõ rệt."
        elif ('price_high' in locals() and price_high):
            advice = "Khuyến nghị: THEO DÕI, giá cổ phiếu đang cao hơn trung bình, nên chờ nhịp điều chỉnh hoặc tích lũy thêm thông tin."
        else:
            advice = "Khuyến nghị: TRUNG LẬP, nên theo dõi thêm các yếu tố vĩ mô, ngành và diễn biến thị trường."
    except Exception:
        advice = "Khuyến nghị: TRUNG LẬP, nên theo dõi thêm các yếu tố vĩ mô, ngành và diễn biến thị trường."

    return {"summary": summary.strip(), "advice": advice}

def format_currency(value, unit="tỷ VND"):
    """Định dạng tiền tệ"""
    if pd.isna(value):
        return "N/A"
    if abs(value) >= 1000:
        return f"{value/1000:.2f} nghìn {unit}"
    return f"{value:.2f} {unit}"

def format_percentage(value, decimals=2):
    """Định dạng phần trăm"""
    if pd.isna(value):
        return "N/A"
    return f"{value*100:.{decimals}f}%"

# ============================================================================
# HEADER - NAVIGATION & SEARCH
# ============================================================================
st.markdown("""
<div style="background: linear-gradient(90deg, #06b6d4 0%, #0891b2 100%); padding: 15px 30px; border-radius: 10px; margin-bottom: 20px;">
    <h1 style="color: #020617; margin: 0; font-size: 28px; font-weight: 900; text-align: center;">PHÂN TÍCH CHI TIẾT DOANH NGHIỆP</h1>
    <p style="color: #0c4a6e; margin: 5px 0 0 0; font-size: 16px; text-align: center; font-style: italic; text-transform: none;">Tổng hợp, trực quan hóa cấu trúc tài chính và hiệu quả hoạt động của doanh nghiệp</p>
</div>
""", unsafe_allow_html=True)


# Tìm kiếm và chọn công ty + năm
col_search1, col_search2, col_search3, col_search4 = st.columns([3, 2, 2, 1])

with col_search1:
    search_query = st.text_input(
        "Tìm kiếm mã cổ phiếu",
        placeholder="VD: VCB, VIC, HPG, FPT...",
        key="company_search"
    )

with col_search2:
    companies_list = sorted(data['health']['MÃ'].unique().tolist())
    selected_company = st.selectbox(
        "Chọn mã cổ phiếu",
        options=companies_list,
        index=0 if len(companies_list) > 0 else None,
        key="company_select"
    )


# Lấy các năm tương ứng với mã đã chọn
ds_nam = []
if selected_company:
    ds_nam = sorted(data['health'][data['health']['MÃ'] == selected_company]['NĂM'].unique().tolist())

with col_search3:
    selected_year = st.selectbox(
        "Chọn năm tài chính",
        options=ds_nam,
        index=len(ds_nam)-1 if len(ds_nam) > 0 else 0,
        key="year_select"
    )

with col_search4:
    st.write("")  # Spacer
    st.write("")  # Spacer
    if st.button("Tìm", use_container_width=True):
        st.session_state['search'] = search_query

# Áp dụng tìm kiếm
if search_query:
    mask = (
        data['health']['MÃ'].str.contains(search_query.upper(), case=False, na=False) |
        data['health']['TÊN CÔNG TY'].str.contains(search_query, case=False, na=False)
    )
    matching = data['health'][mask]['MÃ'].unique()
    if len(matching) > 0:
        selected_company = matching[0]
        years_list = sorted(data['health'][data['health']['MÃ'] == selected_company]['NĂM'].unique().tolist())
        selected_year = years_list[-1] if len(years_list) > 0 else None

if not selected_company or not selected_year:
    st.warning("Vui lòng chọn một mã cổ phiếu và năm tài chính để xem phân tích.")
    st.stop()

# Lọc dữ liệu theo công ty và năm đã chọn
company_data = data['health'][(data['health']['MÃ'] == selected_company)].copy().sort_values('NĂM')
company_year_data = company_data[company_data['NĂM'] == selected_year]
if len(company_year_data) == 0:
    st.error(f"❌ Không tìm thấy dữ liệu cho mã {selected_company} năm {selected_year}")
    st.stop()

# Lấy dữ liệu giá, volume, marketcap, foreign flow theo năm
price_company = None
volume_company = None
marketcap_company = None
foreign_company = None

if data.get('price') is not None:
    if 'Mã' in data['price'].columns:
        price_company = data['price'][(data['price']['Mã'] == selected_company)].copy()
        price_company = price_company.sort_values('Ngày')
        # Lọc theo năm
        price_company = price_company[price_company['Ngày'].dt.year == selected_year]

if data.get('volume') is not None:
    if 'Mã' in data['volume'].columns:
        volume_company = data['volume'][(data['volume']['Mã'] == selected_company)].copy()
        volume_company = volume_company.sort_values('Ngày')
        volume_company = volume_company[volume_company['Ngày'].dt.year == selected_year]

if data.get('marketcap') is not None:
    if 'Mã' in data['marketcap'].columns:
        marketcap_company = data['marketcap'][(data['marketcap']['Mã'] == selected_company)].copy()
        marketcap_company = marketcap_company.sort_values('Ngày')
        marketcap_company = marketcap_company[marketcap_company['Ngày'].dt.year == selected_year]

if data.get('foreign') is not None:
    if 'Mã' in data['foreign'].columns:
        foreign_company = data['foreign'][(data['foreign']['Mã'] == selected_company)].copy()
        foreign_company = foreign_company.sort_values('Ngày')
        foreign_company = foreign_company[foreign_company['Ngày'].dt.year == selected_year]

# Lấy thông tin công ty theo năm
latest_company = company_year_data.iloc[-1]
company_name = latest_company.get('TÊN CÔNG TY', selected_company)
company_nganh = latest_company.get('NGÀNH', 'N/A')
company_year = latest_company.get('NĂM', selected_year)
credit_rating = latest_company.get('Credit_Rating', 'N/A')
financial_health = latest_company.get('financial_health', 'N/A')

# ============================================================================
# COMPANY INFO CARD
# ============================================================================
st.markdown(f"""
<div class="company-info-card">
    <div class="company-name">
        <span class="company-code">{selected_company}</span>
        {company_name}
    </div>
    <div style="margin-top: 15px;">
        <span class="company-tag">{company_nganh}</span>
        <span class="company-tag">Năm: {company_year}</span>
        <span class="company-tag" style="border-color: {'#10b981' if credit_rating in ['AAA','AA'] else '#fbbf24' if credit_rating == 'A' else '#ef4444'};">
            Tín nhiệm: {credit_rating}
        </span>
        <span class="company-tag" style="border-color: {'#10b981' if financial_health == 'Tốt' else '#fbbf24' if financial_health == 'Khá' else '#ef4444'};">
            Sức khỏe: {financial_health}
        </span>
    </div>
    <!-- Thêm ô tín nhiệm với nhận xét -->
    <div class="health-score-container" style="margin-top: 18px;">
        <div class="health-score-label" style="font-size:18px;">Tín nhiệm: <span class="rating-{credit_rating.lower() if credit_rating else 'na'}">{credit_rating}</span></div>
        <div style="color: #94a3b8; font-size: 12px; margin-top: 5px;">
            {('AAA – Tốt: Sinh lời rất cao, đòn bẩy thấp, thanh khoản và khả năng trả lãi vượt trội → doanh nghiệp đầu ngành, rủi ro thấp.' if credit_rating == 'AAA' else
              'AA – Khá: Cơ cấu vốn an toàn, thanh khoản tốt nhưng sinh lời chưa nổi bật → doanh nghiệp phòng thủ, ổn định.' if credit_rating == 'AA' else
              'A – Trung bình: Sinh lời và tăng trưởng ở mức vừa, nợ trung bình → doanh nghiệp hoạt động bình thường.' if credit_rating == 'A' else
              'BBB – Trung bình: Hiệu quả vận hành có nhưng đòn bẩy cao hơn → nhạy cảm với chu kỳ kinh tế.' if credit_rating == 'BBB' else
              'BB – Yếu: Tăng trưởng cao nhưng dòng tiền yếu, rủi ro tài chính lớn → đầu tư mạo hiểm.' if credit_rating == 'BB' else
              'B – Yếu: Sinh lời thấp, nợ cao, khả năng trả lãi kém → rủi ro cao, không an toàn.' if credit_rating == 'B' else
              'Chưa có xếp hạng tín nhiệm.')}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# KEY METRICS & HEALTH SCORE - HÀNG 1
# ============================================================================
col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns([2, 2, 2, 2, 2])

# Tính toán các chỉ số
latest_roa = latest_company.get('ROA')
latest_roe = latest_company.get('ROE')
latest_cr = latest_company.get('CURRENT RATIO')
latest_debt = latest_company.get('NỢ / TỔNG TÀI SẢN')

# Tính thay đổi so với năm trước
prev_year_data = company_data[company_data['NĂM'] == company_year - 1]
roa_change = None
roe_change = None
cr_change = None

if len(prev_year_data) > 0:
    prev_roa = prev_year_data.iloc[0].get('ROA')
    prev_roe = prev_year_data.iloc[0].get('ROE')
    prev_cr = prev_year_data.iloc[0].get('CURRENT RATIO')
    
    if pd.notna(latest_roa) and pd.notna(prev_roa):
        roa_change = (latest_roa - prev_roa) * 100
    if pd.notna(latest_roe) and pd.notna(prev_roe):
        roe_change = (latest_roe - prev_roe) * 100
    if pd.notna(latest_cr) and pd.notna(prev_cr):
        cr_change = latest_cr - prev_cr

# Market Cap và giá
latest_marketcap = None
latest_price = None
price_change_pct = None

if marketcap_company is not None and len(marketcap_company) > 0:
    latest_marketcap = marketcap_company.iloc[-1].get('MarketCap')

if price_company is not None and len(price_company) > 0:
    latest_price = price_company.iloc[-1].get('Giá')
    if len(price_company) > 1:
        prev_price = price_company.iloc[-2].get('Giá')
        if pd.notna(latest_price) and pd.notna(prev_price):
            price_change_pct = ((latest_price - prev_price) / prev_price) * 100

# Volume
latest_volume = None
if volume_company is not None and len(volume_company) > 0:
    latest_volume = volume_company.iloc[-1].get('Khối lượng')


# 1. Vốn hóa thị trường (tỷ VND, ngắn gọn)
with col_m1:
    marketcap_tyvnd = latest_marketcap / 1e9 if latest_marketcap else None
    st.metric(
        label="Vốn hóa thị trường",
        value=f"{marketcap_tyvnd:,.2f} tỷ" if marketcap_tyvnd else "N/A",
        help="Tổng giá trị vốn hóa thị trường (tỷ VND)"
    )

# 2. Giá cổ phiếu thấp nhất trong năm
min_price = None
if price_company is not None and len(price_company) > 0:
    min_price = price_company['Giá'].min()
with col_m2:
    st.metric(
        label="Giá thấp nhất năm",
        value=f"{min_price:,.0f}" if pd.notna(min_price) else "N/A",
        help="Giá cổ phiếu thấp nhất trong năm"
    )

# 3. Khối lượng giao dịch
with col_m3:
    st.metric(
        label="Khối lượng",
        value=f"{latest_volume:,.0f}" if pd.notna(latest_volume) else "N/A",
        help="Khối lượng giao dịch"
    )

# 4. Giá cổ phiếu cao nhất trong năm
max_price = None
if price_company is not None and len(price_company) > 0:
    max_price = price_company['Giá'].max()
with col_m4:
    st.metric(
        label="Giá cao nhất năm",
        value=f"{max_price:,.0f}" if pd.notna(max_price) else "N/A",
        help="Giá cổ phiếu cao nhất trong năm"
    )


# Xếp hạng tín nhiệm + nhận xét

# 5. Trạng thái dòng tiền đầu tư nước ngoài trong năm
with col_m5:
    foreign_status = "Không có dữ liệu"
    if foreign_company is not None and len(foreign_company) > 0 and 'Net.F_Val' in foreign_company.columns:
        net_flow_year = foreign_company['Net.F_Val'].sum()
        if net_flow_year > 0:
            foreign_status = f"Dòng tiền nước ngoài: TÍCH CỰC (+{net_flow_year/1e9:.2f} tỷ VND)"
        elif net_flow_year < 0:
            foreign_status = f"Dòng tiền nước ngoài: TIÊU CỰC ({net_flow_year/1e9:.2f} tỷ VND)"
        else:
            foreign_status = "Dòng tiền nước ngoài: TRUNG LẬP (0 tỷ VND)"
    st.markdown(f"""
    <div class="health-score-container">
        <div class="health-score-label" style="font-size:18px;">{foreign_status}</div>
        <div style="color: #94a3b8; font-size: 12px; margin-top: 5px;">Trạng thái dòng tiền đầu tư nước ngoài trong năm</div>
    </div>
    """, unsafe_allow_html=True)



# 6. Xếp hạng tín nhiệm và nhận xét

# ============================================================================
# PERFORMANCE INDICATORS - HÀNG 2
# ============================================================================
st.markdown("---")
st.subheader("Chỉ Số Hiệu Suất Tài Chính (TTM)")

col_p1, col_p2, col_p3, col_p4 = st.columns(4)

with col_p1:
    st.metric(
        label="ROA (TTM)",
        value=format_percentage(latest_roa) if pd.notna(latest_roa) else "N/A",
        delta=f"{roa_change:+.2f}%" if pd.notna(roa_change) else None,
        delta_color="normal" if (roa_change is None or roa_change >= 0) else "inverse",
        help="Tỷ suất sinh lời trên tài sản"
    )

with col_p2:
    st.metric(
        label="ROE (TTM)",
        value=format_percentage(latest_roe) if pd.notna(latest_roe) else "N/A",
        delta=f"{roe_change:+.2f}%" if pd.notna(roe_change) else None,
        delta_color="normal" if (roe_change is None or roe_change >= 0) else "inverse",
        help="Tỷ suất sinh lời trên vốn chủ sở hữu"
    )



# Lấy dữ liệu các chỉ tiêu bổ sung và tính sự thay đổi qua các năm
def get_latest_and_delta(key):
    latest = latest_company.get(key)
    prev = None
    if len(prev_year_data) > 0:
        prev = prev_year_data.iloc[0].get(key)
    delta = None
    if pd.notna(latest) and pd.notna(prev):
        delta = (latest - prev) * 100 if abs(latest) < 10 else (latest - prev)
    return latest, delta

latest_cr, cr_change = get_latest_and_delta('CURRENT RATIO')
latest_margin, margin_change = get_latest_and_delta('LỢI NHUẬN BIÊN')
latest_debt_equity, debt_equity_change = get_latest_and_delta('NỢ / VỐN CHỦ SỞ HỮU')
latest_ebit_assets, ebit_assets_change = get_latest_and_delta('EBIT/TỔNG TÀI SẢN')
latest_cash_ratio, cash_ratio_change = get_latest_and_delta('CASH RATIO')
latest_equity_ratio, equity_ratio_change = get_latest_and_delta('TỶ LỆ VỐN CHỦ SỞ HỮU')
latest_interest_coverage, interest_coverage_change = get_latest_and_delta('KHẢ NĂNG THANH TOÁN LÃI VAY')
latest_cashflow_sales, cashflow_sales_change = get_latest_and_delta('DÒNG TIỀN / DOANH THU')
latest_net_income_growth, net_income_growth_change = get_latest_and_delta('TĂNG TRƯỞNG LNST')
latest_revenue_growth, revenue_growth_change = get_latest_and_delta('TĂNG TRƯỞNG DOANH THU')
latest_asset_growth, asset_growth_change = get_latest_and_delta('TĂNG TRƯỞNG TÀI SẢN')


# Dàn đều các chỉ tiêu bổ sung vào 4 cột


# Danh sách chỉ tiêu giữ lại, có tính delta
supplement_metrics = [
    ("Current Ratio (Tỷ số thanh khoản hiện tại)", f"{latest_cr:.2f}" if pd.notna(latest_cr) else "N/A", f"{cr_change:+.2f}" if pd.notna(cr_change) else None, "Tỷ số thanh khoản hiện tại"),
    ("Lợi nhuận biên (Net Profit Margin)", format_percentage(latest_margin) if pd.notna(latest_margin) else "N/A", f"{margin_change:+.2f}%" if pd.notna(margin_change) else None, "Tỷ suất lợi nhuận ròng trên doanh thu"),
    ("Nợ / Vốn chủ sở hữu (Debt/Equity)", format_percentage(latest_debt_equity) if pd.notna(latest_debt_equity) else "N/A", f"{debt_equity_change:+.2f}%" if pd.notna(debt_equity_change) else None, "Tỷ lệ nợ trên vốn chủ sở hữu"),
    ("EBIT/Tổng tài sản (EBIT/Total Assets)", format_percentage(latest_ebit_assets) if pd.notna(latest_ebit_assets) else "N/A", f"{ebit_assets_change:+.2f}%" if pd.notna(ebit_assets_change) else None, "Tỷ suất EBIT trên tổng tài sản"),
    ("Cash Ratio (Tỷ số tiền mặt)", f"{latest_cash_ratio:.2f}" if pd.notna(latest_cash_ratio) else "N/A", f"{cash_ratio_change:+.2f}" if pd.notna(cash_ratio_change) else None, "Tỷ số tiền mặt"),
    ("Tỷ lệ vốn chủ sở hữu (Equity Ratio)", format_percentage(latest_equity_ratio) if pd.notna(latest_equity_ratio) else "N/A", f"{equity_ratio_change:+.2f}%" if pd.notna(equity_ratio_change) else None, "Tỷ lệ vốn chủ sở hữu"),
    ("Khả năng thanh toán lãi vay (Interest Coverage)", f"{latest_interest_coverage:.2f}" if pd.notna(latest_interest_coverage) else "N/A", f"{interest_coverage_change:+.2f}" if pd.notna(interest_coverage_change) else None, "Khả năng thanh toán lãi vay"),
    ("Dòng tiền / Doanh thu (Operating Cash Flow/Sales)", format_percentage(latest_cashflow_sales) if pd.notna(latest_cashflow_sales) else "N/A", f"{cashflow_sales_change:+.2f}%" if pd.notna(cashflow_sales_change) else None, "Tỷ lệ dòng tiền hoạt động trên doanh thu"),
    ("Tăng trưởng LNST (Net Income Growth)", format_percentage(latest_net_income_growth) if pd.notna(latest_net_income_growth) else "N/A", f"{net_income_growth_change:+.2f}%" if pd.notna(net_income_growth_change) else None, "Tăng trưởng lợi nhuận sau thuế"),
    ("Tăng trưởng doanh thu (Revenue Growth)", format_percentage(latest_revenue_growth) if pd.notna(latest_revenue_growth) else "N/A", f"{revenue_growth_change:+.2f}%" if pd.notna(revenue_growth_change) else None, "Tăng trưởng doanh thu"),
    ("Tăng trưởng tài sản (Asset Growth)", format_percentage(latest_asset_growth) if pd.notna(latest_asset_growth) else "N/A", f"{asset_growth_change:+.2f}%" if pd.notna(asset_growth_change) else None, "Tăng trưởng tổng tài sản"),
]

cols = [col_p1, col_p2, col_p3, col_p4]
for idx, (label, value, delta, helptext) in enumerate(supplement_metrics):
    with cols[idx % 4]:
        st.metric(label=label, value=value, delta=delta, delta_color="normal" if (delta is None or (isinstance(delta, str) and not delta.startswith('-'))) else "inverse", help=helptext)

with col_p4:
    debt_status = "Ổn định"
    if pd.notna(latest_debt):
        if latest_debt > 0.7:
            debt_status = "Cao"
        elif latest_debt < 0.3:
            debt_status = "Thấp"
    st.metric(
        label="Nợ / Tổng tài sản",
        value=format_percentage(latest_debt) if pd.notna(latest_debt) else "N/A",
        delta=debt_status,
        help="Tỷ lệ nợ trên tổng tài sản"
    )


# ============================================================================
# SO SÁNH VỚI TRUNG BÌNH NGÀNH
# ============================================================================
st.markdown("---")
st.subheader("So Sánh Với Trung Bình Ngành")

# Lọc dữ liệu ngành
industry = latest_company.get('NGÀNH', None)
if industry:
    industry_data = data['health'][(data['health']['NGÀNH'] == industry) & (data['health']['NĂM'] == company_year)]
    if len(industry_data) > 1:
        st.markdown(f"**Ngành:** {industry}")
        compare_metrics = [
            ("ROA", "ROA (TTM)", latest_company.get('ROA'), industry_data['ROA'].mean()),
            ("ROE", "ROE (TTM)", latest_company.get('ROE'), industry_data['ROE'].mean()),
            ("LỢI NHUẬN BIÊN", "Lợi nhuận biên", latest_company.get('LỢI NHUẬN BIÊN'), industry_data['LỢI NHUẬN BIÊN'].mean()),
            ("NỢ / VỐN CHỦ SỞ HỮU", "Nợ / Vốn chủ sở hữu", latest_company.get('NỢ / VỐN CHỦ SỞ HỮU'), industry_data['NỢ / VỐN CHỦ SỞ HỮU'].mean()),
            ("EBIT/TỔNG TÀI SẢN", "EBIT/Tổng tài sản", latest_company.get('EBIT/TỔNG TÀI SẢN'), industry_data['EBIT/TỔNG TÀI SẢN'].mean()),
            ("CASH RATIO", "Cash Ratio", latest_company.get('CASH RATIO'), industry_data['CASH RATIO'].mean()),
            ("TỶ LỆ VỐN CHỦ SỞ HỮU", "Tỷ lệ vốn chủ sở hữu", latest_company.get('TỶ LỆ VỐN CHỦ SỞ HỮU'), industry_data['TỶ LỆ VỐN CHỦ SỞ HỮU'].mean()),
            ("KHẢ NĂNG THANH TOÁN LÃI VAY", "Khả năng thanh toán lãi vay", latest_company.get('KHẢ NĂNG THANH TOÁN LÃI VAY'), industry_data['KHẢ NĂNG THANH TOÁN LÃI VAY'].mean()),
            ("DÒNG TIỀN / DOANH THU", "Dòng tiền / Doanh thu", latest_company.get('DÒNG TIỀN / DOANH THU'), industry_data['DÒNG TIỀN / DOANH THU'].mean()),
            ("TĂNG TRƯỞNG LNST", "Tăng trưởng LNST", latest_company.get('TĂNG TRƯỞNG LNST'), industry_data['TĂNG TRƯỞNG LNST'].mean()),
            ("TĂNG TRƯỞNG DOANH THU", "Tăng trưởng doanh thu", latest_company.get('TĂNG TRƯỞNG DOANH THU'), industry_data['TĂNG TRƯỞNG DOANH THU'].mean()),
            ("TĂNG TRƯỞNG TÀI SẢN", "Tăng trưởng tài sản", latest_company.get('TĂNG TRƯỞNG TÀI SẢN'), industry_data['TĂNG TRƯỞNG TÀI SẢN'].mean()),
        ]
        compare_cols = st.columns(3)
        for idx, (key, label, val, avg) in enumerate(compare_metrics):
            with compare_cols[idx % 3]:
                st.metric(
                    label=label,
                    value=f"{val*100:.2f}%" if pd.notna(val) else "N/A",
                    delta=f"Ngành: {avg*100:.2f}%" if pd.notna(avg) else "N/A",
                    delta_color="normal" if (pd.isna(val) or pd.isna(avg) or val >= avg) else "inverse"
                )
    else:
        st.info("Không đủ dữ liệu để so sánh với ngành.")
else:
    st.info("Không xác định được ngành của doanh nghiệp.")

# ============================================================================
# BẢNG BÁO CÁO TÀI CHÍNH - DƯỚI CÙNG (CHỈ TIÊU TIÊU BIỂU)
# ============================================================================
st.markdown("---")
st.markdown("<h3 style='color:#22d3ee;'>Báo Cáo Tài Chính</h3>", unsafe_allow_html=True)

if data.get('bctc') is not None:
    bctc_company = data['bctc'][data['bctc']['MÃ'] == selected_company].copy()
    bctc_company = bctc_company.sort_values('NĂM')
    tabs = st.tabs(["Bảng Cân Đối", "Kết Quả KD", "Lưu Chuyển Tiền"])

    # 1. Bảng Cân Đối Kế Toán - chỉ tiêu tiêu biểu
    with tabs[0]:
        st.markdown("#### Bảng Cân Đối Kế Toán")
        cdkt_cols = [
            'CĐKT. TỔNG CỘNG TÀI SẢN',
            'CĐKT. TÀI SẢN NGẮN HẠN',
            'CĐKT. TIỀN VÀ TƯƠNG ĐƯƠNG TIỀN',
            'CĐKT. ĐẦU TƯ TÀI CHÍNH NGẮN HẠN',
            'CĐKT. CÁC KHOẢN PHẢI THU NGẮN HẠN',
            'CĐKT. HÀNG TỒN KHO, RÒNG',
            'CĐKT. TÀI SẢN DÀI HẠN',
            'CĐKT. NỢ PHẢI TRẢ',
            'CĐKT. VỐN CHỦ SỞ HỮU',
        ]
        show_cols = [col for col in cdkt_cols if col in bctc_company.columns]
        if show_cols:
            df_cdkt = bctc_company[['NĂM'] + show_cols].set_index('NĂM').T
            st.dataframe(df_cdkt, use_container_width=True)
        else:
            st.info("Không có dữ liệu Bảng Cân Đối.")

    # 2. Kết Quả Kinh Doanh - chỉ tiêu tiêu biểu
    with tabs[1]:
        st.markdown("#### Kết Quả Kinh Doanh")
        kqkd_cols = [
            'KQKD. DOANH THU BÁN HÀNG VÀ CUNG CẤP DỊCH VỤ',
            'KQKD. DOANH THU THUẦN',
            'KQKD. LỢI NHUẬN GỘP VỀ BÁN HÀNG VÀ CUNG CẤP DỊCH VỤ',
            'KQKD. DOANH THU HOẠT ĐỘNG TÀI CHÍNH',
            'KQKD. CHI PHÍ TÀI CHÍNH',
            'KQKD. LỢI NHUẬN SAU THUẾ THU NHẬP DOANH NGHIỆP',
            'KQKD. LÃI CƠ BẢN TRÊN CỔ PHIẾU',
        ]
        show_cols = [col for col in kqkd_cols if col in bctc_company.columns]
        if show_cols:
            df_kqkd = bctc_company[['NĂM'] + show_cols].set_index('NĂM').T
            st.dataframe(df_kqkd, use_container_width=True)
        else:
            st.info("Không có dữ liệu Kết Quả Kinh Doanh.")

    # 3. Lưu Chuyển Tiền Tệ - chỉ tiêu tiêu biểu
    with tabs[2]:
        st.markdown("#### Lưu Chuyển Tiền Tệ")
        lctt_cols = [
            'LCTT. LƯU CHUYỂN TIỀN TỆ RÒNG TỪ CÁC HOẠT ĐỘNG SẢN XUẤT KINH DOANH (TT)',
            'LCTT. LƯU CHUYỂN TIỀN TỆ RÒNG TỪ HOẠT ĐỘNG ĐẦU TƯ (TT)',
            'LCTT. LƯU CHUYỂN TIỀN TỆ TỪ HOẠT ĐỘNG TÀI CHÍNH (TT)',
            'LCTT. LƯU CHUYỂN TIỀN THUẦN TRONG KỲ (TT)',
        ]
        show_cols = [col for col in lctt_cols if col in bctc_company.columns]
        if show_cols:
            df_lctt = bctc_company[['NĂM'] + show_cols].set_index('NĂM').T
            st.dataframe(df_lctt, use_container_width=True)
        else:
            st.info("Không có dữ liệu Lưu Chuyển Tiền Tệ.")
else:
    st.info("Không có dữ liệu BCTC cho mã này.")
# ============================================================================
# FINANCIAL TREND CHARTS - BIỂU ĐỒ XU HƯỚNG
# ============================================================================
st.markdown("---")
st.subheader("Xu Hướng Tài Chính Theo Thời Gian")

# Chuẩn bị dữ liệu cho biểu đồ
if data.get('bctc') is not None:
    bctc_company = data['bctc'][data['bctc']['MÃ'] == selected_company].copy()
    bctc_company = bctc_company.sort_values('NĂM')
else:
    bctc_company = pd.DataFrame()

# Chart 1: Total Assets & Equity Over Time
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.markdown("#### Tổng Tài Sản & Vốn Chủ Sở Hữu")
    
    if len(bctc_company) > 0 and 'CĐKT. TỔNG CỘNG TÀI SẢN' in bctc_company.columns and 'CĐKT. VỐN CHỦ SỞ HỮU' in bctc_company.columns:
        fig_assets = go.Figure()
        
        fig_assets.add_trace(go.Scatter(
            x=bctc_company['NĂM'],
            y=bctc_company['CĐKT. TỔNG CỘNG TÀI SẢN'] / 1e9,  # Chuyển sang tỷ VND
            name='Tổng Tài Sản (Tỷ VND)',
            mode='lines+markers',
            line=dict(color='#22d3ee', width=3),
            marker=dict(size=8)
        ))
        
        fig_assets.add_trace(go.Scatter(
            x=bctc_company['NĂM'],
            y=bctc_company['CĐKT. VỐN CHỦ SỞ HỮU'] / 1e9,  # Chuyển sang tỷ VND
            name='Vốn Chủ Sở Hữu (Tỷ VND)',
            mode='lines+markers',
            line=dict(color='#10b981', width=3, dash='dash'),
            marker=dict(size=8)
        ))
        
        fig_assets.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e5e7eb',
            legend=dict(font_color='#e5e7eb', bgcolor='rgba(0,0,0,0)'),
            height=350,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        
        st.plotly_chart(fig_assets, use_container_width=True)
    else:
        # Fallback: dùng dữ liệu từ health data
        fig_assets_simple = go.Figure()
        if 'TỔNG TÀI SẢN' in company_data.columns:
            fig_assets_simple.add_trace(go.Scatter(
                x=company_data['NĂM'],
                y=company_data['TỔNG TÀI SẢN'],
                name='Tổng Tài Sản',
                mode='lines+markers',
                line=dict(color='#22d3ee', width=3)
            ))
        fig_assets_simple.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e5e7eb',
            height=350
        )
        st.plotly_chart(fig_assets_simple, use_container_width=True)

with col_chart2:
    st.markdown("#### Cấu Trúc Nợ & Vốn Chủ Sở Hữu")
    
    if len(bctc_company) > 0 and 'CĐKT. NỢ PHẢI TRẢ' in bctc_company.columns and 'CĐKT. VỐN CHỦ SỞ HỮU' in bctc_company.columns:
        fig_structure = go.Figure()
        
        fig_structure.add_trace(go.Bar(
            x=bctc_company['NĂM'],
            y=bctc_company['CĐKT. NỢ PHẢI TRẢ'] / 1e9,
            name='Nợ Phải Trả',
            marker_color='#f59e0b'
        ))
        
        fig_structure.add_trace(go.Bar(
            x=bctc_company['NĂM'],
            y=bctc_company['CĐKT. VỐN CHỦ SỞ HỮU'] / 1e9,
            name='Vốn Chủ Sở Hữu',
            marker_color='#10b981'
        ))
        
        fig_structure.update_layout(
            barmode='stack',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e5e7eb',
            legend=dict(font_color='#e5e7eb', bgcolor='rgba(0,0,0,0)'),
            height=350,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        
        st.plotly_chart(fig_structure, use_container_width=True)
    else:
        st.info("Dữ liệu BCTC không khả dụng. Vui lòng kiểm tra file Data BCTC.xlsx")

# Chart 2: Net Income & Operating Income
col_chart3, col_chart4 = st.columns(2)

with col_chart3:
    st.markdown("#### Lợi Nhuận Ròng")
    
    if len(bctc_company) > 0 and 'KQKD. LỢI NHUẬN SAU THUẾ THU NHẬP DOANH NGHIỆP' in bctc_company.columns:
        fig_income = go.Figure()
        # Chỉ lấy năm nguyên nếu có số lẻ
        nam_values = bctc_company['NĂM']
        if not all(nam_values.astype(int) == nam_values):
            # Nếu có số lẻ, làm tròn hoặc chuyển thành chuỗi tháng/năm nếu muốn
            tickvals = nam_values
            ticktext = nam_values.apply(lambda x: f"{int(x)}" if x == int(x) else f"6/{int(x)}")
        else:
            tickvals = nam_values
            ticktext = nam_values.astype(str)
        fig_income.add_trace(go.Scatter(
            x=nam_values,
            y=bctc_company['KQKD. LỢI NHUẬN SAU THUẾ THU NHẬP DOANH NGHIỆP'] / 1e9,
            name='Lợi Nhuận Ròng',
            mode='lines',
            fill='tonexty',
            fillcolor='rgba(34, 211, 238, 0.3)',
            line=dict(color='#22d3ee', width=3)
        ))
        fig_income.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e5e7eb',
            yaxis_title='Tỷ VND',
            height=350,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        fig_income.update_xaxes(tickvals=tickvals, ticktext=ticktext)
        st.plotly_chart(fig_income, use_container_width=True)
    else:
        st.info("Dữ liệu lợi nhuận không khả dụng")

with col_chart4:
    st.markdown("#### Doanh Thu Hoạt Động")
    
    if len(bctc_company) > 0 and 'KQKD. DOANH THU THUẦN' in bctc_company.columns:
        fig_revenue = go.Figure()
        
        fig_revenue.add_trace(go.Bar(
            x=bctc_company['NĂM'],
            y=bctc_company['KQKD. DOANH THU THUẦN'] / 1e9,
            name='Doanh Thu Thuần',
            marker_color='#10b981'
        ))
        
        fig_revenue.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e5e7eb',
            yaxis_title='Tỷ VND',
            height=350,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        
        st.plotly_chart(fig_revenue, use_container_width=True)
    else:
        # Fallback: dùng dữ liệu tăng trưởng
        if 'TĂNG TRƯỞNG DOANH THU' in company_data.columns:
            fig_revenue_growth = go.Figure()
            fig_revenue_growth.add_trace(go.Scatter(
                x=company_data['NĂM'],
                y=company_data['TĂNG TRƯỞNG DOANH THU'] * 100,
                name='Tăng Trưởng Doanh Thu (%)',
                mode='lines+markers',
                line=dict(color='#10b981', width=3)
            ))
            fig_revenue_growth.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#e5e7eb',
                yaxis_title='%',
                height=350
            )
            st.plotly_chart(fig_revenue_growth, use_container_width=True)
        else:
            st.info("Dữ liệu doanh thu không khả dụng")

# ============================================================================
# PRICE HISTORY & FOREIGN FLOW
# ============================================================================
st.markdown("---")
st.subheader("Lịch Sử Giá & Dòng Tiền Nước Ngoài")

col_price1, col_price2 = st.columns([2, 1])

with col_price1:
    st.markdown("#### Lịch Sử Giá & Vốn Hóa Thị Trường")
    
    if price_company is not None and len(price_company) > 0:
        time_filter = st.radio(
            "Chọn khoảng thời gian",
            ["1M", "6M", "1Y", "ALL"],
            horizontal=True,
            index=2
        )
        price_filtered = price_company.copy()
        if time_filter == "1M":
            price_filtered = price_filtered[price_filtered['Ngày'] >= price_filtered['Ngày'].max() - pd.Timedelta(days=30)]
        elif time_filter == "6M":
            price_filtered = price_filtered[price_filtered['Ngày'] >= price_filtered['Ngày'].max() - pd.Timedelta(days=180)]
        elif time_filter == "1Y":
            price_filtered = price_filtered[price_filtered['Ngày'] >= price_filtered['Ngày'].max() - pd.Timedelta(days=365)]

        # Kiểm tra dữ liệu OHLC
        ohlc_cols = ['Open', 'High', 'Low', 'Close']
        ohlc_vn = ['Giá mở cửa', 'Giá cao nhất', 'Giá thấp nhất', 'Giá đóng cửa']
        has_ohlc = all(col in price_filtered.columns for col in ohlc_cols)
        has_ohlc_vn = all(col in price_filtered.columns for col in ohlc_vn)

        # Tính MACD, RSI
        close_col = None
        if has_ohlc:
            close_col = 'Close'
        elif 'Giá' in price_filtered.columns:
            close_col = 'Giá'
        elif has_ohlc_vn:
            close_col = 'Giá đóng cửa'

        if close_col:
            close = price_filtered[close_col]
            # MACD
            ema12 = close.ewm(span=12, adjust=False).mean()
            ema26 = close.ewm(span=26, adjust=False).mean()
            macd = ema12 - ema26
            signal = macd.ewm(span=9, adjust=False).mean()
            # RSI
            delta = close.diff()
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)
            avg_gain = gain.rolling(window=14).mean()
            avg_loss = loss.rolling(window=14).mean()
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))

        # Chỉ vẽ biểu đồ giá và vốn hóa trên cùng
        fig_price = go.Figure()
        # Giá cổ phiếu
        if has_ohlc:
            fig_price.add_trace(
                go.Candlestick(
                    x=price_filtered['Ngày'],
                    open=price_filtered['Open'],
                    high=price_filtered['High'],
                    low=price_filtered['Low'],
                    close=price_filtered['Close'],
                    name='Candlestick'
                )
            )
        elif has_ohlc_vn:
            fig_price.add_trace(
                go.Candlestick(
                    x=price_filtered['Ngày'],
                    open=price_filtered['Giá mở cửa'],
                    high=price_filtered['Giá cao nhất'],
                    low=price_filtered['Giá thấp nhất'],
                    close=price_filtered['Giá đóng cửa'],
                    name='Candlestick'
                )
            )
        elif close_col:
            fig_price.add_trace(
                go.Scatter(
                    x=price_filtered['Ngày'],
                    y=price_filtered[close_col],
                    name='Giá',
                    line=dict(color='#22d3ee', width=2),
                    fill='tonexty'
                )
            )

        # Moving average 50
        if close_col and len(price_filtered) >= 50:
            ma_50 = price_filtered[close_col].rolling(50).mean()
            fig_price.add_trace(
                go.Scatter(
                    x=price_filtered['Ngày'],
                    y=ma_50,
                    name='MA(50)',
                    line=dict(color='#ef4444', width=2, dash='dash')
                )
            )

        fig_price.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e5e7eb',
            legend=dict(font_color='#e5e7eb', bgcolor='rgba(0,0,0,0)'),
            height=350,
            margin=dict(l=20, r=20, t=40, b=20),
            hovermode='x unified',
            title='Giá Cổ Phiếu'
        )
        fig_price.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#1e293b')
        fig_price.update_xaxes(
            showgrid=True, gridwidth=1, gridcolor='#1e293b'
        )
        fig_price.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#1e293b')
        st.plotly_chart(fig_price, use_container_width=True)

        # Biểu đồ vốn hóa riêng phía dưới
        if marketcap_company is not None and len(marketcap_company) > 0:
            st.markdown('#### Vốn Hóa Thị Trường')
            marketcap_filtered = marketcap_company[marketcap_company['Ngày'].isin(price_filtered['Ngày'])]
            if len(marketcap_filtered) > 0:
                fig_marketcap = go.Figure()
                fig_marketcap.add_trace(
                    go.Scatter(
                        x=marketcap_filtered['Ngày'],
                        y=marketcap_filtered['MarketCap'] / 1e9,
                        name='Vốn Hóa (Nghìn Tỷ)',
                        line=dict(color='#06b6d4', width=2),
                        fill='tonexty',
                        fillcolor='rgba(6, 182, 212, 0.2)'
                    )
                )
                fig_marketcap.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#e5e7eb',
                    legend=dict(font_color='#e5e7eb', bgcolor='rgba(0,0,0,0)'),
                    height=250,
                    margin=dict(l=20, r=20, t=20, b=20),
                    hovermode='x unified',
                    title='Vốn Hóa (Nghìn Tỷ)'
                )
                fig_marketcap.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#1e293b')
                fig_marketcap.update_xaxes(
                    showgrid=True, gridwidth=1, gridcolor='#1e293b'
                )
                fig_marketcap.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#1e293b')
                st.plotly_chart(fig_marketcap, use_container_width=True)
    else:
        st.warning("Không có dữ liệu giá. Vui lòng kiểm tra file Price_2124.parquet")

with col_price2:
    st.markdown("#### Dòng Tiền Nước Ngoài (30 ngày)")
    
    if foreign_company is not None and len(foreign_company) > 0:
        foreign_recent = foreign_company.tail(30)
        
        if 'Net.F_Val' in foreign_recent.columns:
            fig_foreign = go.Figure()
            
            colors = ['#10b981' if x >= 0 else '#ef4444' for x in foreign_recent['Net.F_Val']]
            
            fig_foreign.add_trace(go.Bar(
                x=foreign_recent['Ngày'].dt.strftime('%d/%m'),
                y=foreign_recent['Net.F_Val'] / 1e9,  # Chuyển sang tỷ VND
                name='Dòng Tiền Ròng',
                marker_color=colors
            ))
            

            fig_foreign.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#e5e7eb',
                yaxis_title='Tỷ VND',
                xaxis_title='Ngày',
                height=350,
                margin=dict(l=20, r=20, t=20, b=20),
                legend=dict(font_color='#e5e7eb', bgcolor='rgba(0,0,0,0)')
            )

            fig_foreign.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#1e293b')
            fig_foreign.update_xaxes(
                showgrid=True, gridwidth=1, gridcolor='#1e293b'
            )
            fig_foreign.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#1e293b')
            st.plotly_chart(fig_foreign, use_container_width=True)
        else:
            st.info("Không có dữ liệu Net.F_Val cho 30 ngày gần nhất.")

    # Thêm biểu đồ Dòng tiền nước ngoài (1 năm) phía dưới
    if foreign_company is not None and len(foreign_company) > 0 and 'Net.F_Val' in foreign_company.columns:
        st.markdown("#### Dòng tiền nước ngoài (1 năm)")
        fig_foreign_year = go.Figure()
        fig_foreign_year.add_trace(go.Scatter(
            x=foreign_company['Ngày'],
            y=foreign_company['Net.F_Val'] / 1e9,
            mode='lines+markers',
            name='Dòng tiền nước ngoài',
            line=dict(color='#22d3ee', width=3),
            marker=dict(size=6)
        ))
        fig_foreign_year.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e5e7eb',
            height=350,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis_title='Ngày',
            yaxis_title='Tỷ VND'
        )
        fig_foreign_year.update_xaxes(

        )
        st.plotly_chart(fig_foreign_year, use_container_width=True)


# ============================================================================
# AI NHẬN XÉT ĐẦU TƯ (DƯỚI CÙNG)
# ============================================================================
st.markdown("---")
st.subheader("Đánh Giá Cơ Hội Đầu Tư")

# Sinh nhận xét AI với prompt dài hơn, chi tiết hơn
company_data_for_ai = company_data[company_data['NĂM'] <= selected_year].copy()
ai_result = generate_ai_commentary(selected_company, company_data_for_ai, price_company, foreign_company, data)
st.markdown(f"""
<div style='background: #0e2235; border-radius: 8px; padding: 22px 28px; margin-bottom: 18px; color: #e0e7ef; font-size: 1.08em;'>
<b> Nhận xét đa chiều về doanh nghiệp:</b><br>
{ai_result['summary']}<br><br>
<b>Kết luận & khuyến nghị:</b><br>
<span style='color:#38f57a;font-weight:bold'>{ai_result['advice']}</span><br><br>
<b>Lưu ý:</b> Nhận định này được AI tổng hợp đa chiều dựa trên các chỉ số tài chính, tăng trưởng, vị thế ngành, tín nhiệm, dòng tiền, giá cổ phiếu, hành vi nhà đầu tư và các yếu tố liên quan. Nhà đầu tư nên cân nhắc thêm các yếu tố vĩ mô, chiến lược doanh nghiệp và khẩu vị rủi ro cá nhân trước khi quyết định đầu tư.
</div>
""", unsafe_allow_html=True)