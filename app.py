import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error,mean_absolute_error

#load the data set
cal=fetch_california_housing()
df=pd.DataFrame(cal.data,columns=cal.feature_names)
df['Price']=cal.target

#TITLE OF THE APP
st.title("California Housing Price Prediction")

#Data Overview
st.header("Data Overview for first 10 rows")
st.write(df.head(10))

# split the data into input and output
X = df.drop('Price', axis=1) # input features
y = df['Price'] # target
X_train, X_test,y_train, y_test=train_test_split(X,y, test_size=0.2, random_state=0)

#standedize the data
scaler=StandardScaler()
X_train=scaler.fit_transform(X_train)
X_test=scaler.transform(X_test)

#Model Selection
mod=st.selectbox("Select a Model",("Linear Regression","Random Forest","Decision Tree"))

models={
    "Linear Regression":LinearRegression(),
    "Random Forest":RandomForestRegressor(),
    "Decision Tree":DecisionTreeRegressor()}

#Train the Model
selected_model=models[mod] #initializing the selected model

# train the selected model
selected_model.fit(X_train, y_train)

#make Prediction
y_pred=selected_model.predict(X_test)

#model evaluation
r2=r2_score(y_test,y_pred)
mse=mean_squared_error(y_test,y_pred)
mae=mean_absolute_error(y_test,y_pred)

#Display teh results
st.write(f"R2 Score:{r2}")
st.write(f"Mean Squared Error:{mse}")
st.write(f"Mean Absolute Error:{mae}")

#prompt for user input
st.write("Enter the input values for prediction")

user_input={}
for column in X.columns:
    user_input[column]=st.number_input(column, min_value=np.min(X[column]),max_value=np.max(X[column]),value=np.min(X[column]))

#convert user input to dataframe
user_input_df=pd.DataFrame([user_input])

#standardize teh user input
user_input_sc_df=scaler.transform(user_input_df)

#predict the price
predicted_price=selected_model.predict(user_input_sc_df)

#Display teh predicted price
st.write(f"Predicted price for the given house is:{predicted_price[0]*100000}")