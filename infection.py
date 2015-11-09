# TODO overall
# get email back about limted
# think about how we want to do limited
# make sure we understand limited
# make sure their install goes smoothly
# random graphs
# handcrafted graphs that we know the answer to for testing

import networkx as nx
import matplotlib.pyplot as plt
import argparse
import random

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
    num_users = random.randint(0, 1000)
    users = [User(x) for x in xrange(num_users)]

    # how to create coaches and students in our representation?

# TODO create several simple graphs with hand calculated expected results

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
                
# TODO
def limited_infection(start, users, number, visualize=False):
    """Infect a limited number of users related to the given user

    :param start: the User that the infection will begin from
    :param users: a list of Users that represents the graph
    :param number: the desired number of total infections
    """

    # DFS with visited list to find all connected nodes
    visited = set()
    stack = [start]
    while len(stack) > 0 and len(visited) < number:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            node.version = 1
            stack.extend(set(node.students) - visited)
            stack.extend(set(node.coaches) - visited)

    #TODO definitely change this rather than doing brute force simple
    # TODO have feature that displays desired number of infections, actual # of infections, and # of students/coaches w/ diff pairings


def setup_parser():
    """Set up an arg parser in order to capture a -visualize flag"""
    parser = argparse.ArgumentParser(description='Infections! Yay!')
    parser.add_argument('-v', '--visualize', action='store_true', help='on: use matplotlib to visualize infection', default=False)

    return parser

if __name__ == "__main__":
    # figure out if we should visualize or not
    parser = setup_parser()
    args = parser.parse_args()
    visualize = args.visualize

    # ---- demo the total infection
    print "Testing total infection"
    users = create_simple_graph()
    # print the original versions
    for user in users:
        print user.version, 
    print ""

    user = random.choice(users) 
    total_infection(user, users, visualize)
    # print the new versions
    for user in users:
        print user.version, 

    # ---- demo the limited infection
    print "\n"
    print "---------------------"
    print "Testing limited infection"
    users = create_simple_graph()
    # print the original versions
    for user in users:
        print user.version, 
    print ""

    user = random.choice(users) 
    limited_infection(user, users, 5, visualize)
    # print the new versions
    for user in users:
        print user.version,
