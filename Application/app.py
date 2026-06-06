import streamlit as st
import sys
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.optimization import solve_bai01, solve_bai02, solve_bai03, solve_bai04, solve_bai05, solve_bai06, solve_bai07, solve_bai08, solve_bai09, solve_bai10, solve_bai12, solve_bai12_dashboard
from src.rl_env import solve_bai11

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

st.set_page_config(page_title="AIDEOM-VN Streamlit", layout="wide", initial_sidebar_state="expanded")

st.markdown("""<style>
    /* Elegant Neumorphic / Soft Pink UI Theme */
    @import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;600;700;800&display=swap');
    
    :root {
      --bg-color: #FFFFFF; /* Pure white app background */
      --card-bg: #FFE5EE; /* Stronger pink tint for cards */
      --text-main: #1D1D1F; /* Dark grey almost black */
      --text-muted: #86868B;
      --accent-magenta: #F50057; /* Punchy magenta from the image */
      --accent-purple: #9C27B0;
      --accent-blue: #03A9F4;
      --shadow-color: rgba(255, 200, 221, 0.4);
      --border-light: #FFC8DD;
    }
    
    .stApp { 
        background-color: var(--bg-color) !important;
        background-image: none !important; /* Remove starry background */
        color: var(--text-main); 
        font-family: 'Nunito Sans', sans-serif !important; 
    }
    
    /* Remove stars pseudo-element */
    .stApp::before { display: none !important; }

    /* Sidebar */
    [data-testid="stSidebar"] { 
        background-color: #FFFFFF !important; 
        border-right: 1px solid var(--border-light); 
        box-shadow: 4px 0 20px rgba(0,0,0,0.02);
    }
    [data-testid="stSidebar"] * { color: var(--text-muted); font-weight: 600; }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] p { color: var(--text-main) !important; font-weight: 800; }
    
    /* Active styling in sidebar simulation */
    [data-testid="stSidebar"] [data-testid="stSidebarNavItems"] li[data-selected="true"] {
        background-color: rgba(245, 0, 87, 0.05);
        border-right: 3px solid var(--accent-magenta);
    }

    /* Soft UI Buttons */
    .stButton > button {
        background: #FFFFFF !important; 
        border: 1px solid var(--border-light) !important; 
        border-radius: 12px !important;
        box-shadow: 0 4px 12px var(--shadow-color) !important;
        color: var(--text-main) !important; 
        font-weight: 700 !important; 
        padding: 0.5rem 1rem !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover { 
        background: var(--accent-magenta) !important; 
        color: #FFFFFF !important;
        border-color: var(--accent-magenta) !important;
        transform: translateY(-2px); 
        box-shadow: 0 6px 16px rgba(245, 0, 87, 0.3) !important;
    }
    
    /* Soft UI Metrics Cards */
    [data-testid="stMetric"] {
        background: var(--card-bg) !important; 
        border-radius: 20px !important; 
        padding: 20px !important; 
        margin: 10px 0 !important;
        border: 1px solid var(--border-light) !important;
        box-shadow: 0 10px 30px var(--shadow-color) !important; 
        transition: transform 0.2s !important;
        text-align: left;
        height: 100% !important;
    }
    [data-testid="stMetric"]:hover { transform: translateY(-3px); box-shadow: 0 15px 35px rgba(220, 200, 210, 0.7) !important; }
    [data-testid="stMetricValue"] { color: var(--text-main) !important; font-size: 2.2rem !important; font-weight: 800 !important; }
    [data-testid="stMetricLabel"] { color: var(--text-muted) !important; font-weight: 700 !important; font-size: 0.95rem !important; margin-bottom: 5px; }

    /* Soft UI Containers (for charts) */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] > div {
        background: var(--card-bg) !important;
        border-radius: 20px !important;
        border: 1px solid #FFFFFF !important;
        box-shadow: 0 10px 30px var(--shadow-color) !important;
        padding: 20px !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent !important;
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        color: var(--text-muted) !important;
        font-weight: 700;
        padding: 10px 0;
    }
    .stTabs [aria-selected="true"] {
        color: var(--accent-magenta) !important;
        border-bottom: 3px solid var(--accent-magenta) !important;
    }

    /* Typography */
    h1, h2, h3 { color: var(--text-main) !important; font-weight: 800; border: none; margin-bottom: 20px;}
    p, label { color: var(--text-muted); font-weight: 600; }
    
    .block-container { position: relative; z-index: 1; padding-top: 2rem; }
</style>""", unsafe_allow_html=True)

st.sidebar.title("AIDEOM")
st.sidebar.caption("Khổng Phương Thảo")

pages = [
    "Bài 1: Cobb-Douglas", "Bài 2: LP Ngân sách", "Bài 3: Chỉ số ưu tiên",
    "Bài 4: LP Phân bổ vùng", "Bài 5: MIP Lựa chọn dự án", "Bài 6: TOPSIS",
    "Bài 7: Tối ưu đa mục tiêu", "Bài 8: Tối ưu động", "Bài 9: Mô phỏng lao động",
    "Bài 10: Quy hoạch ngẫu nhiên", "Bài 11: Q-learning", "Bài 12: Đồ án tổng hợp"
]
page = st.sidebar.radio("Chọn module:", pages)

st.sidebar.markdown("---")
LINE_COLOR = '#C13346'

