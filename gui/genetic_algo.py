import tkinter as tk
from algorithm.genetic_algorithm import run_algorithm as run_genetic

# create a new window to get the population_size, iterations, nodes, capacity 

def genetic_algo_window(window,nodes,capacity):
    window.destroy()
    window = tk.Tk()
    window.title('Genetic Algorithm')
    window_width = 400
    window_height = 300
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
    population_size_label = tk.Label(frame, text="Population Size", font=label_font, bg='white')
    population_size_label.grid(row=0, column=0, padx=10, pady=10)

    population_size_entry = tk.Entry(frame, font=label_font, bg='white')
    population_size_entry.grid(row=0, column=1, padx=10, pady=10)

    iterations_label = tk.Label(frame, text="Iterations", font=label_font, bg='white')
    iterations_label.grid(row=1, column=0, padx=10, pady=10)

    iterations_entry = tk.Entry(frame, font=label_font, bg='white')
    iterations_entry.grid(row=1, column=1, padx=10, pady=10)

    num_vechiles_label = tk.Label(frame, text="Iterations", font=label_font, bg='white')
    num_vechiles_label.grid(row=1, column=0, padx=10, pady=10)
    
    num_vechiles_entry = tk.Entry(frame, font=label_font, bg='white')
    num_vechiles_entry.grid(row=1, column=1, padx=10, pady=10)
    
    def run_algorithm():
        population_size = population_size_entry.get() or 30
        population_size = int(population_size) 
        iterations = iterations_entry.get()  or 200
        iterations = int(iterations)
        num_vechiles = num_vechiles_entry.get() or 5
        num_vechiles = int(num_vechiles)
        run_genetic(population_size,iterations,nodes,capacity,num_vechiles)
        window.destroy()
    run_button = tk.Button(frame, text="Run Algorithm", command=run_algorithm, font=label_font, bg='white')
    run_button.grid(row=2, column=0, padx=10 , pady=10)

    window.mainloop()