import json
import os
from datetime import datetime
from io import BytesIO

import streamlit as st
from PIL import Image

APP_NAME = "Multimodal Construction Intelligence Platform"

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------ Styling -------------

st.markdown("""
<style>
    .stApp {
        background: #f4f7fb;
        color: #1e293b;
    }

    section[data-testid="stSidebar"] {
        background: #132238;
    }

    section[data-testid="stSidebar"] * {
        color: #f5f7fb;
    }

    .hero {
        padding: 1.5rem;
        border-radius: 18px;
        color: #ffffff !important;
        background: linear-gradient(120deg, #132238, #24557a);
        margin-bottom: 1rem;
        box-shadow: 0 8px 28px rgba(19,34,56,.16);
    }

    .hero h1, .hero p {
        color: #ffffff !important;
    }

    .hero h1 {
        margin: 0;
        font-size: 2rem;
    }

    .hero p {
        margin-top: .5rem;
    }

    .stApp h1, .stApp h2, .stApp h3,
    .stApp label, .stApp p, .stApp li {
        color: #1e293b;
    }

    .stApp [data-testid="stMetric"] {
        background: #ffffff;
        color: #1e293b;
        padding: 14px;
        border-radius: 12px;
        border: 1px solid #dce5ef;
    }

    .stApp [data-testid="stMetricLabel"],
    .stApp [data-testid="stMetricValue"] {
        color: #1e293b;
    }

    .stApp [data-testid="stAlert"] {
        color: #1e293b;
    }

    .pill {
        display: inline-block;
        padding: .35rem .7rem;
        border-radius: 999px;
        font-weight: 700;
        background: #e0ebf8;
        color: #193754 !important;
    }

    .small-note {
        color: #536579;
        font-size: .9rem;
    }


    /* Fix sidebar text contrast */
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] li,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] strong,
    section[data-testid="stSidebar"] em,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #f5f7fb !important;
    }

    /* Keep sidebar headings bright */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }

    /* Make the sidebar information box readable */
    section[data-testid="stSidebar"] [data-testid="stAlert"] {
        background: #24476b !important;
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"] [data-testid="stAlert"] p {
        color: #ffffff !important;
    }

    /* Ensure main page text stays dark on its light background */
    .stApp .main p,
    .stApp .main li,
    .stApp .main label {
        color: #1e293b;
    }


    /* Planning tab: readable download button */
    .stApp [data-testid="stDownloadButton"] button {
        background: #24557a !important;
        color: #ffffff !important;
        border: none !important;
    }

    .stApp [data-testid="stDownloadButton"] button p,
    .stApp [data-testid="stDownloadButton"] button span {
        color: #ffffff !important;
    }

    /* Planning tab: readable prompt text area */
    .stApp [data-testid="stTextArea"] textarea {
        background: #ffffff !important;
        color: #1e293b !important;
        border: 1px solid #b8c8da !important;
        caret-color: #1e293b !important;
    }

    .stApp [data-testid="stTextArea"] label,
    .stApp [data-testid="stTextArea"] label p {
        color: #1e293b !important;
    }

    .stApp [data-testid="stTextArea"] textarea::placeholder {
        color: #64748b !important;
        opacity: 1 !important;
    }


    /* Chatbot input: readable text */
    .stApp [data-testid="stChatInput"] textarea {
        color: #1e293b !important;
        -webkit-text-fill-color: #1e293b !important;
        background-color: #ffffff !important;
        caret-color: #1e293b !important;
    }

    .stApp [data-testid="stChatInput"] textarea::placeholder {
        color: #64748b !important;
        -webkit-text-fill-color: #64748b !important;
        opacity: 1 !important;
    }

    /* Chat messages and chatbot responses */
    .stApp [data-testid="stChatMessage"] {
        background-color: #ffffff !important;
        border: 1px solid #dce5ef;
        border-radius: 12px;
        padding: 12px;
    }

    .stApp [data-testid="stChatMessage"] p,
    .stApp [data-testid="stChatMessage"] li,
    .stApp [data-testid="stChatMessage"] span {
        color: #1e293b !important;
        -webkit-text-fill-color: #1e293b !important;
    }

    /* Keep chatbot labels readable */
    .stApp [data-testid="stChatInput"] label {
        color: #1e293b !important;
    }



</style>
""", unsafe_allow_html=True)


