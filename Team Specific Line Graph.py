# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 21:11:11 2019

@author: Mason
"""

import pandas as pd
from tkinter import filedialog
import matplotlib.pyplot as plt

df = pd.read_csv(filedialog.askopenfilename(title = 'select MatchList file'), sep = '|')
df.set_index("teamNo", inplace = True)
print(df.loc[[1939], ["matchNo"]])
plt.plot(df.loc[[1939], ["matchNo"]], df.loc[[1939], ["teleCargoCargo"]])
plt.show()