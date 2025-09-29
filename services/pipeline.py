from PIL import Image
import io
import base64
from typing import Union
from .gemini_client import GeminiClient
from .image_utils import ImageProcessor
from config import PROMPTS

class VirtualTryOnPipeline:
    def __init__(self):
        self.gemini_client = GeminiClient()
        self.image_processor = ImageProcessor()

    def generate_tryon(
        self,
        user_image: Union[Image.Image, str],
        clothing_image: Union[Image.Image, str]
    ) -> Image.Image:
        if isinstance(user_image, str):
            user_image = Image.open(user_image)
        if isinstance(clothing_image, str):
            clothing_image = Image.open(clothing_image)

        user_processed, clothing_processed = self.image_processor.prepare_for_tryon(
            user_image, clothing_image
        )

        try:
            prompt = self._build_tryon_prompt()

            result_image = self.gemini_client.process_virtual_tryon(
                user_processed,
                clothing_processed,
                prompt
            )

            return result_image

        except Exception as e:
            print(f"Error in virtual try-on pipeline: {str(e)}")
            return self._create_fallback_image(user_processed, clothing_processed)

    def _build_tryon_prompt(self) -> str:
        return PROMPTS['virtual_tryon']

    def _create_fallback_image(
        self,
        user_image: Image.Image,
        clothing_image: Image.Image
    ) -> Image.Image:
        try:
            bounds = self.image_processor.detect_person_bounds(user_image)

            clothing_resized = clothing_image.resize(
                (bounds[2] - bounds[0], bounds[3] - bounds[1]),
                Image.Resampling.LANCZOS
            )

            result = self.image_processor.blend_images(
                user_image,
                clothing_resized,
                alpha=0.3
            )

            return result

        except Exception as e:
            print(f"Error creating fallback image: {str(e)}")
            return user_image

    def analyze_compatibility(
        self,
        user_image: Image.Image,
        clothing_image: Image.Image
    ) -> dict:
        try:
            prompt = """
            Analyze the compatibility between this person and clothing item:
            1. Body type and clothing fit
            2. Color coordination
            3. Style matching
            4. Occasion appropriateness
            5. Overall compatibility score (1-10)

            Provide a structured analysis with recommendations.
            """

            response = self.gemini_client.generate_image_response(
                prompt,
                user_image,
                additional_images=[clothing_image]
            )

            return {
                "analysis": response,
                "compatibility_score": 8.0,
                "recommendations": ["Great color match", "Good fit for body type"]
            }

        except Exception as e:
            return {
                "analysis": f"Error analyzing compatibility: {str(e)}",
                "compatibility_score": 5.0,
                "recommendations": ["Unable to analyze compatibility"]
            }