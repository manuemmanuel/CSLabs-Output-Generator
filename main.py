import streamlit as st
from PIL import Image, ImageDraw, ImageFont

def generate_screenshot(username, hostname, folder, commands, outputs, file_path):
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
    for command, output in zip(commands, outputs):
        y = draw_prompt(x, y, command=command)
        if output.strip():
            for line in output.split('\n'):
                draw.text((20, y), line, font=font, fill=text_color)
                y += font_size + 4
    
    y = draw_prompt(x, y, command=None)

    image.save(file_path)
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

        2. **Add Commands and Outputs**:
            - **Commands**: Enter your commands sequentially in the "Command 1", "Command 2", etc., input boxes. If you need more commands, click the "Add Command" button to create a new command input field.
            - **Outputs**: For each command, you can specify the output in the corresponding "Output 1", "Output 2", etc., text areas. If there is no output for a command, you can leave the output text area blank.

        3. **Manage Commands**:
            - **Add Command**: Click the "Add Command (+)" button to add a new command input field along with its corresponding output text area. The interface will update immediately to reflect the new input fields.
            - **Delete Command**: Click the "Delete Command (-)" button to remove the last command and its associated output text area. The interface will update immediately to reflect the removal.

        4. **Generate Screenshot**:
            - Once you have entered all the commands and their outputs, click the "Generate Image" button. This will create a terminal screenshot based on the provided details.
            - The generated screenshot will be displayed below the button with the caption "Generated Terminal Screenshot".

        5. **Download the Screenshot**:
            - To download the generated screenshot, click the "Download Image" button. This will download the image as `terminal_screenshot.png`.

        #### Example Usage
        Let's go through an example scenario to illustrate how you can use the Terminal Screenshot Generator:
        1. **Username**: `user`
        2. **Hostname**: `my-computer`
        3. **Folder**: `~/projects`
        
        **Commands and Outputs**:
        1. **Command 1**: `gcc main.c`
            - **Output 1**: (leave blank)
        2. **Command 2**: `./a.out`
            - **Output 2**: `Hello, World!`

        **Steps**:
        1. Enter `user` in the Username field.
        2. Enter `my-computer` in the Hostname field.
        3. Enter `~/projects` in the Folder field.
        4. Enter `gcc main.c` in the "Command 1" field and leave the "Output 1" field blank.
        5. Click "Add Command (+)" to create a new command field.
        6. Enter `./a.out` in the "Command 2" field.
        7. Enter `Hello, World!` in the "Output 2" field.
        8. Click the "Generate Image" button to create the screenshot.
        9. View the generated screenshot displayed on the page.
        10. Click the "Download Image" button to save the screenshot to your computer.

        #### Notes
        - The screenshot size is fixed at 800x600 pixels. If your commands and outputs are too long, they may not fit within the image. Adjust the content accordingly.
        """)

    if "commands" not in st.session_state:
        st.session_state.commands = [""]
        st.session_state.outputs = [""]

    username = st.text_input("Username", value="csea2")
    hostname = st.text_input("Hostname", value="sjcet-H81M-DS2")
    folder = st.text_input("Folder", value="~/Documents")
    
    commands = []
    outputs = []
    for i in range(len(st.session_state.commands)):
        commands.append(st.text_input(f"Command {i + 1}", value=st.session_state.commands[i], key=f"command_{i + 1}"))
        outputs.append(st.text_area(f"Output {i + 1}", value=st.session_state.outputs[i], key=f"output_{i + 1}"))
    
    st.write('')
    col1,col5, col2, col4,col6, col3 = st.columns([1,0.1,1, 1.9,1,0.9])
    with col1:
        if st.button("Add command"):
            st.session_state.commands.append("")
            st.session_state.outputs.append("")
            st.experimental_rerun()
    with col2:
        if st.button("Delete command"):
            if st.session_state.commands:
                st.session_state.commands.pop()
                st.session_state.outputs.pop()
                st.experimental_rerun()
    with col3:
        if st.button("Generate"):
            file_path = "terminal_screenshot.png"
            image = generate_screenshot(username, hostname, folder, commands, outputs, file_path)
            
            st.image(image, caption='Generated Terminal Screenshot')

            with open(file_path, "rb") as file:
                st.download_button(
                    label="Download Image",
                    data=file,
                    file_name="terminal_screenshot.png",
                    mime="image/png"
                )

if __name__ == "__main__":
    main()