if page == pages[0]:
    st.title("Bài 1: Hàm sản xuất Cobb-Douglas mở rộng")
    col_main, col_ctrl = st.columns([3, 1], gap="large")
    with col_ctrl:
        with st.form("form_module_1"):
            st.markdown("Thông số đầu vào")
            alpha = st.slider("α (Vốn K)", 0.10, 0.50, 0.33, 0.01)
            beta  = st.slider("β (Lao động L)", 0.10, 0.60, 0.42, 0.01)
            gamma = st.slider("γ (Số hóa D)", 0.01, 0.30, 0.10, 0.01)
            delta = st.slider("δ (AI)", 0.01, 0.20, 0.08, 0.01)
            theta = st.slider("θ (Nhân lực H)", 0.01, 0.20, 0.07, 0.01)
            submit_btn = st.form_submit_button("Chạy mô hình", use_container_width=True)
    with col_main:
        res = solve_bai01(DATA_DIR, alpha, beta, gamma, delta, theta)
        with st.container(border=True):
            st.subheader("1. Xu hướng TFP (A_t) theo năm")
            fig_at = px.line(x=res['years'], y=res['A_t'], title="Năng suất nhân tố tổng hợp A_t (2020-2025)", markers=True, labels={'x': 'Năm', 'y': 'A_t'})
            fig_at.update_traces(line_color=LINE_COLOR)
            st.plotly_chart(fig_at, use_container_width=True)
        with st.container(border=True):
            st.subheader("2. So sánh Ŷ dự báo vs Y thực tế")
            fig_compare = go.Figure()
            fig_compare.add_trace(go.Scatter(x=res['years'], y=res['Y_actual'], name='Y thực tế', mode='lines+markers', line=dict(color='#E53E3E')))
            fig_compare.add_trace(go.Scatter(x=res['years'], y=res['Y_hat'], name='Ŷ dự báo (A̅ trung bình)', mode='lines+markers', line=dict(color=LINE_COLOR, dash='dash')))
            st.plotly_chart(fig_compare, use_container_width=True)
            st.metric("MAPE (Mean Absolute Percentage Error)", f"{res['mape']:.2f}%")
        with st.container(border=True):
            st.subheader("3. Phân rã tăng trưởng GDP 2020-2025")
            contrib = res['contrib_pct']
            df_contrib = pd.DataFrame({'Yếu tố': list(contrib.keys()), 'Đóng góp (%)': list(contrib.values())})
            col1, col2 = st.columns([1, 2])
            with col1:
                st.dataframe(df_contrib, use_container_width=True, hide_index=True)
            with col2:
                fig_decomp = px.bar(df_contrib, x='Yếu tố', y='Đóng góp (%)', title="Đóng góp vào tăng trưởng GDP (%)", color='Yếu tố')
                fig_decomp.update_layout(showlegend=False)
                st.plotly_chart(fig_decomp, use_container_width=True)
        with st.container(border=True):
            st.subheader("4. Dự báo GDP Việt Nam đến 2030")
            fig_forecast = go.Figure()
            fig_forecast.add_trace(go.Scatter(x=res['years'], y=res['Y_actual'], name='Y thực tế (2020-2025)', mode='lines+markers', line=dict(color='#E53E3E')))
            fig_forecast.add_trace(go.Scatter(x=res['forecast_years'], y=res['forecast_series'], name='Dự báo cơ sở', mode='lines+markers', line=dict(color=LINE_COLOR)))
            fig_forecast.add_trace(go.Scatter(x=res['forecast_years'], y=res['forecast_high_tfp'], name='Kịch bản TFP cao', mode='lines+markers', line=dict(color='#48BB78', dash='dash')))
            fig_forecast.add_trace(go.Scatter(x=res['forecast_years'], y=res['forecast_ai_fast'], name='Kịch bản AI nhanh', mode='lines+markers', line=dict(color='#ED8936', dash='dot')))
            st.plotly_chart(fig_forecast, use_container_width=True)
            st.metric("GDP dự báo 2030 (Kịch bản cơ sở)", f"{res['gdp_2030']:,.0f} nghìn tỷ VND")

