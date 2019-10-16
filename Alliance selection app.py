# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 08:30:54 2019

@author: Mason
"""

from tkinter import *  
import pandas as pd
from tkinter import filedialog
  
def piecesMath(TeamDf):
    TeamDf['totalCargo'] = TeamDf['telecargo'] + TeamDf['sandcargo']
    TeamDf['totalHatch'] = TeamDf['telehatch'] + TeamDf['sandhatch']
    
df = pd.read_csv(filedialog.askopenfilename(title = 'select MatchList file'), sep = ',')
piecesMath(df)
df = df.sort_values('totalscored', ascending=False)
topScoringTeams = df['team'].get_values()
df = df.sort_values('totalCargo', ascending=False)
topCargoTeams = df['team'].get_values()
df = df.sort_values('totalHatch', ascending=False)
topHatchTeams = df['team'].get_values()
df = df.sort_values('defense', ascending=False)
topDefenseTeams = df['team'].get_values()

top = Tk()  
  
top.geometry("800x480")  

lbl = Label(top,text = "Top scoring teams")
lbl.grid(column=0, row=0)
listbox = Listbox(top)
listbox.grid(column=0, row=1)
j = 1
for i in topScoringTeams:
    listbox.insert(j, i)
    j+=1
lbl1 = Label(top,text = "Top cargo teams")
lbl1.grid(column=1, row=0)
listbox1 = Listbox(top)  
j = 1
for i in topCargoTeams:
    listbox1.insert(j, i)
    j+=1
listbox1.grid(column=1, row=1)

lbl2 = Label(top,text = "Top hatch teams")
lbl2.grid(column=2, row=0)
listbox2 = Listbox(top)  
j = 1
for i in topHatchTeams:
    listbox2.insert(j, i)
    j+=1
listbox2.grid(column=2, row=1)

lbl3 = Label(top,text = "Top defense teams")
lbl3.grid(column=3, row=0)
listbox3 = Listbox(top)  
j = 1
for i in topDefenseTeams:
    listbox3.insert(j, i)
    j+=1
listbox3.grid(column=3, row=1)

  
top.mainloop()
