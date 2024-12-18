import tkinter as tk
from tkinter import ttk
# from gui.diff_evo import diff_evo
from gui.diff_evo import diff_evo_window
from gui.genetic_algo import genetic_algo_window
from gui.both_algo import both_algo_window

def display_window(window):
    # create a new window
    run_window = tk.Toplevel(window)
    run_window.title('Run Algorithm')
    run_window.resizable(False, False)
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()


    # create the input fields
    label_font = ('Arial', 12)
    entry_font = ('Arial', 10)
    # read and display the data in input.txt
    with open('input.txt', 'r') as file:
        data = file.readlines()
        # if file is empty then return
        if not data:
            return
        cap = float(data[1].split()[1])
        # for loop from nodes_start to end of file
        # create a list of lists
        # each list is a node
        # each node has x, y, demand
        nodes = []
        for i in range(3, len(data)):
            # split the line into a list of strings
            node = data[i].split()
            # convert the strings to floats except for the name
            node[1] = float(node[1])
            node[2] = float(node[2])
            node[3] = float(node[3])
            # add the node to the list of nodes
            nodes.append(node)

    run_window_width = 400
    run_window_height = 400
    run_window.geometry('{}x{}'.format(run_window_width, run_window_height))
    position_top = int(screen_height / 2 - run_window_height / 2)
    position_right = int(screen_width / 2 - run_window_width / 2)
    
    # Set the position of the window to the center of the screen
    run_window.geometry("+{}+{}".format(position_right, position_top))
    # create a table to display the data
    run_window.configure(background='white')
    myTable = ttk.Treeview(run_window)
    myTable["columns"]=("name","demand","x","y")
    myTable.column("#0", width=0, stretch=tk.NO)
    myTable.column("name", width=80, minwidth=80, stretch=tk.NO)
    myTable.column("demand", width=80, minwidth=80, stretch=tk.NO)
    myTable.column("x", width=80, minwidth=80, stretch=tk.NO)
    myTable.column("y", width=80, minwidth=80, stretch=tk.NO)
    myTable.heading("name",text="Name",anchor=tk.W)
    myTable.heading("demand", text="Demand",anchor=tk.W)
    myTable.heading("x", text="X",anchor=tk.W)
    myTable.heading("y", text="Y",anchor=tk.W)
    myTable.pack(pady=20)
    for i in range(len(nodes)):
        myTable.insert(parent='', index='end', iid=i, text="", values=(nodes[i][0],nodes[i][1],nodes[i][2],nodes[i][3]))
        
    # create a frame to hold the buttons
    button_frame = tk.Frame(run_window, bg='white')
    button_frame.pack(pady=20)
        # create a function to run both algorithms
    def run_both():
        both_algo_window(run_window, nodes, cap)
        pass
    # create a function to run the first algorithm
    def run_first():
        genetic_algo_window(run_window, nodes, cap)
        pass
    # create a function to run the second algorithm
    def run_second():
        diff_evo_window(run_window, nodes, cap)
        pass
    # # create the buttons to select run both algorithms or just one of them
    both_button = tk.Button(button_frame, text="Run Both Algorithms", command=lambda: run_both(), font=label_font, bg='white')
    both_button.grid(row=1, column=0, padx=10 , pady=10)

    # create the buttons to select run the first algorithm
    first_button = tk.Button(button_frame, text="Run Genetic Algorithm", command=lambda: run_first(), font=label_font, bg='white')
    first_button.grid(row=0, column=0, padx=10 , pady=10)
    # create the buttons to select run the second algorithm
    second_button = tk.Button(button_frame, text="Run Differential Evolution", command=lambda: run_second(), font=label_font, bg='white')
    second_button.grid(row=0, column=1, padx=10 , pady=10)
    
    
    # add a button to go back to main menu
    back_button = tk.Button(button_frame, text="Back", command=lambda: run_window.destroy(), font=label_font, bg='white')
    back_button.grid(row=1, column=1, padx=10 , pady=10)
