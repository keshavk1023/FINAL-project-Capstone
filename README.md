# Import necessary libraries
import streamlit as st
import pandas as pd
import datetime
import pickle
from PIL import Image

# Load the data and the pre-trained model
df = pd.read_csv('final_data.csv').drop(['Unnamed: 0'], axis=1)  # Load CSV data and drop the unnecessary column
model = pickle.load(open('model.pkl', 'rb'))  # Load the pre-trained machine learning model

# Configure the Streamlit page
st.set_page_config(
    layout="wide",  # Set the page layout to wide
    page_title="Retail Sales Prediction",  # Set the page title
    page_icon="📊",  # Set the page icon
    initial_sidebar_state="expanded"  # Set the initial sidebar state to expanded
)

# Add a styled header to the page
st.markdown("<h1 style='text-align: center; color: violet;'>Retail Weekly Sales Prediction</h1>", unsafe_allow_html=True)
st.divider()  # Add a divider line

# Create tabs for different sections of the app
tab1, tab2, tab3 = st.tabs(['HOME', 'PREDICTION', 'CONCLUSION'])

# Content for the Home tab
with tab1:
    col1, col2 = st.columns(2, gap="large")  # Create two columns with a large gap

    # First column content
    with col1:
        st.markdown("#### Domain", unsafe_allow_html=True)  # Add a subsection header
        st.write("##### Retail Industry")  # Add content for the domain section
        st.markdown("#### Technologies and Tools used", unsafe_allow_html=True)  # Add another subsection header
        st.write("##### Python, Pandas, numpy, matplotlib, seaborn, Plotly, Streamlit, sklearn.")  # List technologies used
        st.markdown("#### Overview of the Project", unsafe_allow_html=True)  # Add another subsection header
        st.write("##### * Predict the weekly sales of a retail store based on historical sales using Machine Learning techniques.")  # Project overview
        st.write("##### * Perform Data cleaning, Exploratory Data Analysis, Feature Engineering, Hypothesis Testing for the ML model.")  # More project details
        st.write("##### * Using the :violet[RANDOM FOREST REGRESSOR] model to predict the weekly sales of the retail store.")  # Mention the model used

    # Second column content
    with col2:
        st.image(Image.open('random_forest.png'), width=600)  # Display an image related to Random Forest

# Content for the Prediction tab
with tab2:
    # Radio buttons for selecting between processed data and prediction process
    option = st.radio('*Select your option*', ('Processed Data', 'Prediction Process'), horizontal=True)

    # If the user selects "Processed Data"
    if option == 'Processed Data':
        st.header("Processed Final Data")  # Add a header
        st.write(df)  # Display the processed data

    # If the user selects "Prediction Process"
    if option == 'Prediction Process':
        col3, col4, col5, col6, col7 = st.columns(5, gap="large")  # Create five columns with a large gap

        # Column for store information
        with col3:
            st.header("Store Info")  # Add a header
            store = st.selectbox('Select the *Store Number*', list(range(1, 46)))  # Dropdown for store number
            dept = st.selectbox('Select the *Department Number*', [  # Dropdown for department number
                1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 
                21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 40, 
                41, 42, 44, 45, 46, 47, 48, 49, 51, 52, 54, 55, 56, 58, 59, 60, 67, 71, 72, 
                74, 79, 80, 81, 82, 83, 85, 87, 90, 91, 92, 93, 94, 95, 97, 78, 96, 99, 39,
                77, 50, 43, 65, 98
            ])
            store_type = st.selectbox('Select the *Store Type*', ['A', 'B', 'C'])  # Dropdown for store type
            size = st.selectbox('Select the *Store Size*', sorted(df['Size'].unique()))  # Dropdown for store size

        # Column for indirect impact on store sales
        with col4:
            st.header("Indirect Impact on Store Sales")  # Add a header
            temp = st.slider('Enter the *Temperature* in Fahrenheit', min_value=5.54, max_value=100.14, value=90.0)  # Slider for temperature
            fuel = st.slider('Enter the *Fuel Price*', min_value=2.472, max_value=4.468, value=3.67)  # Slider for fuel price
            CPI = st.slider('Enter the *CPI*', min_value=126.0, max_value=227.47, value=211.77)  # Slider for CPI
            unemp = st.slider('Enter the *Unemployment Rate* in percentage', min_value=3.879, max_value=14.313, value=8.106)  # Slider for unemployment rate

        # Column for markdown impact on store sales
        with col5:
            st.header("Markdown Impact on Store Sales")  # Add a header

            # Function to perform inverse transformation
            def inv_trans(x):
                return 1 / x if x != 0 else 0  # Avoid division by zero

            # Sliders for different markdowns with inverse transformation
            markdown1 = inv_trans(st.slider('Enter the *Markdown1* in dollars', min_value=0.27, max_value=88646.76, value=2000.00))
            markdown2 = inv_trans(st.slider('Enter the *Markdown2* in dollars', min_value=0.02, max_value=104519.54, value=65000.00))
            markdown3 = inv_trans(st.slider('Enter the *Markdown3* in dollars', min_value=0.01, max_value=141630.61, value=27000.00))
            markdown4 = inv_trans(st.slider('Enter the *Markdown4* in dollars', min_value=0.22, max_value=67474.85, value=11200.00))
            markdown5 = inv_trans(st.slider('Enter the *Markdown5* in dollars', min_value=135.06, max_value=108519.28, value=89000.00))

        # Column for direct impact on store sales
        with col6:
            st.header("Direct Impact on Store Sales")  # Add a header
            duration = st.date_input("Select the *Date*", datetime.date(2012, 7, 20), min_value=datetime.date(2010, 2, 5), max_value=datetime.date.today())  # Date input for selecting date
            holiday = st.selectbox('Select the *Holiday*', ["YES", "NO"])  # Dropdown for holiday selection

        # Column for predicting weekly sales
        with col7:
            st.header("Weekly Sales")  # Add a header

            # Button to trigger prediction
            if st.button('Predict'):
                try:
                    # Prepare the input data for prediction
                    input_data = [
                        store, dept, size, temp, fuel, CPI, unemp, markdown1, markdown2, markdown3, markdown4, markdown5,
                        duration.year, duration.month, duration.day, {'A': 0, 'B': 1, 'C': 2}[store_type], {'YES': 1, 'NO': 0}[holiday]
                    ]
                    result = model.predict([input_data])  # Predict the weekly sales
                    price = result[0].round(2)  # Round the result to two decimal places
                    st.success(f'Predicted weekly sales of the retail store is: $ {price}')  # Display the prediction result
                except Exception as e:
                    st.error(f"Error in prediction: {str(e)}")  # Display any error that occurs during prediction

# Content for the Conclusion tab
with tab3:
    col8, col9 = st.columns(2, gap="large")  # Create two columns with a large gap

    # First column content
    with col8:
        st.subheader("My observation from analysis and prediction of this data...")  # Add a subheader
        st.write(" * The *Weekly Sales* of the retail store is dependent on many factors.")  # Observation
        st.write(" * These factors are directly or indirectly affecting the Weekly Sales.")  # Observation
        st.write(" * *Size of the store* is playing a major role.")  # Observation
        st.write(" * Combination of *Fuel Price* and *Unemployment rate* is significantly impacting the Weekly Sales.")  # Observation
        st.write(" * *Temperature* and *Markdown* are in indirect relation and sometimes in direct relationship.")  # Observation
        st.write(" * Both of them are highly impacting the Weekly Sales of the retail store.")  # Observation

    # Second column content
    with col9:
        st.image(Image.open('sales-forecast.png'), width=400)  # Display an image related to sales forecast
