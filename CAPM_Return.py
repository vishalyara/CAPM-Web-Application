import streamlit as st # type: ignore
import pandas as pd
import yfinance as yf # type: ignore
import pandas_datareader.data as web # type: ignore
import datetime
import CAPM_Functions 
st.set_page_config(page_title="Calculate",page_icon="chart_with_upwards_trends",layout='wide')

st.title("Capital Asset Pricing Model")
#Input from the user
try:
    column1,column2=st.columns([1,1])

    with column1:
        stocks_list=st.multiselect("Choose any stocks from below to proceed",('TSLA','AAPL','NFLX','MGM','AMZN','NVDA','GOOG','MSFT','INTC','CVX','NKE','MRK','MCD','AVGO','JPM','COST','AMD','MA'),['TSLA','AAPL','NFLX','GOOG','AMZN'])
    with column2:
        year=st.number_input('Number of years ',1,10)

    #downloading the data for SP500

    start= datetime.date(datetime.date.today().year-year,datetime.date.today().month,datetime.date.today().day)
    end=datetime.date.today()
    SP500 = web.DataReader(['sp500'],'fred',start,end)

    stocks_df=pd.DataFrame()

    for stock in stocks_list:
        data=yf.download(stock,period=f'{year}y')
        stocks_df[f'{stock}']=data['Close']

    stocks_df.reset_index(inplace=True)
    SP500.reset_index(inplace=True)
    SP500.columns=['Date','sp500']
    stocks_df['Date']=stocks_df['Date'].astype('datetime64[ns]')
    stocks_df['Date']=stocks_df['Date'].apply(lambda x:str(x)[:10])
    stocks_df['Date']=pd.to_datetime(stocks_df['Date'])
    stocks_df=pd.merge(stocks_df,SP500,on='Date',how='inner')

    column1,column2=st.columns([1,1])
    with column1:
        st.markdown("### Dataframe head")
        st.dataframe(stocks_df.head(),width='stretch')
    with column2:
        st.markdown("### Dataframe tail")
        st.dataframe(stocks_df.tail(),width='stretch')

    column1,column2=st.columns([1,1])
    with column1:
        st.markdown('### Price of all the stocks')
        st.plotly_chart(CAPM_Functions.interactive_plot(stocks_df))
    with column2:
        st.markdown('### Price of all the stocks after normalizing')
        st.plotly_chart(CAPM_Functions.interactive_plot(CAPM_Functions.normalize(stocks_df)))


    stocks_daily_return=CAPM_Functions.daily_return(stocks_df)
    print(stocks_daily_return.head())

    beta={}
    alpha={}

    for i in stocks_daily_return.columns:
        if i !='Date' and i!='sp500':
                b,a=CAPM_Functions.calculate_beta(stocks_daily_return,i)
                beta[i]=b
                alpha[i]=a
    print(beta,alpha)

    beta_df=pd.DataFrame(columns=['Stock','Beta Value'])
    beta_df['Stock']=beta.keys()
    beta_df['Beta Value']=[str(round(i,2)) for i in beta.values()]

    with column1:
        st.markdown("### Calculated Beta Value")
        st.dataframe(beta_df,width='stretch')

    rf=0
    rm=stocks_daily_return['sp500'].mean()*252

    return_df=pd.DataFrame()
    return_value=[]
    for stock,value in beta.items():
        return_value.append(str(round(rf+(value*(rm-rf)),2)))
    return_df['Stock']=stocks_list

    return_df['Return Value']= return_value

    with column2:
        st.markdown("### Calulated return using CAPM")
        
        st.dataframe(return_df,width='stretch')

except:
    st.write("Please select valid inputs")