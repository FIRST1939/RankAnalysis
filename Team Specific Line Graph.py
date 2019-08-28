# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 21:11:11 2019

@author: Mason
"""

import pandas as pd

from tkinter import filedialog
import matplotlib.pyplot as plt
team = int(input('Enter Which Team you want to generate a graph for:'))

df = pd.read_csv(filedialog.askopenfilename(title = 'select MatchList file'), sep = '|')
df.set_index("teamNo", inplace = True)
print(df.loc[[team], ["matchNo"]])
plt.plot(df.loc[[team], ["matchNo"]], df.loc[[team], ["teleCargoCargo"]])
plt.show()