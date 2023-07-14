#!/usr/bin/python3

import time
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

os.system("mkdir -p results")

exp_name = "exp4"
os.system("mkdir -p results/"+exp_name)
timestr = time.strftime("%m.%d-%H_%M_%S")
folder = "results/"+exp_name+"/"+timestr
os.system("mkdir "+folder)

cap_lo = 16;
cap_high = 17; # up to but not including
bsize_lo = 2;
bsize_high = 15; # up to but not including
assoc = [4]

plot_points = []
block_size = [x for x in range(bsize_lo, bsize_high)]

##############
# TODO: find the line number in the output file you need to access for the total memory traffic calculations
LINE1 = ...
LINE2 = ...
##############

for i in range(cap_lo, cap_high):
    for j in assoc:
        for k in range(bsize_lo, bsize_high):
            os.system("./p5 -t hmmer.1M.txt -cache "+str(i)+" "+str(k)+" "+str(j)+" >> "+folder+"/"+str(i).zfill(2)+"_"+str(k).zfill(2)+"_"+str(j)+".out")


os.chdir(folder)

for j in assoc:
    points = []
    for i in range(cap_lo, cap_high):
        for k in range(bsize_lo, bsize_high):
            file_name = str(i).zfill(2)+"_"+str(k).zfill(2)+"_"+str(j)+".out"
            f = open(file_name, "r")
            lines = f.readlines()
            #########
            # TODO: parse the values using float(lines[<line number>].split()[1])
            # TODO: do the calculation and append to the point array using points.append(<calculated value>)
            # your code here
            #########
    plot_points.append(points)

for a in range(len(assoc)):
    plt.plot(block_size, plot_points[a], label="Direct Mapped" if assoc[a] == 1 else str(assoc[a]) + "-way Set Associative", marker = 'o')

plt.title('Total Memory Traffic vs Block Size')
plt.xlabel('Log of Block Size')
plt.ylabel('Total Memory Traffic')
plt.legend()
plt.savefig('Experiment4.png')