# ---------- Demo data ----------
def demo_safety():
    return {
        "safety_score": 78,
        "overall_status": "Needs Improvement",
        "ppe_detection": {
            "helmet": {"status": "Partially visible / uncertain", "compliant": False},
            "high_visibility_vest": {"status": "Visible on some workers", "compliant": False},
            "steel_toe_boots": {"status": "Not verifiable from image", "compliant": None},
            "safety_harness": {"status": "Not applicable or not visible; verify work-at-height tasks", "compliant": None}
        },
        "site_hazards": [
            {"hazard": "Potential missing head protection", "severity": "High",
             "remedy": "Stop affected work until correctly fitted helmets are verified."},
            {"hazard": "PPE details obscured by image angle", "severity": "Medium",
             "remedy": "Capture closer, well-lit photos from multiple angles and conduct a physical site inspection."}
        ],
        "limitations": "Demonstration output only; not a real image analysis."
    }

def demo_crack():
    return {
        "defect_type": "Hairline",
        "estimated_crack_width_mm": None,
        "root_causes": ["Cannot be established from a photo alone", "Possible shrinkage or thermal movement; requires site context"],
        "recommended_repairs": ["Measure crack width and monitor progression", "Have a qualified structural engineer inspect before selecting a repair"],
        "urgency": "Inspection recommended",
        "limitations": "Demonstration output only. A photo cannot establish structural safety or reliably measure crack width."
    }

def extract_json(text):
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
        if text.endswith("```"):
            text = text[:-3]
    start, end = text.find("{"), text.rfind("}")
    if start >= 0 and end > start:
        text = text[start:end+1]
    return json.loads(text)

def analyze_image_with_gemini(image, prompt, api_key):
    """Optional Gemini integration. Key is held in session state, never written to disk."""
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-3.8-flash")
        response = model.generate_content([prompt, image])
        return extract_json(response.text)
    except Exception as exc:
        raise RuntimeError(
            "Gemini analysis failed. Check your API key, model availability, and network connection. "
            f"Technical detail: {type(exc).__name__}: {exc}"
        ) from exc

def json_download(data, filename):
    return json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")

def money_inr(value):
    if value >= 1e7:
        return f"₹{value / 1e7:.2f} Cr"
    if value >= 1e5:
        return f"₹{value / 1e5:.2f} Lakh"
    return f"₹{value:,.0f}"

def render_json_report(data, prefix):
    st.json(data, expanded=True)
    st.download_button(
        "⬇️ Download JSON report",
        data=json_download(data, f"{prefix}_{datetime.now():%Y%m%d_%H%M%S}.json"),
        file_name=f"{prefix}_report.json",
        mime="application/json",
        key=f"download_{prefix}_{st.session_state.get(prefix+'_nonce', 0)}",
    )

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 🏗️ Construction AI")
    st.caption("Skill Wallet Capstone · Project 1")
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    st.caption("No key? The app runs with clearly labelled demo outputs.")
    st.divider()
    st.markdown("### Architecture")
    st.markdown("**UI:** Streamlit  \n**Vision / reasoning:** Gemini (optional)  \n**Image handling:** Pillow  \n**Reports:** JSON downloads  \n**Storage:** No external database")
    st.divider()
    st.markdown("### Feature navigation")
    st.markdown("1. Site Safety & PPE Audit  \n2. Crack Diagnostics  \n3. Planning & Valuation  \n4. Site Assistant & Weather")
    st.info("AI output is decision support, not a substitute for an on-site safety officer or licensed structural engineer.")

