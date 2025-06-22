import streamlit as st
import random
import base64
import openai
import os
from backend.fetchai_agent import startupmesh_pipeline

# ---- OpenAI DALL·E 3 setup ----
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

st.set_page_config(page_title="StartupMesh: AGI x Y Combinator", page_icon="🚀", layout="wide")

# --- Cyberpunk City Hero Image Setup ---
city_images = [
    "DALL·E 2025-06-22 06.10.47 - A futuristic skyline inspired by New York, Shanghai, and Dubai, featuring thousands of skyscrapers with flowing curves and opalescent windows. These t.webp",
]
skyline_image = random.choice(city_images)
with open(skyline_image, "rb") as img_file:
    b64_img = base64.b64encode(img_file.read()).decode()

# --- Cyberpunk Animated CSS ---
st.markdown("""
<style>
.stApp {
    background: linear-gradient(120deg, #13132a 0%, #1f1045 100%) !important;
    min-height: 100vh;
    font-family: 'Orbitron', 'Roboto', sans-serif;
}
.impact-badge {
    font-size: 1.25rem !important;
    font-weight: 900 !important;
    color: #fc03be !important;
    text-shadow: 0 0 14px #00f9ff, 0 0 10px #fc03be, 0 0 6px #fff;
    background: linear-gradient(90deg,#0ff4,#fc03be8a);
    border-radius: 18px;
    padding: 0.35em 1.3em;
    box-shadow: 0 0 18px #fc03be99, 0 0 32px #00f9ff99;
    letter-spacing: 1.7px;
    border: 2.1px solid #00f9ff99;
    display: inline-block;
}

.hero-img-container {
    position: relative;
    width: 100%;
    text-align: center;
    margin-bottom: -1.3rem;
}
.hero-img-city {
    width: 99vw;
    max-width: 1200px;
    border-radius: 24px;
    box-shadow: 0 0 56px #00f9ffcc;
}
.hero-img-title-block {
    position: absolute;
    top: 12%;
    left: 50%;
    transform: translate(-50%, 0);
    background: rgba(16,20,44,0.81);
    padding: 2.2rem 3.6rem 1.1rem 3.6rem;
    border-radius: 26px;
    color: #fff;
    font-size: 2.45rem;
    font-weight: 900;
    text-shadow: 0 0 28px #00f9ff, 0 0 18px #fc03be;
    letter-spacing: 1.3px;
    border: 2.8px solid #00f9ff77;
    box-shadow: 0 0 50px #fc03be55, 0 0 100px #00f9ff33;
    z-index: 2;
    animation: glowmove 3.6s infinite alternate;
}
@keyframes glowmove {
    0% { box-shadow: 0 0 40px #00f9ff77, 0 0 10px #fc03be33;}
    100% { box-shadow: 0 0 90px #fc03becc, 0 0 110px #00f9ffcc;}
}
.think-step {
    margin: 1.8rem 0 2.2rem 0;
    background: linear-gradient(94deg, #0ff7 0%, #1b0f4fdd 100%);
    border: 2.5px solid #00f9ff77;
    border-radius: 22px;
    box-shadow: 0 0 24px #00f9ffcc, 0 0 66px #fc03be55;
    font-size: 1.85rem;
    padding: 1.4rem 1.7rem 1.3rem 1.7rem;
    position: relative;
    animation: popfade 0.8s;
}
@keyframes popfade {
    from {opacity: 0; transform: translateY(32px);}
    to   {opacity: 1; transform: translateY(0);}
}
.think-step-label {
    font-size: 1.32rem;
    color: #fc03be;
    font-weight: 800;
    text-shadow: 0 0 14px #00f9ff, 0 0 4px #fc03be;
    margin-bottom: 0.31rem;
}
</style>
""", unsafe_allow_html=True)