elif page == pages[1]:
    st.title("Bài 2: Quy hoạch tuyến tính phân bổ ngân sách")
    col_main, col_ctrl = st.columns([3, 1], gap="large")
    with col_ctrl:
        with st.form("form_module_2"):
            st.markdown("Thông số đầu vào")
            tb  = st.slider("Tổng ngân sách", 50, 200, 100, 5)
            mi  = st.slider("Min I (Hạ tầng)", 5, 50, 25)
            mai = st.slider("Min AI", 5, 50, 15)
            submit_btn = st.form_submit_button("Chạy mô hình", use_container_width=True)
    with col_main:
        res = solve_bai02(budget=tb, min_I=mi, min_AI=mai)
        with st.container(border=True):
            st.subheader("1. Giải bằng scipy.optimize.linprog")
            if res['status'] == 'Optimal':
                st.success(f"Khả thi. Z* = {res['Z']:.2f}")
                fig = px.bar(x=list(res['allocation'].keys()), y=list(res['allocation'].values()), title="Phân bổ tối ưu (linprog)", color=list(res['allocation'].keys()))
                fig.update_layout(showlegend=False, xaxis_title="Hạng mục", yaxis_title="Nghìn tỷ VND")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("Không khả thi với các ràng buộc này.")
        with st.container(border=True):
            st.subheader("2. Giải bằng PuLP – Giá đối ngẫu (Shadow Prices)")
            if res['dual_values']:
                dual_labels = {'C1_Budget': 'C1: Ngân sách tổng', 'C2_Tech35': 'C2: Tỷ lệ công nghệ ≥ 35%', 'C3_MinI': 'C3: Min Hạ tầng (I)', 'C4_MinAI': 'C4: Min AI', 'C5_MinH': 'C5: Min Nhân lực (H)', 'C6_MinRD': 'C6: Min R&D'}
                df_dual = pd.DataFrame({'Ràng buộc': [dual_labels.get(k, k) for k in res['dual_values'].keys()], 'Shadow Price (π)': list(res['dual_values'].values())})
                st.dataframe(df_dual, use_container_width=True, hide_index=True)
            else:
                st.warning("Không có dual values.")
        with st.container(border=True):
            st.subheader("3. Phân tích độ nhạy – Đường cong Z*(B)")
            fig_sens = px.line(x=res['sensitivity_budgets'], y=res['sensitivity_z'], title="Z* theo Ngân sách tổng B", markers=True)
            fig_sens.update_traces(line_color=LINE_COLOR)
            st.plotly_chart(fig_sens, use_container_width=True)
        with st.container(border=True):
            st.subheader("4. Kịch bản: Ưu tiên nhân lực số (x₃ ≥ 30)")
            sc = res['scenario_x3']
            if sc['status'] == 'Optimal':
                col1, col2 = st.columns(2)
                col1.metric("Z* gốc (x₃ ≥ 20)", f"{res['Z']:.2f}")
                col2.metric("Z* mới (x₃ ≥ 30)", f"{sc['Z']:.2f}", delta=f"{sc['Z'] - res['Z']:.2f}")
                st.success("Bài toán vẫn khả thi.")
            else:
                st.error("Bài toán không còn khả thi khi thêm ràng buộc x₃ ≥ 30.")

elif page == pages[2]:
    st.title("Bài 3: Xây dựng chỉ số ưu tiên ngành")
    col_main, col_ctrl = st.columns([3, 1], gap="large")
    with col_ctrl:
        with st.form("form_module_3"):
            st.markdown("Thông số đầu vào")
            w_growth = st.slider("w Tăng trưởng", 0.0, 0.5, 0.15, 0.01)
            w_prod = st.slider("w Năng suất", 0.0, 0.5, 0.15, 0.01)
            w_spill = st.slider("w Lan tỏa", 0.0, 0.5, 0.20, 0.01)
            w_exp = st.slider("w Xuất khẩu", 0.0, 0.5, 0.15, 0.01)
            w_emp = st.slider("w Việc làm", 0.0, 0.5, 0.10, 0.01)
            w_ai = st.slider("w AI Readiness", 0.0, 0.5, 0.20, 0.01)
            w_risk = st.slider("w Rủi ro (Penalty)", 0.0, 0.5, 0.15, 0.01)
            submit_btn = st.form_submit_button("Chạy mô hình", use_container_width=True)
    with col_main:
        res = solve_bai03(w_growth=w_growth, w_productivity=w_prod, w_spillover=w_spill, w_export=w_exp, w_employment=w_emp, w_ai=w_ai, w_risk=w_risk)
        with st.container(border=True):
            st.subheader("1. Ma trận chuẩn hóa Min-Max (đảo dấu Rủi ro)")
            df_norm = pd.DataFrame(res['norm_matrix'], columns=res['col_names'], index=res['sectors'])
            st.dataframe(df_norm.style.format("{:.4f}"), use_container_width=True)
        with st.container(border=True):
            st.subheader("2. Xếp hạng 10 ngành theo Priority")
            names = [r['sector_name_vi'] for r in res['ranking']]
            scores = [r['Priority'] for r in res['ranking']]
            fig = px.bar(x=names, y=scores, title="Chỉ số ưu tiên theo ngành (giảm dần)", color=scores, color_continuous_scale='Reds')
            st.plotly_chart(fig, use_container_width=True)
        with st.container(border=True):
            st.subheader("3. Phân tích độ nhạy: Trọng số AI Readiness (a₆)")
            df_heatmap = pd.DataFrame(res['heatmap_data'], columns=[f"a₆={v}" for v in res['a6_values']], index=res['sectors'])
            fig_hm = px.imshow(df_heatmap, title="Heatmap Priority theo a₆", color_continuous_scale="Reds", aspect="auto", text_auto=".3f")
            st.plotly_chart(fig_hm, use_container_width=True)
        with st.container(border=True):
            st.subheader("4. So sánh: Tăng trưởng vs Bao trùm")
            sc = res['scenario_comparison']
            col1, col2 = st.columns(2)
            with col1:
                fig_g = px.bar(x=list(sc['growth']['scores'].keys()), y=list(sc['growth']['scores'].values()), title="Điểm ưu tiên – Tăng trưởng")
                fig_g.update_traces(marker_color='#F50057')
                st.plotly_chart(fig_g, use_container_width=True)
            with col2:
                fig_i = px.bar(x=list(sc['inclusive']['scores'].keys()), y=list(sc['inclusive']['scores'].values()), title="Điểm ưu tiên – Bao trùm")
                fig_i.update_traces(marker_color='#F50057')
                st.plotly_chart(fig_i, use_container_width=True)

