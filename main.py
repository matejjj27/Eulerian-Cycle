from graph import Graph
from multiprocessing import Process
import time
import threading


# Function for Creating a graph which has an Eulerian Cycle
def create_graph(size):
    G = Graph([], {})
    for x in range(1, size + 1):
        G.add_vertex(x)
    for x in range(1, size + 1):
        for y in range(x + 1, size + 1):
            G.add_edge(x, y)
    return G


if __name__ == '__main__':

    # Creating graphs with custom number of Vertices
    G1 = create_graph(51)
    G2 = create_graph(111)
    G3 = create_graph(151)
    G4 = create_graph(211)

    # Creating a graph which does not have an Euler cycle
    G5 = Graph([1, 2, 3], {(1, 2), (2, 3)})

    # Putting all graphs in a List
    graphs = [G1, G2, G3, G4]

    # Parallel execution with MultiThreading - finding only 1 Euler cycle
    print("Multithreading, single vertex:")
    threads = []
    for x in graphs:
        thread = threading.Thread(target=x.euler_tour, args=(x.get_any_vertex(), ))
        threads.append(thread)
    before = time.perf_counter()
    for x in threads:
        x.start()
    for x in threads:
        x.join()
    after = time.perf_counter()
    difference = after - before
    print(f"\tThreads took {difference} seconds")

    # Parallel execution with MultiProcessing - finding only 1 Euler cycle
    print("Multiprocessing, single vertex:")
    processes = []
    for x in graphs:
        process = Process(target=x.euler_tour, args=(x.get_any_vertex(), ))
        processes.append(process)
    before = time.perf_counter()
    for x in processes:
        x.start()
    for x in processes:
        x.join()
    after = time.perf_counter()
    difference = after - before
    print(f"\tProcesses took {difference} seconds")

    # Parallel execution with MultiThreading - finding every last one Euler cycle in specified graph
    print("Multithreading, all vertices:")
    for x in graphs:
        threads = []
        for y in x.V:
            thread = threading.Thread(target=x.euler_tour, args=(y, ))
            threads.append(thread)
        before = time.perf_counter()
        for z in threads:
            z.start()
        for z in threads:
            z.join()
        after = time.perf_counter()
        difference = after - before
        print(f"\tThreads took {difference} seconds")

    # Parallel execution with MultiProcessing - finding every last one Euler cycle in specified graph
    print("Multiprocessing, all vertices:")
    for x in graphs:
        processes = []
        for y in x.V:
            process = Process(target=x.euler_tour, args=(y, ))
            processes.append(process)
        before = time.perf_counter()
        for z in processes:
            z.start()
        for z in processes:
            z.join()
        after = time.perf_counter()
        difference = after - before
        print(f"\tProcesses took {difference} seconds")
