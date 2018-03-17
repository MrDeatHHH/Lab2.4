import pandas as pd
import numpy as np
import time
from urllib.request import urlopen

def number_of_region(x):
    S = [24, 25, 5, 6, 27, 23, 26, 7, 11, 13, 14, 15, 16, 17, 18, 19, 21, 22, 8, 9, 10, 1, 3, 2, 4]
    return S[x - 1]

def get_state_name(id):
    if (id == 1):
        state = 'Vinnitska'
        return state
    elif (id == 2):
        state = 'Volynska'
        return state
    elif (id == 3):
        state = 'Dniprovska'
        return state
    elif (id == 4):
        state = 'Donetska'
        return state
    elif (id == 5):
        state = 'Zhytomyrska'
        return state
    elif (id == 6):
        state = 'Zakarpatska'
        return state
    elif (id == 7):
        state = 'Zaporozhska'
        return state
    elif (id == 8):
        state = 'Ivano-Frankivska'
        return state
    elif (id == 9):
        state = 'Kyivska'
        return state
    elif (id == 10):
        state = 'Kirovogradska'
        return state
    elif (id == 11):
        state = 'Luganskska'
        return state
    elif (id == 12):
        state = 'Lvivska'
        return state
    elif (id == 13):
        state = 'Nikolaevska'
        return state
    elif (id == 14):
        state = 'Odessaska'
        return state
    elif (id == 15):
        state = 'Poltavaska'
        return state
    elif (id == 16):
        state = 'Rivnenska'
        return state
    elif (id == 17):
        state = 'Sumska'
        return state
    elif (id == 18):
        state = 'Ternopilska'
        return state
    elif (id == 19):
        state = 'Kharkovska'
        return state
    elif (id == 20):
        state = 'Khersonska'
        return state
    elif (id == 21):
        state = 'Khmelnytska'
        return state
    elif (id == 22):
        state = 'Cherkaska'
        return state
    elif (id == 23):
        state = 'Chernivetska'
        return state
    elif (id == 24):
        state = 'Chernihivska'
        return state
    elif (id == 25):
        state = 'Republic of Crimea'
        return state

def name_with_time(index):
    strtime = time.strftime("%Hh%Mm%Ss")
    strdate = time.strftime("%d-%m-%Y")
    name = get_state_name(index)
    id = str(index)
    file_name = id + '_' + name + strdate + strtime + '.csv'
    return file_name

def save_all(id):
    print(id)

    filename = name(id)

    appropriate_id = number_of_region(id)

    url2 = r"https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_provinceData.php?country=UKR&provinceID=%s&year1=1990&year2=2000&type=Mean" % appropriate_id
    vhi_url2 = urlopen(url2)
    out2 = open(r"rawdata1/%s" % filename, 'wb')
    out2.write(vhi_url2.read())
    out2.close()
    print("Step 1")

    col = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI']
    df = pd.read_csv(r"rawdata1/%s" % filename, index_col=False, header=1, sep=", {0,3}|\s+", engine='python')
    df.columns = col
    df1 = df.drop(df.index[549])
    print("Step 2")

    url1 = r"https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_provinceData.php?country=UKR&provinceID=%s&year1=1990&year2=2000&type=VHI_Parea" % appropriate_id
    vhi_url1 = urlopen(url1)
    out1 = open(r"rawdata2/%s" % filename, 'wb')
    out1.write(vhi_url1.read())
    out1.close()
    print("Step 3")

    col = ['Year', 'Week', '0', '5', '10', '15', '20','25','30','35','40','45','50','55','60','65','70','75','80','85','90','95','100',]
    df = pd.read_csv(r"rawdata2/%s" % filename, index_col=False, header=1, sep=", {0,3}|\s+", engine='python')
    df.columns = col
    df2 = df.drop(df.index[549])
    print("Step 4")

    df2 = df2.drop(['Year' , 'Week'],axis = 1)
    frames = [ df1 ,df2 ]
    result = pd.concat(frames, axis=1)
    result.to_csv(r"freshdata/%s" % filename)
    print("Step 5")

def name(index):
    index_string = str(index)
    filename = index_string + '_' + get_state_name(index) + '.csv'
    return filename

def min_VHI(index):
    filename = name(index)
    df = pd.read_csv(r"freshdata/%s" % filename)
    print("\nMin for " + get_state_name(index) + " : " + str(df['VHI'].min()))


def max_VHI(index):
    filename= name(index)
    df = pd.read_csv(r"freshdata/%s" % filename)
    print("\nMax for " + get_state_name(index) + " : " + str(df['VHI'].max()))

def VHI_drought1(index):
    filename = name(index)
    df = pd.read_csv(r"freshdata/%s" % filename)
    df=df[(df['VHI']<15)]
    print('\nDrought in '+get_state_name(index))
    print (df[['Year','Week','VHI']])

def VHI_drought2(index,area):
    filename = name(index)
    df = pd.read_csv(r"freshdata/%s" % filename)
    sum_rows = pd.DataFrame(np.zeros((549, 1)))
    for i in range(0,3):
        n = i*5
        result = pd.concat([sum_rows,df[r"%s" % n]],axis=1)
        sum_rows = result.sum(axis=1)

    df['VHI<15'] = sum_rows
    print(df[df['VHI<15']>area][['Year','VHI']])


for index in range(1,26):
    save_all(index)
    min_VHI(index)
    max_VHI(index)
    VHI_drought1(index)
    VHI_drought2(index,50)










