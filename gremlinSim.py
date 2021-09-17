'''

gremlinSim.py - gremlin simulation, based on three rules and random movement

Rules:
    First of all, keep him out of the light, he hates bright light, 
        especially sunlight, it'll kill him. 
    Second, don't give him any water, not even to drink. 
    But the most important rule, the rule you can never forget, 
        no matter how much he cries, no matter how much he begs, 
        never feed him after midnight. 

'''

import matplotlib.pyplot as plt
import numpy as np
import random

MAXROW = 20
MAXCOL = 30

def processlist(linelist):
    newlist = [(int(l.split(",")[0]),int(l.split(",")[1])) for l in linelist[1:]]
    return newlist
    
def read_data(filename):
    # add file IO code here - use processlist (above) once you've split the line 
    with open("Gremlins.txt") as f:
        wlist = processlist(f.readline().strip().split(':'))
        llist = processlist(f.readline().strip().split(':'))
        flist = processlist(f.readline().strip().split(':'))
    return wlist, llist, flist
    
def move_em(current, moves):
    nextgrid = np.zeros(current.shape, dtype="int16")
    
    for row in range(MAXROW):
        for col in range(MAXCOL):
            for g in range(current[row,col]):
                nextrow = row + random.choice(moves)
                nextcol = col + random.choice(moves)
                #print("Newpos = ", nextrow, nextcol)
                if nextrow < 0:
                    nextrow = 0
                if nextcol < 0:
                    nextcol = 0
                if nextrow >= MAXROW:
                    nextrow = MAXROW - 1
                if nextcol >= MAXCOL:
                    nextcol = MAXCOL - 1
                nextgrid[nextrow, nextcol] += 1
    return nextgrid

def rule1(pop, lightlist):                 
    for row in range(MAXROW):
        for col in range(MAXCOL):
            if (row, col) in lightlist:
                for g in range(pop[row,col]):
                    pop[row, col] -= 1
                    print("Goodnight, Sweet Prince")
    
def rule2(pop, waterlist):
    for row in range(MAXROW):
        for col in range(MAXCOL):
            if (row, col) in waterlist:
                for g in range(pop[row,col]):
                    pop[row, col] += 1
                    print("More gremlins")
    
def rule3(good, evil, foodlist):
    for row in range(MAXROW):
        for col in range(MAXCOL):
            if (row, col) in foodlist and good[row, col] > 0:
                print(good[row, col], "Gremlins turned evil")
                evil[row, col] += good[row, col]
                good[row, col] = 0

def make_feature_scatter(itemlist, colour):
    xlist = []
    ylist = []
    for r,c in itemlist:
        ylist.append(MAXROW - r - 1)  
        xlist.append(c) 
    plt.scatter(xlist,ylist,color=colour, marker='s')
    
def make_gremlin_scatter(pop, colour):
    xlist = []
    ylist = []
    slist = []
    for row in range(MAXROW):
        for col in range(MAXCOL):
            if pop[row,col] > 0:
                ylist.append(MAXROW - row - 1)  
                xlist.append(col) #flip rows/columns to y/x
                slist.append(pop[row,col]*20)
    plt.scatter(xlist,ylist,s=slist,color=colour)
  

def main():

    goodarray = np.zeros((MAXROW,MAXCOL), dtype="int16")
    evilarray = np.zeros((MAXROW,MAXCOL), dtype="int16")

    water, light, food = read_data("gremlins.txt")    # read in data
    
    moves  = [-1,0,1]
    emoves = [-2,-1,0,1,2]

    # Starting population
    initpop = 10
    
    for i in range(initpop):  # add good gremlins to grid
        goodarray[random.randint(0,MAXROW-1),random.randint(0,MAXCOL-1)] += 1 

    # Simulation
    
    for t in range(30):    # @ 8 hour / timestep = 10 days
        print("### Summary of Timestep ", t, "###\n")
        print('Number of Good Gremlins: ', str(goodarray.sum()))
        print('Number of Evil Gremlins: ', str(evilarray.sum()))
        print('Number of Gremlins: ', str(goodarray.sum() + evilarray.sum()))
        goodnext = move_em(goodarray, moves)
        evilnext = move_em(evilarray, emoves)
        
        rule1(goodnext, light)
        rule1(evilnext, light)
        rule2(goodnext, water)
        rule2(evilnext, water)
        if t%3 == 0:       # after midnight till 8am
            rule3(goodnext, evilnext, food)
        
        goodarray = goodnext
        evilarray = evilnext
      
        make_gremlin_scatter(goodarray, "b")
        make_gremlin_scatter(evilarray, "r")
        make_feature_scatter(water, "c")
        make_feature_scatter(light, "y")
        make_feature_scatter(food, "g")
        plt.title("Gremlin Simulation (time = " + str(t) + ")")
        plt.xlabel("Columns")
        plt.ylabel("Rows")
        plt.xlim(-1,MAXCOL)
        plt.ylim(-1,MAXROW)
        plt.pause(1)
        plt.clf()
    
if __name__ == "__main__":
    main()
