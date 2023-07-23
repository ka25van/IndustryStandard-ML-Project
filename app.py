#Building app using streamlit
#Streamlit is an open source app framework in Python language. It helps us create web apps for data science and machine learning in a short time. 
#It is compatible with major Python libraries such as scikit-learn, Keras, PyTorch, SymPy(latex), NumPy, pandas, Matplotlib etc.

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import pickle
import xgboost as xg
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder

#Need pickle file to run web application, which is in saved_models; so instead we copy and paste it outside the folder
model=pickle.load(open('model.pkl', 'rb'))
transformer=pickle.load(open('transformer.pkl', 'rb'))
encoder=pickle.load(open('target_encoder.pkl', 'rb'))

st.title("Insurance Premium Prediction")  #by running command: streamlit run app.py ; we see the title in a new url


#Now by looking into the columns mentioned in the raw dataset, we build the web app by specifying inputs whenever user enters

age=st.text_input("Please select age:", 18) 
age=int(age)

sex=st.selectbox("Select Gender:",("male","female"))

bmi=st.text_input("Enter BMI(Body Measure Index:", 10)
bmi=float(bmi)

url = 'https://www.calculator.net/bmi-calculator.html'
st.markdown(f'''<a href={url}><button style="background-color:GreenYellow;">Click here for BMI Calculator</button></a>''',
unsafe_allow_html=True)

children=st.selectbox("Enter Number of Children:",(0,1,2,3,4,5))

smoker=st.selectbox("Are you a regular smoker:",("yes","no"))

region=st.selectbox("Select your region:",("northeast","northwest","southeast","southwest"))


#Saving it as a dictornary
l = {}
l['age'] = age
l['sex'] = sex
l['bmi'] = bmi
l['children'] = children
l['smoker'] = smoker
l['region'] = region

#Converting the dictornary values into a dataframe
df=pd.DataFrame(l,index=[0])

#We need to encode the categorical values to get he prediction so here sex, smoker, region ae the categorical areas

df['region']=encoder.transform(df['region'])
df['smoker']=df['smoker'].map({'yes':0, 'no':1})
df['sex']=df['sex'].map({'male':0, 'female':1})

#Now since all the areas are transformed, we once again run the transform 
df = transformer.transform(df)

#Doing the predictiction
y_pred = model.predict(df)

if st.button("Get Results"):
    st.header(f"The Insurance Premium would be:   Rs.{round(y_pred[0],2)}")  #For 2 decimals