elif page == pages[3]:
    st.title("Bài 4: LP Phân bổ ngân sách ngành - vùng")
    col_main, col_ctrl = st.columns([3, 1], gap="large")
    with col_ctrl:
        with st.form("form_module_4"):
            st.markdown("Thông số đầu vào")
            budget = st.slider("Tổng ngân sách (Tỷ VND)", 20000, 80000, 50000, 5000)
            w_gdp = st.slider("w GDP", 0.0, 1.0, 0.40, 0.05)
            w_equity = st.slider("w Công bằng", 0.0, 1.0, 0.25, 0.05)
            w_ai = st.slider("w AI", 0.0, 1.0, 0.20, 0.05)
            submit_btn = st.form_submit_button("Chạy mô hình", use_container_width=True)
    with col_main:
        res = solve_bai04(budget, w_gdp=w_gdp, w_equity=w_equity, w_ai=w_ai)
        with st.container(border=True):
            st.subheader("1. Giải bằng PuLP (CBC) – Ma trận phân bổ 6×4")
            if res['status'] == 'Optimal':
                st.success(f"Z* (PuLP) = {res['Z']:,.1f}")
                df_pulp = pd.DataFrame(res['allocation']).T
                st.dataframe(df_pulp.style.format("{:,.1f}"), use_container_width=True)
            else:
                st.error("Không khả thi.")

        with st.container(border=True):
            st.subheader("2. Heatmap phân bổ tối ưu")
            if res['status'] == 'Optimal':
                df_hm = pd.DataFrame(res['allocation']).T
                fig = px.imshow(df_hm, labels=dict(x="Hạng mục", y="Vùng", color="Ngân sách"), color_continuous_scale="Reds", aspect="auto", text_auto=",.0f")
                st.plotly_chart(fig, use_container_width=True)
        with st.container(border=True):
            st.subheader("3. Chi phí kinh tế của công bằng vùng miền (bỏ C5)")
            col1, col2, col3 = st.columns(3)
            col1.metric("Z* có C5", f"{res['Z']:,.1f}")
            col2.metric("Z* không C5", f"{res['no_equity_z']:,.1f}")
            col3.metric("Chi phí công bằng (ΔZ)", f"{res['equity_cost']:,.1f} tỷ VND", delta=f"-{res['equity_cost']:,.1f}")
            df_noeq = pd.DataFrame(res['no_equity_alloc']).T
            fig_noeq = px.imshow(df_noeq, title="Heatmap KHÔNG có ràng buộc công bằng (bỏ C5)", color_continuous_scale="Reds", aspect="auto", text_auto=",.0f")
            st.plotly_chart(fig_noeq, use_container_width=True)

elif page == pages[4]:
    st.title("Bài 5: MIP Lựa chọn dự án")
    col_main, col_ctrl = st.columns([3, 1], gap="large")
    with col_ctrl:
        with st.form("form_module_5"):
            st.markdown("Thông số đầu vào")
            budget = st.slider("Ngân sách tổng (Tỷ VND)", 40000, 120000, 80000, 5000)
            w_gdp = st.slider("w GDP", 0.0, 1.0, 0.40, 0.05)
            w_equity = st.slider("w Công bằng", 0.0, 1.0, 0.30, 0.05)
            w_ai = st.slider("w AI", 0.0, 1.0, 0.30, 0.05)
            submit_btn = st.form_submit_button("Chạy mô hình", use_container_width=True)
    with col_main:
        res = solve_bai05(budget, w_gdp=w_gdp, w_equity=w_equity, w_ai=w_ai)
        with st.container(border=True):
            st.subheader("1. Kết quả giải gốc (PuLP - CBC)")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Tổng Lợi ích (Z*)", f"{res['Z']:,.2f}")
            c2.metric("Tổng Chi phí", f"{res['cost']:,.2f}")
            c3.metric("Tổng NPV", f"{res['total_npv']:,.2f}")
            c4.metric("NPV Biên (Z*/Cost)", f"{res['npv_margin']:.4f}")
            if res['selected']:
                df_proj = pd.DataFrame(res['projects']).T
                st.dataframe(df_proj.style.format("{:.2f}"), use_container_width=True)
            else:
                st.warning("Infeasible")
        with st.container(border=True):
            st.subheader("2. Phân tích: Nới ngân sách lên 100.000 tỷ")
            r100 = res['res_100k']
            st.metric("Lợi ích Z* (100k)", f"{r100['Z']:,.2f}", delta=f"{r100['Z'] - res['Z']:,.2f}")
        with st.container(border=True):
            st.subheader("3. Phân tích: Bắt buộc chọn P1 và P2")
            rP = res['res_p1p2']
            if rP['status'] == 'Optimal':
                st.metric("Lợi ích Z* (P1+P2)", f"{rP['Z']:,.2f}", delta=f"{rP['Z'] - res['Z']:,.2f}")
            else:
                st.error("Không khả thi")
        with st.container(border=True):
            st.subheader("4. Mở rộng: Rủi ro dự án (Tối đa hóa E[Z])")
            rR = res['res_risk']
            st.metric("E[Z] Kỳ vọng", f"{rR['Z']:,.2f}")
            st.write(f"Tập dự án chọn an toàn: {', '.join(rR['selected'])}")

