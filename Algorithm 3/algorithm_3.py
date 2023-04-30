from pulp import *
from matplotlib import *
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np

# Use the following solver
solver = COIN_CMD(path="/usr/bin/cbc",threads=8)

def bakery():

    input_filename = './bakery.txt'
    
    # Open dataset
    data = np.loadtxt(input_filename, dtype=int)

    # Initialize LP Problem
    prob = LpProblem("Bakery", LpMinimize)
    start_time = LpVariable.dicts("Start Time", [i for i in range(0, 17)], lowBound = 0, cat = "Continuous")
    tot = LpVariable("Total Time", lowBound = 0)
    overlap = LpVariable.dicts("Overlapping of i, j", [(i, j) for i in range(17) for j in range(17)], cat = "Binary")

    # Add objective value (to be minimized)
    prob += tot

    # Big-M Method
    M = np.amax(data) + 25

    # Add constraints (including the ones of Big-M Method)
    for i in range(17):
        prob += start_time[i] >= data[i][1]
        prob += start_time[i] + data[i][3] <= data[i][2]
        prob += tot >= start_time[i] + data[i][3]
        for j in range(i+1, 17):
            prob += start_time[i] + data[i][3] <= start_time[j] + M * overlap[i, j]
            prob += start_time[j] + data[j][3] <= start_time[i] + M * (1 - overlap[i, j])

    # Solve LP Problem
    prob.solve(solver)
    
    # Create a dictionary to store the starting times of each pastry
    retval = {}

    # Extract the starting times for each pastry and store in the dictionary
    for i in range(17):
        retval['s_{}'.format(i)] = start_time[i].varValue
        
    # Get the start times and baking times of the pastries
    start_times = [value(start_time[i]) for i in [i for i in range(0, 17)]]
    durations = [data[i][3] for i in [i for i in range(0, 17)]]

    # Sort the pastries based on their finish times
    finish_times = [start_times[i] + durations[i] for i in range(17)]
    sorted_indices = sorted(range(17), key=lambda k: finish_times[k])

    # Initialize the figure
    fig, ax = plt.subplots(figsize=(14, 7))

    # Plot each pastry as a horizontal bar with the appropriate color
    for i in sorted_indices:
        x_start = value(start_time[i])/60
        y_pos = sorted_indices.index(i)
        duration = durations[i]/60
        
        # Choosing color based on how critical a preparation is (i.e. based on the time frame between expected finish time and customer arrival, either of the current pastry or of the next one in the schedule, since a mistake could cause a delay in the preparation)
        try:
            next_pos = sorted_indices.index(i)+1
            next_pastry = sorted_indices[next_pos]
            
            # As measure of how critical a preparation is, the parameter used here is "less than 10 minutes = critical" and "less than 5 minutes = highly critical"
            if (data[next_pastry][2]-finish_times[next_pastry] > 600) and (data[i][2]-finish_times[i] > 600):
                color = 'lightyellow'
            if (data[next_pastry][2]-finish_times[next_pastry] <= 600) or (data[i][2]-finish_times[i] <= 600):
                color = 'orange'
            if (data[next_pastry][2]-finish_times[next_pastry] <= 300) or (data[i][2]-finish_times[i] <= 300):
                color = 'red'
            ax.broken_barh([(x_start, duration)], (y_pos-0.4, 0.8), facecolors=color, edgecolors='black', linewidth=1)
         
        except IndexError:
            if data[i][2]-finish_times[i] > 600: color = 'lightyellow'
            if data[i][2]-finish_times[i] <= 600: color = 'orange'
            if data[i][2]-finish_times[i] <= 300: color = 'red'
            ax.broken_barh([(x_start, duration)], (y_pos-0.4, 0.8), facecolors=color, edgecolors='black', linewidth=1)
        
        # Plot the time frame between ready-for-baking time and actual start time
        ax.broken_barh([(data[i][1]/60, x_start-data[i][1]/60)], (y_pos-0.2, 0.6), facecolors='powderblue', linewidth=1)
        
        # Plot the time frame between finish time and customer arrival time
        ax.broken_barh([(finish_times[i]/60, data[i][2]/60-finish_times[i]/60)], (y_pos-0.2, 0.6), facecolors='lavender', linewidth=1)

    
    # Define the labels for the x-axis (only representing times when the oven must be opened)
    converted_times = ["00.00"]

    for time in finish_times:
        hours = int(time // 3600)
        minutes = int((time % 3600) // 60)
        converted_times.append(f"0{hours}.{minutes}")
    
    xticks = [0]
    for i in finish_times:
        xticks.append(i/60) 
    
    # Define the labels for the y-axis (representing pastries already sorted, so it is easier to check the baking order)
    yticklabels = ['Pastry {}'.format(i) for i in sorted_indices]

    # Add legend and set axis labels
    labels = ['Highly Critical', 'Critical', 'Not Critical', 'Ready for Baking', 'Time before Customer Arrival']
    colors = ['red', 'orange', 'lightyellow', 'powderblue', 'lavender']
    legend_patches = [mpatches.Patch(facecolor=color, edgecolor='black', label=label) for label, color in zip(labels, colors)]

    ax.legend(handles=legend_patches, loc='best', bbox_to_anchor=(0.95, 0.44))
    
    ax.set_xlabel('Time of the day')
    ax.set_xticks(xticks)
    ax.set_xticklabels(converted_times, rotation = 45)
    
    ax.set_ylabel('Pastries')
    ax.set_yticks(range(17))
    ax.set_yticklabels(yticklabels)

    # Set the title and make the layout tight
    plt.title('Bakery Schedule')
    plt.tight_layout()

    # Write visualization to the correct file:
    visualization_filename = './visualization.png'
    plt.savefig(visualization_filename, dpi=300)

    # retval should be a dictionary such that retval['s_i'] is the starting time of pastry i
    return retval
