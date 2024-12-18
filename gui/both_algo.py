import tkinter as tk
from algorithm.differential_evolution import run_algorithm as run_diff_evo
from algorithm.genetic_algorithm import run_algorithm as run_genetic
import threading

# create a new window to get the population_size and generations count and crossover rate and mutation factor and iterations and population size
def both_algo_window(window,nodes,capacity):
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

    crossover_rate_label = tk.Label(frame, text="Crossover Rate", font=label_font, bg='white')
    crossover_rate_label.grid(row=2, column=0, padx=10, pady=10)

    crossover_rate_entry = tk.Entry(frame, font=label_font, bg='white')
    crossover_rate_entry.grid(row=2, column=1, padx=10, pady=10)

    mutation_factor_label = tk.Label(frame, text="Mutation Factor", font=label_font, bg='white')
    mutation_factor_label.grid(row=3, column=0, padx=10, pady=10)

    mutation_factor_entry = tk.Entry(frame, font=label_font, bg='white')
    mutation_factor_entry.grid(row=3, column=1, padx=10, pady=10)
    
    generations_label = tk.Label(frame, text="Generations", font=label_font, bg='white')
    generations_label.grid(row=4, column=0, padx=10, pady=10)
    
    generations_entry = tk.Entry(frame, font=label_font, bg='white')
    generations_entry.grid(row=4, column=1, padx=10, pady=10)
    
    def run_algorithm():
        population_size = population_size_entry.get() or 30
        population_size = int(population_size) 
        iterations = iterations_entry.get()  or 200
        iterations = int(iterations)
        crossover_rate = crossover_rate_entry.get() or 0.5
        crossover_rate = float(crossover_rate)
        mutation_factor = mutation_factor_entry.get() or 0.5
        mutation_factor = float(mutation_factor)
        generations = generations_entry.get()  or 200
        generations = int(generations)
        best_solution_genetic, best_fitness_genetic,time_genetic = run_genetic(population_size,iterations,nodes,capacity)
        best_solution_diff, best_fitness_diff,time_diff = run_diff_evo(population_size,generations,crossover_rate,mutation_factor,nodes,capacity)
        window.destroy()
        # create new window to display the results and make a comparison between the two algorithms
        new_window = tk.Tk()
        new_window.title('Results')
        new_window_width = 900
        new_window_height = 300
        new_window.geometry('{}x{}'.format(new_window_width, new_window_height))
        screen_width = new_window.winfo_screenwidth()
        screen_height = new_window.winfo_screenheight()
        position_top = int(screen_height / 2 - new_window_height / 2)
        position_right = int(screen_width / 2 - new_window_width / 2)
        
        # Set the position of the window to the center of the screen
        new_window.geometry("+{}+{}".format(position_right, position_top))
        
        new_window.configure(background='white')
        label_font = ('Arial', 12)
        frame = tk.Frame(new_window)
        frame.configure(background='white')
        frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # add option to choose Generate Random Data or Upload Data
        genetic_label = tk.Label(frame, text="Genetic Algorithm", font=label_font, bg='white')
        genetic_label.grid(row=0, column=1, padx=10, pady=10)
        
        diff_label = tk.Label(frame, text="Differential Evolution", font=label_font, bg='white')
        diff_label.grid(row=0, column=2, padx=10, pady=10)
        
        best_fitness_label = tk.Label(frame, text="Best Fitness", font=label_font, bg='white')
        best_fitness_label.grid(row=1, column=0, padx=10, pady=10)
        
        best_fitness_genetic_label = tk.Label(frame, text=best_fitness_genetic, font=label_font, bg='white')
        best_fitness_genetic_label.grid(row=1, column=1, padx=10, pady=10)
        
        best_fitness_diff_label = tk.Label(frame, text=best_fitness_diff, font=label_font, bg='white')
        best_fitness_diff_label.grid(row=1, column=2, padx=10, pady=10)
        
        best_solution_label = tk.Label(frame, text="Best Solution", font=label_font, bg='white')
        best_solution_label.grid(row=2, column=0, padx=10, pady=10)
        
        best_solution_genetic_label = tk.Label(frame, text=best_solution_genetic, font=label_font, bg='white')
        best_solution_genetic_label.grid(row=2, column=1, padx=10, pady=10)
        
        best_solution_diff_label = tk.Label(frame, text=best_solution_diff, font=label_font, bg='white')
        best_solution_diff_label.grid(row=2, column=2, padx=10, pady=10)
        
        time_label = tk.Label(frame, text="Time(seconds)", font=label_font, bg='white')
        time_label.grid(row=3, column=0, padx=10, pady=10)
        
        time_genetic_label = tk.Label(frame, text=time_genetic, font=label_font, bg='white')
        time_genetic_label.grid(row=3, column=1, padx=10, pady=10)
        
        time_diff_label = tk.Label(frame, text=time_diff, font=label_font, bg='white')
        time_diff_label.grid(row=3, column=2, padx=10, pady=10)
        
        # add a button to go back to main menu
        back_button = tk.Button(frame, text="Back", command=lambda: new_window.destroy(), font=label_font, bg='white')
        back_button.grid(row=4, column=1, padx=10 , pady=10)
        
        new_window.mainloop()
        
        
    run_algorithm_button = tk.Button(frame, text="Run Algorithm", command=run_algorithm, font=label_font, bg='white')
    run_algorithm_button.grid(row=5, column=0, padx=10, pady=10)
    window.mainloop()
    