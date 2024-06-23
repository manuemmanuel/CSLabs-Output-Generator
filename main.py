from PIL import Image, ImageDraw, ImageFont
def generate_screenshot:
    width = 800
    height = 600
    background_color = (58, 12, 43)
    text_color = (255, 255, 255)
    username_color = (63, 116, 98)
    symbol_color = (55, 59, 105)
    font_path = "fonts/UbuntuMono-R.ttf"
    bold_font_path = "fonts/UbuntuMono-B.ttf"
    font_size = 20

    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(font_path, font_size)
    bold_font = ImageFont.truetype(bold_font_path, font_size)

    prompt = f"{username}@{hostname}:{folder}$ {command}"