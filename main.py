import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from typing import List

css = """
<style>
    /* Import a monospace font */
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono&display=swap');

    /* Apply the font to the entire app */
    html, body, [class*="css"]  {
        font-family: 'Roboto Mono', monospace !important;
    }

    /* Style for all text elements */
    div, p, span, li, code, pre {
        font-family: 'Roboto Mono', monospace !important;
    }

    /* Style for input fields */
    input, textarea {
        font-family: 'Roboto Mono', monospace !important;
    }

    /* Style for titles and labels */
    h1, h2, h3, h4, h5, h6, label, .stSelectbox label {
        font-family: 'Roboto Mono', monospace !important;
    }

    /* Style for buttons */
    button, .stButton>button, .stDownloadButton>button {
        font-family: 'Roboto Mono', monospace !important;
    }

    /* Style for dropdown options */
    .stSelectbox>div>div>select, div[data-baseweb="select"] > div, 
    div[data-baseweb="select"] span, div[data-baseweb="select"] ul {
        font-family: 'Roboto Mono', monospace !important;
    }

    /* Additional styles to cover more Streamlit components */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        font-family: 'Roboto Mono', monospace !important;
    }

    .stMarkdown, .stText, .stCode {
        font-family: 'Roboto Mono', monospace !important;
    }

    /* Style for radio buttons and checkboxes */
    .stRadio label, .stCheckbox label {
        font-family: 'Roboto Mono', monospace !important;
    }

    /* Ensure sidebar also uses monospace */
    .sidebar .sidebar-content {
        font-family: 'Roboto Mono', monospace !important;
    }
</style>
"""

# Set page config to inject the CSS
st.set_page_config(page_title="Terminal Screenshot Generator", page_icon="🖥️", initial_sidebar_state="expanded")

# Inject CSS with markdown
st.markdown(css, unsafe_allow_html=True)

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

COLOR_MAP = {
    "White": (255, 255, 255),
    "Blue": (55, 59, 105),
    "Green": (63, 116, 98)
}

def calculate_height(commands: List[str], outputs: List[str], font_size: int, padding: int) -> int:
    total_lines = len(commands) + 1 
    for output in outputs:
        total_lines += output.count('\n') + 1 
    
    height = (total_lines * (font_size + padding)) + (2 * padding) 
    return height

@st.cache_data
def generate_screenshot(username: str, hostname: str, folder: str, commands: List[str], outputs: List[str], colors: List[str], file_path: str) -> Image.Image:
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
    for command, (output, color) in zip(commands, zip(outputs, colors)):
        y = draw_prompt(x, y, command=command)
        if output.strip():
            for line in output.split('\n'):
                draw.text((SIDE_PADDING, y), line, font=font, fill=COLOR_MAP[color])
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
        # Terminal Screenshot Generator Guide

        The Terminal Screenshot Generator is a Streamlit-based web application that allows you to create customized terminal screenshots. This guide will walk you through the steps to use the application effectively.
        
        ## Getting Started
        
        1. **Access the Application**: Open the application in your web browser. You'll see the title "Terminal Screenshot Generator" at the top.
        2. **Initial Setup**: The application initializes with one empty command and one empty output text field.
        
        ## Step-by-Step Instructions
        
        ### 1. Enter User Details
        
        - **Username**: Enter your desired username (default is `csea2`).
        - **Hostname**: Enter the hostname for your terminal (default is `sjcet-H81M-DS2`).
        - **Folder**: Specify the current working directory or folder (default is `~/Documents`).
        - **Image file name**: Enter the desired file name for the generated image (default is `filename`).
        - **Image file format**: Select the desired file format from the dropdown menu (options: png, jpg, jpeg, svg, webp).
        
        ### 2. Add Commands and Outputs
        
        - **Commands**: Enter your commands sequentially in the "Command 1", "Command 2", etc., input boxes.
        - **Outputs**: For each command, specify the output in the corresponding "Output 1", "Output 2", etc., text areas. Leave blank if there's no output.
        - **Output Color**: For each output, select a color from the dropdown menu (options: White, Blue, Green).
        
        ### 3. Manage Commands
        
        - **Add Command**: Click the "Add command" button to add a new set of command, output, and color fields.
        - **Delete Command**: Click the "Delete command" button to remove the last set of command, output, and color fields.
        
        ### 4. Generate Screenshot
        
        - After entering all details, click the "Generate Image" button to create the terminal screenshot.
        - The generated screenshot will be displayed below with the caption "Generated Terminal Screenshot".
        
        ### 5. Download the Screenshot
        
        - Click the "Download Image" button to save the screenshot with the specified file name and format.
        
        ## New Features
        
        1. **Color Selection**: You can now choose a color for each command output (White, Blue, or Green).
        2. **File Format Selection**: You can select the desired image file format (png, jpg, jpeg, svg, webp).
        3. **Expanded How-to Guide**: An expandable section with detailed instructions is now available at the top of the application.
        
        ## Example Usage
        
        1. **Username**: `user`
        2. **Hostname**: `my-computer`
        3. **Folder**: `~/projects`
        4. **Image file name**: `my_terminal_screenshot`
        5. **Image file format**: `png`
        
        **Commands, Outputs, and Colors**:
        1. **Command 1**: `gcc main.c`
           - **Output 1**: (leave blank)
           - **Color 1**: White
        2. **Command 2**: `./a.out`
           - **Output 2**: `Hello, World!`
           - **Color 2**: Green
        
        **Steps**:
        1. Fill in the user details as specified above.
        2. Enter the commands, outputs, and select colors as described.
        3. Click "Generate Image" to create the screenshot.
        4. View the generated screenshot on the page.
        5. Click "Download Image" to save the screenshot to your computer.

        """)

    if "num_commands" not in st.session_state:
        st.session_state.num_commands = 1

    username = st.text_input("Username", value="csea2")
    hostname = st.text_input("Hostname", value="sjcet-H81M-DS2")
    folder = st.text_input("Folder", value="~/Documents")
    file_name = st.text_input("Image file name", value="filename")
    file_format = st.selectbox("Image file format", options=["png", "jpg", "jpeg", "svg", "webp"])

    commands = []
    outputs = []
    colors = []

    for i in range(st.session_state.num_commands):
        command = st.text_input(f"Command {i + 1}", key=f"command_{i}")
        output = st.text_area(f"Output {i + 1}", key=f"output_{i}")
        color = st.selectbox(f"Output Color {i + 1}", options=["White", "Blue", "Green"], key=f"color_{i}")
        
        commands.append(command)
        outputs.append(output)
        colors.append(color)
    
    st.write('')
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("Add command"):
            st.session_state.num_commands += 1
            st.rerun()
    with col2:
        if st.button("Delete command") and st.session_state.num_commands > 1:
            st.session_state.num_commands -= 1
            st.rerun()
    with col3:
        if st.button("Generate Image"):
            file_path = f"{file_name}.{file_format}"
            image = generate_screenshot(username, hostname, folder, commands, outputs, colors, file_path)
            
            if image:
                st.image(image, caption='Generated Terminal Screenshot', use_column_width=True)

                with open(file_path, "rb") as file:
                    st.download_button(
                        label="Download Image",
                        data=file,
                        file_name=f"{file_name}.{file_format}",
                        mime=f"image/{file_format}"
                    )

main()
