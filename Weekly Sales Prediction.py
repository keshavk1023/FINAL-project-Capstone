import streamlit as st
import pandas as pd
import datetime
import pickle
from PIL import Image

# Load data and model
df = pd.read_csv('final_data.csv').drop(['Unnamed: 0'], axis=1)
model = pickle.load(open('model.pkl', 'rb'))

# Page configuration
st.set_page_config(
    layout="wide",
    page_title="Retail Sales Prediction",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

st.markdown("<h1 style='text-align: center; color: violet;'>Retail Weekly Sales Prediction</h1>", unsafe_allow_html=True)
st.divider()

# Tabs
tab1, tab2, tab3 = st.tabs(['HOME', 'PREDICTION', 'CONCLUSION'])

# Home Tab
with tab1:
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("#### Domain", unsafe_allow_html=True)
        st.write("##### Retail Industry")
        st.markdown("#### Technologies and Tools used", unsafe_allow_html=True)
        st.write("##### Python, Pandas, numpy, matplotlib, seaborn, Plotly, Streamlit, sklearn.")
        st.markdown("#### Overview of the Project", unsafe_allow_html=True)
        st.write("##### * Predict the weekly sales of a retail store based on historical sales using Machine Learning techniques.")
        st.write("##### * Perform Data cleaning, Exploratory Data Analysis, Feature Engineering, Hypothesis Testing for the ML model.")
        st.write("##### * Using the :violet[RANDOM FOREST REGRESSOR] model to predict the weekly sales of the retail store.")

    with col2:
        st.image(Image.open('random_forest.png'), width=600)

# Prediction Tab
with tab2:
    option = st.radio('*Select your option*', ('Processed Data', 'Prediction Process'), horizontal=True)

    if option == 'Processed Data':
        st.header("Processed Final Data")
        st.write(df)

    if option == 'Prediction Process':
        col3, col4, col5, col6, col7 = st.columns(5, gap="large")

        with col3:
            st.header("Store Info")
            store = st.selectbox('Select the *Store Number*', list(range(1, 46)))
            dept = st.selectbox('Select the *Department Number*', [
                1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 
                21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 40, 
                41, 42, 44, 45, 46, 47, 48, 49, 51, 52, 54, 55, 56, 58, 59, 60, 67, 71, 72, 
                74, 79, 80, 81, 82, 83, 85, 87, 90, 91, 92, 93, 94, 95, 97, 78, 96, 99, 39,
                77, 50, 43, 65, 98
            ])
            store_type = st.selectbox('Select the *Store Type*', ['A', 'B', 'C'])
            size = st.selectbox('Select the *Store Size*', sorted(df['Size'].unique()))

        with col4:
            st.header("Indirect Impact on Store Sales")
            temp = st.slider('Enter the *Temperature* in Fahrenheit', min_value=5.54, max_value=100.14, value=90.0)
            fuel = st.slider('Enter the *Fuel Price*', min_value=2.472, max_value=4.468, value=3.67)
            CPI = st.slider('Enter the *CPI*', min_value=126.0, max_value=227.47, value=211.77)
            unemp = st.slider('Enter the *Unemployment Rate* in percentage', min_value=3.879, max_value=14.313, value=8.106)

        with col5:
            st.header("Markdown Impact on Store Sales")

            def inv_trans(x):
                return 1 / x if x != 0 else 0  # Avoid division by zero

            markdown1 = inv_trans(st.slider('Enter the *Markdown1* in dollars', min_value=0.27, max_value=88646.76, value=2000.00))
            markdown2 = inv_trans(st.slider('Enter the *Markdown2* in dollars', min_value=0.02, max_value=104519.54, value=65000.00))
            markdown3 = inv_trans(st.slider('Enter the *Markdown3* in dollars', min_value=0.01, max_value=141630.61, value=27000.00))
            markdown4 = inv_trans(st.slider('Enter the *Markdown4* in dollars', min_value=0.22, max_value=67474.85, value=11200.00))
            markdown5 = inv_trans(st.slider('Enter the *Markdown5* in dollars', min_value=135.06, max_value=108519.28, value=89000.00))

        with col6:
            st.header("Direct Impact on Store Sales")
            duration = st.date_input("Select the *Date*", datetime.date(2012, 7, 20), min_value=datetime.date(2010, 2, 5), max_value=datetime.date.today())
            holiday = st.selectbox('Select the *Holiday*', ["YES", "NO"])

        with col7:
            st.header("Weekly Sales")

            if st.button('Predict'):
                try:
                    input_data = [
                        store, dept, size, temp, fuel, CPI, unemp, markdown1, markdown2, markdown3, markdown4, markdown5,
                        duration.year, duration.month, duration.day, {'A': 0, 'B': 1, 'C': 2}[store_type], {'YES': 1, 'NO': 0}[holiday]
                    ]
                    result = model.predict([input_data])
                    price = result[0].round(2)
                    st.success(f'Predicted weekly sales of the retail store is: $ {price}')
                except Exception as e:
                    st.error(f"Error in prediction: {str(e)}")

# Conclusion Tab
with tab3:
    col8, col9 = st.columns(2, gap="large")
    with col8:
        st.subheader("My observation from analysis and prediction of this data...")
        st.write(" * The *Weekly Sales* of the retail store is dependent on many factors.")
        st.write(" * These factors are directly or indirectly affecting the Weekly Sales.")
        st.write(" * *Size of the store* is playing a major role.")
        st.write(" * Combination of *Fuel Price* and *Unemployment rate* is significantly impacting the Weekly Sales.")
        st.write(" * *Temperature* and *Markdown* are in indirect relation and sometimes in direct relationship.")
        st.write(" * Both of them are highly impacting the Weekly Sales of the retail store.")

    with col9:
        st.image(Image.open('sales-forecast.png'), width=400)