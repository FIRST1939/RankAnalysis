# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 21:11:11 2019

@author: Mason
"""

import pandas as pd
from tkinter import filedialog
import matplotlib.pyplot as plt
#import numpy

team = int(input('Enter Which Team you want to generate a graph for:'))
print('Enter 0 to generate a total pieces graph')
print('Enter 1 to generate a sandstorm graph')
print('Enter 2 to generate a tele graph')
selection = input('Enter your selection here: ')

df = pd.read_csv(filedialog.askopenfilename(title = 'select MatchList file'), sep = ',')
df.set_index("team", inplace = True)


print(df.loc[[team], ["match"]])
print(df.loc[[team], ["totalScored"]])
print(df.loc[[team], ["totalCargo"]])
print(df.loc[[team], ["totalHatch"]])

if selection == "0":
    plt.figure()
    
    plt.subplots(sharey = 'col')

    plt.subplot(311)
    plt.title('Total Pieces')
    plt.plot(df.loc[[team], ["match"]], df.loc[[team], ["totalScored"]])
    plt.ylabel('Total Objects')
    
    plt.subplot(312)
    plt.title('Total Cargo')
    plt.plot(df.loc[[team], ["match"]], df.loc[[team], ["totalCargo"]], color="green")
    plt.ylabel('Cargo')

    plt.subplot(313)
    plt.title('Total Hatch')
    plt.plot(df.loc[[team], ["match"]], df.loc[[team], ["totalHatch"]], color="red")
    plt.ylabel('HP')
    
if selection == "1":
    plt.figure()
    plt.subplots(sharey = 'col')

    plt.subplot(311)
    plt.title('Total Sand')
    plt.plot(df.loc[[team], ["match"]], df.loc[[team], ["totalSand"]])
    plt.ylabel('Total Objects')
    
    plt.subplot(312)
    plt.title('Total Sand Cargo')
    plt.plot(df.loc[[team], ["match"]], df.loc[[team], ["sandcargo"]], color="green")
    plt.ylabel('Cargo')

    plt.subplot(313)
    plt.title('Total Sand Hatch')
    plt.plot(df.loc[[team], ["match"]], df.loc[[team], ["sandhatch"]], color="red")
    plt.ylabel('HP')

if selection == "2":
    plt.figure()
    plt.subplots(sharey = 'col')

    plt.subplot(311)
    plt.title('Total Tele Pieces')
    plt.plot(df.loc[[team], ["match"]], df.loc[[team], ["totalTele"]])
    plt.ylabel('Total Objects')
    
    plt.subplot(312)
    plt.title('Total Tele Cargo')
    plt.plot(df.loc[[team], ["match"]], df.loc[[team], ["telecargo"]], color="green")
    plt.ylabel('Cargo')

    plt.subplot(313)
    plt.title('Total Tele Hatch')
    plt.plot(df.loc[[team], ["match"]], df.loc[[team], ["telehatch"]], color="red")
    plt.ylabel('HP')

