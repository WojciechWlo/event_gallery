from PIL import Image, ImageOps
import os

def convert_image_to_webp(file_path: str) -> str:

    image = Image.open(file_path)
    image = ImageOps.exif_transpose(image)
    webp_path = os.path.splitext(file_path)[0] + ".webp"
    
    image.save(webp_path, "WEBP")
    image.close()
    
    os.remove(file_path)
    return webp_path