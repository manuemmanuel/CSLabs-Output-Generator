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
