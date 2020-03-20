import pandas as pd
import os
import re
import numpy as np
pd.options.mode.chained_assignment = None
pd.set_option('display.max_columns', None)

def getDF(csv):
    colsName = ['Year', 'Coach1', 'Balance1', 'Coach2', 'Balance2', 'Coach3', 'Balance3', 'Coach4', 'Balance4']
    df =  pd.read_csv(csv, engine='python', names= colsName, error_bad_lines=False)
    return df

def removeDuplicate(df):
    df = df.iloc[1:]
    return df.drop_duplicates(subset='Year', keep='last')

def getDataFiles(path):
    return os.listdir(path)

def cleanDataFile(file):
    df = getDF(file)
    df = removeDuplicate(df)
    return df

def removeNAN(df):
    for col in df:
        if df[col].dtype != 'object':
            df[col] = df[col].astype('str')
    return df


def winLosCols(df):
    df['Coach1Wins'] = df['Coach1Lose'] = df['Coach2Wins'] = df['Coach2Lose'] = df['Coach3Wins'] = df['Coach3Lose'] =df['Coach4Wins'] = df['Coach4Lose'] = None
    for indx, row in df.iterrows():
        for i in range(1, 4):
            if row['Coach'+str(i)] is not None and row['Coach'+str(i)] != 'nan':
                bal = str(row['Balance'+str(i)]).split('-')
                df['Coach'+str(i)+'Wins'][indx] = bal[0]
                df['Coach'+str(i)+'Lose'][indx] = bal[1]
    return df

def precentage(a, b):
    return (a/b)*100

def getPrecentagePerCoache(df):
    df['Precentage1'] = df['Precentage2'] = df['Precentage3'] = df['Precentage4'] = None
    for indx, row in df.iterrows():
        for i in range(1,4):
            if row['Coach' + str(i)] is not None and row['Coach'+str(i)] != 'nan':
                df['Precentage'+str(i)][indx] = int(precentage(int(row['Coach'+str(i)+'Wins']), int(row['Coach'+str(i)+'Wins'])+int(row['Coach'+str(i)+'Lose'])))
    return df


def joinDataFile(path):
    filesList = getDataFiles(path)
    dfs = []
    for file in filesList:
        df = cleanDataFile(path+'\\'+file)
        df = removeNAN(df)
        print(df.head())
        df = winLosCols(df)
        df = getPrecentagePerCoache(df)
        print(df.head())
        dfs.append(df)
        print(dfs)
    joindDF = pd.concat(dfs)
    joindDF.to_csv(path+'/Joind Data.csv')



joinDataFile('Data')
