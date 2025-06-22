import streamlit as st
import random
import base64
import openai
from backend.gemini_agent import gemini_extract_features
from backend.claude_agent import summarize_market, create_launch_plan
from backend.groq_agent import query_groq
from backend.compliance_agent import compliance_check
import os

# ---- OpenAI DALL·E 3 setup ----
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # set in .env or your dashboard
openai.api_key = OPENAI_API_KEY

st.set_page_config(page_title="StartupMesh: AGI x Y Combinator", page_icon="🚀", layout="wide")

# --- Random AI-City Image for background only ---
city_images = [
    "ai-generated-8229795_1280.jpg",
    "DALL·E 2025-06-22 06.10.47 - A futuristic skyline inspired by New York, Shanghai, and Dubai, featuring thousands of skyscrapers with flowing curves and opalescent windows. These t.webp",
    "ai-generated-futuristic-city-at-night-futuristic-city-3d-rendering-ai-generated-free-photo.jpg"
]
skyline_image = random.choice(city_images)
with open(skyline_image, "rb") as img_file:
    b64_img = base64.b64encode(img_file.read()).decode()

# --- Majestic Animated CSS ---
st.markdown("""
<style>
.stApp {
    background: linear-gradient(120deg, #13132a 0%, #1f1045 100%) !important;
    animation: neonbg 10s ease-in-out infinite alternate;
    min-height: 100vh;
    font-family: 'Orbitron', 'Roboto', sans-serif;
}
@keyframes neonbg {
    0% { background: linear-gradient(120deg, #13132a 0%, #1f1045 100%);}
    40% { background: linear-gradient(120deg, #18124b 0%, #27326e 100%);}
    65% { background: linear-gradient(120deg, #2a195c 0%, #0035a5 100%);}
    100% { background: linear-gradient(120deg, #101a3e 0%, #371e6f 100%);}
}
.hero-img-container {
    position: relative;
    text-align: center;
    margin-bottom: -1.3rem;
}
.hero-img-title {
    position: absolute;
    top: 7.5%;
    left: 0;
    width: 100%;
    color: #fff;
    font-size: 2.35rem;
    text-shadow: 0 0 24px #00f9ff, 0 0 9px #fc03be;
    font-weight: 800;
    letter-spacing: 1.3px;
    background: rgba(0,0,0,0.26);
    padding: 10px 0 6px 0;
    border-radius: 18px;
    z-index: 2;
}
.neon-card {
    background: rgba(22,25,52,0.97);
    border-radius: 22px;
    border: 2.5px solid #00f9ff77;
    box-shadow:
        0 0 12px 2px #00f9ff,
        0 0 30px 4px #fc03be55,
        0 0 2px #fff8;
    padding: 1.3rem 1.7rem 1.3rem 1.7rem;
    margin: 1.1rem 0 1.3rem 0;
    transition: box-shadow 0.4s;
    font-family: 'Share Tech Mono', 'Menlo', monospace;
}
.glow-label {
    color: #fc03be;
    font-weight: 700;
    font-size: 1.13rem;
    letter-spacing: 1.2px;
    margin-bottom: 0.2rem;
    text-shadow: 0 0 8px #fc03be, 0 0 8px #00f9ff;
}
.impact-badge {
    display: inline-block;
    background: linear-gradient(90deg, #0ff 10%, #fc03be 90%);
    color: #1c1b29;
    border-radius: 14px;
    padding: 0.23em 0.95em;
    margin-left: 10px;
    font-weight: 700;
    letter-spacing: 1.4px;
    font-size: 1.03rem;
    box-shadow: 0 0 10px #fc03be55, 0 0 16px #00f9ff44;
    text-shadow: 0 0 6px #fff, 0 0 2px #00f9ff;
    animation: impactpulse 2.4s infinite alternate;
}
@keyframes impactpulse {
    0% { box-shadow: 0 0 10px #fc03be99, 0 0 16px #00f9ff55; }
    100% { box-shadow: 0 0 16px #fc03becc, 0 0 36px #00f9ffcc; }
}
.hero-glow {
    text-align:center;
    background: linear-gradient(92deg, #0ff5 0%, #fc03be33 90%);
    border-radius:28px;
    margin-bottom:2rem;
    box-shadow: 0 0 88px #00f9ff22;
    padding: 2rem 2rem 1.2rem 2rem;
    border: 2px solid #fc03be77;
    animation: glowshadow 2.7s infinite alternate;
}
@keyframes glowshadow {
    0% { box-shadow: 0 0 28px #0ff, 0 0 18px #fc03be44; }
    100% { box-shadow: 0 0 40px #fc03beaa, 0 0 44px #0ff9; }
}
</style>
""", unsafe_allow_html=True)

