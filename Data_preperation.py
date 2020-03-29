import pandas as pd
import os
import numpy as np
pd.options.mode.chained_assignment = None
pd.set_option('display.max_columns', None)

def getDF(csv):
    colsName = ['Year', 'Coach1', 'Balance1', 'Coach2', 'Balance2', 'Coach3', 'Balance3', 'Coach4', 'Balance4']
    df = pd.read_csv(csv, engine='python', names= colsName, error_bad_lines=False)
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
    df.fillna('nan', inplace=True)
    return df


def winLosCols(df):
    df['Coach1Wins'] = df['Coach1Lose'] = df['Coach2Wins'] = df['Coach2Lose'] = df['Coach3Wins'] = df['Coach3Lose'] = df['Coach4Wins'] = df['Coach4Lose'] = 0.0
    df['Total1'] = df['Total2'] = df['Total3'] = df['Total4'] = 0
    for indx, row in df.iterrows():
        for i in range(1, 5):
            if isNotNaN(row['Coach' + str(i)]) and isNotNaN(row['Balance'+str(i)]):
                bal = row['Balance'+str(i)].split('-')
                df['Coach'+str(i)+'Wins'][indx] = int(bal[0])
                df['Coach'+str(i)+'Lose'][indx] = int(bal[1])
                df['Total'+str(i)][indx] = int(bal[0]) + int(bal[1])
    return df

def precentage(a, b):
    return (a/b)*100

def isNotNaN(arg):
    return arg is not None and arg is not np.nan and arg is not 'nan'


def getPrecentagePerCoache(df):
    df['Precentage1'] = df['Precentage2'] = df['Precentage3'] = df['Precentage4'] = None
    for indx, row in df.iterrows():
        for i in range(1,4):
            if isNotNaN(row['Coach' + str(i)]):
                df['Precentage'+str(i)][indx] = int(precentage(int(row['Coach'+str(i)+'Wins']), int(row['Coach'+str(i)+'Wins'])+int(row['Coach'+str(i)+'Lose'])))
    return df


def joinDataFile(path):
    filesList = getDataFiles(path)
    dfs = []
    for file in filesList:
        if 'Visual' not in file and 'Joined' not in file:
            df = cleanDataFile(path+'\\'+file)
            df = removeNAN(df)
            df = winLosCols(df)
            df = getPrecentagePerCoache(df)
            dfs.append(df)
    joindDF = pd.concat(dfs)
    joindDF.to_csv(path+'/Joined Data.csv')