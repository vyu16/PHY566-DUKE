import numpy as np
import random as rd
import pylab as plt
import matplotlib.cm as cm

def move(u,available,num,ar,al,br,bl,count):

    # pick one site from the available list
    pick = int(rd.uniform(0,num-1))
    i = available[pick][0]
    j = available[pick][1]
    
    # check possible direction
    left,right,down,up = 0,0,0,0
    if j-1 >= 0 and u[i,j-1] == 0:  # left is good, i.e. not out of bound, not occupied
        left = 1
    if j+1 <= W and u[i,j+1] == 0:  # right
        right = 1
    if i-1 >= 0 and u[i-1,j] == 0:  # down
        down = 1
    if i+1 <= H and u[i+1,j] == 0:  # up
        up = 1

    # random walk
    if left+right+down+up == 0:  # no possible movement
        return u,available,num,ar,al,br,bl,count  # return without any change
    else:  # at least one direction is available
        dice = god_dice(left,right,down,up)  # always obtain a number leading to an allowed direction
        if dice < 0.25:  # left
            u[i,j-1] = u[i,j]
            u[i,j] = 0
            if u[i,j-1] == 1:
                if ar < j-1 < bl:
                    for ii in range(H+1):
                        available.append([ii,j-1])  # list of available sites is adjusted dymanically
                        num += 1
                    bl = j-1
                if W > j > br:
                    for ii in range(H+1):
                        available.append([ii,j+1])
                        num += 1
                    br = j
        elif dice < 0.50:  # right
            u[i,j+1] = u[i,j]
            u[i,j] = 0
            if u[i,j+1] == -1:
                if bl > j+1 > ar:
                    for ii in range(H+1):
                        available.append([ii,j+1])
                        num += 1
                    ar = j+1
                if 0 < j < al:
                    for ii in range(H+1):
                        available.append([ii,j-1])
                        num += 1
                    al = j
        elif dice < 0.75:  # down
            u[i-1,j] = u[i,j]
            u[i,j] = 0
        else:  # up
            u[i+1,j] = u[i,j]
            u[i,j] = 0
        
        count += 1
        
        return u,available,num,ar,al,br,bl,count

def god_dice(left,right,down,up):  # I believe this can be done through an elegant way
    # must lead to an allowed direction
    if left == 0 and right == 0 and down == 0 and up == 1:
        god = 0.8
    if left == 0 and right == 0 and down == 1 and up == 0:
        god = 0.6
    if left == 0 and right == 0 and down == 1 and up == 1:
        god = rd.uniform(0.5,1)
    if left == 0 and right == 1 and down == 0 and up == 0:
        god = 0.4
    if left == 0 and right == 1 and down == 0 and up == 1:
        if rd.random() < 0.5:
            god = 0.4
        else:
            god = 0.8
    if left == 0 and right == 1 and down == 1 and up == 0:
        god = rd.uniform(0.25,0.75)
    if left == 0 and right == 1 and down == 1 and up == 1:
        god = rd.uniform(0.25,1)
    if left == 1 and right == 0 and down == 0 and up == 0:
        god = 0.2
    if left == 1 and right == 0 and down == 0 and up == 1:
        if rd.random() < 0.5:
            god = 0.2
        else:
            god = 0.8
    if left == 1 and right == 0 and down == 1 and up == 0:
        if rd.random() < 0.5:
            god = 0.2
        else:
            god = 0.6
    if left == 1 and right == 0 and down == 1 and up == 1:
        if rd.random() < 1.0/3.0:
            god = 0.2
        else:
            god = rd.uniform(0.5,1)
    if left == 1 and right == 1 and down == 0 and up == 0:
        god = rd.uniform(0,0.5)
    if left == 1 and right == 1 and down == 0 and up == 1:
        if rd.random() < 2.0/3.0:
            god = rd.uniform(0,0.5)
        else:
            god = 0.8
    if left == 1 and right == 1 and down == 1 and up == 0:
        god = rd.uniform(0,0.75)
    if left == 1 and right == 1 and down == 1 and up == 1:
        god = rd.uniform(0,1)
        
    return god

# initialize u
H = 400  # height of area
W = 600  # width of area, should be a multiple of 3
u = np.zeros((H+1,W+1))
for i in range(H+1):
    for j in range(W/3+1):
        u[i,j] = -1
    for j in range(W/3+1,2*W/3+1):
        u[i,j] = 0
    for j in range(2*W/3+1,W+1):
        u[i,j] = 1

# initialize available sites
available = []
num = 0  # number of available sites
for i in range(H+1):
    available.append([i,W/3])  # available sites at the beginning
    available.append([i,2*W/3+1])
    num +=2
ar = W/3
al = W/3+1
br = 2*W/3
bl = 2*W/3+1

# mixing gases
nstep = 1000000
count = 0  # count how many actual movements
for m in range(10000):  # here a double-loop works more efficiently somehow
    for n in range(nstep):
        u,available,num,ar,al,br,bl,count = move(u,available,num,ar,al,br,bl,count)
    if np.mod(m,50) == 0:  # output every 50 outer steps
        print 'iteration number: ',m,'x 10e6'
        print 'number of moves so far: ',count
        plt.figure()
        plt.imshow(u, cmap=cm.Spectral)  # which color map looks better??
        plt.xlabel('x',fontsize=20,fontweight='bold')
        plt.ylabel('y',fontsize=20,fontweight='bold')
        plt.xticks((0,200,400,600),('0','200','400','600'),fontsize=14)
        plt.yticks((0,200,400),('0','200','400'),fontsize=14)
        #plt.title('Mixing two gases',fontsize=22,fontweight='bold')
        plt.savefig('gases_'+str(m)+'.png')  # name each figure with index
        plt.show()