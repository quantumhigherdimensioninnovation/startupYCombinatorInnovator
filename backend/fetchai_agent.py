from uagents import Agent, Context, Model
import base64

# --- Import your pipeline functions ---
from .gemini_agent import gemini_extract_features
from .claude_agent import summarize_market, create_launch_plan
from .groq_agent import query_groq
from .compliance_agent import compliance_check

# --- Step 1: Define the schema for requests ---
class StartupRequest(Model):
    idea: str
    input_type: str = "text"
    input_data: str
    mime_type: str = None
    contract_text: str = None

# --- Step 3: Define the orchestration logic (for CLI/testing) ---
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

# --- Step 4: Only run this if called from CLI (for actual agent use) ---
if __name__ == "__main__":
    # Agent creation and event loop is CLI only
    fetchai_agent = Agent(
        name="startupmesh",
        seed="startupmesh-elite-hackathon-agent-2025"
    )

    @fetchai_agent.on_message(model=StartupRequest)
    async def handle(ctx: Context, msg: StartupRequest):
        # --- Full logic from above ---
        if msg.input_type == "text":
            gemini_out = gemini_extract_features(msg.input_data, input_type="text")
        elif msg.input_type == "file":
            file_bytes = base64.b64decode(msg.input_data)
            gemini_out = gemini_extract_features(file_bytes, input_type="file", mime_type=msg.mime_type)
        else:
            gemini_out = "[Unknown input type: only text or file supported]"

        claude_market = summarize_market(msg.idea, "", gemini_out)
        claude_plan = create_launch_plan(msg.idea, claude_market)
        groq_prompt = (
            f"Startup Idea: {msg.idea}\n"
            f"Market Summary: {claude_market}\n"
            f"Pitch Analysis: {gemini_out}\n"
            "Generate a creative tagline, a unique differentiator, and a launch tweet for this startup."
        )
        groq_copy = query_groq(groq_prompt)
        compliance_report = compliance_check(msg.contract_text) if msg.contract_text else "No contract/ToS provided."

        result = {
            "market_summary": {"content": claude_market, "powered_by": "Claude + Gemini"},
            "action_plan": {"content": claude_plan, "powered_by": "Claude"},
            "creative_assets": {"content": groq_copy, "powered_by": "Groq"},
            "compliance_report": {"content": compliance_report, "powered_by": "Compliance Agent"},
            "raw_gemini_output": gemini_out
        }
        await ctx.send(ctx.sender, result)

    print("=== TESTING STARTUPMESH PIPELINE ===")
    result = startupmesh_pipeline(
        idea="AI driven productivity blocks & ability to block distractions via benevolent detection with voice command and AI agent handling all daily tasks on phone/computer",
        input_type="text",
        input_data="AI CoPilot Productivity Friend: improves productivity by 10x with voice commands and AI agent handling all daily tasks for students and professionals.",
        mime_type=None,
        contract_text=None
    )
    import json
    print(json.dumps(result, indent=2))

    # Start agent (if needed)
    # fetchai_agent.run()
