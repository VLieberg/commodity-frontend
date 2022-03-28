from re import S
import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd
from PIL import Image
import datetime


st.set_page_config(layout="wide")


st.write('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: black;'>Soybean Trading Strategy for Futures Market</h1>", unsafe_allow_html=True)
df_fut_price = pd.read_csv("soybean_daily_price.csv")
df_predc_price = pd.read_csv("predicted_soybean_prices.csv")
url = 'https://soybean-price-prediction-ts7i4cg3ha-ew.a.run.app/predict'
resposta = requests.get(url).json()
respostalista = list(resposta)


st.sidebar.write("<h1 style='text-align: center; color: black;'>Soybean Futures</h1>", unsafe_allow_html=True)
st.sidebar.write("<h3 style='text-align: center; color: black;'>Contract Specs</h3>", unsafe_allow_html=True)
st.sidebar.write("<h3 style='text-align: center; color: gray;'>CME Globex: ZS <br>Contract: 5,000 bushels<br>Price $: U.S. cents per bushel</h3>", unsafe_allow_html=True)
st.sidebar.write('<p style="text-align:center; font-size: 20px"><a href="https://holoviews-exhaokhxdq-uc.a.run.app/Holoviews">Crop Dashboard</a> </p>', unsafe_allow_html=True)
#x = st.sidebar.date_input("Select a date:",datetime.date(2022, 3, 22), max_value=(datetime.date(2022, 4, 21)), min_value=datetime.date(2022, 3, 22))
# x = str(x)
# x = x.replace('-','/')
# predict_price = round(resposta[x],2)
# st.sidebar.metric(label=f"Predicted Price at {x}", value=f'${round(resposta[x],2)}', delta=(f'{round((predict_price-1691.00)/1691,2)}%, {round((predict_price-1691.00),2)}$'))
# imagem_teste = st.sidebar.image("soybean_image.png", width = 350 )
# st.sidebar.write("<h2 style='text-align: center; color: black;'>Model Developed by:</h2>", unsafe_allow_html=True)
# st.sidebar.write("<h4 style='text-align: center; color: gray;'>Alexandre Valadares,<br>Felipe Buongermino,<br>Vanessa Lieberg</h4>", unsafe_allow_html=True)



lista_dias = []
lista_valores = []
for keys,values in resposta.items():
    lista_dias.append(keys)
    lista_valores.append(round(values,2))

with st.container():
    fig = go.Figure()
    fig.add_trace(
    go.Scatter(x=list(df_fut_price.Date), y=list(df_fut_price.Close), name= 'Real Price'))
    fig.add_trace(
    go.Scatter(x=list(df_predc_price['Date']), y=list(df_predc_price['Predicted Price']), name= 'Prediction Model',  marker = dict(color = 'rgba(48, 217, 189, 1)')))
    # Set title
    fig.update_layout(
    title_text="Historical Futures Prices for Soybeans")
    fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                    label="1m",
                    step="month",
                    stepmode="backward"),
                dict(count=6,
                    label="6m",
                    step="month",
                    stepmode="backward"),
                dict(count=1,
                    label="YTD",
                    step="year",
                    stepmode="todate"),
                dict(count=1,
                    label="1y",
                    step="year",
                    stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
        )
    )
    fig.update_layout(width=1000,height=600)
    fig.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01
    ))
    st.plotly_chart(fig)

with st.container():
    fig2 = go.Figure()
    st.markdown("<h1 style='text-align: center; color: black;'>Forecast of Soybeans prices for the next month</h1>", unsafe_allow_html=True)
    fig2.add_trace(
    go.Scatter(x=lista_dias, y=lista_valores, name= 'Predicted Prices', marker = dict(color = 'rgba(146, 39, 245, 0.88)')))
    # Set title
    fig2.update_layout(title_text="Soybean Futures Prices Forecast by LSTM Predict Model")
    fig2.update_layout(width=1000,height=500)
    st.plotly_chart(fig2)
