import tkinter as tk
from gui.generate_window import generate_window
from gui.generate_window import upload_data
from gui.display_data import display_window

window = tk.Tk()
window.title('Vehicle Routing Problem Solver')
window_width = 400
window_height = 100
window.geometry('{}x{}'.format(window_width, window_height))
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)

# Set the position of the window to the center of the screen
window.geometry("+{}+{}".format(position_right, position_top))

window.configure(background='white')
label_font = ('Arial', 12)
frame = tk.Frame(window)
frame.configure(background='white')
frame.place(relx=0.5, rely=0.5, anchor='center')

# add option to choose Generate Random Data or Upload Data
generate_button = tk.Button(frame, text="Generate Random Data", command=lambda: generate_window(window), font=label_font, bg='white')
generate_button.grid(row=0, column=0, padx=10)

upload_button = tk.Button(frame, text="Upload Data", command=upload_data ,font=label_font, bg='white')
upload_button.grid(row=0, column=1, padx=10)

run_algorithm_button = tk.Button(frame, text="Run Algorithm", command=lambda: display_window(window), font=label_font, bg='white')
run_algorithm_button.grid(row=1, column=0 , pady=10)

window.mainloop()

# Path: main.py