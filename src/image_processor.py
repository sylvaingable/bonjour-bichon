"""
Image processing utilities for resizing photos before sending via Signal.
Mimics the behavior of WhatsApp/Signal mobile apps by resizing images
to reasonable dimensions while maintaining aspect ratio and good quality.
"""

from __future__ import annotations

import io

from PIL import Image, ImageOps

# Configuration similar to WhatsApp/Signal mobile apps
MAX_DIMENSION = 1600  # Max width or height in pixels
JPEG_QUALITY = 85  # Good balance between quality and file size
MAX_FILE_SIZE_MB = 1  # Maximum file size in MB


class ImageProcessingError(Exception):
    """Raised when image processing fails."""


def resize_image(image_bytes: bytes) -> bytes:
    """Resize an image to mobile-friendly dimensions while maintaining aspect ratio."""
    try:
        # Open image from bytes
        with Image.open(io.BytesIO(image_bytes)) as img:
            # Convert to RGB if necessary (handles RGBA, P mode images)
            if img.mode in ("RGBA", "LA", "P"):
                # Create white background for transparency
                background = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "P":
                    img = img.convert("RGBA")
                background.paste(
                    img, mask=img.split()[-1] if img.mode in ("RGBA", "LA") else None
                )
                img = background
            elif img.mode != "RGB":
                img = img.convert("RGB")

            # Fix orientation based on EXIF data
            img = ImageOps.exif_transpose(img)

            # Calculate new dimensions maintaining aspect ratio
            width, height = img.size
            if width <= MAX_DIMENSION and height <= MAX_DIMENSION:
                # Image is already small enough, just optimize quality/size
                new_img = img
            else:
                # Resize maintaining aspect ratio
                if width > height:
                    new_width = MAX_DIMENSION
                    new_height = int((height * MAX_DIMENSION) / width)
                else:
                    new_height = MAX_DIMENSION
                    new_width = int((width * MAX_DIMENSION) / height)

                # Use high-quality resampling
                new_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Save to bytes with optimization
            output_buffer = io.BytesIO()
            new_img.save(
                output_buffer,
                format="JPEG",
                quality=JPEG_QUALITY,
                optimize=True,
                progressive=True,  # Better for web/mobile viewing
            )

            result = output_buffer.getvalue()

            # Check if file size is reasonable
            size_mb = len(result) / (1024 * 1024)
            if size_mb > MAX_FILE_SIZE_MB:
                # If still too large, reduce quality
                output_buffer = io.BytesIO()
                new_img.save(
                    output_buffer,
                    format="JPEG",
                    quality=70,  # Lower quality for very large images
                    optimize=True,
                    progressive=True,
                )
                result = output_buffer.getvalue()

            return result

    except Exception as exc:
        raise ImageProcessingError(f"Failed to resize image: {exc}") from exc


def get_image_info(image_bytes: bytes) -> dict[str, object]:
    """
    Get basic information about an image.

    Args:
        image_bytes: Image as bytes

    Returns:
        Dictionary with image info (width, height, format, size_mb)
    """
    try:
        with Image.open(io.BytesIO(image_bytes)) as img:
            return {
                "width": img.size[0],
                "height": img.size[1],
                "format": img.format,
                "mode": img.mode,
                "size_mb": len(image_bytes) / (1024 * 1024),
            }
    except Exception as exc:
        raise ImageProcessingError(f"Failed to get image info: {exc}") from exc
