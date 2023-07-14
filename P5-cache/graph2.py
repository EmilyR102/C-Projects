#!/usr/bin/python3

import time
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

os.system("mkdir -p results")

exp_name = "exp2"
os.system("mkdir -p results/"+exp_name)
timestr = time.strftime("%m.%d-%H_%M_%S")
folder = "results/"+exp_name+"/"+timestr
os.system("mkdir "+folder)

cap_lo = 9
cap_high = 23; # up to but not including
bsize_lo = 6
bsize_high = 7; # up to but not including
assoc = [2]

plot_points = []
capacity = [x for x in range(cap_lo, cap_high)]
WRITE_BACK_LINE = 29
WRITE_THROUGH_LINE = 30

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
            lines = f.readlines()
            points.append(float(lines[WRITE_BACK_LINE].split()[1]))
            points.append(float(lines[WRITE_THROUGH_LINE].split()[1]))
    plot_points.append(points)

write_traffic = []
for i in range(len(plot_points)):
    write_back = []
    write_through = []
    for j in range(len(plot_points[i])):
        if j % 2 == 0:
            write_back.append(plot_points[i][j])
        else:
            write_through.append(plot_points[i][j])
    write_traffic += [[write_back, write_through]]

for a in range(len(assoc)):
    plt.plot(capacity, write_traffic[a][0], label="Direct Mapped - write-back" if assoc[a] == 1 else str(assoc[a]) + "-way Set Associative - write-back", marker = 'o')
    plt.plot(capacity, write_traffic[a][1], label="Direct Mapped - write-through" if assoc[a] == 1 else str(assoc[a]) + "-way Set Associative - write-through", marker = 'o')

plt.title('Bus Writes vs Cache Size')
plt.xlabel('Log of Cache Size')
plt.ylabel('Bus Writes')
plt.legend()
plt.savefig('Experiment2.png')
