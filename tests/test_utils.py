import unittest
from PIL import Image
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.image_utils import ImageProcessor

class TestImageProcessor(unittest.TestCase):
    def setUp(self):
        self.test_image_rgb = Image.new('RGB', (800, 600), color='red')
        self.test_image_rgba = Image.new('RGBA', (800, 600), color='blue')

    def test_resize_image(self):
        resized = ImageProcessor.resize_image(self.test_image_rgb, (400, 300))

        self.assertLessEqual(resized.width, 400)
        self.assertLessEqual(resized.height, 300)

    def test_resize_image_default_size(self):
        large_image = Image.new('RGB', (2000, 1500), color='green')
        resized = ImageProcessor.resize_image(large_image)

        self.assertLessEqual(resized.width, 1024)
        self.assertLessEqual(resized.height, 1024)

    def test_normalize_image_rgb(self):
        normalized = ImageProcessor.normalize_image(self.test_image_rgb)

        self.assertEqual(normalized.mode, 'RGB')
        self.assertEqual(normalized.size, self.test_image_rgb.size)

    def test_normalize_image_rgba(self):
        normalized = ImageProcessor.normalize_image(self.test_image_rgba)

        self.assertEqual(normalized.mode, 'RGB')

    def test_enhance_image_quality(self):
        enhanced = ImageProcessor.enhance_image_quality(self.test_image_rgb)

        self.assertIsInstance(enhanced, Image.Image)
        self.assertEqual(enhanced.size, self.test_image_rgb.size)

    def test_create_mask(self):
        white_image = Image.new('RGB', (100, 100), color=(255, 255, 255))
        mask = ImageProcessor.create_mask(white_image)

        self.assertIsInstance(mask, Image.Image)
        self.assertEqual(mask.size, white_image.size)

    def test_blend_images(self):
        image1 = Image.new('RGB', (200, 200), color='red')
        image2 = Image.new('RGB', (200, 200), color='blue')

        blended = ImageProcessor.blend_images(image1, image2, alpha=0.5)

        self.assertIsInstance(blended, Image.Image)
        self.assertEqual(blended.size, image1.size)

    def test_blend_images_different_sizes(self):
        image1 = Image.new('RGB', (200, 200), color='red')
        image2 = Image.new('RGB', (100, 100), color='blue')

        blended = ImageProcessor.blend_images(image1, image2)

        self.assertEqual(blended.size, image1.size)

    def test_detect_person_bounds(self):
        bounds = ImageProcessor.detect_person_bounds(self.test_image_rgb)

        self.assertIsInstance(bounds, tuple)
        self.assertEqual(len(bounds), 4)
        self.assertGreaterEqual(bounds[2], bounds[0])
        self.assertGreaterEqual(bounds[3], bounds[1])

    def test_prepare_for_tryon(self):
        user_img = Image.new('RGB', (800, 600), color='red')
        clothing_img = Image.new('RGB', (400, 300), color='blue')

        user_processed, clothing_processed = ImageProcessor.prepare_for_tryon(
            user_img, clothing_img
        )

        self.assertIsInstance(user_processed, Image.Image)
        self.assertIsInstance(clothing_processed, Image.Image)
        self.assertEqual(user_processed.mode, 'RGB')
        self.assertEqual(clothing_processed.mode, 'RGB')

if __name__ == '__main__':
    unittest.main()