import streamlit as st
from PIL import Image, ImageDraw, ImageFont

def generate_screenshot(username, hostname, folder, commands, output, file_path):
    width, height = 800, 600
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
    
    def draw_prompt(x, y, command=None):
        parts = [
            (f"{username}@{hostname}", username_color, bold_font),
            (":", text_color, font),
            (folder, symbol_color, font),
            ("$", text_color, font)
        ]
        if command:
            parts.append((f" {command}", text_color, font))
        for text, color, font_type in parts:
            draw.text((x, y), text, font=font_type, fill=color)
            x += draw.textbbox((0, 0), text, font=font_type)[2]
        return y + font_size + 4

    y = 20
    x = 20
    for command in commands:
        y = draw_prompt(x, y, command=command)
    
    for line in output.split('\n'):
        draw.text((20, y), line, font=font, fill=text_color)
        y += font_size + 4
    
    y = draw_prompt(x, y, command=None)

    image.save(file_path)
    return image

def main():
    st.title("Terminal Screenshot Generator")
    if "commands" not in st.session_state:
        st.session_state.commands = [""]
    
    username = st.text_input("Username", value="csea2")
    hostname = st.text_input("Hostname", value="sjcet-H81M-DS2")
    folder = st.text_input("Folder", value="~/Documents")
    
    commands = []
    for i, command in enumerate(st.session_state.commands):
        commands.append(st.text_input(f"Command {i + 1}", value=command, key=f"command_{i + 1}"))
      
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Add Command"):
            st.session_state.commands.append("")
    with col2:
        if st.button("Delete Last Command"):
            if st.session_state.commands:
                st.session_state.commands.pop()
    
    output = st.text_area("Output", value="Hello, World!")
    
    if st.button("Generate Screenshot"):
        file_path = "terminal_screenshot.png"
        image = generate_screenshot(username, hostname, folder, commands, output, file_path)
        
        st.image(image, caption='Generated Terminal Screenshot')

        with open(file_path, "rb") as file:
            btn = st.download_button(
                label="Download Image",
                data=file,
                file_name="terminal_screenshot.png",
                mime="image/png"
            )

if __name__ == "__main__":
    main()
