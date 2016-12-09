#!/usr/bin/python

import numpy as np
import pandas as pd

df = pd.read_csv("table.tsv", sep=" ")

pivot = pd.pivot_table(df, index=["A", "B"], values="D", columns=["C"], aggfunc=np.sum)
print pivot
