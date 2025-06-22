from uagents import Agent, Context, Model
import base64

# === Import your actual pipeline functions ===
from gemini_agent import gemini_extract_features
from claude_agent import summarize_market, create_launch_plan
from groq_agent import query_groq
from compliance_agent import compliance_check

# === Step 1: Define the schema for requests ===
class StartupRequest(Model):
    idea: str                    # User's startup idea as text
    input_type: str = "text"     # "text" or "file"
    input_data: str              # Raw text OR base64 string for file/image
    mime_type: str = None        # e.g. "application/pdf", required if input_type="file"
    contract_text: str = None    # (Optional) For compliance, ToS/contracts

# === Step 2: Create the agent ===
fetchai_agent = Agent(
    name="startupmesh",
    seed="startupmesh-elite-hackathon-agent-2025",  # Use a unique seed for your project
)

# === Step 3: Define the orchestration logic ===
@fetchai_agent.on_message(model=StartupRequest)
async def handle(ctx: Context, msg: StartupRequest):
    # --- GEMINI: Multimodal feature extraction ---
    if msg.input_type == "text":
        gemini_out = gemini_extract_features(msg.input_data, input_type="text")
    elif msg.input_type == "file":
        file_bytes = base64.b64decode(msg.input_data)
        gemini_out = gemini_extract_features(file_bytes, input_type="file", mime_type=msg.mime_type)
    else:
        gemini_out = "[Unknown input type: only text or file supported]"

    # --- CLAUDE: Market summary, launch plan ---
    claude_market = summarize_market(msg.idea, "", gemini_out)  # You can wire in FetchAI outputs if needed
    claude_plan = create_launch_plan(msg.idea, claude_market)

    # --- GROQ: Creative copy (tagline, differentiator, tweet) ---
    groq_copy = query_groq(msg.idea, claude_market, gemini_out)

    # --- COMPLIANCE: Contract/ToS analysis (if provided) ---
    if msg.contract_text:
        compliance_report = compliance_check(msg.contract_text)
    else:
        compliance_report = "No contract or ToS provided for compliance check."

    # --- FINAL DOSSIER: Structure for UI/cards ---
    result = {
        "market_summary": {
            "content": claude_market,
            "powered_by": "Claude + Gemini"
        },
        "action_plan": {
            "content": claude_plan,
            "powered_by": "Claude"
        },
        "creative_assets": {
            "content": groq_copy,
            "powered_by": "Groq"
        },
        "compliance_report": {
            "content": compliance_report,
            "powered_by": "Compliance Agent"
        },
        "raw_gemini_output": gemini_out
    }
    await ctx.send(ctx.sender, result)

def startupmesh_pipeline(
    idea, input_type="text", input_data=None, mime_type=None, contract_text=None
):
    if input_type == "text":
        gemini_out = gemini_extract_features(input_data, input_type="text")
    elif input_type == "file":
        gemini_out = gemini_extract_features(input_data, input_type="file", mime_type=mime_type)
    else:
        gemini_out = "[Unknown input type]"

    claude_market = summarize_market(idea, "", gemini_out)
    claude_plan = create_launch_plan(idea, claude_market)

    # === Create one Groq prompt to satisfy the one parameter requirement of query_groq ===
    if idea is None or claude_market is None or gemini_out is None:
        raise ValueError("All parameters (idea, claude_market, gemini_out) must be provided for Groq query.")
    
    groq_prompt = (
        f"Startup Idea: {idea}\n"
        f"Market Summary: {claude_market}\n"
        f"Pitch Analysis: {gemini_out}\n"
        "Generate a creative tagline, a unique differentiator, and a launch tweet for this startup."
    )

    groq_copy = query_groq(groq_prompt)
    compliance_report = compliance_check(contract_text) if contract_text else "No contract/ToS provided."

    return {
        "market_summary": {"content": claude_market, "powered_by": "Claude + Gemini"},
        "action_plan": {"content": claude_plan, "powered_by": "Claude"},
        "creative_assets": {"content": groq_copy, "powered_by": "Groq"},
        "compliance_report": {"content": compliance_report, "powered_by": "Compliance Agent"},
        "raw_gemini_output": gemini_out
    }

# === Step 4: Run the agent ===
if __name__ == "__main__":
    print("=== TESTING STARTUPMESH PIPELINE ===")
    # -- Test with a simple text idea --
    result = startupmesh_pipeline(
        idea="AI driven productiivty blocks & ability to block distractions via benevolent detection with voice command and AI agent handling all daily tasks on phone/computer",
        input_type="text",
        input_data="AI CoPilot Productiivity Friend: improves productivity by 10x with voice commands and AI agent handling all daily tasks for students and professionals.",
        mime_type=None,
        contract_text=None
    )
    import json
    print(json.dumps(result, indent=2))

    # -- Test with PDF (optional, if you have a sample file) --
    import base64
    with open("backend/agents/SamplePitch.pdf", "rb") as f:
        pdf_bytes = f.read()
    result_pdf = startupmesh_pipeline(
         idea="Uber for study groups",
         input_type="file",
         input_data=pdf_bytes,
         mime_type="application/pdf",
         contract_text=None
     )
    print(json.dumps(result_pdf, indent=2))