elif page == pages[5]:
    st.title("Bài 6: TOPSIS Xếp hạng vùng")
    col_main, col_ctrl = st.columns([3, 1], gap="large")
    with col_ctrl:
        with st.form("form_module_6"):
            st.markdown("Thông số đầu vào")
            mode = st.radio("Chế độ trọng số:", ["Entropy (Tự động)", "Chuyên gia (Manual)"], index=0)
            weight_mode = 0 if mode == "Entropy (Tự động)" else 1
            w_expert = None
            if weight_mode == 1:
                w_grdp = st.slider("w GRDP/capita", 0.0, 0.5, 0.10, 0.01)
                w_digi = st.slider("w Digital", 0.0, 0.5, 0.10, 0.01)
                w_ai = st.slider("w AI ready", 0.0, 0.5, 0.15, 0.01)
                w_labor = st.slider("w Lao động", 0.0, 0.5, 0.20, 0.01)
                w_rd = st.slider("w R&D", 0.0, 0.5, 0.15, 0.01)
                w_gini = st.slider("w Gini (cost)", 0.0, 0.5, 0.15, 0.01)
                w_expert = [w_grdp, w_digi, w_ai, w_labor, w_rd, w_gini]
                s = sum(w_expert)
                if s > 0: w_expert = [x/s for x in w_expert]
            submit_btn = st.form_submit_button("Chạy mô hình", use_container_width=True)
    with col_main:
        res = solve_bai06(w_manual=w_expert, weight_mode=weight_mode)
        with st.container(border=True):
            st.subheader("1 & 2. Xếp hạng vùng theo TOPSIS")
            names = [r['region_name_vi'] for r in res['ranking']]
            scores = [r['TOPSIS'] for r in res['ranking']]
            fig = px.bar(x=names, y=scores, title=f"Điểm TOPSIS", color=scores, color_continuous_scale='Reds')
            st.plotly_chart(fig, use_container_width=True)
        with st.container(border=True):
            st.subheader("3. Phân tích độ nhạy: Thay đổi trọng số w_AI (0.10 - 0.40)")
            sens_data = []
            for w_val, ranks in res['sensitivity'].items():
                for region, score in ranks.items():
                    sens_data.append({"w_AI": w_val, "Region": region, "Score": score})
            df_sens = pd.DataFrame(sens_data)
            df_pivot = df_sens.pivot(index="Region", columns="w_AI", values="Score")
            fig_heat = px.imshow(df_pivot, text_auto=".3f", aspect="auto", color_continuous_scale="Reds")
            st.plotly_chart(fig_heat, use_container_width=True)
        with st.container(border=True):
            st.subheader("4. So sánh phương pháp: TOPSIS vs AHP đơn giản")
            df_comp = pd.DataFrame(res['ranks_comparison'])
            st.dataframe(df_comp, use_container_width=True)

elif page == pages[6]:
    st.title("Bài 7: Tối ưu đa mục tiêu (NSGA-II)")
    col_main, col_ctrl = st.columns([3, 1], gap="large")
    with col_ctrl:
        with st.form("form_module_7"):
            st.markdown("Thông số đầu vào")
            n_gen = st.slider("Số thế hệ", 50, 300, 200, 50)
            pop_size = st.slider("Kích thước quần thể", 50, 200, 100, 50)
            submit_btn = st.form_submit_button("Chạy mô hình", use_container_width=True)
    with col_main:
        with st.spinner("Đang chạy NSGA-II..."):
            res = solve_bai07(n_gen, pop_size)
        if res['n_pareto'] == 0:
            st.error("Không tìm thấy nghiệm Pareto hợp lệ.")
        else:
            with st.container(border=True):
                st.subheader("1. Tập Pareto: 3 mục tiêu đầu (Scatter 3D)")
                fig_3d = go.Figure(data=[go.Scatter3d(x=res['f1_gdp'], y=res['f2_equity'], z=res['f3_env'], mode='markers', marker=dict(size=4, color=res['f1_gdp'], colorscale='Reds'))])
                st.plotly_chart(fig_3d, use_container_width=True)
            with st.container(border=True):
                st.subheader("2. Biểu đồ Tọa độ song song (Parallel Coordinates)")
                fig_parc = go.Figure(data=go.Parcoords(line=dict(color=res['f1_gdp'], colorscale='Reds'), dimensions=list([dict(label='GDP', values=res['f1_gdp']), dict(label='Equity', values=res['f2_equity']), dict(label='Emission', values=res['f3_env']), dict(label='Security', values=res['f4_sec'])])))
                st.plotly_chart(fig_parc, use_container_width=True)
            with st.container(border=True):
                st.subheader("3. Nghiệm thỏa hiệp duy nhất (TOPSIS)")
                top = res['topsis_compromise']
                st.write(f"GDP: {top['GDP']:,.2f} | Equity: {top['Equity_MAD']:,.2f} | Emission: {top['Emission']:,.2f} | Security: {top['Security']:,.2f}")
            with st.container(border=True):
                st.subheader("4. Phân tích Chi phí cơ hội")
                opp = res['opportunity_cost']
                st.warning(f"Hi sinh Bao trùm: {opp['sacrifice']['Equity_MAD_pct']:,.1f}%")

