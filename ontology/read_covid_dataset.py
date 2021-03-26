# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 18:27:28 2021

@author: Home
"""

# import pandas module
import pandas as pd 

''' creating function to open read the data and save the data '''
def data(url,path):
    
    ''' storing dataset in dataframe uisng pandas '''
    
    df = pd.read_csv(url) 
    #print(df.head())
        
    ''' saving dataframe locally using pickle,  '''
    df.to_pickle(path)
    
    ''' load the pickle file to read the saved data '''
    covid_data = pd.read_pickle(path)
    #type(covid_data)
    #print(covid_data.head())
        
    return 1

'''  pass url of the dataset that we want to analyze '''
url = "https://opendata.ecdc.europa.eu/covid19/nationalcasedeath_eueea_daily_ei/csv/data.csv"    

''' specify path to save the data locally '''
path = r'C:\Users\Home\Desktop\interview\covid_data.pkl'

''' call function here'''
data(url,path)






