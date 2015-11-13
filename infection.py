# TODO overall
# make sure their install goes smoothly
# random graphs
# handcrafted graphs that we know the answer to for testing

import networkx as nx
import matplotlib.pyplot as plt
import argparse
import random
import time

class User:
    def __init__(self, id):
        """Create a User
        :param id: a unique number making it easier to name and visualize users
        """
        self.id = id
        self.students = []
        self.coaches = []
        self.version = 0 

    def __repr__(self):
        return str(self.id)

    def __str__(self):
        return str(self.id)

def create_random_graph():
    """Create a random graph"""
    num_users = random.randint(1, 1000)
    users = [User(x) for x in xrange(num_users)]

    coached = set()
    for user in users:
        # probabalistically assign students
        while random.random() > .5:
            # pick a random student that isn't already being coached
            if len( set(users) - ({user}.union(coached)) ) > 0:
                student = random.sample(set(users) - ({user}.union(coached)), 1)[0]
                user.students.append(student)
                student.coaches.append(user)
                coached.add(student)

    return users

def create_simple_graph():
    """Create a simple repeatable graph with two islands 
    to demonstrate success of infection"""

    num_users = 20
    users = [User(x) for x in xrange(num_users)]

    # user 0 will be a coach to users1-4
    users[0].students.extend(users[1:5])
    for user in users[1:5]:
        user.coaches.append(users[0])

    # user 1 will be a coach to users5-14
    users[1].students.extend(users[5:15])
    for user in users[5:15]:
        user.coaches.append(users[1])

    # user 15 will be a coach to users16-19
    users[15].students.extend(users[16:])
    for user in users[16:]:
        user.coaches.append(users[15])

    # so users0-14 are all connected, and users15-19 are a separate island
    return users

def load_graph(users):
    """Create a graph from an adjacency list of users 
    and then draw it
    :param users: a list of Users
    """
    G = nx.DiGraph()
    for user in users:
        G.add_node(user.id)

    for user in users:
        for student in user.students:
            G.add_edges_from([(user.id, student.id)])
    graph_color_values = [0 for node in G.nodes()]
    disp = nx.spring_layout(G, k=.75)
    nx.draw_networkx_nodes(G, disp, node_color = graph_color_values)
    nx.draw_networkx_edges(G, disp)
    plt.draw()

    return G, graph_color_values, disp

def redraw_graph(G, graph_color_values, disp):
    """Redraw a given graph
    :param G: the graph
    :param graph_color_values: list containing the color values for the graph nodes
    :param disp: matplotlib var for keeping track of display window
    """
    nx.draw_networkx_nodes(G, disp, cmap=plt.get_cmap('jet'), node_color = graph_color_values)
    plt.draw()
    plt.pause(.5)

def total_infection(start, users, visualize=False):
    """Infect everyone related to the user via coach-student pairing

    :param start: the User that the infection will begin from
    :param users: a list of Users that represents the graph
    :param visualize: boolean that determines whether we want to visualize the infection
    """

    print "Infecting all users related to user", start

    # load up the graph and keep the relevant graph parts
    if visualize:
        G, graph_color_values, disp = load_graph(users)
        
    # DFS with visited list to find all connected nodes
    visited = set()
    stack = [start]
    while len(stack) > 0:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            # update the version to 1
            node.version = 1
            # add neighbors that haven't been visited yet
            stack.extend(set(node.coaches) - visited)
            stack.extend(set(node.students) - visited)

            # update the node color and redraw
            if visualize:
                graph_color_values[node.id] = 1
                redraw_graph(G, graph_color_values, disp)

    # let the finished infection display for a second
    if visualize:
        plt.pause(1)