st.markdown(f"""
<div class="hero">
  <h1>🏗️ {APP_NAME}</h1>
  <p>Multimodal construction intelligence for safer sites, clearer planning, and faster decisions.</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "🦺 Site Safety & PPE", "🧱 Crack Diagnostics",
    "📐 Planning & Valuation", "🌦️ Site Assistant"
])

# ---------- Tab 1: PPE audit ----------
with tab1:
    st.subheader("Site Safety & PPE Audit")
    st.write("Upload a clear site photo. For best results, include workers' head-to-toe PPE and the surrounding work area.")
    safety_file = st.file_uploader("Construction site photo", type=["jpg", "jpeg", "png"], key="safety_image")
    if safety_file:
        try:
            img = Image.open(safety_file).convert("RGB")
            left, right = st.columns([1, 1.2], gap="large")
            with left:
                st.image(img, caption="Uploaded site photo", use_container_width=True)
            with right:
                st.markdown("**Analysis mode**")
                mode = "Live Gemini vision" if api_key else "Demonstration mode"
                st.markdown(f'<span class="pill">{mode}</span>', unsafe_allow_html=True)
                if st.button("Run PPE audit", type="primary", key="run_safety"):
                    with st.spinner("Reviewing image and preparing structured report..."):
                        if api_key:
                            prompt = """
You are a construction-site safety decision-support assistant. Inspect the supplied image conservatively.
Return ONLY valid JSON with keys:
safety_score (integer 0-100), overall_status (Compliant, Needs Improvement, Unsafe, or Unable to Determine),
ppe_detection (object with helmet, high_visibility_vest, steel_toe_boots, safety_harness; each has status and compliant true/false/null),
site_hazards (array of objects with hazard, severity [Low, Medium, High, Critical], remedy),
limitations (string).
Do not claim equipment is absent if it is not visible. Mark uncertain or not-verifiable when the image cannot support a conclusion.
Do not claim legal compliance from a photo. Mention that OSHA/Indian requirements and site-specific rules must be verified by a qualified safety professional.
"""
                            try:
                                result = analyze_image_with_gemini(img, prompt, api_key)
                                st.session_state["safety_result"] = result
                            except RuntimeError as e:
                                st.error(str(e))
                        else:
                            st.session_state["safety_result"] = demo_safety()
                            st.session_state["safety_result"]["limitations"] = "DEMO MODE: this is sample data and was not inferred from the uploaded image."
                result = st.session_state.get("safety_result")
                if result:
                    st.markdown("### Audit summary")
                    m1, m2 = st.columns(2)
                    m1.metric("Safety score", f"{result.get('safety_score', '—')}/100")
                    m2.metric("Overall status", result.get("overall_status", "Unknown"))
                    st.markdown("**PPE checklist**")
                    ppe = result.get("ppe_detection", {})
                    if isinstance(ppe, dict):
                        for item, details in ppe.items():
                            details = details if isinstance(details, dict) else {"status": str(details)}
                            status = details.get("status", "Unknown")
                            compliant = details.get("compliant")
                            icon = "✅" if compliant is True else ("❌" if compliant is False else "⚠️")
                            st.write(f"{icon} **{item.replace('_', ' ').title()}** — {status}")
                    st.markdown("**Hazards and corrective actions**")
                    hazards = result.get("site_hazards", [])
                    if hazards:
                        for h in hazards:
                            severity = h.get("severity", "Unknown")
                            st.warning(f"**{severity} — {h.get('hazard', 'Unspecified hazard')}**\n\n{h.get('remedy', 'Obtain qualified review.')}")
                    else:
                        st.write("No hazards were returned; this is not proof that the site is safe.")
                    st.caption(result.get("limitations", "Visual inspection has limitations."))
                    render_json_report(result, "safety")
        except Exception as e:
            st.error(f"Could not open image: {e}")

# ---------- Tab 2: crack diagnostics ----------
with tab2:
    st.subheader("Crack Diagnostics & Structural Integrity")
    st.write("Use a sharp, well-lit photo with a scale reference if possible. Width estimates from images are unreliable without calibration.")
    crack_file = st.file_uploader("Concrete or wall surface photo", type=["jpg", "jpeg", "png"], key="crack_image")
    if crack_file:
        try:
            crack_img = Image.open(crack_file).convert("RGB")
            c1, c2 = st.columns([1, 1.2], gap="large")
            with c1:
                st.image(crack_img, caption="Uploaded surface photo", use_container_width=True)
            with c2:
                if st.button("Assess visible defect", type="primary", key="run_crack"):
                    with st.spinner("Preparing defect assessment..."):
                        if api_key:
                            prompt = """
Act as a conservative construction defect triage assistant. Inspect the supplied image and return ONLY valid JSON:
defect_type (one of Hairline, Settlement, Structural Shear, Thermal Expansion, Spalling, Other, Unable to Determine),
estimated_crack_width_mm (number or null; use null if there is no calibrated scale),
root_causes (array of strings),
recommended_repairs (array of strings),
urgency (Routine monitoring, Inspection recommended, Urgent professional assessment, Immediate evacuation / emergency assessment),
limitations (string).
Do not diagnose structural integrity or prescribe definitive repairs from a photo. Clearly state that width needs on-site measurement and a qualified structural engineer must assess potentially structural cracks. If there are signs of immediate danger, recommend clearing the area and seeking emergency professional assessment.
"""
                            try:
                                st.session_state["crack_result"] = analyze_image_with_gemini(crack_img, prompt, api_key)
                            except RuntimeError as e:
                                st.error(str(e))
                        else:
                            st.session_state["crack_result"] = demo_crack()
                            st.session_state["crack_result"]["limitations"] = "DEMO MODE: sample triage only; not inferred from the uploaded image."
                result = st.session_state.get("crack_result")
                if result:
                    st.markdown(f"**Defect category:** {result.get('defect_type', 'Unknown')}")
                    st.markdown(f"**Estimated width:** {str(result.get('estimated_crack_width_mm') if result.get('estimated_crack_width_mm') is not None else 'Not reliably measurable from this image')} mm")
                    st.markdown(f"**Urgency:** {result.get('urgency', 'Requires professional review')}")
                    st.markdown("**Possible causes**")
                    for cause in result.get("root_causes", []):
                        st.write(f"• {cause}")
                    st.markdown("**Recommended next steps**")
                    for repair in result.get("recommended_repairs", []):
                        st.write(f"• {repair}")
                    st.warning("If a crack is widening, diagonal near columns/beams, accompanied by sagging, falling concrete, or unusual sounds, keep people away and contact a qualified structural engineer promptly.")
                    st.caption(result.get("limitations", "Photo-based triage cannot certify structural safety."))
                    render_json_report(result, "crack")
        except Exception as e:
            st.error(f"Could not open image: {e}")

# ---------- Tab 3: planning / valuation ----------
with tab3:
    st.subheader("Project Planning & Indicative Real Estate Valuation")
    st.caption("Planning estimates only. Replace assumptions with local BOQ, current material rates, and comparable market transactions before using commercially.")
    col1, col2 = st.columns(2)
    with col1:
        structure = st.selectbox("Structure type", ["Residential", "Commercial", "Industrial", "Institutional"])
        area = st.number_input("Built-up area (sq ft)", min_value=100, max_value=2_000_000, value=2500, step=100)
        tier = st.selectbox("Location tier", ["Tier 1", "Tier 2", "Tier 3"])
    with col2:
        completion = st.slider("Completion percentage", 0, 100, 35, 5)
        floors = st.number_input("Number of floors", min_value=1, max_value=100, value=2)
        custom_rate = st.number_input("Estimated construction cost (₹/sq ft)", min_value=800, max_value=20000, value=2200, step=100)
    tier_value = {"Tier 1": 1.25, "Tier 2": 1.0, "Tier 3": 0.82}[tier]
    structure_factor = {"Residential": 1.0, "Commercial": 1.18, "Industrial": 0.95, "Institutional": 1.08}[structure]
    total_budget = float(area * custom_rate * structure_factor)
    incurred = total_budget * completion / 100
    market_multiplier = {"Tier 1": 1.65, "Tier 2": 1.25, "Tier 3": 0.95}[tier]
    asset_value = area * custom_rate * market_multiplier * structure_factor
    # Approximate thumb rules only; actual quantities depend on structural design and BOQ.
    steel_kg = area * 4.0 * (1 + max(floors - 2, 0) * 0.06)
    cement_bags = area * 0.40 * (1 + max(floors - 2, 0) * 0.04)
    a, b, c = st.columns(3)
    a.metric("Indicative total budget", money_inr(total_budget))
    b.metric("CapEx incurred to date", money_inr(incurred))
    c.metric("Indicative asset valuation", money_inr(asset_value))
    st.progress(completion / 100, text=f"Milestone progress: {completion}%")
    st.markdown("### Preliminary material planning")
    m1, m2 = st.columns(2)
    m1.metric("Steel thumb-rule estimate", f"{steel_kg:,.0f} kg", help="Illustrative 4 kg/sq ft baseline; not a structural quantity take-off.")
    m2.metric("Cement thumb-rule estimate", f"{cement_bags:,.0f} bags", help="Illustrative 0.40 bags/sq ft baseline; verify against design and BOQ.")
    report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "structure_type": structure,
        "built_up_area_sqft": area,
        "location_tier": tier,
        "completion_percent": completion,
        "floors": floors,
        "assumed_cost_inr_per_sqft": custom_rate,
        "indicative_total_budget_inr": round(total_budget, 2),
        "estimated_capex_incurred_inr": round(incurred, 2),
        "indicative_asset_valuation_inr": round(asset_value, 2),
        "illustrative_steel_kg": round(steel_kg, 1),
        "illustrative_cement_bags": round(cement_bags, 1),
        "assumptions": "Indicative formulas only. Market valuation and material quantities require local professional verification."
    }
    st.download_button("⬇️ Download planning estimate", json_download(report, "planning_estimate.json"),
                       file_name="planning_estimate.json", mime="application/json")
    st.markdown("### Conceptual 3D rendering prompt")
    render_prompt = st.text_area(
        "Prompt for an image-generation service",
        value=f"Photorealistic conceptual architectural visualization of a {structure.lower()} building, {floors} floors, approximately {area:,} square feet built-up area, contemporary Indian context, realistic construction materials, professional daylight architectural render, no text, no logos.",
        height=100,
    )
    st.caption("This app generates a prompt only. Connect an approved image-generation API separately if you need rendered images.")

# ---------- Tab 4: assistant and weather ----------
with tab4:
    st.subheader("Daily Site Assistant & Weather-Aware Advisory")
    weather = st.selectbox("Today's site condition", ["Normal", "High Wind", "Heavy Rain", "Extreme Heat"])
    advisories = {
        "Normal": [
            "Complete toolbox talks and verify permits before work starts.",
            "Inspect access routes, scaffolds, lifting gear, and PPE.",
            "Record near misses and keep emergency access clear."
        ],
        "High Wind": [
            "Pause crane and lifting operations when wind exceeds equipment or lift-plan limits.",
            "Secure loose materials, temporary roofing, hoardings, and elevated tools.",
            "Reassess work-at-height and scaffold conditions before restarting."
        ],
        "Heavy Rain": [
            "Stop work in flooded, unstable, or lightning-exposed areas; follow the site emergency plan.",
            "Isolate electrical equipment where water ingress is possible; only qualified personnel should restore power.",
            "Reassess excavations, slopes, access roads, and formwork. Protect fresh concrete and follow the approved curing/specification plan."
        ],
        "Extreme Heat": [
            "Schedule strenuous work for cooler hours where feasible and provide shaded recovery areas.",
            "Provide drinking water, acclimatization, work-rest cycles, and buddy checks for heat illness.",
            "Follow concrete placement, finishing, and curing procedures for hot-weather conditions specified by the engineer."
        ]
    }
    st.markdown(f"### Advisory: {weather}")
    for item in advisories[weather]:
        if weather != "Normal":
            st.warning(item)
        else:
            st.info(item)

    st.divider()
    st.markdown("### Construction engineering assistant")
    st.caption("Ask about planning, material basics, site processes, or safety checklists. Responses are general guidance, not engineering approval.")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    user_q = st.chat_input("Ask a construction/site question…", key="site_chat_input")
    if user_q:
        st.session_state.chat_history.append({"role": "user", "content": user_q})
        if api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-3.8-flash")
                history_text = "\n".join(
                    f'{m["role"].upper()}: {m["content"]}' for m in st.session_state.chat_history[-10:]
                )
                response = model.generate_content(
                    "You are a cautious construction site assistant. Provide concise, practical general guidance. "
                    "Do not certify structural safety or replace licensed professionals. For immediate hazards, "
                    "prioritize stopping work, isolating the area, and contacting qualified site leadership.\n\n" + history_text
                )
                answer = response.text
            except Exception as e:
                answer = f"I couldn't reach Gemini right now ({type(e).__name__}). Please retry or use the demo mode. For safety-critical decisions, contact the site engineer."
        else:
            q = user_q.lower()
            if any(word in q for word in ["crack", "beam", "column", "structural"]):
                answer = "For a potentially structural crack, document its location and changes, keep people away if there are signs of movement or falling material, and arrange a qualified structural engineer's inspection. A photo alone cannot confirm safety."
            elif any(word in q for word in ["rain", "weather", "wind", "heat", "hot"]):
                answer = f"For today's selected condition ({weather}), use the advisory checklist above, follow your site emergency plan, and restart affected work only after the responsible supervisor verifies conditions."
            elif any(word in q for word in ["cost", "budget", "cement", "steel", "estimate"]):
                answer = "Start with a measured BOQ, approved drawings, local supplier quotations, labor and equipment rates, taxes, contingency, and escalation assumptions. The planner tab uses thumb rules only and is not a tender estimate."
            else:
                answer = "Demo assistant: clarify the task, check the approved drawings/method statement, use the relevant site checklist, and escalate safety-critical or design decisions to the responsible qualified professional. Add a Gemini API key for AI-generated responses."
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()

st.divider()
st.caption("© Skill Wallet Capstone Project 1 · Demo estimates are illustrative. Always verify with qualified construction, safety, and valuation professionals.")
