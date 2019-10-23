# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 08:30:54 2019

@author: Mason
"""

from tkinter import *  
import pandas as pd
from tkinter import filedialog
from tkinter import ANCHOR

picklist = [[],[],[],[],[]]

def deleteFromListbox(lb):
    listList = lb.get(0,END)
#        listList.append[i]
    for i in len(listList):
        print(listList[i])

def getAndRemoveAnchor(lb):
    print(lb.get(ANCHOR))
    team = lb.get(ANCHOR)
#    index.set(str(team))
    picklist[4].append(int(team))
    if lb == totalbox:
        picklist[0].append(int(team))
    if lb == cargobox:
        picklist[1].append(int(team))
        totalbox.delete(cargobox.get(ACTIVE))
        cargobox.delete(ACTIVE)
#        deleteFromListbox(hatchbox)
    if lb == hatchbox:
        picklist[2].append(int(team))
    if lb == defensebox:
        picklist[3].append(int(team))
    totalbox.delete(team)
    cargobox.delete(team)
    hatchbox.delete(team)
    defensebox.delete(team)
#    return totalbox, cargobox, hatchbox, defensebox
#    print(picklist)
  
def piecesMath(TeamDf):
    TeamDf['totalCargo'] = TeamDf['telecargo'] + TeamDf['sandcargo']
    TeamDf['totalHatch'] = TeamDf['telehatch'] + TeamDf['sandhatch']
    
df = pd.read_csv(filedialog.askopenfilename(title = 'select analyzed data file'), sep = ',')
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
totalbox = Listbox(top)
totalbox.grid(column=0, row=1)
j = 1
for i in topScoringTeams:
    totalbox.insert(j, i)
    j+=1
lbl1 = Label(top,text = "Top cargo teams")
lbl1.grid(column=1, row=0)
cargobox = Listbox(top)  
j = 1
for i in topCargoTeams:
    cargobox.insert(j, i)
    j+=1
cargobox.grid(column=1, row=1)


lbl2 = Label(top,text = "Top hatch teams")
lbl2.grid(column=2, row=0)
hatchbox = Listbox(top)  
j = 1
for i in topHatchTeams:
    hatchbox.insert(j, i)
    j+=1
hatchbox.grid(column=2, row=1)

lbl3 = Label(top,text = "Top defense teams")
lbl3.grid(column=3, row=0)
defensebox = Listbox(top)  
j = 1
for i in topDefenseTeams:
    defensebox.insert(j, i)
    j+=1
defensebox.grid(column=3, row=1)
btn = Button(top,text = "Select", command=lambda: totalbox.delete(ACTIVE))
btn.grid(column=0, row=2)
btn1 = Button(top,text = "Select", command=lambda: getAndRemoveAnchor(cargobox))
btn1.grid(column=1, row=2)
btn2 = Button(top,text = "Select", command=lambda: getAndRemoveAnchor(hatchbox))
btn2.grid(column=2, row=2)
btn3 = Button(top,text = "Select", command=lambda: getAndRemoveAnchor(defensebox))

btn3.grid(column=3, row=2)
top.mainloop()