def limited_infection(users, number, visualize=False):
    """Infect a limited number of users related to the given user

    :param users: a list of Users that represents the graph
    :param number: the desired number of total infections
    """

    components = get_components(users)
    infected = 0

    if visualize:
        G, graph_color_values, disp = load_graph(users)

    for component in components:
        if len(component) + infected < number:
            # the whole component is connected so no need to dfs it
            for user in component:
                # update the original data
                users[user.id].version = 1
                if visualize:
                    graph_color_values[user.id] = 1
                    redraw_graph(G, graph_color_values, disp)
            infected += len(component)

        # bring in the big guns 
        else:
            to_infect= bfs_infect(component, number-infected)
            for user in to_infect:
                # update the original data
                users[user.id].version = 1
                if visualize:
                    graph_color_values[user.id] = 1
                    redraw_graph(G, graph_color_values, disp)
            infected += len(to_infect)
            break

    if visualize:
        plt.pause(1)
        
def bfs_infect(graph, number):
    """Partition the graph into two subsets so that we isolate classrooms as much as possible

    :param graph: an adjacency list of Users
    :param number: max size of set A
    """
    
    to_infect = set()

    # do a sort of bfs starting from a pure student

    for user in graph:
        if len(to_infect) == number:
            break
        if len(user.students) == 0:
            queue = [user]
            while len(queue) > 0:
                if len(to_infect) == number:
                    break
                node = queue.pop(0)
                if node not in to_infect:
                    to_infect.add(node)
                    # prioritize students
                    queue.extend(set(user.students) - to_infect)
                    queue.extend(set(user.coaches) - to_infect)

    # if there are no pure students
    if len(to_infect) < number:
        user = graph[0]
        queue = [user]
        while len(queue) > 0:
            if len(to_infect) == number:
                break
            node = queue.pop(0)
            if node not in to_infect:
                to_infect.add(node)
                # prioritize students
                queue.extend(set(user.students) - to_infect)
                queue.extend(set(user.coaches) - to_infect)
    
    return to_infect

def get_components(users):
    """Get all islands of users, sort them by ascending size, and return the list of them

    :param users: a list of Users
    """

    components = []
    visited = set()

    for user in users:
        if user not in visited:
            component = []
            stack = [user]
            while len(stack) > 0:
                node = stack.pop()
                if node not in visited:
                    visited.add(node)
                    component.append(node)
                    
                    # add neighbors that haven't been visited yet
                    stack.extend(set(node.coaches) - visited)
                    stack.extend(set(node.students) - visited)
            components.append(component)

    components.sort(key=len)

    return components

def setup_parser():
    """Set up an arg parser in order to capture a -visualize flag"""
    parser = argparse.ArgumentParser(description='Infections! Yay!')
    parser.add_argument('-v', '--visualize', action='store_true', help='on: use matplotlib to visualize infection', default=False)
    parser.add_argument('-l', '--limited', action='store_true', help='on: do a limited infection instead of a total', default=False)
    parser.add_argument('-r', '--randomgraph', action='store_true', help='on: create a random graph', default=False)

    return parser

if __name__ == "__main__":
    # figure out if we should visualize or not
    parser = setup_parser()
    args = parser.parse_args()
    visualize = args.visualize
    limited = args.limited
    random_graph = args.randomgraph

    if not limited:
        # ---- demo the total infection
        print "Testing total infection"
        if random_graph:
            users = create_random_graph()
        else:
            users = create_simple_graph()
        print "Graph has", len(users), "nodes"
        # print the original versions
        for user in users:
            print user.version, 
        print ""

        user = random.choice(users) 
        then = time.time()
        total_infection(user, users, visualize)
        # print the new versions
        for user in users:
            print user.version, 

        print "\n"
        print "Total infection took", time.time() - then, "seconds"

    else:
        # ---- demo the limited infection
        print "---------------------"
        print "Testing limited infection"
        if random_graph:
            users = create_random_graph()
        else:
            users = create_simple_graph()
        print "Graph has", len(users), "nodes"
        # print the original versions
        for user in users:
            print user.version, 
        print ""

        user = random.choice(users) 
        number = random.randint(1, len(users))
        print "Infecting", number, "users"
        limited_infection(users, number, visualize)
        # print the new versions
        for user in users:
            print user.version,
        print "\n"
