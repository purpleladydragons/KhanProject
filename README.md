Installation
-----------
Nothing needs to be installed if this program runs without visualizations. 
Otherwise, this program requires Networkx and matplotlib to be installed.
Their python bindings also need to be installed.

To install Networkx, matplotlib, and pip on a mac, run the included installer:

    sudo ./install_dependencies

Running
-------
To run the program:

    python infection.py -v -l -r

-v, -l, and -r are optional flags. 
-v will turn on visualizations
-l will perform a limited infection. Omitting the -l will run a total infection
-r will create a random graph instead of using the simple 20-node graph I hard-coded

The arrows in the graph represent the 'coaches' relationship. That is, an arrow from A to B means A coaches B. 

Visualization
-------------
Visualization is done using Networkx and matplotlib. 
Visualization only works well on small graphs (< 30 nodes).
The visualization is somewhat random, so the graph will look different every time the program is run.
Sometimes, this will result in jumbled-looking graphs. 
If you do not want to install these packages, I have included a video of the visualization
on a small graph.

Tests
-----
My test suite shows room for improvement. Currently, I only have one small,
simple graph to test the accuracy of my infections. For total infection, one of
the two islands should be totally infected. For the limited infection, the smaller
island should be prioritized and then a student-prioritized BFS is carried out on the 
second island (or the first if the desired number is less than 5). As for speed,
the infections seem to run relatively fast. The major bottleneck is actually creating 
a large random graph (this is very, very slow).

Infection Algos
---------
Total infection is just a simple DFS from the given user.
Limited infection breaks the graph up into its separate components first.
It then totally infects the components in order of size until they get too
large to fit under the desired number of infections. At that point, the remaining
smallest component is split into subgroups in order to minimize the number of pure students
with different versions than their teachers. Then a priorized BFS searches for pure students, 
students, and pure coaches in that order until reaching the desired number of infected users. 

To Do
-------
* I would have liked to have the random graphs represent actual classroom structures instead of being purely random. 
* I would have liked to create more simple graphs to test the accuracy of my algorithms. 
* I wish I could guarantee that the visualization would work out of the box. 
* I would have liked the visualization to been more robust and cleaner.
* I wanted to spend more time on the limited infection algorithm. I chose what I believed to be a compromise between implementation difficulty and usefulness. I do believe that my method follows the spirit of the problem, but having a robust algorithm like Kernighan-Lin to partition the graph would have been really cool to at least see how effective it would have been.
