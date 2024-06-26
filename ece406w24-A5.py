#!/usr/bin/env python3
"""
ECE406: Assignment 5, Q4
You will need to install scipy ('pip3 install scipy') for the import command to work.  Do not use any other external libraries
"""
from scipy.optimize import linprog

################################################################################
# SUBMISSION INSTRUCTIONS FOR A5Q4
#   1. Write your username and student number in the box below
#   2. Submit your code as ece406w24-A5-<WatIAMusername>.py to the LEARN Dropbox
#      where <WatIAMusername> is replaced by your WatIAM username
#   3. Submit the signed Academic Integrity form to the LEARN Dropbox
#   4. Submit a screencap of your max_flow function 
#      and the comment box containing your username and student
#      number to Crowdmark.
################################################################################

################################################################################
# student info
#
# WatIAM username: sy37chen
# Student number: 20830005
################################################################################


def max_flow(cap, s, t):
    """
    Input: A matrix giving the capacity on each edge.
           If cap[i,j] = 0, then the edge (i,j) is not in the graph
           A source s and sink node t,
    Output: A matrix giving the flow on each edge,
            A number giving the value of the max flow.
    """
    n = len(cap)
    c = [-1 if i < n else 0 for i in range(n*n)]
    
    template = [0] * (n*n)
    A_eq = []
    for i in range(n):
        if i == t or i == s:
            continue
        here = template.copy()
        for j in range(n):
            here[i*n+j] = 1
            if cap[j][i] != 0:
                here[j*n+i] = -1
        A_eq.append(here)
    
    b_eq = [0]*len(A_eq)

    bounds = []
    for i in range(n):
    	for j in range(n):
        	bounds.append((0,cap[i][j]))
    opt = linprog(c=c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
    
    flows_per_edge = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            flows_per_edge[i][j] = opt.x[i*n+j]
    
    total_flow = opt.fun * -1
    
    return flows_per_edge, total_flow
def example():
    """
    The following is an example to get you started
    """
    # nine variables, each has an upper and lower bound
    bounds = [(0, 0), (0, 3), (0, 1),
              (0, 0), (0, 0), (0, 1),
              (0, 0), (0, 0), (0, 0)]

    # an equality constraint
    Aeq = [[0, -1, 0, 1, 1, 1, 0, -1, 0]]
    beq = [0]

    # the objective c function
    c = [-1, -1, -1, 0, 0, 0, 0, 0, 0]

    # solving
    opt = linprog(c=c, A_eq=Aeq, b_eq=beq, bounds=bounds, method='revised simplex')
    print("\n example output: \n", opt)


def main():
    """
    Testing your LP.  The following is a single example.  Your alg
    should work for any input.
    """
    example()
    # the output of the example is the following :
     #     con: array([0.])
     #     fun: -2.0
     # message: 'Optimization terminated successfully.'
     #     nit: 2
     #   slack: array([], dtype=float64)
     #  status: 0
     # success: True
     #       x: array([0., 1., 1., 0., 0., 1., 0., 0., 0.])

    # Note:
    # 1) the optimization has a value of opt.val = -2.0.
    #    linprog solves minimization problems.
    #    To solve a maximization we solve:  min -c^T x.
    #
    # 2)  the array opt.x contains the value of each variable.
    #     For example, the value of variable 1 (0 indexing) has value 1.0,
    #     which lies between its lower and upper bounds of 0 and 3.

    # TEST PROBLEM -- the optimal solution for this should be 7
    c = [[0, 3, 4, 0, 0],
         [0, 0, 1, 0, 2],
         [0, 0, 0, 5, 0],
         [0, 0, 0, 0, 6],
         [1, 1, 0, 0, 0]]
    s = 0
    t = 4

    print()
    print('Running LP for test problem')
    print(max_flow(c, s, t))
    ##############
    ## Hint:
    # To call linprog, you need variables with a single index.  That is,
    # you can't directly define the variables flow[i,j].  So, you'll have
    # to concatenate the columns/rows into a single array x of length n^2.
    # A common way is to store flow[i,j] in position i * n + j of the array x.

    # Notice, that when thought of like this, example() encodes a max flow problem for a graph with three vertices and nine edges.
    # Just three of the edges have non-zero capacity: (0,1), (0,2) and (1,2),
    # with capacities of 3, 1, and 1, respectively. s = 0 and t = 2.
    ####################


if __name__ == '__main__':
    main()
