import streamlit as st
import matplotlib.pyplot as plt
import pdfplumber
import pandas as pd
from collections import Counter

# BACKEND (UNCHANGED)
from src.predict import predict_clause
from src.clause_splitter import extract_clauses

# PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="AI Legal Risk Analyzer", layout="wide")

# =========================
# PREMIUM UI CSS
# =========================
st.markdown("""
<style>
body {
    background: radial-gradient(circle at top, #1f2a40, #0a0f1c);
}
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #e6edf3;
}
.big-title {
    font-size: 60px;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg, #4facfe, #00f2fe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.subtitle {
    text-align: center;
    color: #9aa4b2;
    margin-bottom: 25px;
}
section[data-testid="stSidebar"] {
    background: #0b0f19;
}
.stButton>button {
    width: 100%;
    border-radius: 10px;
    padding: 12px;
    font-size: 18px;
    background: linear-gradient(90deg, #4facfe, #00f2fe);
    color: black;
    font-weight: bold;
}
.kpi-card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 16px;
    text-align: center;
    transition: 0.3s;
}
.kpi-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 0 25px rgba(0,255,255,0.2);
}
.kpi-value {
    font-size: 38px;
    font-weight: bold;
}
.kpi-label {
    color: #9aa4b2;
}
.clause-box {
    padding: 18px;
    border-radius: 12px;
    background: rgba(255,255,255,0.05);
    margin-bottom: 15px;
}
.high { border-left: 5px solid #ff4d4d; }
.medium { border-left: 5px solid #f1c40f; }
.low { border-left: 5px solid #2ecc71; }
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown("<div class='big-title'>⚖ AI Legal Risk Analyzer</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Smart Contract Risk Intelligence System</div>", unsafe_allow_html=True)
st.markdown("---")

# =========================
# SIDEBAR
# =========================
st.sidebar.title("⚖ Navigation")
page = st.sidebar.radio("Go to", ["🏠 Dashboard", "📄 Clauses", "🧠 Insights"])

show_high_only = st.sidebar.checkbox("🔴 High Risk Only")
search_term = st.sidebar.text_input("🔍 Search Clause")

# =========================
# FILE UPLOAD
# =========================
st.markdown("### 📂 Upload Agreement")
uploaded_file = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])

agreement_text = ""
if uploaded_file:
    with st.spinner("Reading document..."):
        if uploaded_file.type == "application/pdf":
            with pdfplumber.open(uploaded_file) as pdf:
                for p in pdf.pages:
                    agreement_text += p.extract_text() + "\n"
        else:
            agreement_text = uploaded_file.read().decode()

# =========================
# SESSION
# =========================
if "results" not in st.session_state:
    st.session_state.results = None

# =========================
# ANALYZE
# =========================
if st.button("🚀 Analyze Agreement"):
    with st.spinner("Analyzing clauses..."):
        clauses = extract_clauses(agreement_text)

        results = []
        counter = Counter()
        high = medium = low = 0

        for clause in clauses:
            category, risk, _, cat_conf, risk_conf, _, explanation = predict_clause(clause)

            results.append({
                "clause": clause,
                "category": category,
                "risk": risk,
                "cat_conf": cat_conf,
                "risk_conf": risk_conf,
                "explanation": explanation
            })

            counter[category] += 1

            if risk == "High": high += 1
            elif risk == "Medium": medium += 1
            else: low += 1

        total = high + medium + low
        score = ((high*2 + medium)/(total*2))*100 if total else 0

        st.session_state.results = {
            "data": results,
            "high": high,
            "medium": medium,
            "low": low,
            "score": score,
            "categories": counter
        }

# =========================
# HIGHLIGHT FUNCTION
# =========================
def highlight_keywords(text):
    keywords = ["terminate", "penalty", "liability", "breach", "notice", "refund"]
    for word in keywords:
        text = text.replace(word, f"<span style='color:#ff4d4d;font-weight:bold'>{word}</span>")
    return text

# =========================
# PDF FUNCTION
# =========================
def generate_pdf(data):
    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("AI LEGAL ANALYSIS REPORT", styles["Title"]))
    elements.append(Spacer(1,10))

    elements.append(Paragraph(
        f"High: {data['high']} | Medium: {data['medium']} | Low: {data['low']} | Score: {data['score']:.2f}%",
        styles["Normal"]
    ))

    for i,item in enumerate(data["data"],1):
        elements.append(Paragraph(f"<b>Clause {i}</b>: {item['clause']}", styles["Normal"]))
        elements.append(Paragraph(f"Risk: {item['risk']} | {item['explanation']}", styles["Normal"]))
        elements.append(Spacer(1,10))

    doc.build(elements)
    return "report.pdf"

# =========================
# DASHBOARD
# =========================
if page == "🏠 Dashboard" and st.session_state.results:

    d = st.session_state.results

    st.markdown("## 📊 Overview")

    c1,c2,c3,c4 = st.columns(4)

    c1.markdown(f"<div class='kpi-card'><div class='kpi-value'>{d['high']}</div><div class='kpi-label'>High</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='kpi-card'><div class='kpi-value'>{d['medium']}</div><div class='kpi-label'>Medium</div></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='kpi-card'><div class='kpi-value'>{d['low']}</div><div class='kpi-label'>Low</div></div>", unsafe_allow_html=True)
    c4.markdown(f"<div class='kpi-card'><div class='kpi-value'>{d['score']:.1f}%</div><div class='kpi-label'>Score</div></div>", unsafe_allow_html=True)

    st.progress(int(d["score"]))

    st.markdown("## 🎯 Risk Status")

    if d["high"] > 0:
        st.error(f"🚨 High Risk Detected ({d['high']} clauses)")
    elif d["medium"] > 0:
        st.warning(f"⚠ Moderate Risk ({d['medium']} clauses)")
    else:
        st.success("✅ Low Risk Agreement")

    st.markdown("## 🚨 Most Critical Clause")

    sorted_clauses = sorted(d["data"], key=lambda x: x["risk_conf"], reverse=True)
    if sorted_clauses:
        st.error(sorted_clauses[0]["clause"])

    # =========================
    # 🎯 DONUT CHART (FIXED)
    # =========================
    st.markdown("## 📊 Risk Distribution")

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        fig, ax = plt.subplots(figsize=(3,3))

        sizes = [d["high"], d["medium"], d["low"]]
        labels = ["High", "Medium", "Low"]
        colors = ["#ff4d4d", "#f1c40f", "#2ecc71"]

        wedges, _, _ = ax.pie(
            sizes,
            labels=None,
            autopct='%1.0f%%',
            startangle=90,
            colors=colors,
            wedgeprops=dict(width=0.30)
        )

        ax.text(0, 0, f"{d['score']:.0f}%", 
                ha='center', va='center', 
                fontsize=14, fontweight='bold')

        ax.legend(wedges, labels, 
                  loc="lower center", 
                  bbox_to_anchor=(0.5, -0.2), 
                  ncol=3)

        st.pyplot(fig)


    if st.button("📄 Generate PDF"):
        path = generate_pdf(d)
        with open(path,"rb") as f:
            st.download_button("⬇ Download PDF", f, "report.pdf")

# =========================
# CLAUSES + INSIGHTS SAME AS BEFORE
# =========================
if page == "📄 Clauses" and st.session_state.results:

    st.markdown("## 📄 Clause Analysis")

    for i,item in enumerate(st.session_state.results["data"],1):

        clause = item["clause"]

        if search_term and search_term.lower() not in clause.lower():
            continue
        if show_high_only and item["risk"]!="High":
            continue

        styled = highlight_keywords(clause)

        cls = "low"
        if item["risk"]=="High": cls="high"
        elif item["risk"]=="Medium": cls="medium"

        st.markdown(f"""
        <div class='clause-box {cls}'>
        <b>Clause {i}</b><br><br>
        {styled}<br><br>
        <b>Risk:</b> {item['risk']} ({item['risk_conf']}%)<br>
        <b>Explanation:</b> {item['explanation']}
        </div>
        """, unsafe_allow_html=True)

# =========================
# INSIGHTS
# =========================
if page == "🧠 Insights" and st.session_state.results:

    d = st.session_state.results

    st.markdown("## 🧠 Smart Insights")

    if d["high"] > 0:
        st.error("🚨 High-risk clauses detected")
    elif d["medium"] > 0:
        st.warning("⚠ Moderate risks present")
    else:
        st.success("✅ Agreement looks safe")

    st.markdown("## 🔥 Top Risky Clauses")

    high_risk = [c for c in d["data"] if c["risk"] == "High"]
    for item in high_risk[:3]:
        st.error(item["clause"][:200] + "...")

    st.markdown("## 📊 Category Table")

    df = pd.DataFrame(list(d["categories"].items()), columns=["Category", "Count"])
    st.dataframe(df)

    st.markdown("## 💡 Recommendations")

    st.info("""
    • Review termination clauses  
    • Check penalty and liability  
    • Ensure payment clarity  
    • Avoid vague conditions  
    """)