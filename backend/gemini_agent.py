import os
from google import genai
from google.genai import types
from dotenv import load_dotenv 

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

client = genai.Client(api_key=GEMINI_API_KEY)

def gemini_extract_features(
    input_data,
    input_type="text",       # "text", "file", or "image"
    mime_type=None,          # e.g. "application/pdf" or "image/png"
    model="gemini-2.5-flash"
):
    """
    Extracts business features, competitors, strengths, weaknesses, and market gaps.
    - input_type: "text" for plain text, "file" for PDF, "image" for PNG/JPG
    - mime_type: required for file/image (e.g. "application/pdf", "image/png")
    """
    # Use a strong system prompt for structured output
    system_prompt = (
        "Extract ALL of the following from the input (pitch text, PDF, or image) as a structured JSON object. "
        "The JSON should contain keys for 'features', 'competitors', 'strengths', 'weaknesses', "
        "'market_opportunities_gaps'. Each value should be a list of strings.\n"
        "Example Output:\n"
        "{\n"
        "  \"features\": [\"feature1\", \"feature2\"],\n"
        "  \"competitors\": [\"competitorA\", \"competitorB\"],\n"
        "  \"strengths\": [\"strength1\"],\n"
        "  \"weaknesses\": [\"weakness1\", \"weakness2\"],\n"
        "  \"market_opportunities_gaps\": [\"opportunity1\"]\n"
        "}"
    )
    if input_type == "text":
        contents = [system_prompt, input_data]
    elif input_type == "file":
        if not mime_type:
            raise ValueError("mime_type required for file input.")
        part = types.Part.from_bytes(data=input_data, mime_type=mime_type)
        contents = [part, system_prompt]
    elif input_type == "image":
        # input_data here should be a PIL Image or file path
        from PIL import Image
        if isinstance(input_data, str):  # If file path
            image = Image.open(input_data)
        else:
            image = input_data
        contents = [image, system_prompt]
    else:
        raise ValueError("input_type must be 'text', 'file', or 'image'.")

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(
            temperature=0.2,
            # You can enable/disable "thinking" as needed
        )
    )
    return response.text

# ---- Test block ----
if __name__ == "__main__":
    print("--- GEMINI TEXT TEST ---")
    test_text = (
        "Project Nova: An AI-powered personal assistant designed for productivity and task management. "
        "Competes with Google Assistant and Siri. Strengths: seamless integration, deep learning. "
        "Weaknesses: high cost, privacy concerns. Big gap for assistants in professional workflows."
    )
    print(gemini_extract_features(test_text, input_type="text"))

    print("\n--- GEMINI PDF TEST (if file exists) ---")
    pdf_path = "backend/agents/SamplePitch.pdf"
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
        print(gemini_extract_features(pdf_bytes, input_type="file", mime_type="application/pdf"))
    else:
        print("PDF file not found. Skipping PDF test.")

    print("\n--- GEMINI IMAGE TEST (if file exists) ---")
    img_path = "backend/agents/sample_pitch.png"
    if os.path.exists(img_path):
        print(gemini_extract_features(img_path, input_type="image", mime_type="image/png"))
    else:
        print("Image file not found. Skipping image test.")