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
