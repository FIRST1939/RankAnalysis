# -*- coding: utf-8 -*-
"""
Graph samples

Created on Thu Aug 15 17:26:20 2019

@author: Victoria Cook

To use, repoint the filename variable to a 2019 matchScoutData excel file.
"""

from tkinter import filedialog

filename = filedialog.askopenfilename(title = 'select analyzed data file')

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel(filename)


#print(df.columns)

print('Maximum scored objects in a match', df.totalscored.max())

print('This program will generate a histogram with two subplots. \n The first graph will create a file that with the average total points scored. \n The second will generate a cargo scored graph. \n The third will generate a hatch scored graph.')
print('If you would like to generate the other two as sandstorm cargo and hatch graphs enter 1')
print('If you would like to generate the other two as tele cargo and hatch graphs enter anything but 1')
selection = input('Your selection here:')

if selection == '1':
    selection = 'sand'
else:
    selection = 'tele'

def basicHist(df):
    '''
    This function will plot a basic histogram using default settings of the
    total game objects scored.
    
    Each bar will show the count of the number of data values in the bin.
    
    Since the values are all integers, the lower bound of the bin is the value
    counted for that bar.
    '''
    plt.hist(df.sandhatch)
    
    plt.show()


def teamNumHist(df):
    '''
    This function will plot a basic histogram using default settings of the
    total game objects scored.
    
    Each bar will show the count of the number of data values in the bin.
    
    Since the values are all integers, the lower bound of the bin is the value
    counted for that bar.
    '''
    plt.hist(df.team)
    
    plt.show()

def funHist(df):
    '''
    This function will plot a basic histogram using default settings of the
    total game objects scored.
    
    Each bar will show the count of the number of data values in the bin.
    
    Since the values are all integers, the lower bound of the bin is the value
    counted for that bar.
    '''
    plt.hist(df.teledropCargo)
    
    plt.show()
    
def cleanBasicHist(df):
    '''
    This is the same data as basicHist, but the color is explicitly specified.
    The bins are explicitly specified (note that if the bins don't cover 
    the max value, you will miss information).  I've centered the bars on the
    lower bound, which is the value since the first bin is [0-1) 
    (i.e. 0 is in, 1 is not).  I've made the bins half as wide, and I set the 
    vertical axis to show the density, which is the number of measurements in 
    the bin divided by the number of measurements in the data.
    '''
    plt.hist(df.totalscored,color="teal",bins = [0,1,2,3,4,5,6,7,8,9,10], 
             align = 'left',rwidth=0.5, density = True)
    
    plt.show()
    
def complexSubplots(df, selection):    
    '''
    For this, I took the same graph settings and made subplots showing total
    objects scored, teleop cargo scored, and teleop hatch panels scored in a 
    three row, one column display, and put some y-axis labels on.
    '''
    plt.figure()
    plt.subplots(sharey = 'col')
    plt.subplot(311)
    plt.hist(df.totalscored,color="blue",bins = [0,1,2,3,4,5,6,7,8,9,10],
             align = 'left',rwidth=0.5, density = True)
    plt.ylabel('Total Objects')
    
    if selection == 'tele':
        plt.subplot(312)
        plt.hist(df.telecargo, color="green",bins = [0,1,2,3,4,5,6,7,8,9,10],
                 align = 'left',rwidth=0.5, density = True)
        plt.ylabel('Cargo')
        plt.subplot(313)
        plt.hist(df.telehatch, color="red",bins = [0,1,2,3,4,5,6,7,8,9,10],
                 align = 'left',rwidth=0.5, density = True)
        plt.ylabel('HP')

    else:
        plt.subplot(312)
        plt.hist(df.sandcargo, color="green",bins = [0,1,2,3,4,5,6,7,8,9,10],
                 align = 'left',rwidth=0.5, density = True)
        plt.ylabel('Cargo')
        plt.subplot(313)
        plt.hist(df.sandhatch, color="red",bins = [0,1,2,3,4,5,6,7,8,9,10],
                 align = 'left',rwidth=0.5, density = True)
        plt.ylabel('HP')        
    plt.show()


def basicBar(df):
    plt.bar(df.team,df.totalscored, label="Example two", color='g')
    plt.legend()
    plt.xlabel('Team #')
    plt.ylabel('Total scored')
    plt.title('')
    plt.show()
    print(df.team)


complexSubplots(df, selection)
basicBar(df)
teamNumHist(df)
funHist(df)
print(df.columns)