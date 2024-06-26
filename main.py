import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from typing import List

WIDTH = 800
BACKGROUND_COLOR = (58, 12, 43)
TEXT_COLOR = (255, 255, 255)
USERNAME_COLOR = (63, 116, 98)
SYMBOL_COLOR = (55, 59, 105)
FONT_PATH = "fonts/UbuntuMono-R.ttf"
BOLD_FONT_PATH = "fonts/UbuntuMono-B.ttf"
FONT_SIZE = 20
LINE_PADDING = 4
SIDE_PADDING = 20

def calculate_height(commands: List[str], outputs: List[str], font_size: int, padding: int) -> int:
    total_lines = len(commands) + 1 
    for output in outputs:
        total_lines += output.count('\n') + 1 
    
    height = (total_lines * (font_size + padding)) + (2 * padding) 
    return height

@st.cache_data
def generate_screenshot(username: str, hostname: str, folder: str, commands: List[str], outputs: List[str], file_path: str) -> Image.Image:
    temp_image = Image.new("RGB", (1, 1))
    temp_draw = ImageDraw.Draw(temp_image)
    
    try:
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
        bold_font = ImageFont.truetype(BOLD_FONT_PATH, FONT_SIZE)
    except IOError:
        st.error("Error loading fonts. Please check if the font files exist.")
        return None

    prompt = f"{username}@{hostname}:{folder}$ "
    prompt_width = temp_draw.textbbox((0, 0), prompt, font=bold_font)[2]

    max_content_width = max([
        temp_draw.textbbox((0, 0), cmd, font=font)[2] for cmd in commands
    ] + [
        max([temp_draw.textbbox((0, 0), line, font=font)[2] for line in output.split('\n')])
        for output in outputs
    ])

    total_width = max(WIDTH, prompt_width + max_content_width + 2 * SIDE_PADDING)

    total_height = calculate_height(commands, outputs, FONT_SIZE, LINE_PADDING)

    image = Image.new("RGB", (total_width, total_height), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(image)

    def draw_prompt(x: int, y: int, command: str = None) -> int:
        parts = [
            (f"{username}@{hostname}", USERNAME_COLOR, bold_font),
            (":", TEXT_COLOR, font),
            (folder, SYMBOL_COLOR, font),
            ("$", TEXT_COLOR, font)
        ]
        if command:
            parts.append((f" {command}", TEXT_COLOR, font))
        for text, color, font_type in parts:
            draw.text((x, y), text, font=font_type, fill=color)
            x += draw.textbbox((0, 0), text, font=font_type)[2]
        return y + FONT_SIZE + LINE_PADDING

    y = SIDE_PADDING
    x = SIDE_PADDING
    for command, output in zip(commands, outputs):
        y = draw_prompt(x, y, command=command)
        if output.strip():
            for line in output.split('\n'):
                draw.text((SIDE_PADDING, y), line, font=font, fill=TEXT_COLOR)
                y += FONT_SIZE + LINE_PADDING
    
    draw_prompt(x, y, command=None)

    try:
        image.save(file_path)
    except IOError:
        st.error("Error saving the image. Please check file permissions.")
        return None

    return image

def main():
    st.title("Terminal Screenshot Generator")
    
    with st.expander("How to Use This Application"):
        st.markdown("""
        ### Terminal Screenshot Generator Guide

        The Terminal Screenshot Generator is a simple Streamlit-based web application that allows you to create terminal screenshots with customized commands and outputs. This guide will walk you through the steps to use the application effectively.

        #### Getting Started

        1. **Access the Application**: Open the application in your web browser. You should see the title "Terminal Screenshot Generator" at the top.
        2. **Initial Setup**: When you first load the application, it will initialize with one empty command and one empty output text field.

        #### Step-by-Step Instructions

        1. **Enter User Details**:

        - **Username**: Enter your desired username in the "Username" input box (default is `csea2`).
        - **Hostname**: Enter the hostname for your terminal in the "Hostname" input box (default is `sjcet-H81M-DS2`).
        - **Folder**: Specify the current working directory or folder in the "Folder" input box (default is `~/Documents`).
        - **Image file name**: Enter the desired file name for the generated image in the "Image file name" input box (default is `filename`).

        2. **Add Commands and Outputs**:

        - **Commands**: Enter your commands sequentially in the "Command 1", "Command 2", etc., input boxes. If you need more commands, click the "Add Command" button to create a new command input field.
        - **Outputs**: For each command, you can specify the output in the corresponding "Output 1", "Output 2", etc., text areas. If there is no output for a command, you can leave the output text area blank.

        3. **Manage Commands**:

        - **Add Command**: Click the "Add Command" button to add a new command input field along with its corresponding output text area. The interface will update immediately to reflect the new input fields.
        - **Delete Command**: Click the "Delete Command" button to remove the last command and its associated output text area. The interface will update immediately to reflect the removal.

        4. **Generate Screenshot**:

        - Once you have entered all the commands and their outputs, click the "Generate Image" button. This will create a terminal screenshot based on the provided details.
        - The generated screenshot will be displayed below the button with the caption "Generated Terminal Screenshot".

        5. **Download the Screenshot**:
        - To download the generated screenshot, click the "Download Image" button. This will download the image with the file name you specified.

        #### Example Usage

        Let's go through an example scenario to illustrate how you can use the Terminal Screenshot Generator:

        1. **Username**: `user`
        2. **Hostname**: `my-computer`
        3. **Folder**: `~/projects`
        4. **Image file name**: `my_terminal_screenshot`

        **Commands and Outputs**:

        1. **Command 1**: `gcc main.c`
        - **Output 1**: (leave blank)
        2. **Command 2**: `./a.out`
        - **Output 2**: `Hello, World!`

        **Steps**:

        1. Enter `user` in the Username field.
        2. Enter `my-computer` in the Hostname field.
        3. Enter `~/projects` in the Folder field.
        4. Enter `my_terminal_screenshot` in the Image file name field.
        5. Enter `gcc main.c` in the "Command 1" field and leave the "Output 1" field blank.
        6. Click "Add Command" to create a new command field.
        7. Enter `./a.out` in the "Command 2" field.
        8. Enter `Hello, World!` in the "Output 2" field.
        9. Click the "Generate Image" button to create the screenshot.
        10. View the generated screenshot displayed on the page.
        11. Click the "Download Image" button to save the screenshot to your computer.

        """)

    if "terminal_data" not in st.session_state:
        st.session_state.terminal_data = [{"command": "", "output": ""}]

    username = st.text_input("Username", value="csea2")
    hostname = st.text_input("Hostname", value="sjcet-H81M-DS2")
    folder = st.text_input("Folder", value="~/Documents")
    file_name = st.text_input("Image file name", value="filename")

    for i, data in enumerate(st.session_state.terminal_data):
        command = st.text_input(f"Command {i + 1}", value=data["command"], key=f"command_{i + 1}")
        output = st.text_area(f"Output {i + 1}", value=data["output"], key=f"output_{i + 1}")
        st.session_state.terminal_data[i] = {"command": command, "output": output}
    
    st.write('')
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("Add command"):
            st.session_state.terminal_data.append({"command": "", "output": ""})
            st.experimental_rerun()
    with col2:
        if st.button("Delete command"):
            if len(st.session_state.terminal_data) > 1:
                st.session_state.terminal_data.pop()
                st.experimental_rerun()
    with col3:
        if st.button("Generate Image"):
            commands = [data["command"] for data in st.session_state.terminal_data]
            outputs = [data["output"] for data in st.session_state.terminal_data]
            
            file_path = f"{file_name}.png"
            image = generate_screenshot(username, hostname, folder, commands, outputs, file_path)
            
            if image:
                st.image(image, caption='Generated Terminal Screenshot', use_column_width=True)

                with open(file_path, "rb") as file:
                    st.download_button(
                        label="Download Image",
                        data=file,
                        file_name=f"{file_name}.png",
                        mime="image/png"
                    )

if __name__ == "__main__":
    main()