# --- Hero Section with Overlayed Image & Title ---
st.markdown(f"""
<div class="hero-img-container">
    <img src="data:image/jpg;base64,{b64_img}" class="hero-img-city"/>
    <div class="hero-img-title-block">
        🚀 <span style="color:#fc03be;">StartupMesh</span>: <span style="color:#00f9ff">AGI x Y Combinator</span>
        <div style="font-size:1.16rem;font-weight:600;color:#bbfffc;margin-top:14px;">
            Next-Gen AGI Product Studio: Instantly Generate Market Analysis, Launch Plans, Creative Assets, and Cyberpunk Product Visuals.<br>
            <span style="color:#f8d442;">Your AI-powered startup pipeline. Just add your idea.</span>
        </div>
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

# --- User Input Card ---
st.markdown("""
<div style='background:rgba(20,20,40,0.95);padding:1.2rem 1.4rem 1.2rem 1.4rem;border-radius:18px;
            box-shadow:0 0 24px #00f9ff88,0 0 32px #fc03be77;border:2.5px solid #00f9ff88;margin-bottom:1.6rem;'>
    <span style='font-size:1.12rem;color:#00f9ff;letter-spacing:1.1px;font-weight:700;
                 text-shadow:0 0 10px #0ff,0 0 4px #fff;'>
        Enter your startup idea and watch the AGI agents build your full dossier—plus an AI-generated product visual.
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

def think_step_box(label, content, color="#00f9ff"):
    st.markdown(f"""
    <div class="think-step" style="border-color:{color};box-shadow:0 0 26px {color}99,0 0 44px #fc03be55;">
      <div class="think-step-label">{label}</div>
      <div style="font-size:1.13rem;color:#f8d442;text-shadow:0 0 8px #222,0 0 10px {color};word-break:break-word;">
        {content}
      </div>
    </div>
    """, unsafe_allow_html=True)

if run_button and idea:
    st.markdown("---")
    st.header("🤖 StartupMesh: Agentic Thinking Steps")
    # --- SINGLE FUNCTION CALL: everything in one shot! ---
    with st.spinner("Running full agent pipeline..."):
        try:
            result = startupmesh_pipeline(
                idea=idea,
                input_type="text",
                input_data=idea,
                mime_type=None,
                contract_text=contract_text if contract_text else None
            )
        except Exception as e:
            st.error(f"Agent error: {e}")
            result = None

    if result:
        think_step_box(
            "Step 0: Fetch.ai Agent Mesh Orchestration",
            "Your startup dossier is assembled by a decentralized Fetch.ai agent mesh, routing your idea through Gemini, Claude, Groq, and Compliance agents in real time for maximal accuracy and creativity.",
            color="#0ff"
        )
        think_step_box("Step 1: Market Summary (Claude + Gemini)", result.get("market_summary", {}).get("content", ""), color="#fc03be")
        think_step_box("Step 2: Action Plan (Claude)", result.get("action_plan", {}).get("content", ""), color="#f8d442")
        think_step_box("Step 3: Creative Assets (Groq)", result.get("creative_assets", {}).get("content", ""), color="#00f9ff")
        think_step_box("Step 4: Compliance Report", result.get("compliance_report", {}).get("content", ""), color="#fcfcfc")
        think_step_box("Step 5: Gemini Raw Output", result.get("raw_gemini_output", ""), color="#bbff00")
        st.download_button(
            "Download Startup Dossier",
            data=(
                f"Market: {result.get('market_summary',{}).get('content','')}\n"
                f"Plan: {result.get('action_plan',{}).get('content','')}\n"
                f"Creative: {result.get('creative_assets',{}).get('content','')}\n"
                f"Compliance: {result.get('compliance_report',{}).get('content','')}"
            ),
            file_name="startup_dossier.txt"
        )
        # --- Product Image LAST (always at the bottom) ---
        st.markdown("### 🖼️ <span style='color:#fc03be'>AGI Product Image</span> (auto-generated):", unsafe_allow_html=True)
        dalle_prompt = f"{idea} as a product, in a majestic, cyberpunk, futuristic style, ultra-detailed, concept art"
        img_url = generate_image_dalle3(dalle_prompt)
        if img_url:
            st.image(img_url, use_column_width=True, caption="AGI-generated product visual")
        else:
            st.warning("Product image could not be generated.")
    else:
        st.warning("Could not generate dossier. Please try again.")
else:
    st.info("Enter your idea, then hit 'Run StartupMesh AGI 🚀' to build your dossier.")
