###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time
import random

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    # TODO: Your code here
    dict={}
    file = open(filename, 'r')
    #print(file.read())
    lines = file.readlines()
    for line in lines:
        splited_line = line.split(',')
       # print(splited_line[1])
        dict[splited_line[0]] = splited_line[1][0]
    
    return  dict

#print(load_cows('ps1_cow_data.txt'))

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    #diction  = load_cows('ps1_cow_data.txt')
    sorted_cows = sorted(cows.items(), key = lambda x: x[1], reverse = True)
    lst_trip = []
    
    while len(sorted_cows)>0:
        weight = 0
        trip = []
        for cow in sorted_cows:
            if weight + int(cow[1]) <= limit:
                trip.append(cow[0])
                weight = weight + int(cow[1])
                
        sorted_cows = list(filter(lambda x: x[0] not in trip, sorted_cows))
        # for items in sorted_cows, filter(choose) item x if x[0] not in trip
        lst_trip.append(trip)
                  
    return lst_trip
#print(greedy_cow_transport(cows = load_cows('ps1_cow_data.txt') ,limit=10))


# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    
    lst_cows = list(cows.items())
    ls = []
    for partition in get_partitions(lst_cows):
        partition_weit = []
        for i in range(len(partition)):
            weight = 0
            partition_i = partition[i]
            for j in range(len(partition_i)):
                weight = weight + int(partition_i[j][1])
            partition_weit.append(weight)
        if all(num <= 10 for num in partition_weit) == True:
            ls.append(partition)
    
    final_chose = min(ls,key = len)
    final_trip = []
    for ele in final_chose:
        name_ele = []
        for tup in ele:
            name_ele.append(tup[0])
        final_trip.append(name_ele)
    
    return final_trip

#print(brute_force_cow_transport(cows=load_cows('ps1_cow_data.txt'),limit=10))
        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here
    start = time.time()
    #print(greedy_cow_transport(cows = load_cows('ps1_cow_data.txt') ,limit=10))
    print(brute_force_cow_transport(cows=load_cows('ps1_cow_data.txt'),limit=10))
    end = time.time()
    print(end - start)
    
    return
compare_cow_transport_algorithms()