# --- Hero Section with Overlayed Image & Title ---
st.markdown(f"""
<div class="hero-img-container">
    <img src="data:image/jpg;base64,{b64_img}" style="width:99vw;max-width:1200px;border-radius:24px;box-shadow:0 0 56px #00f9ffcc;" />
    <div class="hero-img-title">
      🚀 StartupMesh: <span style='color:#fc03be;'>AGI</span> x <span style='color:#00f9ff'>Y Combinator</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Animated Badge (SVG fallback only, always works) ---
st.markdown("""
<div style='display:flex;justify-content:center;margin-bottom:0.6rem;'>
  <img src="https://www.svgrepo.com/show/522381/globe-planet-earth.svg" width="80" style="filter:drop-shadow(0 0 22px #0ff);" />
  <span class='impact-badge' style="margin-left:18px;">AGI for Humanity</span>
</div>
""", unsafe_allow_html=True)

# --- Social Impact Toggle ---
impact_mode = st.toggle(
    "🌎 AGI for Humanity: Social Impact Mode",
    value=False,
    help="Turn ON to reframe every step for maximum positive social impact."
)

def apply_impact_mode_prompt(prompt: str) -> str:
    impact_modifier = (
        "\n\n[INSTRUCTION FOR AGENT: Reframe ALL outputs to maximize positive social impact, "
        "inclusion, and benefit for the most disadvantaged or the environment. "
        "Prioritize ideas that reduce inequality, empower communities, or solve real-world problems at scale. "
        "DO NOT suggest profit over impact unless both are aligned.]"
    )
    return prompt + impact_modifier

def neon_card(text, label=None, color="#00f9ff"):
    label_html = f"<div class='glow-label' style='color:{color}'>{label}</div>" if label else ""
    return st.markdown(f"""
    <div class="neon-card" style="border-color:{color}88;box-shadow:0 0 22px {color}77, 0 0 52px #fff2;">
        {label_html}
        <div style="font-size:1.13rem; color:#f8d442; text-shadow:0 0 5px #222, 0 0 11px {color};word-break:break-word;">
            {text}
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- User Inputs ---
st.markdown("""
<div style='background:rgba(20,20,40,0.93);padding:1.0rem 1.2rem 0.5rem 1.2rem;border-radius:16px;box-shadow:0 0 18px #00f9ff99,0 0 22px #fc03be88;border:2px solid #00f9ff88;margin-bottom:1.3rem;'>
    <span style='font-size:1.04rem;color:#00f9ff;letter-spacing:1.1px;text-shadow:0 0 10px #0ff;'>
        Enter your startup idea and let the AGI generate your entire dossier—including a product image!
    </span>
</div>
""", unsafe_allow_html=True)
idea = st.text_input("Startup Idea (e.g., 'Uber for study groups')")
contract_text = st.text_area("Contract/ToS for Compliance Agent (optional):", height=100)
run_button = st.button("Run StartupMesh AGI 🚀")

def generate_image_dalle3(prompt):
    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024",
            quality="standard"
        )
        return response.data[0].url
    except Exception as e:
        st.warning(f"Image generation error: {e}")
        return None

