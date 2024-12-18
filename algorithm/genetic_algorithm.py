import sys
import random
import math
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Patch
import numpy as np

def run_algorithm(population_size, iterations, nodes, capacity,num_vechiles):
  vrp = {}


  vrp['nodes'] = [{'label' : 'depot', 'demand' : 0, 'posX' : 0, 'posY' : 0}]
  for i in range(len(nodes)):
    vrp['nodes'].append({'label' : nodes[i][0], 'demand' : nodes[i][1], 'posX' : nodes[i][2], 'posY' : nodes[i][3]})
  vrp['capacity'] = capacity
  # add nodes to the vrp['nodes'] list
  
  
  customer_demands = [node['demand'] for node in vrp['nodes'][1:]] # Customer demands
  customer_demands = np.array(customer_demands)
  customer_demands = np.concatenate(([0], customer_demands))
  NUM_CUSTOMERS = len(vrp['nodes']) - 1
  NUM_VEHICLES = num_vechiles
  popsize = population_size
  iterations = iterations
  locations = [(node['posX'], node['posY']) for node in vrp['nodes']] # Customer locations
  locations = np.array(locations)
  CAPACITY = vrp['capacity'] # Vehicle capacity
  distances = np.zeros((NUM_CUSTOMERS + 1, NUM_CUSTOMERS + 1))
  for i in range(NUM_CUSTOMERS + 1):
      for j in range(NUM_CUSTOMERS + 1):
          distances[i, j] = np.linalg.norm(locations[i] - locations[j])
  ## After inputting and validating it, now computing the algorithm ##


  def distance(n1, n2):
    dx = n2['posX'] - n1['posX']
    dy = n2['posY'] - n1['posY']
    return math.sqrt(dx * dx + dy * dy)

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

  def fitness(p):
      total_distance = 0
      route = np.array(p)
      # route = np.concatenate(([0],p_,[0]))
      routes = np.split(np.atleast_1d(p), np.where(np.atleast_1d(p) == 0)[0])
      routes = [r for r in routes if len(r) > 0]
      for r in routes:
          route_distance = 0
          for i in range(len(r) - 1):
              if r[i] < len(distances) and r[i] >= 0 and r[i+1] < len(distances) and r[i+1] >= 0:
                  route_distance += distances[r[i], r[i+1]]
          total_distance += route_distance
      valid_solution = check_validity(route, customer_demands)
      total_distance += ((np.sum(distances) * len(distances)) / np.count_nonzero(distances)) * valid_solution
      return total_distance

  def adjust(p):
    # Adjust repeated
    repeated = True
    while repeated:
      repeated = False
      for i1 in range(len(p)):
        for i2 in range(i1):
          if p[i1] == p[i2]:
            haveAll = True
            for nodeId in range(len(vrp['nodes'])):
              if nodeId not in p:
                p[i1] = nodeId
                haveAll = False
                break
            if haveAll:
              del p[i1]
            repeated = True
          if repeated: break
        if repeated: break
    # Adjust capacity exceed
    i = 0
    s = 0.0
    cap = vrp['capacity']
    while i < len(p):
      s += vrp['nodes'][p[i]]['demand']
      if s > cap:
        p.insert(i, 0)
        s = 0.0
      i += 1
    i = len(p) - 2
    # Adjust two consective depots
    while i >= 0:
      if p[i] == 0 and p[i + 1] == 0:
        del p[i]
      i -= 1


  import time
  start_time = time.time()
  pop = []

  # Generating random initial population
  for i in range(popsize): 
      p=range(1, len(vrp['nodes']))
      p =list(p)
      random.shuffle(p)
      pop.append(p)
  for p in pop:
    adjust(p)

  # Running the genetic algorithm
  for i in range(iterations):
    nextPop = []
    # Each one of this iteration will generate two descendants individuals. Therefore, to guarantee same population size, this will iterate half population size times
    for j in range(int(len(pop) / 2)):
      # Selecting randomly 4 individuals to select 2 parents by a binary tournament
      parentIds = set()
      while len(parentIds) < 4:
        parentIds |= {random.randint(0, len(pop) - 1)}
      parentIds = list(parentIds)
      # Selecting 2 parents with the binary tournament
      parent1 = pop[parentIds[0]] if fitness(pop[parentIds[0]]) < fitness(pop[parentIds[1]]) else pop[parentIds[1]]
      parent2 = pop[parentIds[2]] if fitness(pop[parentIds[2]]) < fitness(pop[parentIds[3]]) else pop[parentIds[3]]
      # Selecting two random cutting points for crossover, with the same points (indexes) for both parents, based on the shortest parent
      cutIdx1, cutIdx2 = random.randint(1, min(len(parent1), len(parent2)) - 1), random.randint(1, min(len(parent1), len(parent2)) - 1)
      cutIdx1, cutIdx2 = min(cutIdx1, cutIdx2), max(cutIdx1, cutIdx2)
      # Doing crossover and generating two children
      child1 = parent1[:cutIdx1] + parent2[cutIdx1:cutIdx2] + parent1[cutIdx2:]
      child2 = parent2[:cutIdx1] + parent1[cutIdx1:cutIdx2] + parent2[cutIdx2:]
      nextPop += [child1, child2]
    # Doing mutation: swapping two positions in one of the individuals, with 1:15 probability
    if random.randint(1, 15) == 1:
      ptomutate = nextPop[random.randint(0, len(nextPop) - 1)]
      i1 = random.randint(0, len(ptomutate) - 1)
      i2 = random.randint(0, len(ptomutate) - 1)
      ptomutate[i1], ptomutate[i2] = ptomutate[i2], ptomutate[i1]
    # Adjusting individuals
    for p in nextPop:
      adjust(p)
    # Updating population generation
    pop = nextPop

  # Selecting the best individual, which is the final solution
  fitness_history = []
  better = None
  bf = float('inf')
  for p in pop:
    f = fitness(p)
    fitness_history.append(f)
    if f < bf:
      bf = f
      better = p


  ## After processing the algorithm, now outputting it ##

  end_time = time.time()
  print ("Genetic Algorithm")
  print("--- %s seconds ---" % (end_time - start_time))
  # Printing the solution
  print (' route:')
  print ('depot')
  best_solution = []
  for nodeIdx in better:
    print (vrp['nodes'][nodeIdx]['label'])
    best_solution.append(nodeIdx)
  print ('depot')
  #best solution i need it array of nodes numbers
  best_solution = [0] + best_solution + [0]
  print ('Best Solution:', best_solution)
  print( 'Best fitness:', bf)

  # Plotting the fitness history
  # sort fitness history descending
  fitness_history = sorted(fitness_history, reverse=True)

  # plt.plot(fitness_history)
  # plt.xlabel('Generation')
  # plt.ylabel('Fitness')
  # plt.title('Fitness History')
  # plt.show()

  # print (better)

  def plot_cvrp_solution(locations, solution):
      solution = np.concatenate(([0],solution,[0]))
      # Define a color map to use for the routes
      cmap = mpl.colormaps['hsv']

      # Create a dictionary to store the colors for each route
      color_dict = {}
      
      # Create a plot and set the plot size
      fig, ax = plt.subplots(figsize=(7, 7))
      
      # Plot the customer locations
      ax.scatter([loc[0] for loc in locations], [loc[1] for loc in locations], s=100, color='black')

      # Get the solution vehicle routes
      routes_ = np.split(solution, np.where(solution == 0)[0])
      routes = routes_
      # Remove the first and last element from all routes
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
      ax.set_title(f'CVRP Solution ({1} Vehicle, Capacity {CAPACITY})')

      # # Create a legend for the solution routes
      legend_handles = [Patch(facecolor=color_dict[label], label=label) for label in color_dict.keys()]

      # # Define the coordinates for the legend box
      legend_x = 1
      legend_y = 0.5
      
      # # Place the legend box outside of the graph area
      plt.legend(handles=legend_handles, bbox_to_anchor=(legend_x, legend_y), loc='center left', title='Routes')
      
      # # Show the plot
      plt.show()
      
  # # Plot graph with solution
  plot_cvrp_solution(locations, better)
  
  return best_solution, bf,end_time - start_time
  


