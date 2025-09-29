from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import numpy as np
import cv2
from typing import Tuple, Optional
from config import IMAGE_CONFIG

class ImageProcessor:
    @staticmethod
    def fix_image_orientation(image: Image.Image) -> Image.Image:
        """Fix image orientation based on EXIF data"""
        try:
            image = ImageOps.exif_transpose(image)
        except (AttributeError, KeyError, TypeError):
            pass
        return image

    @staticmethod
    def resize_image(image: Image.Image, max_size: Tuple[int, int] = None) -> Image.Image:
        if max_size is None:
            max_size = IMAGE_CONFIG["max_image_size"]

        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        return image

    @staticmethod
    def normalize_image(image: Image.Image) -> Image.Image:
        image = ImageProcessor.fix_image_orientation(image)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        return image

    @staticmethod
    def enhance_image_quality(image: Image.Image) -> Image.Image:
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.2)

        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.1)

        return image

    @staticmethod
    def create_mask(image: Image.Image, background_color: Tuple[int, int, int] = (255, 255, 255)) -> Image.Image:
        img_array = np.array(image)

        lower_bound = np.array([c - 20 for c in background_color])
        upper_bound = np.array([c + 20 for c in background_color])

        mask = cv2.inRange(img_array, lower_bound, upper_bound)
        mask = cv2.bitwise_not(mask)

        return Image.fromarray(mask)

    @staticmethod
    def blend_images(
        base_image: Image.Image,
        overlay_image: Image.Image,
        mask: Optional[Image.Image] = None,
        position: Tuple[int, int] = (0, 0),
        alpha: float = 0.8
    ) -> Image.Image:
        if base_image.size != overlay_image.size:
            overlay_image = overlay_image.resize(base_image.size, Image.Resampling.LANCZOS)

        if mask:
            mask = mask.resize(base_image.size, Image.Resampling.LANCZOS)
            result = Image.composite(overlay_image, base_image, mask)
        else:
            result = Image.blend(base_image, overlay_image, alpha)

        return result

    @staticmethod
    def detect_person_bounds(image: Image.Image) -> Tuple[int, int, int, int]:
        img_array = np.array(image)
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

        edges = cv2.Canny(gray, 50, 150)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            return (x, y, x + w, y + h)

        return (0, 0, image.width, image.height)

    @staticmethod
    def prepare_for_tryon(
        user_image: Image.Image,
        clothing_image: Image.Image
    ) -> Tuple[Image.Image, Image.Image]:
        user_processed = ImageProcessor.normalize_image(user_image)
        user_processed = ImageProcessor.resize_image(user_processed)
        user_processed = ImageProcessor.enhance_image_quality(user_processed)

        clothing_processed = ImageProcessor.normalize_image(clothing_image)
        clothing_processed = ImageProcessor.resize_image(clothing_processed)

        return user_processed, clothing_processed