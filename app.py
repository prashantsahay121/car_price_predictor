import streamlit as st
import pandas as pd
import pickle

# Load trained model
model = pickle.load(open('LinearRegressionModel.pkl', 'rb'))

# Load cleaned data
data = pd.read_csv('Cleaned car.csv')

# Create a mapping of car names to companies
car_company_mapping = data[['name', 'company']].drop_duplicates().set_index('name')['company'].to_dict()

# Add background image and customize text style
def set_custom_styles(image_url):
    """
    Set the background image for the Streamlit app.
    """
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("{image_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Call the function with your image URL
set_custom_styles("https://www.shutterstock.com/image-photo/car-dealer-key-auto-dealership-260nw-343313450.jpg")  # Replace with your image URL

# Streamlit App Title and Inputs
st.title("Car Price Prediction App 🚗")

# Input for car name
st.markdown("**Select Car Name**", unsafe_allow_html=True)
car_name = st.selectbox('', list(car_company_mapping.keys()))

# Automatically set the company based on selected car name
company = car_company_mapping[car_name]
st.markdown(f"**Selected Company: {company}**", unsafe_allow_html=True)

# Input fields for other details
st.markdown("**Year of Manufacture**", unsafe_allow_html=True)
year = st.slider('', int(data['year'].min()), int(data['year'].max()), step=1)

st.markdown("**Kilometers Driven**", unsafe_allow_html=True)
kms_driven = st.number_input('', min_value=0, max_value=1000000, step=500, value=0)

st.markdown("**Fuel Type**", unsafe_allow_html=True)
fuel_type = st.selectbox('', data['fuel_type'].unique())

# Predict button
if st.button('Predict Price'):
    # Prepare input DataFrame
    input_data = pd.DataFrame([[car_name, company, year, kms_driven, fuel_type]],
                              columns=['name', 'company', 'year', 'kms_driven', 'fuel_type'])
    
    # Prediction
    prediction = model.predict(input_data)[0]
    
    st.subheader(f"Predicted Price: ₹{int(prediction):,}")
