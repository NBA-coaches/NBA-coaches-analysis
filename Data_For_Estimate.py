import pandas as pd
from Data_preperation import isNotNaN, precentage, getDataFiles, cleanDataFile, removeNAN
pd.options.mode.chained_assignment = None
pd.set_option('display.max_columns', None)


def buildCoachTable(df):
    rows = []
    for index, row in df.iterrows():
        for i in range(1, 4):
            if isNotNaN(row['Coach' + str(i)]) and \
                    isNotNaN(row['Balance'+str(i)]) and \
                    isNotNaN(row['Coach' + str(i+1)]) and \
                    isNotNaN(row['Balance'+str(i+1)]):
                tempDfRow = {}
                tempDfRow['Year'] = int(row['Year'])
                bal = row['Balance' + str(i)].split('-')
                tempDfRow['Wins'] = int(bal[0])
                tempDfRow['Loses'] = int(bal[1])
                tempDfRow['Percentage'] = precentage(int(bal[0]), int(bal[0]) + int(bal[1]))
                newBal = row['Balance' + str(i+1)].split('-')
                tempDfRow['IsSuccessful'] = tempDfRow['Percentage'] < \
                                         precentage(int(newBal[0]), int(newBal[0]) + int(newBal[1]))
                rows.append(tempDfRow)
    return pd.DataFrame(rows).set_index('Year')


def joinDataFileForVisual(path):
    filesList = getDataFiles(path)
    dfs = []
    for file in filesList:
        if 'Visual' not in file and 'Joined' not in file:
            df = cleanDataFile(path+'\\'+file)
            df = removeNAN(df)
            df = buildCoachTable(df)
            dfs.append(df)
    joindDF = pd.concat(dfs)
    joindDF.to_csv(path+'/Visual DataFrame.csv')


joinDataFileForVisual('Data')