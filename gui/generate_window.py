import tkinter as tk
from tkinter import filedialog
# import from vrp-sample-gen.py the generate function
from vrp_sample_gen import generate

def generate_window(window):
    # create a new window
    random_data_window = tk.Toplevel(window)
    random_data_window.title('Generate Random Data')
    random_data_window.geometry('400x400')
    random_data_window.resizable(False, False)
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    random_data_window_width = 400
    random_data_window_height = 400
    position_top = int(screen_height / 2 - random_data_window_height / 2)
    position_right = int(screen_width / 2 - random_data_window_width / 2)
    
    # Set the position of the window to the center of the screen
    random_data_window.geometry("+{}+{}".format(position_right, position_top))
    
    random_data_window.configure(background='white')

    # create a frame to hold the input fields
    input_frame = tk.Frame(random_data_window, bg='white')
    input_frame.pack(pady=20)

    # create a frame to hold the buttons
    button_frame = tk.Frame(random_data_window, bg='white')
    button_frame.pack(pady=20)

    # create the input fields
    label_font = ('Arial', 12)
    entry_font = ('Arial', 10)

    nodescount_label = tk.Label(input_frame, text="Number of Nodes", font=label_font, bg='white')
    nodescount_label.grid(row=0, column=0, padx=10, pady=10)
    nodescount_entry = tk.Entry(input_frame, font=entry_font)
    nodescount_entry.grid(row=0, column=1, padx=10, pady=10)

    maxcap_label = tk.Label(input_frame, text="Maximum Capacity", font=label_font, bg='white')
    maxcap_label.grid(row=1, column=0, padx=10, pady=10)
    maxcap_entry = tk.Entry(input_frame, font=entry_font)
    maxcap_entry.grid(row=1, column=1, padx=10, pady=10)
    
    minX_label = tk.Label(input_frame, text="Minimum X", font=label_font, bg='white')
    minX_label.grid(row=2, column=0, padx=10, pady=10)
    minX_entry = tk.Entry(input_frame, font=entry_font)
    minX_entry.grid(row=2, column=1, padx=10, pady=10)
    
    maxX_label = tk.Label(input_frame, text="Maximum X", font=label_font, bg='white')
    maxX_label.grid(row=3, column=0, padx=10, pady=10)
    maxX_entry = tk.Entry(input_frame, font=entry_font)
    maxX_entry.grid(row=3, column=1, padx=10, pady=10)
    
    minY_label = tk.Label(input_frame, text="Minimum Y", font=label_font, bg='white')
    minY_label.grid(row=4, column=0, padx=10, pady=10)
    minY_entry = tk.Entry(input_frame, font=entry_font)
    minY_entry.grid(row=4, column=1, padx=10, pady=10)
    
    maxY_label = tk.Label(input_frame, text="Maximum Y", font=label_font, bg='white')
    maxY_label.grid(row=5, column=0, padx=10, pady=10)
    maxY_entry = tk.Entry(input_frame, font=entry_font)
    maxY_entry.grid(row=5, column=1, padx=10, pady=10)
    
    # create the generate button
    generate_button = tk.Button(button_frame, text="Generate", command=lambda: generate_data(nodescount_entry.get() or 10, maxcap_entry.get() or 50, minX_entry.get()or -20, maxX_entry.get()or 20, minY_entry.get() or -10, maxY_entry.get() or 10,
                                                                                             random_data_window.destroy()), font=label_font, bg='white')
    generate_button.grid(row=0, column=0, padx=10)

    # create the cancel button
    cancel_button = tk.Button(button_frame, text="Cancel", command=random_data_window.destroy ,font=label_font, bg='white')
    cancel_button.grid(row=0, column=1, padx=10)
    
def generate_data(nodescount, maxcap, minX, maxX, minY, maxY, window):
    """
      this function will be called when the user clicks the generate button
      it will generate the random data and save it in a file called input.txt
    """
    # generate the data
    data = generate(int(nodescount), float(maxcap), float(minX), float(maxX), float(minY), float(maxY))
    # save the data in a file called input.txt
    with open('input.txt', 'w') as f:
        f.write(data)


def upload_data():
    filename = filedialog.askopenfilename()
    if filename == '':
        return
    # rename the file to input.txt then save it in the same directory
    with open(filename, 'r') as f:
        data = f.read()
    with open('input.txt', 'w') as f:
        f.write(data)