import numpy as np
import networkx as nx

def normalize_file(file):
    
    # Read file contents as lines and strip empty lines
    with open(file, "r") as f:
        lines = list(line for line in (l.strip() for l in f) if line)
        
        # Initialize an array of zeros with the shape of the file
        num_file = np.zeros((len(lines), len(lines[0].strip())))
        
        # Convert each character in the file to a number and store it in the array
        for k, line in enumerate(lines):
            for j, char in enumerate(line.strip()):
                char = int(char)
                num_file[k][j] = char

    norm_file = []
    pixels_sum = 0
    
    # Compute the sum of all pixels in the file
    for row in num_file:
        pixels_sum += sum(row)
        
    # Normalize the pixel values, to compare files with different brightness levels
    for row in num_file:
        if pixels_sum == 80:
            norm_file.append(row * 39)
        if pixels_sum == 39:
            norm_file.append(row * 80)
            
    return np.array(norm_file)

def comp_dist(file1, file2):
    
    matrix1 = normalize_file(file1)
    matrix2 = normalize_file(file2)

    G = nx.DiGraph()
    
    # Add a node for each pixel in each file
    for i in range(10):
        for j in range(80):
            G.add_node((i, j, f"{file1}"), demand = - matrix1[i][j])
            G.add_node((i, j, f"{file2}"), demand = matrix2[i][j])   
            
    # Add an edge between each pair of pixels that have non-zero values in both files 
    for row_1 in range(10):
        for val_1 in range(80):
            for row_2 in range(10):
                for val_2 in range(80):
                    if matrix1[row_1][val_1] != 0 and matrix2[row_2][val_2] != 0:
                        if val_1 - val_2 < 0:
                            G.add_edge((row_1, val_1, f"{file1}"), (row_2, val_2, f"{file2}"), weight = val_2 - val_1)
                        else:
                            G.add_edge((row_1, val_1, f"{file1}"), (row_2, val_2, f"{file2}"), weight = 80 - (val_1 - val_2))       
    
    # Compute the EMD distance as minimum cost flow of the graph
    distance = nx.min_cost_flow_cost(G)
    
    # Return the EMD distance, it should be float.
    return float(distance)


def sort_files():

    files = ['P1.txt', 'P2.txt', 'P3.txt', 'P4.txt', 'P5.txt', 'P6.txt', 'P7.txt', 'P8.txt', 'P9.txt', 'P10.txt', 'P11.txt', 'P12.txt', 'P13.txt', 'P14.txt', 'P15.txt']
    
    file_1 = 'P1.txt'
    distances = {}
    
    # Compute the EMD distance between file_1 and each of the other files and store it in the distances dictionary
    for i in range(1, len(files)):
        file_2 = files[i]
        
        try:
            distance = comp_dist(file_1, file_2)
            distances[(file_2)] = distance
            
        except:
            # If there is an error in comp_dist function for a pair of files, skip that pair
            pass
        
    # Sort the files based on their EMD distances to file_1
    sorted_files = ['P1.txt'] + [files for files, _ in sorted(distances.items(), key = lambda x:  x[1])]

    # Return sorted list of file names
    return sorted_files
