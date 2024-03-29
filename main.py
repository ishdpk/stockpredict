import streamlit as st
from datetime import date
 
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objects as go
 
 
#Data
START="2015-01-01"
TODAY=date.today().strftime("%Y-%m-%d")
 
st.title("Moonkey Stock Prediction")
 
stocks = ("AAPL", "GOOG", "MSFT", "AMC", "GME", "SQ", "PLTR", "PYPL", "PTON", "SBSW", "META", "AMZN", "TSLA", "DIS", "NFLX", "RBLX",)
selected_stocks = st.selectbox("Select dataset for prediction", stocks)
 
n_years = st.slider("Years of prediction:", 0, 5)
period = n_years * 365
 
@st.cache
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data
 
data_load_state = st.text("Loading Raw Data...")
data = load_data(selected_stocks)
data_load_state.text("Loading data ... done!")
 
st.subheader('Raw data')
st.write(data.tail())
 
def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='stock_open'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='stock_close'))
    fig.layout.update(title_text="Past and current data", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)
 
plot_raw_data()
 
#Prediction
prediction_load_state = st.text("Calculating Prediction Data...")
df_train = data[['Date', 'Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})
 
m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
prediction = m.predict(future)
 
st.subheader('Prediction data')
st.write(prediction.tail())
prediction_load_state.text("Prediction Calculation Done!")
 
st.write('Prediction data')
fig1 = plot_plotly (m, prediction)
st.plotly_chart(fig1)
 
st.write('Forecast components')
fig2 = m.plot_components(prediction)
st.write(fig2)

