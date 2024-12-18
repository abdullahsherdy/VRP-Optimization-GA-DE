import tkinter as tk
from algorithm.differential_evolution import run_algorithm as run_diff_evo
# create a new window to get the population_size and generations count and crossover rate and mutation factor 
def diff_evo_window(window,nodes,capacity):
    window.destroy()
    window = tk.Tk()
    window.title('Differential Evolution')
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

    generations_label = tk.Label(frame, text="Generations", font=label_font, bg='white')
    generations_label.grid(row=1, column=0, padx=10, pady=10)

    generations_entry = tk.Entry(frame, font=label_font, bg='white')
    generations_entry.grid(row=1, column=1, padx=10, pady=10)

    crossover_rate_label = tk.Label(frame, text="Crossover Rate", font=label_font, bg='white')
    crossover_rate_label.grid(row=2, column=0, padx=10, pady=10)

    crossover_rate_entry = tk.Entry(frame, font=label_font, bg='white')
    crossover_rate_entry.grid(row=2, column=1, padx=10, pady=10)

    mutation_factor_label = tk.Label(frame, text="Mutation Factor", font=label_font, bg='white')
    mutation_factor_label.grid(row=3, column=0, padx=10, pady=10)

    mutation_factor_entry = tk.Entry(frame, font=label_font, bg='white')
    mutation_factor_entry.grid(row=3, column=1, padx=10, pady=10)
    
    def run_algorithm():
        population_size = population_size_entry.get() or 30
        population_size = int(population_size) 
        generations = generations_entry.get()  or 200
        generations = int(generations)
        crossover_rate = crossover_rate_entry.get() or 0.5
        crossover_rate = float(crossover_rate)
        mutation_factor = mutation_factor_entry.get() or 0.5
        mutation_factor = float(mutation_factor)
        run_diff_evo(population_size,generations,crossover_rate,mutation_factor,nodes,capacity)
        window.destroy()
    run_algorithm_button = tk.Button(frame, text="Run Algorithm", command=run_algorithm, font=label_font, bg='white')
    run_algorithm_button.grid(row=4, column=0, padx=10, pady=10)
    
    window.mainloop()
    