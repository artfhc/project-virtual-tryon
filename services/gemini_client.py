import google.generativeai as genai
from PIL import Image, ImageOps
import io
import base64
from typing import Optional, Union
from config import GEMINI_API_KEY, MODEL_CONFIG

class GeminiClient:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(MODEL_CONFIG["model_name"])

    def generate_virtual_tryon_image(
        self,
        prompt: str,
        user_image: Image.Image,
        clothing_image: Image.Image
    ) -> Image.Image:
        try:
            user_image = ImageOps.exif_transpose(user_image)
            clothing_image = ImageOps.exif_transpose(clothing_image)

            if user_image.mode != 'RGB':
                user_image = user_image.convert('RGB')
            if clothing_image.mode != 'RGB':
                clothing_image = clothing_image.convert('RGB')

            content = [prompt, user_image, clothing_image]

            response = self.model.generate_content(content)

            for i, part in enumerate(response.candidates[0].content.parts):
                if part.inline_data is not None:
                    try:
                        image_data = base64.b64decode(part.inline_data.data)
                        generated_image = Image.open(io.BytesIO(image_data))
                        return generated_image
                    except:
                        generated_image = Image.open(io.BytesIO(part.inline_data.data))
                        return generated_image

            raise Exception("No image data found in response")

        except Exception as e:
            raise Exception(f"Error generating virtual try-on image: {str(e)}")

    def generate_image_response(
        self,
        prompt: str,
        image: Union[Image.Image, str],
        additional_images: Optional[list] = None
    ) -> str:
        try:
            content = [prompt]

            if isinstance(image, str):
                image = Image.open(image)
            content.append(image)

            if additional_images:
                for img in additional_images:
                    if isinstance(img, str):
                        img = Image.open(img)
                    content.append(img)

            response = self.model.generate_content(
                content,
                generation_config=genai.types.GenerationConfig(
                    temperature=MODEL_CONFIG["temperature"],
                    max_output_tokens=MODEL_CONFIG["max_output_tokens"]
                )
            )

            return response.text

        except Exception as e:
            raise Exception(f"Error generating response from Gemini: {str(e)}")

    def analyze_image(self, image: Union[Image.Image, str], prompt: str) -> str:
        return self.generate_image_response(prompt, image)

    def process_virtual_tryon(
        self,
        user_image: Image.Image,
        clothing_image: Image.Image,
        prompt: str
    ) -> Image.Image:
        return self.generate_virtual_tryon_image(prompt, user_image, clothing_image)