elif page == pages[7]:
    st.title("Bài 8: Tối ưu động liên thời gian")
    col_main, col_ctrl = st.columns([3, 1], gap="large")
    with col_ctrl:
        with st.form("form_module_8"):
            st.markdown("Thông số đầu vào")
            discount = st.slider("Chiết khấu δ", 0.0, 0.15, 0.05, 0.01)
            cap_growth = st.slider("Tăng vốn/năm", 0.02, 0.12, 0.06, 0.01)
            target_ai = st.slider("Mục tiêu AI 2035", 0.5, 1.0, 0.85, 0.05)
            bud_growth = st.slider("Tăng NS/năm", 0.03, 0.15, 0.08, 0.01)
            submit_btn = st.form_submit_button("Chạy mô hình", use_container_width=True)
    with col_main:
        res = solve_bai08(discount=discount, capital_growth=cap_growth, target_ai=target_ai, budget_growth=bud_growth)
        with st.container(border=True):
            st.subheader("1. Tổng phúc lợi tối ưu")
            st.info(f"Tổng phúc lợi tối ưu (Z*): {res['welfare_opt']:,.1f} tỷ VND")
        with st.container(border=True):
            st.subheader("2. Quỹ đạo tối ưu (2026-2035)")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=res['years'], y=res['K'], name='Vốn (K)'))
            fig.add_trace(go.Scatter(x=res['years'], y=res['Y'], name='Sản lượng (Y)'))
            fig.add_trace(go.Scatter(x=res['years'], y=res['C'], name='Tiêu dùng (C)'))
            fig.add_trace(go.Scatter(x=res['years'], y=res['D'], name='Số hóa (D)', yaxis='y2'))
            fig.add_trace(go.Scatter(x=res['years'], y=res['H'], name='Nhân lực (H)', yaxis='y2'))
            fig.add_trace(go.Scatter(x=res['years'], y=res['AI'], name='AI', yaxis='y2', line=dict(dash='dash')))
            fig.update_layout(yaxis2=dict(overlaying='y', side='right'))
            st.plotly_chart(fig, use_container_width=True)
        with st.container(border=True):
            st.subheader("3. Phân tích cú sốc 2028 (Giảm 8% Y)")
            st.metric("Welfare (Có cú sốc)", f"{res['welfare_shock']:,.1f}", delta=f"{res['welfare_shock'] - res['welfare_opt']:,.1f}")
        with st.container(border=True):
            st.subheader("4. Trải đều vs Front-load")
            st.success(f"Chiến lược tốt hơn: {res['better_strategy']}")

elif page == pages[8]:
    st.title("Bài 9: Mô phỏng tác động AI lên lao động")
    col_main, col_ctrl = st.columns([3, 1], gap="large")
    with col_ctrl:
        with st.form("form_module_9"):
            st.markdown("Thông số đầu vào")
            ai_rate = st.slider("Tốc độ áp dụng AI", 0.10, 0.70, 0.30, 0.05)
            retrain = st.slider("Ngân sách đào tạo", 5, 50, 15, 5)
            speed = st.slider("Tốc độ chuyển đổi", 0.1, 1.0, 0.5, 0.1)
            new_job = st.slider("Hệ số việc mới/AI", 0.1, 0.8, 0.4, 0.05)
            submit_btn = st.form_submit_button("Chạy mô hình", use_container_width=True)
    with col_main:
        res = solve_bai09(ai_adoption_rate=ai_rate, retraining_budget=retrain, transition_speed=speed, new_job_multiplier=new_job)
        
        with st.container(border=True):
            st.subheader("1. Phân bổ tối ưu (PuLP)")
            st.metric("Tổng Việc làm ròng (NetJob)", f"{res['total_net']:,.2f} triệu")
            df_sectors = pd.DataFrame(res['sector_table']).T
            st.dataframe(df_sectors.style.format("{:.3f}"), use_container_width=True)

        with st.container(border=True):
            st.subheader("2. Ngưỡng đầu tư đào tạo ngành Chế biến chế tạo (Ngành 2)")
            st.info(f"**Ngưỡng $x_{{H, 2}}$ tối thiểu** để $NetJob_2 \ge 0$ khi tối đa hóa AI ($x_{{AI, 2}}=1$): **{res['threshold_xH2']:.4f}**")

        with st.container(border=True):
            st.subheader("3. Luồng dịch chuyển lao động nhóm dễ tổn thương (Ngành 1, 3, 4)")
            fig_sankey = go.Figure(data=[go.Sankey(
                node = dict(
                  pad = 15,
                  thickness = 20,
                  line = dict(color = "black", width = 0.5),
                  label = res['sankey_nodes']
                ),
                link = dict(
                  source = res['sankey_links']['source'],
                  target = res['sankey_links']['target'],
                  value = res['sankey_links']['value']
                ))])
            fig_sankey.update_layout(title_text="Biểu đồ Sankey: Dịch chuyển lao động phổ thông", font_size=12)
            st.plotly_chart(fig_sankey, use_container_width=True)

        with st.container(border=True):
            st.subheader("4. Ràng buộc mở rộng: Không ngành nào mất quá 5% lao động")
            if res['ext_feasible']:
                st.success("✅ **Khả thi:** Mô hình CÓ THỂ tìm được phân bổ thỏa mãn điều kiện không ngành nào mất >5% lao động.")
            else:
                st.error("❌ **Không khả thi:** Ngân sách đào tạo không đủ hoặc tốc độ chuyển đổi quá chậm để giữ mức mất việc <5% ở tất cả các ngành.")

