import pandas as pd
from Data_preperation import isNotNaN, precentage, getDataFiles, cleanDataFile, removeNAN


def buildCoachTable(df, diffPrecentage):
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
                tempDfRow['Total'] = int(bal[0])+int(bal[1])
                tempDfRow['Percentage1'] = int(precentage(int(bal[0]), int(bal[0]) + int(bal[1])))
                newBal = row['Balance' + str(i+1)].split('-')
                tempDfRow['IsSuccessful'] = tempDfRow['Percentage1'] <= \
                                         precentage(int(newBal[0]), int(newBal[0]) + int(newBal[1])) - diffPrecentage
                bal = row['Balance' + str(i+1)].split('-')
                tempDfRow['Percentage2'] = int(precentage(int(bal[0]), int(bal[0]) + int(bal[1])))
                rows.append(tempDfRow)
    return pd.DataFrame(rows).set_index('Year')


def joinDataFileForVisual(path):
    filesList = getDataFiles(path)
    dfsRegularDiff = []
    dfsFiveDiff = []
    for file in filesList:
        if 'Visual' not in file and 'Joined' not in file:
            df = cleanDataFile(path+'\\'+file)
            df = removeNAN(df)
            dfRegular = buildCoachTable(df, 0)
            dfFiveDiff = buildCoachTable(df, 5)
            dfsRegularDiff.append(dfRegular)
            dfsFiveDiff.append(dfFiveDiff)
    joindDF = pd.concat(dfsRegularDiff)
    joindDF.to_csv(path+'/Visual DataFrame Regular.csv')
    joindDF = pd.concat(dfsFiveDiff)
    joindDF.to_csv(path + '/Visual DataFrame FiveDiff.csv')


joinDataFileForVisual('Data')