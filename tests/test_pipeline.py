import unittest
from unittest.mock import Mock, patch, MagicMock
from PIL import Image
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.pipeline import VirtualTryOnPipeline
from services.gemini_client import GeminiClient
from services.image_utils import ImageProcessor

class TestVirtualTryOnPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = VirtualTryOnPipeline()

        self.test_user_image = Image.new('RGB', (512, 512), color='blue')
        self.test_clothing_image = Image.new('RGB', (256, 256), color='red')

    @patch('services.pipeline.GeminiClient')
    def test_pipeline_initialization(self, mock_gemini):
        pipeline = VirtualTryOnPipeline()
        self.assertIsInstance(pipeline.image_processor, ImageProcessor)

    def test_generate_tryon_with_images(self):
        with patch.object(self.pipeline.gemini_client, 'process_virtual_tryon') as mock_process:
            mock_process.return_value = "Generated virtual try-on description"

            result = self.pipeline.generate_tryon(
                self.test_user_image,
                self.test_clothing_image
            )

            self.assertIsInstance(result, Image.Image)
            mock_process.assert_called_once()

    def test_generate_tryon_with_file_paths(self):
        with patch('PIL.Image.open') as mock_open:
            mock_open.side_effect = [self.test_user_image, self.test_clothing_image]

            with patch.object(self.pipeline.gemini_client, 'process_virtual_tryon') as mock_process:
                mock_process.return_value = "Generated virtual try-on description"

                result = self.pipeline.generate_tryon("user.jpg", "clothing.png")

                self.assertIsInstance(result, Image.Image)
                self.assertEqual(mock_open.call_count, 2)

    def test_generate_tryon_error_handling(self):
        with patch.object(self.pipeline.gemini_client, 'process_virtual_tryon') as mock_process:
            mock_process.side_effect = Exception("API Error")

            result = self.pipeline.generate_tryon(
                self.test_user_image,
                self.test_clothing_image
            )

            self.assertIsInstance(result, Image.Image)

    def test_build_tryon_prompt(self):
        prompt = self.pipeline._build_tryon_prompt()

        self.assertIsInstance(prompt, str)
        self.assertIn("virtual_tryon", prompt.lower())
        self.assertIn("realistic", prompt.lower())

    def test_analyze_compatibility(self):
        with patch.object(self.pipeline.gemini_client, 'process_virtual_tryon') as mock_process:
            mock_process.return_value = "Compatibility analysis result"

            result = self.pipeline.analyze_compatibility(
                self.test_user_image,
                self.test_clothing_image
            )

            self.assertIsInstance(result, dict)
            self.assertIn("analysis", result)
            self.assertIn("compatibility_score", result)
            self.assertIn("recommendations", result)

    def test_create_fallback_image(self):
        result = self.pipeline._create_fallback_image(
            self.test_user_image,
            self.test_clothing_image
        )

        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, self.test_user_image.size)

if __name__ == '__main__':
    unittest.main()