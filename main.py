from PIL import Image, ImageDraw, ImageFont
def generate_screenshot(username, hostname, folder, command, output, file_path):
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
    prompt_parts = [
        (f"{username}@{hostname}", username_color, bold_font),
        (":", text_color, font),
        (folder, symbol_color, font),
        ("$", text_color, font),
        (f"{command}", text_color, font)
    ]

    y = 20
    x = 20
    for text, color, font_type in prompt_parts:
        draw.text((x,y), text, font=font_type, fill=color)
        x += draw.textbbox((0, 0), text, font=font_type)[2]

    y += font_size + 4
    for line in output.split('\n'):
        draw.text((20, y), line, font=font, fill=text_color)
        y += font_size + 4
         
    