elif page == pages[9]:
    st.title("Bài 10: Quy hoạch ngẫu nhiên 2 giai đoạn")
    col_main, col_ctrl = st.columns([3, 1], gap="large")
    with col_ctrl:
        with st.form("form_module_10"):
            st.markdown("Thông số đầu vào")
            p1 = st.slider("P(Lạc quan)", 0.0, 1.0, 0.3, 0.05)
            p2 = st.slider("P(Cơ sở)", 0.0, 1.0, 0.45, 0.05)
            p3 = st.slider("P(Bi quan)", 0.0, 1.0, 0.2, 0.05)
            budget = st.slider("Ngân sách GĐ1", 30, 80, 65, 5)
            submit_btn = st.form_submit_button("Chạy mô hình", use_container_width=True)
    with col_main:
        res = solve_bai10(p_optimistic=p1, p_baseline=p2, p_pessimistic=p3, first_stage_cap=budget)
        with st.container(border=True):
            st.subheader("1. So sánh Lợi nhuận kỳ vọng")
            col1, col2, col3 = st.columns(3)
            col1.metric("Giải pháp ngẫu nhiên (SP)", f"{res['sp_value']:,.1f}")
            col2.metric("Kỳ vọng giá trị hoàn hảo (EVPI)", f"{res['evpi']:,.1f}")
            col3.metric("Giá trị của giải pháp ngẫu nhiên (VSS)", f"{res['vss']:,.1f}")
        with st.container(border=True):
            st.subheader("2. Quyết định phân bổ Giai đoạn 1")
            df_alloc = pd.DataFrame(res['sp_alloc']).T
            st.dataframe(df_alloc.style.format("{:.2f}"), use_container_width=True)
        with st.container(border=True):
            st.subheader("3. Robust Optimization")
            categories = ['I', 'D', 'AI', 'H']
            colA, colB = st.columns(2)
            with colA:
                fig_sp = px.pie(names=categories, values=res['x_sp'], title="Phân bổ SP")
                st.plotly_chart(fig_sp, use_container_width=True)
            with colB:
                fig_rob = px.pie(names=categories, values=res['x_rob'], title="Phân bổ Robust")
                st.plotly_chart(fig_rob, use_container_width=True)

