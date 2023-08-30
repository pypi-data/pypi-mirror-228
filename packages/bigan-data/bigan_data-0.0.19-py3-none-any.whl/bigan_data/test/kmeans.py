import numpy as np
from sklearn.cluster import KMeans
import pandas as pd





if __name__ == '__main__':
    data = pd.read_csv("C:\\Users\\cong\\Documents\\BotTrader\\2017-2022-summary.csv",
                       usecols=['SELECT_V2', 'SELECT_V1','BUILD_N1']).to_numpy()
    #print(data)
    index = pd.read_csv("C:\\Users\\cong\\Documents\\BotTrader\\2017-2022-summary.csv", usecols=['index']).to_numpy()
    km = KMeans(n_clusters=3)
    label = km.fit_predict(data)
    expenses = np.sum(km.cluster_centers_, axis=1)
    print(expenses)
    cluster = [[], [], []]
    for i in range(len(index)):
        cluster[label[i]].append(index[i])
    for i in range(len(cluster)):
        print("Expenses:%.2f" % expenses[i])
        print(cluster[i])
