
import tkinter as tk
from llm import get_new_coordinates
from PIL import Image, ImageGrab
from algorithm import initialize, validate
import threading
import time

# Initial matrix data (replace this with your matrix)
initial_matrix = [
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
]

# Global variables
matrix_frame = None
coordinate_text = None
loading_label = None
loading = False
matrix_labels = []  # List to store labels for each cell in the matrix
coordinates = [None, None]

# Function to update the matrix and get coordinates asynchronously
def update_matrix_async(validateAns=None):
    global loading, loading_label, coordinates
    loading = True
    loading_label.config(text="Waiting for LLM's response...")  # Display loading message
    if(validateAns == None):
        validateAns = validate(coordinates[0], coordinates[1])
    print("validateAns: ", validateAns)
    
    # Get the new matrix
    # Update the matrix
    if(type(validateAns) is list):
        new_matrix = '\n'.join([''.join(row) for row in validateAns[1]])
        update_matrix(new_matrix)
        if(validateAns[0]):
            loading_label.config(state=tk.DISABLED)
            loading_label.pack_forget()
            update_button.config(state=tk.DISABLED)
            update_button.pack_forget()
            update_matrix_highlight(coordinates, new_matrix, game_over=True)
        else:
            # Get coordinates asynchronously
            threading.Thread(target=get_coordinates_async, args=(new_matrix,)).start()
    else:
        new_matrix = validateAns
        update_matrix(new_matrix)
        threading.Thread(target=get_coordinates_async, args=(new_matrix,)).start()

# Function to get coordinates asynchronously
def get_coordinates_async(new_matrix):
    global coordinates, loading, loading_label

    time.sleep(2)
    root.update()
    # Capture the current screen area containing the matrix_frame
    x, y, w, h = root.winfo_rootx() + matrix_frame.winfo_x(), root.winfo_rooty() + matrix_frame.winfo_y(), matrix_frame.winfo_width(), matrix_frame.winfo_height()
    screenshot = ImageGrab.grab(bbox=(x, y, x + w, y + h))
    coordinates = get_new_coordinates(screenshot)

    if not loading:
        return

    loading = False
    loading_label.config(text="")  # Clear loading message

    # Highlight the coordinates
    update_matrix_highlight(coordinates, new_matrix)

# Create a function to update the matrix with highlighted coordinates
def update_matrix_highlight(coordinates, new_matrix, game_over = False):
    try:
        matrix_data = [list(row.strip()) for row in new_matrix.split('\n')]

        # Display the updated matrix
        for i, row_data in enumerate(matrix_data):
            for j, cell_data in enumerate(row_data):
                # Convert the integer to a string
                cell_text = str(cell_data)

                # Determine the background color for the selected cell
                if game_over and cell_text == 'M':
                    background_color = "red"
                elif cell_text == 'X':
                    background_color = "lightgray"
                elif cell_text == '3':
                    background_color = "orange"
                elif cell_text == '2':
                    background_color = "orange"
                elif cell_text == '1':
                    background_color = "yellow"
                elif i == coordinates[0] and j == coordinates[1]:
                    background_color = "lightblue"
                else:
                    background_color = "white"
                matrix_labels[i][j].config(text=cell_text, bg=background_color)

        # Display the selected coordinate text
        if(game_over):
            coordinate_text.config(text="Game Over! You opened a mine.", fg="red")
        else:
            coordinate_text.config(text=f"LLM suggested to open this: ({coordinates[0]}, {coordinates[1]})")
    except ValueError:
        error_label.config(text="Invalid input. Please enter a valid matrix.")

# Create a function to update the matrix (initialization and updates)
def update_matrix(new_matrix):
    global matrix_frame, matrix_labels  # Use the global variable

    try:
        matrix_data = [list(row.strip()) for row in new_matrix.split('\n')]

        # Initialize the matrix frame and labels if it's the first time
        if matrix_frame is None:
            matrix_frame = tk.Frame(root)
            matrix_frame.pack()
            matrix_labels = []

        # Display the updated matrix or update existing labels
        for i, row_data in enumerate(matrix_data):
            row_labels = []
            for j, cell_data in enumerate(row_data):
                cell_text = str(cell_data)
                if cell_text == 'M':
                    background_color = "red"
                elif cell_text == 'X':
                    background_color = "lightgray"
                elif cell_text == '3':
                    background_color = "orange"
                elif cell_text == '2':
                    background_color = "orange"
                elif cell_text == '1':
                    background_color = "yellow"
                elif i == coordinates[0] and j == coordinates[1]:
                    background_color = "lightblue"
                else:
                    background_color = "white"
                label = tk.Label(matrix_frame, text=cell_data, width=5, height=2, bg=background_color)
                label.grid(row=i, column=j)
                row_labels.append(label)
            matrix_labels.append(row_labels)

        # Display the selected coordinate text
        coordinate_text.config(text="LLM suggested to open this: loading..")
    except ValueError:
        error_label.config(text="Invalid input. Please enter a valid matrix.")



#init
initialize()
# Create the main window
root = tk.Tk()
root.title("Minesweeper LLM")

# Create a frame to hold the matrix (initializing the global variable)
matrix_frame = tk.Frame(root)
matrix_frame.pack()

# Create a button to update the matrix asynchronously
update_button = tk.Button(root, text="Go with it", command=update_matrix_async)
update_button.pack()

# Create a label to display the selected coordinate text
coordinate_text = tk.Label(root, text="", fg="blue")
coordinate_text.pack()

# Create a label to display loading message
loading_label = tk.Label(root, text="", fg="gray")
loading_label.pack()

# Create a label to display error messages
error_label = tk.Label(root, text="", fg="red")
error_label.pack()

# Initialize the matrix display with the initial initial_matrix
update_matrix_async('\n'.join([''.join(row) for row in initial_matrix]))

# Start the GUI main loop
root.mainloop()
