import numpy as np
import matplotlib.pyplot as plt
import sys
import random
import math
import matplotlib as mpl
from matplotlib.patches import Patch
vrp = {}


def run_algorithm(population_size, max_generations, crossover_rate, f, nodes , capacity):
    # add depot to the nodes
    nodes = [["depot", 0, 0, 0]] + nodes
    # convert 
    DE_POPULATION_SIZE = population_size
    DE_MAX_GENERATIONS = max_generations
    DE_CR = crossover_rate
    DE_F = f
    NUM_VEHICLES = 1 # Number of vehicles
    NUM_CUSTOMERS = len(nodes) -1  # Number of customers
    CAPACITY = capacity

    # node has name, demand, x, y
    customer_demands = [node[1] for node in nodes] # Customer demands
    customer_demands = np.array(customer_demands)
    customer_demands = np.concatenate(([0], customer_demands))
    
    locations = [(node[2], node[3]) for node in nodes] # Customer locations
    locations = np.array(locations)

    distances = np.zeros((NUM_CUSTOMERS + 1, NUM_CUSTOMERS + 1)) # Distance matrix
    for i in range(NUM_CUSTOMERS + 1):
      for j in range(NUM_CUSTOMERS + 1):
        distances[i, j] = np.linalg.norm(locations[i] - locations[j])
        
    def distance(x1, y1, x2, y2):
      dx = x1 - x2
      dy = y1 - y2
      return math.sqrt(dx * dx + dy * dy)

    # # # Define problem parameters
    # NUM_CUSTOMERS = len(vrp['nodes']) - 1 # Number of customers
    # NUM_VEHICLES = 1 # Number of vehicles
    # CAPACITY = vrp['capacity'] # Vehicle capacity
    # DE_POPULATION_SIZE = int(sys.argv[1])  # Population size  
    # DE_MAX_GENERATIONS = int(sys.argv[2]) # Number of generations
    # DE_CR = 0.5 # Crossover rate
    # DE_F = 0.5 # Mutation factor

    # customer_demands = [node['demand'] for node in vrp['nodes'][1:]] # Customer demands
    # customer_demands = np.array(customer_demands)
    # customer_demands = np.concatenate(([0], customer_demands))
    # # print('Customer Demands: \n', customer_demands)
    # locations = [(node['posX'], node['posY']) for node in vrp['nodes']] # Customer locations
    # locations = np.array(locations)
    # # print('Customer Locations: \n', locations)
    # distances = np.zeros((NUM_CUSTOMERS + 1, NUM_CUSTOMERS + 1)) # Distance matrix
    # for i in range(NUM_CUSTOMERS + 1):
    #   for j in range(NUM_CUSTOMERS + 1):
    #     distances[i, j] = np.linalg.norm(locations[i] - locations[j])
    # print('Distance Matrix: ', distances)

    def check_validity(trial_solution, customer_demands):
        valid_solution = 0
        start_position = 0
        temp = [i for i in trial_solution if i != 0]
        np_trail_solution = np.array(trial_solution)
        unique = np.unique(temp)
        if len(unique) != len(temp):
            # # Makes sure all customer IDs are unique
            valid_solution += 1
        elif np_trail_solution.max() > NUM_CUSTOMERS:
            # # Makes sure the largest customer ID is no larger the the total number of customers
            valid_solution += 1
        elif np_trail_solution.min() < 0:
            # # Makes sure the largest customer ID is greater than 0
            valid_solution += 1
        else: 
            for _ in range(NUM_VEHICLES):
                route_start = None
                route_end = None
                count = 0
                for l in range(start_position, NUM_CUSTOMERS + NUM_VEHICLES + 1):
                    if np_trail_solution[l] == 0 and route_start is None:
                        route_start = l
                    elif np_trail_solution[l] == 0 and route_start is not None:
                        route_end = l
                        break
                    else:
                        count += 1
                if route_start is None or route_end is None or count == 0:
                    # # Makes sure there is a start and end to each route and each vehicle
                    # # visits at least 1 customer
                    valid_solution += 1
                route = np_trail_solution[route_start:route_end+1]
                if np.sum(np.fromiter([customer_demands[i] for i in route[route != 0]], float)) > CAPACITY:
                    # # Makes sure the total customer demand for a route isn't greater than the capacity
                    # # of a vehicle.
                    valid_solution += 1
                start_position = route_end
            if start_position != len(np_trail_solution) - 1:
                # # Makes sure that the final vehicle return to the depot
                valid_solution += 1
        return valid_solution


    def fitness(solution, distances, customer_demands):
        """
        Computes the total distance traveled by all vehicles in the solution, given a list of routes.
        """
        total_distance = 0
        routes = np.split(solution, np.where(solution == 0)[0])
        routes = [r for r in routes if len(r) > 0]
        # print(routes)
        # total_distance = 0
        for r in routes:
            r = np.concatenate((r, [0]))
            route_distance = 0
            # print(r)
            for i in range(len(r) - 1):
                if r[i] < len(distances) and r[i] >= 0 and r[i+1] < len(distances) and r[i+1] >= 0:
                    route_distance += distances[r[i]][r[i + 1]]
            total_distance += route_distance

        # # Check validity of solution
        valid_solution = check_validity(solution, customer_demands)
        total_distance += ((np.sum(distances) * len(distances)) / np.count_nonzero(distances)) * valid_solution

        return total_distance


    solution = np.array([0, 5, 1, 0, 2, 0, 4, 3,0])
    total_distance = fitness(solution, distances, customer_demands)
    # print('The total distance is: ', total_distance)
    def handle_capacity(solution, customer_demands, CAPACITY):
      """
      If the capacity is exceeded, add a depot to the route.
      """
      # solution is a numpy array
      # covert solution to a list
      # print("TYPEEEEEEEEEEEEEE",type(solution))
      if type(solution) != list:
        solution = solution.tolist()
      # remove 0s from the solution
      solution = [i for i in solution if i != 0]
      new_solution = []
      total_demand = 0
      for i in range(len(solution)):
        current_customer = solution[i]
        current_demand = customer_demands[current_customer]
        if total_demand + current_demand <= CAPACITY:
          new_solution.append(current_customer)
          total_demand += current_demand
        else:
          new_solution.append(0)
          new_solution.append(current_customer)
          total_demand = current_demand
      # add first and last depot
      new_solution = [0] + new_solution + [0]
      return np.array(new_solution)
      
    def generate_population(population_size, customer_demands, CAPACITY):
        population = []
        for _ in range(population_size):
            # Create a shuffled list of customers
            customers = np.random.permutation(NUM_CUSTOMERS) + 1
            solution = [0]  # Start at the depot
            for customer in customers:
                    solution.append(customer)
            solution.append(0)  # Return to the depot at the end
            population.append(handle_capacity(solution, customer_demands, CAPACITY))
        return population
      
    # print(generate_population(DE_POPULATION_SIZE, customer_demands, CAPACITY)[0])

    def perform_mutation(population, population_size, current_idx, f, crossover_rate):
        # # Select three random individuals from the population
        a_idx, b_idx, c_idx = np.random.choice(population_size, size=3, replace=False)
        a_, b_, c_ = population[a_idx], population[b_idx], population[c_idx]
        # check if a is np array
        if type(a_) != np.ndarray:
            a = np.array(a_)
        else:
            a = a_
        if type(b_) != np.ndarray:
            b = np.array(b_)
        else:
            b = b_
        if type(c_) != np.ndarray:
            c = np.array(c_)
        else:
            c = c_
            
        # delete all the 0 from the array
        a = a[a != 0]
        b = b[b != 0]
        c = c[c != 0]
        # # Select current population member
        current_pop_ = population[current_idx].copy()
        if type(current_pop_) != np.ndarray:
            current_pop = np.array(current_pop_)
        else:
            current_pop = current_pop_
        current_pop = current_pop[current_pop != 0]
        # # Set up trial solution
        trial_solution = np.zeros(len(current_pop), dtype=int)

        # # Perform crossover operation
        chosen = np.random.randint(NUM_CUSTOMERS )
        values = np.arange(NUM_CUSTOMERS  )
        count = 0
        swapped = []
        for k in range(len(current_pop)):
            if k not in swapped:
                if np.random.rand() <= crossover_rate or k == chosen:
                    if len(values) != 0:
                        value_index = int((a[k] + f * (b[k] - c[k])) % (len(values)))
                    else:
                        break
                    swap_index = values[value_index]
                    trial_solution[k] = current_pop[swap_index]
                    trial_solution[swap_index] = current_pop[k]
                    swapped.append(swap_index)
                    swapped.append(k)
                    values = np.delete(values, value_index)
                    values = np.delete(values, np.where(values == k))
                else:
                    trial_solution[k] = current_pop[k]

        trial_solution = np.concatenate(([0], trial_solution))
        trial_solution = np.concatenate((trial_solution, [0]))
        new_solution = handle_capacity(trial_solution, customer_demands, CAPACITY)
        return new_solution
      
    trial = perform_mutation(generate_population(DE_POPULATION_SIZE, customer_demands, CAPACITY), DE_POPULATION_SIZE, 0, DE_F, DE_CR)
    # print("Trial: ", trial)
    # print the demand of each customer
    # print("Trail demand: ", [customer_demands[i] for i in trial])

    # print("Fitness: ", fitness(trial, distances, customer_demands))

    def update_population(population, current_idx, trial_solution, trial_fitness, best_fitness, best_solution, fitness_fn, distances, customer_demands):
        # # Update population with trial solution if it is better
        if trial_fitness < fitness_fn(population[current_idx], distances, customer_demands):
            population[current_idx] = trial_solution
            if trial_fitness < best_fitness:
                best_fitness = trial_fitness
                best_solution = trial_solution
        return population, best_fitness, best_solution
      

    def differential_evolution(fitness_fn, population_size, max_generations, crossover_rate, f, customer_demands, distances, print_iter = 0, output = False):
        # # Initialize population
        population = generate_population(population_size, customer_demands, CAPACITY)
        # print the population formated
        best_fitness = np.inf
        for solution in population:
            fitness = fitness_fn(solution, distances, customer_demands)
            if fitness < best_fitness:
                best_fitness = fitness
                best_solution = solution
                
        fitness_history = []
        for i in range(max_generations):
            for j in range(population_size):
                # # Perform mutation and crossover
                trial_solution = perform_mutation(population.copy(), population_size, j, f, crossover_rate)
                # print("Trial solution: %d : %d", i,j, trial_solution)
                trial_fitness = fitness_fn(trial_solution, distances, customer_demands)
                # # Update population with trial solution if it is better
                population, best_fitness, best_solution = update_population(population, j, trial_solution, trial_fitness, best_fitness, best_solution, fitness_fn, distances, customer_demands)
            fitness_history.append(best_fitness)
            if output:
                if i % 10**print_iter == 0:
                    print(f"Generation {i + 1}/{max_generations}: Best fitness = {best_fitness}")

        return best_solution, best_fitness, fitness_history
      
    #keep track of time 
    import time
    start_time = time.time()
    best_solution, best_fitness, fitness_history = differential_evolution(
        fitness_fn=fitness,
        population_size=DE_POPULATION_SIZE,
        max_generations=DE_MAX_GENERATIONS,
        crossover_rate=DE_CR,
        f=DE_F,
        customer_demands=customer_demands,
        distances=distances,
        output = False
    )
    end_time = time.time()
    print("Differential Evolution:")
    print("--- %s seconds ---" % (end_time - start_time))
    
    # Print best solution and fitness
    print(f"Best solution: {best_solution}")
    print(f"Best fitness: {best_fitness}")

    # # Visualize fitness history
    plt.plot(fitness_history)
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.title("Fitness History")
    plt.show()


    def plot_cvrp_solution(locations, solution):
        
        # # Define a color map to use for the routes
        cmap = mpl.colormaps['hsv']

        # # Create a dictionary to store the colors for each route
        color_dict = {}
        
        # # Create a plot and set the plot size
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # # Plot the customer locations
        ax.scatter([loc[0] for loc in locations], [loc[1] for loc in locations], s=100, color='black')

        # # Get the solution vehicle routes
        routes_ = np.split(solution, np.where(solution == 0)[0])
        #  now routes is a list numbers split by 0
        routes = routes_
        # create a list of lists
        # for i in range(len(routes_)):
        #     if i == 0:
        #         routes.append([0])
        #     if routes_[i] != 0:
        #         routes[-1].append(routes_[i])
        #     else:
        #         routes.append([0])
        routes.pop(0)
        routes.pop(-1)
        
        # # Plot the solution routes
        for i in range(len(routes)):
            route = routes[i]
            route = np.concatenate((route, [0]))

            color = cmap(i / len(routes))
            
            # # Create a line plot for the route
            ax.plot([locations[x][0] for x in route], [locations[x][1] for x in route], color=color, linewidth=3, label=f'Vehicle {i}')

            color_dict[f"Route {i}"] = color
            
        
        # # Set the axis limits and labels
        ax.set_xlim([0, max([loc[0] for loc in locations]) * 1.1])
        ax.set_ylim([0, max([loc[1] for loc in locations]) * 1.1])
        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')
        
        # # Set the title
        ax.set_title(f'CVRP Solution ({NUM_VEHICLES} Vehicles, Capacity {CAPACITY})')

        # # Create a legend for the solution routes
        legend_handles = [Patch(facecolor=color_dict[label], label=label) for label in color_dict.keys()]

        # # Define the coordinates for the legend box
        legend_x = 1
        legend_y = 0.5
        
        # # Place the legend box outside of the graph area
        plt.legend(handles=legend_handles, bbox_to_anchor=(legend_x, legend_y), loc='center left', title='Routes')
        
        # # Show the plot
        plt.show()
        return routes  
      

    # # Plot graph with solution
    plot_cvrp_solution(locations, best_solution)
    
    return best_solution.tolist(), best_fitness,end_time - start_time

