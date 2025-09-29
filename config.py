import os
from dotenv import load_dotenv

load_dotenv()

try:
    import streamlit as st
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_CONFIG = {
    "model_name": "gemini-2.5-flash-image-preview",
    "temperature": 0.7,
    "max_output_tokens": 1024,
}

IMAGE_CONFIG = {
    "max_image_size": (1024, 1024),
    "supported_formats": ["JPEG", "PNG", "JPG"],
    "output_format": "PNG",
    "quality": 95
}

APP_CONFIG = {
    "title": "Virtual Try-On App",
    "page_icon": "👗",
    "layout": "wide",
    "max_file_size_mb": 10
}

PROMPTS = {
    "virtual_tryon": """
    Put the item on the person while preserving pose, identity, and body proportions, as well as all unchanged items. 
    Ensure the item fits naturally on the body with correct drape, seams, occlusions, and perspective. 
    Match lighting, color, and fabric texture to maintain photorealistic shading and contact shadows.

    Please ensure:
    - Natural lighting and shadows
    - Accurate fit and body proportions
    - Realistic fabric draping and texture
    - Consistent background and preserved pose
    """,

    "image_processing": """
    Process this image for virtual try-on application:
    - Detect person's pose and body shape
    - Identify clothing regions
    - Extract key features for realistic overlay
    """
}