from django.core.exceptions import ValidationError
from django.utils.timezone import now
import os
import uuid

import os
from django.core.validators import FileExtensionValidator
from django.conf import settings


def validate_image_file(value):
    """
    Custom validator that handles both regular image files and Cloudinary URLs
    """
    # Skip validation for existing Cloudinary URLs in production
    if settings.ENVIRONMENT == "production" and hasattr(value, "url"):
        # Check if it's a Cloudinary URL
        url_str = str(value.url) if hasattr(value, "url") else str(value)
        if any(
            domain in url_str for domain in ["cloudinary.com", "res.cloudinary.com"]
        ):
            return  # Skip extension validation for Cloudinary URLs

    # For local files or new uploads, validate file extension
    if hasattr(value, "name") and value.name:
        allowed_extensions = ["jpg", "jpeg", "png", "webp"]
        # Get file extension
        file_ext = os.path.splitext(value.name)[1][1:].lower()

        if file_ext and file_ext not in allowed_extensions:
            raise ValidationError(
                f'File extension "{file_ext}" is not allowed. '
                f'Allowed extensions are: {", ".join(allowed_extensions)}.'
            )

    # If it's a file object, also validate using Django's validator for new uploads
    if hasattr(value, "file"):
        validator = FileExtensionValidator(
            allowed_extensions=["jpg", "jpeg", "png", "webp"]
        )
        try:
            validator(value)
        except ValidationError:
            # Only raise if it's not a Cloudinary URL
            if not (hasattr(value, "url") and "cloudinary" in str(value.url)):
                raise


def validate_image_size(image):
    max_size_kb = 5000  # 5 MB
    if image.size > max_size_kb * 1024:
        raise ValidationError(f"Image file size must not exceed {max_size_kb} KB.")


def unique_image_path(instance, filename):
    ext = filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4().hex}_{int(now().timestamp())}.{ext}"

    return os.path.join("places", unique_filename)
