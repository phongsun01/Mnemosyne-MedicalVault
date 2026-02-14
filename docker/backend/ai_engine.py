import os
import google.generativeai as genai
import json
import logging

logger = logging.getLogger(__name__)

def setup_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY not found in environment!")
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.0-flash')

async def extract_metadata(file_path, content_text=None, image_parts=None):
    model = setup_gemini()
    if not model:
        return None

    prompt = """
    You are a medical device documentation expert. 
    Analyze the provided content and extract the following information in JSON format:
    {
      "model": "model name",
      "brand": "manufacturer brand",
      "origin": "country of origin",
      "category": "medical category",
      "specs": {
        "key_feature_1": "value",
        "key_feature_2": "value"
      },
      "price_range": [min_vnd, max_vnd]
    }
    If information is missing, use null.
    Respond ONLY with the JSON object.
    """

    try:
        inputs = [prompt]
        if content_text:
            inputs.append(f"Document content:\n{content_text}")
        if image_parts:
            inputs.extend(image_parts)

        response = await model.generate_content_async(inputs)
        # Parse JSON
        text = response.text
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        
        return json.loads(text.strip())
    except Exception as e:
        logger.error(f"Gemini extraction failed: {e}")
        return None
