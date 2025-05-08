from openai import OpenAI
from typing import List
import requests
from io import BytesIO
from PIL import Image
import base64

class ImageAgent:
    def __init__(self, model: str = "dall-e-3", quality: str = "standard", size: str = "1024x1024"):
        self.client = None  # Will be initialized with API key
        self.model = model
        self.quality = quality
        self.size = size
        self.default_num_images = 1  # DALL-E 3 only supports n=1

    def set_api_key(self, api_key: str):
        """Initialize the OpenAI client with the provided API key"""
        self.client = OpenAI(api_key=api_key)

    def generate_images(self, summary: str, num_images: int = 1, download: bool = False) -> List[str]:
        """Generate images using OpenAI's DALL-E.
        
        Args:
            summary: Text summary to base images on
            num_images: Number of images to generate (max 1 for DALL-E 3)
            download: If True, returns base64 encoded images instead of URLs
            
        Returns:
            List of image URLs or base64 strings if download=True
            
        Raises:
            RuntimeError: If API key is not set
        """
        if not self.client:
            raise RuntimeError("OpenAI API key not set. Call set_api_key() first.")

        print(f"[ImageAgent] Generating {num_images} images with {self.model}...")

        try:
            # Adjust for DALL-E 3 limitations
            if self.model == "dall-e-3":
                num_images = min(num_images, 1)  # DALL-E 3 only supports n=1

            response = self.client.images.generate(
                model=self.model,
                prompt=f"Create a professional, high-quality image illustrating: {summary}. "
                       "Use a clean, modern style suitable for LinkedIn posts.",
                n=num_images,
                quality=self.quality,
                size=self.size,
                response_format="url" if not download else "b64_json"
            )

            if download:
                return [img.b64_json for img in response.data if img.b64_json]
            return [img.url for img in response.data if img.url]

        except Exception as e:
            print(f"[ImageAgent] Error generating images: {str(e)}")
            return []

    def download_image(self, url: str) -> bytes:
        """Download image from URL and return as bytes."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.content
        except Exception as e:
            print(f"[ImageAgent] Error downloading image: {str(e)}")
            return None

    def display_image(self, image_data: str):
        """Display base64 encoded image (for Streamlit or notebooks)."""
        try:
            if image_data.startswith("http"):
                img_bytes = self.download_image(image_data)
                if img_bytes:
                    return Image.open(BytesIO(img_bytes))
            else:
                return Image.open(BytesIO(base64.b64decode(image_data)))
        except Exception as e:
            print(f"[ImageAgent] Error displaying image: {str(e)}")
            return None