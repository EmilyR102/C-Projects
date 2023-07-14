#!/usr/bin/python3

import time
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

os.system("mkdir -p results")

exp_name = "exp1"
os.system("mkdir -p results/"+exp_name)
timestr = time.strftime("%m.%d-%H_%M_%S")
folder = "results/"+exp_name+"/"+timestr
os.system("mkdir "+folder)

cap_lo = 9
cap_high = 23; # up to but not including
bsize_lo = 6
bsize_high = 7; # up to but not including
assoc = [1, 2, 4, 8]

plot_points = []
capacity = [x for x in range(cap_lo, cap_high)]
MISS_RATE_LINE = 22

# run the experiment
for i in capacity:
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
            points.append(float(f.readlines()[MISS_RATE_LINE].split()[1]))
    plot_points.append(points)

for a in range(len(assoc)):
    plt.plot(capacity, plot_points[a], label="Direct Mapped" if assoc[a] == 1 else str(assoc[a]) + "-way Set Associative", marker = 'o')

plt.title('Miss Rate vs. Capacity')
plt.xlabel('Log of Cache Size')
plt.ylabel('Miss Rate')
plt.legend()
plt.gca().yaxis.set_major_formatter(PercentFormatter())
plt.savefig('Experiment1.png')