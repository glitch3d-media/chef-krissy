from PIL import Image, ImageDraw, ImageOps

def rotate_image(img: Image.Image) -> Image.Image:
    """Rotates the image 90 degrees clockwise."""
    return img.rotate(-90, expand=True)

def crop_image(img: Image.Image, box: tuple) -> Image.Image:
    """Crops the image to a bounding box (left, upper, right, lower)."""
    # Ensure the box is within the image bounds
    width, height = img.size
    left, upper, right, lower = box
    left = max(0, min(left, width))
    right = max(0, min(right, width))
    upper = max(0, min(upper, height))
    lower = max(0, min(lower, height))
    
    if right > left and lower > upper:
        return img.crop((left, upper, right, lower))
    return img

def apply_mask(img: Image.Image, mask_type: str) -> Image.Image:
    """Applies a transparent mask (rectangle, rounded, circle) to the image."""
    width, height = img.size
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)

    if mask_type == "circle":
        # Fit the circle to the shortest dimension
        radius = min(width, height) // 2
        center = (width // 2, height // 2)
        draw.ellipse(
            (center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius), 
            fill=255
        )
    elif mask_type == "rounded":
        draw.rounded_rectangle((0, 0, width, height), radius=min(width, height)//8, fill=255)
    else:
        # Rectangle
        draw.rectangle((0, 0, width, height), fill=255)

    # Convert original to RGBA and apply mask to alpha channel
    img = img.convert("RGBA")
    img.putalpha(mask)
    return img

def remove_background(img: Image.Image, target_color: tuple, tolerance: int = 30) -> Image.Image:
    """
    Removes a specific color from the image, making it transparent.
    tolerance: 0 (exact match) to 255 (broad match).
    """
    img = img.convert("RGBA")
    datas = img.getdata()
    new_data = []
    
    tr, tg, tb = target_color

    for item in datas:
        # Check if the pixel is within the tolerance range of the target color
        if (abs(item[0] - tr) <= tolerance and 
            abs(item[1] - tg) <= tolerance and 
            abs(item[2] - tb) <= tolerance):
            # Make transparent
            new_data.append((255, 255, 255, 0))
        else:
            # Keep original pixel
            new_data.append(item)
            
    img.putdata(new_data)
    return img