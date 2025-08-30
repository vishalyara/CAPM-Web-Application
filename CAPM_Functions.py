import plotly.express as px # type: ignore
import numpy as np

#function to plot interactive plotly chart
def interactive_plot(df):
    fig = px.line()
    for i in df.columns[1:]:
        fig.add_scatter(x=df['Date'],y=df[i],name=i)
    fig.update_layout(width=450,margin=dict(l=20,r=20,t=50,b=20),legend=dict(orientation='h',yanchor='bottom',y=1.02,xanchor='right',x=1))
    return fig


#Function to normalize the prize on the initial price
def normalize(df_new):
    df=df_new.copy()
    for i in df.columns[1:]:
        df[i]=df[i]/df[i][0]
    return df

#Function to calculate daily return

import pandas as pd

def daily_return(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate daily percentage returns for all stock price columns in the dataframe.
    Assumes 'Date' is one of the columns.

    Parameters:
        df (pd.DataFrame): Dataframe with stock prices (including 'Date' and 'sp500').

    Returns:
        pd.DataFrame: Dataframe with daily percentage returns.
    """
    df_ret = df.copy()
    
    for col in df_ret.columns:
        if col != 'Date':   # Skip the Date column
            df_ret[col] = df_ret[col].pct_change()   # daily % return
    
    return df_ret.dropna()   # drop first NaN row



#Function to calculate beta
def calculate_beta(stocks_daily_return,stock):
    rm=stocks_daily_return['sp500'].mean()*252

    b,a=np.polyfit(stocks_daily_return['sp500'],stocks_daily_return[stock],1)
    return b,a

