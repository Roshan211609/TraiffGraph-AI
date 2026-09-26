import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from backend.tariff_engine import analyze_scenario
from backend.graph_engine import build_graph_figure
from backend.model import explain_exposure
from backend.database import init_db, save_scenario, get_recent_scenarios

# Full list of countries
COUNTRIES = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Argentina", "Armenia", "Australia", 
    "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", 
    "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", 
    "Bulgaria", "Burkina Faso", "Burundi", "Cambodia", "Cameroon", "Canada", "Chile", "China", 
    "Colombia", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Dominican Republic", 
    "Ecuador", "Egypt", "El Salvador", "Estonia", "Ethiopia", "Fiji", "Finland", "France", "Georgia", 
    "Germany", "Ghana", "Greece", "Guatemala", "Haiti", "Honduras", "Hungary", "Iceland", "India", 
    "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", 
    "Kazakhstan", "Kenya", "Kuwait", "Latvia", "Lebanon", "Libya", "Lithuania", "Luxembourg", 
    "Madagascar", "Malaysia", "Maldives", "Mali", "Malta", "Mexico", "Moldova", "Monaco", "Mongolia", 
    "Montenegro", "Morocco", "Myanmar", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Nigeria", 
    "North Korea", "Norway", "Oman", "Pakistan", "Panama", "Paraguay", "Peru", "Philippines", "Poland", 
    "Portugal", "Qatar", "Romania", "Russia", "Saudi Arabia", "Senegal", "Serbia", "Singapore", 
    "Slovakia", "Slovenia", "South Africa", "South Korea", "Spain", "Sri Lanka", "Sudan", "Sweden", 
    "Switzerland", "Syria", "Taiwan", "Thailand", "Tunisia", "Turkey", "Uganda", "Ukraine", 
    "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Venezuela", 
    "Vietnam", "Yemen", "Zambia", "Zimbabwe"
]

st.set_page_config(page_title="TariffGraph AI", page_icon="🌐", layout="wide")
init_db()

st.markdown("""
<style>
.main-title {font-size: 2.5rem; font-weight: 800; margin-bottom: 0;}
.subtitle {font-size: 1.05rem; color: #666; margin-bottom: 1rem;}
.card {padding: 18px; border-radius: 14px; border: 1px solid #ddd; background: #fafafa;}
</style>
""", unsafe_allow_html=True)

st.title("🌐 TariffGraph AI")
st.markdown('<div class="subtitle">AI-powered supply-chain ripple-effect simulator</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Scenario")
    product = st.selectbox("Product", ["Electronics", "Automotive Components", "Textiles", "Machinery"])
    origin = st.selectbox("Import source", COUNTRIES)
    market = st.selectbox("Target market", COUNTRIES)
    current_tariff = st.slider("Current tariff (%)", 0, 100, 10)
    new_tariff = st.slider("Scenario tariff (%)", 0, 100, 25)
    st.caption("Demo uses simulated trade relationships. Replace with verified public data for a real-world deployment.")
    analyze = st.button("🔎 Analyze Impact", type="primary", use_container_width=True)

if "result" not in st.session_state or analyze:
    st.session_state.result = analyze_scenario(product, origin, market, current_tariff, new_tariff)

r = st.session_state.result

c1, c2, c3, c4 = st.columns(4)
c1.metric("Exposure Score", f"{r['exposure_score']}/100")
c2.metric("Tariff Change", f"{r['tariff_change']:+.1f} pts")
c3.metric("Estimated Cost Impact", f"{r['cost_impact_pct']:.1f}%")
c4.metric("Risk Level", r["risk_level"])

st.divider()

st.subheader("📈 Real-Time Tariff & Cost Comparison")

# Build data for the interactive line chart
chart_data = pd.DataFrame({
    "Category": ["Current Tariff (%)", "Scenario Tariff (%)", "Cost Impact (%)"],
    "Percentage": [current_tariff, new_tariff, r["cost_impact_pct"]]
})

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=chart_data["Category"],
    y=chart_data["Percentage"],
    mode='lines+markers+text',
    text=[f"{v:.1f}%" for v in chart_data["Percentage"]],
    textposition="top center",
    line=dict(color='#0068c9', width=4),
    marker=dict(size=12, color='#ff4b4b')
))

fig.update_layout(
    title=f"Impact Trend: {origin} ➔ {market} ({product})",
    yaxis_title="Percentage (%)",
    template="plotly_white",
    height=400
)

st.plotly_chart(fig, use_container_width=True)

# --- BOB AI ANALYZE IMPACT SECTION ---
st.divider()
st.subheader("🤖 Bob AI Impact Analysis")

if analyze:
    with st.status("🤖 Bob AI is evaluating trade corridors and supply chain risk...", expanded=True) as status:
        # Generate model insights based on scenario parameters
        summary = explain_exposure(r)
        status.update(label="Analysis complete!", state="complete", expanded=True)
        
    st.info(f"**Bob AI Executive Summary:**\n\n{summary}")
else:
    st.caption("Click **🔎 Analyze Impact** in the sidebar to generate a full scenario breakdown from Bob AI.")