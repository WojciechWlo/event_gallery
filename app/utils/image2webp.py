from PIL import Image
import os

def convert_image_to_webp(file_path: str) -> str:
    """Konwertuje obraz do formatu WebP i usuwa oryginał."""
    image = Image.open(file_path)
    webp_path = os.path.splitext(file_path)[0] + ".webp"
    
    image.save(webp_path, "WEBP")
    image.close()
    
    os.remove(file_path)  # usuń oryginalny plik
    return webp_path