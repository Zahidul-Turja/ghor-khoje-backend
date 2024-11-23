from django.core.exceptions import ValidationError
from django.utils.timezone import now
import os
import uuid


def validate_image_size(image):
    max_size_kb = 5000  # 5 MB
    if image.size > max_size_kb * 1024:
        raise ValidationError(f"Image file size must not exceed {max_size_kb} KB.")


def unique_image_path(instance, filename):
    ext = filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4().hex}_{int(now().timestamp())}.{ext}"

    return os.path.join("places", unique_filename)
