# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 18:49:43 2015

@author: Steve
"""

def set_day(df):
    '''
    This function assigns day names to each of the 
    rows in the data set. The function needs to account
    for the fact that some days are missing and there 
    may be some missing hours as well.
    '''  
    ## Assumes the first day of the data set is Saturday
    days = ["Sat", "Sun", "Mon", "Tue", "Wed", 
            "Thr", "Fri"]
    temp = ['d']*df.shape[0]  
    i = 0   
    indx = 0
    cur_day = df.dteday[0]    
    for day in df.dteday:
        if(cur_day != day): 
            cur_day = day
#            i = lambda i: retun 0 if i == 6 else retun i + 1
            if(i == 6): i = 0
            else: i += 1 
        temp[indx] = days[i]
        indx += 1
    df['dayWeek'] = temp
    return df      
    
    
def azureml_main(BikeShare):
    from sklearn import preprocessing
    import numpy as np
    import matplotlib.pyplot as plt
    import statsmodels.graphics.correlation as pltcor
    import statsmodels.nonparametric.smoothers_lowess as lw

## Set the font size for the plots    
    import matplotlib
    matplotlib.rcParams.update({'font.size': 20})
    
    Azure = False
    
    arry = BikeShare.drop('dteday', axis = 1).as_matrix()  
    arry = preprocessing.scale(arry, axis = 1)
    corrs = np.corrcoef(arry, rowvar = 0)
    np.fill_diagonal(corrs, 0)
    
    col_nms = list(BikeShare)[1:]  
    fig = plt.figure(figsize = (9,9))
    ax = fig.gca()
    pltcor.plot_corr(corrs, xnames = col_nms, ax = ax) 
    plt.show()
    if(Azure == True): fig.savefig('cor1.png')
    

## Make time series plots of bike demand by times of the day.    
    times = [7, 9, 12, 15, 18, 20, 22]
    for tm in times:
        fig = plt.figure(figsize=(8, 6))
        fig.clf()
        ax = fig.gca()
        BikeShare[BikeShare.hr == tm].plot(kind = 'line', 
                                           x = 'dayCount', y = 'cnt',
                                           ax = ax)    
        plt.xlabel("Days from start of plot")
        plt.ylabel("Count of bikes rented")
        plt.title("Bikes rented by days for hour = " + str(tm))
        plt.show()
 
## Boxplots to for the predictor values vs the demand for bikes.
    BikeShare = set_day(BikeShare)
    labels = ["Box plots of hourly bike demand",
            "Box plots of monthly bike demand",
            "Box plots of bike demand by weather factor",
            "Box plots of bike demand by workday vs. holiday",
            "Box plots of bike demand by day of the week"]
    xAxes = ["hr", "mnth", "weathersit", 
              "isWorking", "dayWeek"]
    for lab, xaxs in zip(labels, xAxes):
        fig = plt.figure(figsize=(10, 6))
        fig.clf()
        ax = fig.gca()  
        BikeShare.boxplot(column = ['cnt'], by = [xaxs], ax = ax)   
        plt.xlabel('')
        plt.ylabel('Number of bikes')
        plt.show() 
        
## Make scater plot of bike demand vs. various features.
        
    labels = ["Bike demand vs temperature",
            "Bike demand vs humidity",
            "Bike demand vs windspeed",
            "Bike demand vs hr",
            "Bike demand vs xformHr",
            "Bike demand vs xformWorkHr"]
    xAxes = ["temp", "hum", "windspeed", "hr", 
           "xformHr", "xformWorkHr"]
    for lab, xaxs in zip(labels, xAxes):
        ## first compute a lowess fit to the data
        los = lw.lowess(BikeShare['cnt'], BikeShare[xaxs], frac = 0.2)
    
        ## Now make the plots
        fig = plt.figure(figsize=(8, 6))
        fig.clf()
        ax = fig.gca()
        BikeShare.plot(kind = 'scatter', x = xaxs, y = 'cnt', ax = ax, alpha = 0.05)
        plt.plot(los[:, 0], los[:, 1], axes = ax, color = 'red')
        plt.show() 
    
## Explore bike demand for certain times on working and nonworking days
    labels = ["Boxplots of bike demand at 0900 \n\n",
               "Boxplots of bike demand at 1800 \n\n"]
    times = [8, 17]
    for lab, tms in zip(labels, times):
        temp = BikeShare[BikeShare.hr == tms]
        fig = plt.figure(figsize=(8, 6))
        fig.clf()
        ax = fig.gca()  
        temp.boxplot(column = ['cnt'], by = ['isWorking'], ax = ax)   
        plt.xlabel('')
        plt.ylabel('Number of bikes')
        plt.title(lab)
        plt.show() 

    return BikeShare    

      
        