'''
TP - Implémentation d'A*
Réalisé par Kim Aurore Biloni

Cours d'Intelligence Artificielle donné par M. Stefano Carrino
à la Haute-Ecole Arc Ingénierie de Neuchâtel, semestre d'automne 2018
'''
import math, time

class CityNode(object):
    '''
    Class CityNode that represent a city as a node
    '''
    def __init__(self, label, coorX, coorY):
        self.label = label      # city name
        self.coorX = coorX      # Georgraphic coordonates
        self.coorY = coorY
        self.neighbours = {}    # dictionnary of neighbour cities and the road lenght

    def __hash__(self):
        return str(self).__hash__()

    def __str__(self):
        return str(self.label)

    def __eq__(self, other):
        return (self.label == other.label) and (self.coorX == other.coorY) and (self.coorY == other.coorY)

    def addRoad(self, neighbour, distance):
        '''
        Add a direct road between the current city and
        its neighbour specifying the length of the road
        '''
        self.neighbours[neighbour] = distance

    def roadWith(self, city):
        '''
        return true if there's a direct road between the current city
        and the specify city in the parameter
        '''
        return city in self.neighbours.keys()

    def getNeighbourDistance(self, neighbour):
        '''
        return the length of the road between the current
        city and its neighbour
        '''
        return self.neighbours[neighbour]

def constructCities():
    '''
    Read a file containig a list of cities and their
    geographical coordonates.
    Return a dictionnary with keys the name of cities
    and value as the corresponding CityNode
    '''
    f = open("./data/positions.txt").read()

    d = {}
    for c in [l.split(" ") for l in f.split("\n")]:
        d[c[0]] = CityNode(c[0], int(c[1]), int(c[2]))
    
    return d

def linkCities(cities):
    '''
    Read a file containing the roads and length of them
    between cities.
    Foreach road, it links the CityNodes contained in
    the dictionnary. 
    '''
    f = open("./data/connections.txt").read()
    links = [l.split(" ") for l in f.split("\n")]
    for link in links:
        cities[link[0]].addRoad(cities[link[1]], int(link[2]))
        cities[link[1]].addRoad(cities[link[0]], int(link[2]))

### Heuristic

def h0(B : CityNode, n: CityNode):
    'Always returning 0'
    return 0

def h1(B : CityNode, n: CityNode):
    'distance between B and n considering only the x value'
    return abs(B.coorX - n.coorX)

def h2(B : CityNode, n: CityNode):
    'distance between B and n considering only the y value'
    return abs(B.coorY - n.coorY)

def h3(B : CityNode, n: CityNode):
    'distance between B and n as the crow flies'
    x = B.coorX - n.coorX
    y = B.coorY - n.coorY
    return math.sqrt(x**2 + y**2)

def h4(B : CityNode, n: CityNode):
    'Manhattan distance between B and n'
    x = B.coorX - n.coorX
    y = B.coorY - n.coorY
    return abs(x) + abs(y)

heuristics = [h0, h1, h2, h3, h4]

### Implementation de A*

def lowest_f_score_of(f_score, _set):
    ''' Find the node with lowest f_score present in the _set '''
    min_node = list(_set)[0]
    for k in _set:
        try:
            if f_score[k] < f_score[min_node]:
                min_node = k
        except KeyError:
            pass
    return min_node

def print_path(came_from, current):
    ''' Print the path of nodes'''
    i = 1
    while current in came_from.keys():
        print(f"{i}) {current}")
        i+=1
        current = came_from[current]

def a_star(start_city : CityNode, dest_city : CityNode, heuristic):
    ''' A* Algorithm '''
    history = set()             # Nodes already evaluated
    frontiere = {start_city}    # Nodes to evaluate
    came_from = {}              # From wich node we find the following

    g_score = {}                # Dictionnary containing all the calculated g_score
    g_score[start_city] = 0     # The cost to go to the start point is 0

    f_score = {}                # Dictionnary containing all the calculated f_score
    f_score[start_city] = heuristic(start_city, dest_city)    # score based on the heuristic

    while len(frontiere) != 0:  # While there still nodes to explore
        current = lowest_f_score_of(f_score, frontiere) # considering the nearest node
        
        if current is dest_city:    # it has found the best solution
            return came_from, g_score[current], len(history)
        
        frontiere.remove(current)   # the node is being evaluated
        history.add(current)

        for n in current.neighbours.keys(): # foreach neighbours
            if n in history:    # the node has already been evaluated
                continue        # so we skip it
            tmp_g_score = g_score[current] + current.getNeighbourDistance(n)    # Compute the cost
            if n not in frontiere:  # first time see this node
                frontiere.add(n)
            elif n in g_score.keys():           # if we have store its cost
                if tmp_g_score >= g_score[n] :  # if the past cost is better
                    continue                    # we skip it
            
            # saving the node and its scores
            came_from[n] = current
            g_score[n] = tmp_g_score
            f_score[n] = tmp_g_score + heuristic(n, dest_city)

class Timer:
    '''
    Context manager to compute execution time of some code.
    From Célien Donzé
    '''
    def __init__(self, name=""):
        self.name = name    

    def __enter__(self):
        self.start = time.perf_counter() * 1000
        return self

    def __exit__(self, *args):
        self.end = time.perf_counter() * 1000
        self.interval = self.end - self.start
        msg = "Time elapsed"
        if self.name:
            msg += " for " + self.name
        msg += ":"
        print(msg ,round(self.interval,3), "milliseconds\n")

if __name__ == '__main__':
    cities = constructCities()
    linkCities(cities)

    cityA = cities["Paris"]
    cityB = cities["Prague"]

    for h in heuristics:
        path, distance, visited = None, None, None
        print("--------------------------------------------------------")
        print(f"heuristic used : '{h.__doc__}'")
        print(f"Path from {cityA} to {cityB}:")
        with Timer():
            path, distance, visited = a_star(cityA, cityB, h)

        print_path(path, cityB)
        print("Length (km):", distance)
        print(f"{visited} has been visited to find the best path")
