# -*- coding: utf-8 -*-
"""
Created on Fri May  8 23:43:58 2020

@author: enes_
"""
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats.mstats import winsorize
from scipy.stats import boxcox
import warnings
warnings.filterwarnings("ignore")
pd.set_option('display.float_format', lambda x: '%.2f' % x)

class miss:
    
    def check(df,check_type="percentage"):
        if check_type == "percentage":
            
            missing = df.isnull().sum() *100 /df.shape[0]
            
        elif check_type == "bool":
            
            missing = df.isnull().sum() *100 /df.shape[0] !=0

            
        else:
            missing = print("Wrong 'check_type'")
    
        return missing

    




    def delete(df,percentage=0.6):
        missing_percentage_flag = (df.isnull().sum() *100 /df.shape[0]) > percentage
        
        for column in df.columns[missing_percentage_flag]:
                
            del df[column]
            
        return df
        
        
    
    
    def fill(df,method="median"):

    
        df_to_fill = df[df.columns[df.dtypes != object]]       
        if method=="median":
                
            need_to_fill = df_to_fill.columns[df_to_fill.isnull().sum() *100 /df_to_fill.shape[0] !=0]
                
            for feature in need_to_fill:
                for i in df_to_fill[df_to_fill[feature].isnull()].index:
                    all_nonull_values_for_feature =df_to_fill[feature][df_to_fill[feature].isnull()==False]
                    df_to_fill.loc[i,feature] = np.median(all_nonull_values_for_feature)
                           
            return pd.merge(df,df_to_fill)
                        
        elif method=="mean":
            return df.fillna(np.mean(df))
           
            
           
        elif method=="intplt":
            return df.interpolate()
            
            
        else:
            return print("method should be one of these:\n* median\n* mean\n* intplt")
                
            
class meet:
    def hello(df):
        print(df.info(),end="\n\n\n")
        print("is there any missing value:",miss.check(df,check_type="bool").any())
        print("row count:",df.shape[0])
        count_object = df[df.columns[df.dtypes == object]].shape[1]
        print("feature count:",df.shape[1])
        print("object feature count:",count_object)
        return df.describe()
    
    def transform(df,ttype="boxcox"):
    
        features_to_trans = df.columns[df.dtypes != object]
        if ttype=="boxcox":
            for feature in features_to_trans:
                df[feature],_ = boxcox(df[feature])
        elif ttype=="log":
            for feature in features_to_trans:
                df[feature] = np.log(df[feature])
        else:
            print("ttype should be one of these:\n*boxcox\n*log")
            
        return df
            
  
    def plots(df,transformation="boxcox",fig_size=(15,8),whis=1.5,wins=(0,0)):
        
        features_to_plot = df.columns[df.dtypes != object]
        positive_features = list()
        
        for feature in features_to_plot:
            if (df[feature] > 0).all():
                positive_features.append(feature)

        if transformation == "boxcox":
            for feature in positive_features:
                df[feature],_ = boxcox(winsorize(df[feature],wins))
                plt.figure(figsize=fig_size)
                plt.subplot(1,2,1)
                sns.boxplot(df[feature],whis=whis)
                plt.subplot(1,2,2)
                sns.distplot(df[feature])
                plt.show()
            
        elif transformation == "log":
            for feature in positive_features:
                df[feature] = np.log(winsorize(df[feature],wins))
                plt.figure(figsize=fig_size)
                plt.subplot(1,2,1)
                sns.boxplot(df[feature])
                plt.subplot(1,2,2)
                sns.distplot(df[feature])   
                plt.show()
            
        else:
            print("tranformation type should be one of these:\n*log\n*boxcox")
            
            
    def corr(df,target,scatter=False,sort=True):
        cor= df.corr()
        non_obj = df[df.columns[df.dtypes != object]]
        if sort==True:
            print(pd.DataFrame(cor[target]).sort_values(by=target,ascending=False))
            
        elif sort == False:
            print(pd.DataFrame(cor[target]))
            
        else:
            print("sort parameter should be boolean")
            
        if scatter==True:
            for feature in non_obj:
                sns.scatterplot(df[target],df[feature])
            
    