elif page == pages[10]:
    st.title("Bài 11: Học tăng cường (Q-learning & DQN)")
    col_main, col_ctrl = st.columns([3, 1], gap="large")
    with col_ctrl:
        with st.form("form_module_11"):
            st.markdown("Thông số đầu vào")
            alpha = st.slider("Learning rate α", 0.01, 0.5, 0.1, 0.01)
            gamma = st.slider("Discount γ", 0.5, 0.99, 0.95, 0.01)
            episodes = st.slider("Số episodes", 1000, 20000, 10000, 1000)
            use_dqn = st.checkbox("Huấn luyện DQN", value=True)
            submit_btn = st.form_submit_button("Chạy mô hình", use_container_width=True)
    with col_main:
        with st.spinner("Đang huấn luyện..."):
            res = solve_bai11(learning_rate=alpha, discount_factor=gamma, episodes=episodes, use_dqn=use_dqn)
        with st.container(border=True):
            st.subheader("1. Đánh giá Learning Curve")
            fig = go.Figure()
            x_q = list(range(0, res['episodes'], max(1, res['episodes']//100)))
            fig.add_trace(go.Scatter(x=x_q, y=res['q_smoothed'], mode='lines', name='Q-Learning', line=dict(color='#3182CE')))
            if len(res['dqn_smoothed']) > 0:
                x_dqn = list(range(0, 20000, max(1, 20000//100)))[:len(res['dqn_smoothed'])]
                fig.add_trace(go.Scatter(x=x_dqn, y=res['dqn_smoothed'], mode='lines', name='DQN (Neural Net)', line=dict(color='#E53E3E')))
            fig.update_layout(title="Tổng phần thưởng trung bình theo Episodes", xaxis_title="Episodes", yaxis_title="Reward")
            st.plotly_chart(fig, use_container_width=True)
            
        with st.container(border=True):
            st.subheader("2. Chính sách tối ưu $\\pi^*(s)$ tại các trạng thái khởi đầu")
            df_policies = pd.DataFrame(list(res['extracted_policies'].items()), columns=["Trạng thái giả định", "Hành động (Policy) được chọn"])
            st.dataframe(df_policies, use_container_width=True)

        with st.container(border=True):
            st.subheader("3. So sánh phần thưởng tích lũy trung bình")
            df_rules = pd.DataFrame(list(res['rules_perf'].items()), columns=["Chính sách", "Phần thưởng trung bình"])
            fig_bar = px.bar(df_rules, x="Chính sách", y="Phần thưởng trung bình", color="Chính sách", title="Hiệu suất so với Rule-based Policies")
            st.plotly_chart(fig_bar, use_container_width=True)

elif page == pages[11]:
    st.title("Bài 12: Đồ án tổng hợp AIDEOM-VN")
    col_main, col_ctrl = st.columns([3, 1], gap="large")
    with col_ctrl:
        with st.form("form_module_12"):
            st.markdown("Thông số đầu vào")
            scenario = st.selectbox("Kịch bản:", ['S1','S2','S3','S4','S5'], index=4,
                format_func=lambda s: {'S1':'S1. Truyền thống','S2':'S2. Số hóa nhanh','S3':'S3. AI dẫn dắt','S4':'S4. Bao trùm số','S5':'S5. Tối ưu cân bằng'}[s])
            budget = st.slider("Ngân sách tổng", 10000, 100000, 50000, 5000)
            submit_btn = st.form_submit_button("Chạy mô hình", use_container_width=True)
    with col_main:
        res = solve_bai12_dashboard(DATA_DIR, budget, scenario)
        st.info(f"**Mô tả kịch bản:** {res['description']}")
        
        tab1, tab2, tab3, tab4 = st.tabs([" Tổng quan & Phân bổ", " Kịch bản so sánh", " Tăng trưởng GDP & Việc làm", " Rủi ro & Vùng miền"])
        with tab1:
            with st.container(border=True):
                st.subheader("Phân bổ ngân sách (Tỷ VND)")
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Hạ tầng (I)", f"{res['allocation']['I']:,.0f}")
                c2.metric("Số hóa (D)", f"{res['allocation']['D']:,.0f}")
                c3.metric("AI", f"{res['allocation']['AI']:,.0f}")
                c4.metric("Nhân lực (H)", f"{res['allocation']['H']:,.0f}")
            
                fig_radar = go.Figure(data=go.Scatterpolar(
                    r=res['radar']['values'],
                    theta=res['radar']['dimensions'],
                    fill='toself', line_color=LINE_COLOR
                ))
                fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, title="Đánh giá tổng hợp đa chiều", height=400)
                st.plotly_chart(fig_radar, use_container_width=True)
                
        with tab2:
            with st.container(border=True):
                st.subheader("So sánh 3 kịch bản chính (Năm 2030)")
                s1 = solve_bai12_dashboard(DATA_DIR, budget, 'S1')
                s3 = solve_bai12_dashboard(DATA_DIR, budget, 'S3')
                s5 = solve_bai12_dashboard(DATA_DIR, budget, 'S5')
            
                comp_data = {
                    "Chỉ số (2030)": ["GDP (Nghìn tỷ VND)", "Tỷ trọng AI (%)", "Điểm Rủi ro", "Mất việc ròng (Ngàn người)"],
                    "S1 (Truyền thống)": [
                        f"{s1['gdp_forecast']['gdp'][-1]:,.2f}",
                        f"{s1['risk']['ai_budget_share']}%",
                        f"{s1['risk']['risk_score']} ({s1['risk']['level']})",
                        f"{s1['labor_impact']['net_total']:,.1f}"
                    ],
                    "S3 (AI dẫn dắt)": [
                        f"{s3['gdp_forecast']['gdp'][-1]:,.2f}",
                        f"{s3['risk']['ai_budget_share']}%",
                        f"{s3['risk']['risk_score']} ({s3['risk']['level']})",
                        f"{s3['labor_impact']['net_total']:,.1f}"
                    ],
                    "S5 (Tối ưu cân bằng)": [
                        f"{s5['gdp_forecast']['gdp'][-1]:,.2f}",
                        f"{s5['risk']['ai_budget_share']}%",
                        f"{s5['risk']['risk_score']} ({s5['risk']['level']})",
                        f"{s5['labor_impact']['net_total']:,.1f}"
                    ]
                }
                st.dataframe(pd.DataFrame(comp_data), use_container_width=True)
                st.info("💡 **Phân tích:** Kịch bản S3 (AI dẫn dắt) cho GDP cao nhất nhưng rủi ro việc làm và an toàn hệ thống lớn. S5 (Cân bằng) hy sinh một phần GDP để duy trì an sinh xã hội và giảm rủi ro.")
        
        with tab3:
            with st.container(border=True):
                st.subheader("Dự báo GDP & Tác động Việc làm")
                colA, colB = st.columns(2)
                fig = px.line(x=res['gdp_forecast']['years'], y=res['gdp_forecast']['gdp'], title="Dự báo GDP (Nghìn tỷ VND)", markers=True)
                fig.update_traces(line_color=LINE_COLOR)
                colA.plotly_chart(fig, use_container_width=True)
            
                fig2 = px.bar(x=res['labor_impact']['sectors'], y=res['labor_impact']['net_jobs'], title="Tác động việc làm ròng",
                    color=res['labor_impact']['net_jobs'], color_continuous_scale='Blues')
                colB.plotly_chart(fig2, use_container_width=True)
            
            with st.container(border=True):
                st.subheader("Xếp hạng Ưu tiên Ngành")
                df_prio = pd.DataFrame(res['priority'])
                fig3 = px.bar(df_prio, x='sector', y='score', title="Điểm ưu tiên theo ngành (Đa tiêu chí)", color='score', color_continuous_scale='Blues')
                st.plotly_chart(fig3, use_container_width=True)
        
        with tab4:
            with st.container(border=True):
                st.subheader("Rủi ro & Xếp hạng Vùng (TOPSIS)")
                col1, col2 = st.columns([1, 2])
                col1.metric("Điểm rủi ro", f"{res['risk']['risk_score']}", delta=res['risk']['level'], delta_color="inverse")
                col1.metric("Tỷ trọng vốn AI", f"{res['risk']['ai_budget_share']}%")
            
                df_topsis = pd.DataFrame(res['topsis'])
                fig4 = px.bar(df_topsis, x='region', y='score', title="Điểm TOPSIS các vùng", text='rank', color='score', color_continuous_scale='Blues')
                col2.plotly_chart(fig4, use_container_width=True)