if run_button and idea:
    st.markdown("---")
    st.header("🤖 StartupMesh Orchestration: Classic vs Social Impact")
    tab1, tab2 = st.tabs(["🚀 Classic Startup", "🌎 Social Impact Mode"])
    for tab, is_impact in zip([tab1, tab2], [False, True]):
        with tab:
            st.subheader("🧠 Thinking Steps")
            with st.status("Step 1: Gemini Feature Extraction...", expanded=True):
                system_prompt = (
                    "Extract ALL of the following from the input (pitch text) as a structured JSON object. "
                    "The JSON should contain keys for 'features', 'competitors', 'strengths', 'weaknesses', "
                    "'market_opportunities_gaps'. Each value should be a list of strings."
                )
                if is_impact:
                    system_prompt = apply_impact_mode_prompt(system_prompt)
                try:
                    gemini_out = gemini_extract_features(idea, input_type="text")
                    st.success("Gemini features extracted.")
                except Exception as e:
                    st.error(f"Gemini error: {str(e)}")
                    gemini_out = "Gemini extraction failed."
            with st.status("Step 2: Claude Market Analysis...", expanded=True):
                claude_prompt = (
                    f"Analyze the market for: {idea}\n"
                    f"Gemini pitch analysis: {gemini_out}\n"
                    "Summarize the market gap in 2-3 sentences."
                )
                if is_impact:
                    claude_prompt = apply_impact_mode_prompt(claude_prompt)
                try:
                    claude_market = summarize_market(idea, "", gemini_out if not is_impact else claude_prompt)
                    st.success("Claude market summary complete.")
                except Exception as e:
                    st.error(f"Claude error: {str(e)}")
                    claude_market = "Claude market analysis failed."
            with st.status("Step 3: Claude Launch Plan...", expanded=True):
                plan_prompt = (
                    f"Given this idea: {idea}\n"
                    f"And this market gap: {claude_market}\n"
                    "Generate a 5-step actionable launch plan, with one risk and one differentiator."
                )
                if is_impact:
                    plan_prompt = apply_impact_mode_prompt(plan_prompt)
                try:
                    claude_plan = create_launch_plan(idea, claude_market if not is_impact else plan_prompt)
                    st.success("Claude launch plan ready.")
                except Exception as e:
                    st.error(f"Claude error: {str(e)}")
                    claude_plan = "Claude launch plan failed."
            with st.status("Step 4: Groq Creative Copy...", expanded=True):
                groq_prompt = (
                    f"Startup Idea: {idea}\n"
                    f"Market Summary: {claude_market}\n"
                    f"Pitch Analysis: {gemini_out}\n"
                    "Generate a creative tagline, a unique differentiator, and a launch tweet for this startup."
                )
                if is_impact:
                    groq_prompt = apply_impact_mode_prompt(groq_prompt)
                try:
                    groq_copy = query_groq(groq_prompt)
                    st.success("Groq creative copy ready.")
                except Exception as e:
                    st.error(f"Groq error: {str(e)}")
                    groq_copy = "Groq creative step failed."
            with st.status("Step 5: Compliance Agent (optional)...", expanded=True):
                compliance_input = contract_text or ""
                if is_impact and compliance_input:
                    compliance_input = apply_impact_mode_prompt(compliance_input)
                try:
                    compliance_report = compliance_check(compliance_input) if compliance_input else "No contract/ToS provided."
                    st.success("Compliance check complete.")
                except Exception as e:
                    st.error(f"Compliance error: {str(e)}")
                    compliance_report = "Compliance check failed."

            # --- Generate product image ---
            st.markdown("### 🖼️ AGI Product Image (auto-generated):")
            dalle_prompt = f"{idea} as a product, in a majestic, cyberpunk, futuristic style, ultra-detailed, concept art"
            img_url = generate_image_dalle3(dalle_prompt)
            if img_url:
                st.image(img_url, use_column_width=True, caption="AGI-generated product visual")
            else:
                st.warning("Product image could not be generated.")

            neon_card(claude_market, label="Market Summary", color="#fc03be")
            neon_card(claude_plan, label="Launch Plan", color="#f8d442")
            neon_card(groq_copy, label="Creative Assets", color="#00f9ff")
            neon_card(compliance_report, label="Compliance Report", color="#fcfcfc")
            neon_card(gemini_out, label="Gemini Raw Output", color="#bbff00")
            st.download_button(
                f"Download Startup Dossier ({'Impact' if is_impact else 'Classic'})",
                data=f"Market: {claude_market}\nPlan: {claude_plan}\nCreative: {groq_copy}\nCompliance: {compliance_report}",
                file_name=f"startup_dossier_{'impact' if is_impact else 'classic'}.txt"
            )
else:
    st.info("Enter your idea, then hit 'Run StartupMesh AGI 🚀' to build your dossier.")

