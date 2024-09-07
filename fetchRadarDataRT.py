import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import timedelta
import glob
import os

def dellfiles(file):
    py_files = glob.glob(file)
    err = 0
    for py_file in py_files:
        try:
            os.remove(py_file)
        except OSError as e:
            print(f"Error:{e.strerror}")
            err = e.strerror
    return err


limite_amostra = 0.015 # tempo s

txt_files = glob.glob('input/*.csv')

print(txt_files)

dellfiles('output/*.csv')

for file_name in txt_files:
    df = pd.read_csv(file_name,
                skipinitialspace=True,
                # skiprows=range(10),
                # dtype = str,
                delimiter=';')
    df[['TU1', 'TU2', 'TU3']] = df['TU'].str.split('.', expand=True)
    df["TU1d"]= pd.to_datetime("2024-06-09 " + df["TU1"], format="%Y-%m-%d %H:%M:%S") + pd.to_timedelta(df["TU2"].astype('int64'), unit='ms') + pd.to_timedelta(df["TU3"].astype('int64'), unit='us')
    df["TU1d_1"]=df["TU1d"].shift(1)
    df["sample"]=df["TU1d"] - df["TU1d_1"]
    
    df['sample_txt'] = df['sample'].astype('str')
    df['sample_txt'] = df['sample_txt'].str.split(' ', expand=True)[2]
    df['sample_txt'] = df['sample_txt'].str[7:]
    df['sample_txt'] = df['sample_txt'].str.replace('.',',')

    df.to_csv('output' + os.path.sep + file_name.split(os.path.sep)[-1],
          index=False,
          #date_format='%H:%M:%S,%f',
          decimal=',',
          sep=';'
          )
    
    df_filtrado = df[df['sample'] > timedelta( seconds=0.015) ]

    if len(df_filtrado.index)>0:
        print("levou mais de ", limite_amostra, " s nas seguintes amostras:")
        print(df_filtrado)
        
        df_filtrado.to_csv('output' + os.path.sep + 'warning_' + file_name.split(os.path.sep)[-1],
            index=False,
            #date_format='%H:%M:%S,%f',
            decimal=',',
            sep=';'
            )