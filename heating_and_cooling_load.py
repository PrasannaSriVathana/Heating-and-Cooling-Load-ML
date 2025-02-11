# -*- coding: utf-8 -*-
"""Heating and Cooling Load.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/133b_0LyUoKn5Rl0vtr4CEeggEmutIurq
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.preprocessing import StandardScaler

data_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00242/ENB2012_data.xlsx"
data = pd.read_excel(data_url)

X = data.iloc[:, :-2]
y_heating = data.iloc[:, -2]
y_cooling = data.iloc[:, -1]

original_dim = X.shape[1]
print(f"Original number of features: {original_dim}")

X_train, X_test, y_train_heating, y_test_heating = train_test_split(X, y_heating, test_size=0.3, random_state=42)
X_train, X_test, y_train_cooling, y_test_cooling = train_test_split(X, y_cooling, test_size=0.3, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

def train_evaluate_model(X_train, X_test, y_train, y_test, model):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    return rmse, mae

linear_model_heating = LinearRegression()
rmse_linear_heating, mae_linear_heating = train_evaluate_model(X_train_scaled, X_test_scaled, y_train_heating, y_test_heating, linear_model_heating)

svr_model_heating = SVR(kernel='linear')
rmse_svr_heating, mae_svr_heating = train_evaluate_model(X_train_scaled, X_test_scaled, y_train_heating, y_test_heating, svr_model_heating)

print(f"Heating Load - Linear Regression - RMSE: {rmse_linear_heating}, MAE: {mae_linear_heating}")
print(f"Heating Load - SVR - RMSE: {rmse_svr_heating}, MAE: {mae_svr_heating}")

linear_model_cooling = LinearRegression()
rmse_linear_cooling, mae_linear_cooling = train_evaluate_model(X_train_scaled, X_test_scaled, y_train_cooling, y_test_cooling, linear_model_cooling)

svr_model_cooling = SVR(kernel='linear')
rmse_svr_cooling, mae_svr_cooling = train_evaluate_model(X_train_scaled, X_test_scaled, y_train_cooling, y_test_cooling, svr_model_cooling)

print(f"Cooling Load - Linear Regression - RMSE: {rmse_linear_cooling}, MAE: {mae_linear_cooling}")
print(f"Cooling Load - SVR - RMSE: {rmse_svr_cooling}, MAE: {mae_svr_cooling}")

selector_heating = SelectKBest(score_func=f_regression, k=4)
X_train_reduced_heating = selector_heating.fit_transform(X_train_scaled, y_train_heating)
X_test_reduced_heating = selector_heating.transform(X_test_scaled)

reduced_dim_heating = X_train_reduced_heating.shape[1]
print(f"Reduced number of features for Heating Load: {reduced_dim_heating}")

rmse_linear_heating_reduced, mae_linear_heating_reduced = train_evaluate_model(X_train_reduced_heating, X_test_reduced_heating, y_train_heating, y_test_heating, linear_model_heating)
rmse_svr_heating_reduced, mae_svr_heating_reduced = train_evaluate_model(X_train_reduced_heating, X_test_reduced_heating, y_train_heating, y_test_heating, svr_model_heating)

print(f"Reduced Heating Load - Linear Regression - RMSE: {rmse_linear_heating_reduced}, MAE: {mae_linear_heating_reduced}")
print(f"Reduced Heating Load - SVR - RMSE: {rmse_svr_heating_reduced}, MAE: {mae_svr_heating_reduced}")

selector_cooling = SelectKBest(score_func=f_regression, k=4)
X_train_reduced_cooling = selector_cooling.fit_transform(X_train_scaled, y_train_cooling)
X_test_reduced_cooling = selector_cooling.transform(X_test_scaled)

reduced_dim_cooling = X_train_reduced_cooling.shape[1]
print(f"Reduced number of features for Cooling Load: {reduced_dim_cooling}")

rmse_linear_cooling_reduced, mae_linear_cooling_reduced = train_evaluate_model(X_train_reduced_cooling, X_test_reduced_cooling, y_train_cooling, y_test_cooling, linear_model_cooling)
rmse_svr_cooling_reduced, mae_svr_cooling_reduced = train_evaluate_model(X_train_reduced_cooling, X_test_reduced_cooling, y_train_cooling, y_test_cooling, svr_model_cooling)

print(f"Reduced Cooling Load - Linear Regression - RMSE: {rmse_linear_cooling_reduced}, MAE: {mae_linear_cooling_reduced}")
print(f"Reduced Cooling Load - SVR - RMSE: {rmse_svr_cooling_reduced}, MAE: {mae_svr_cooling_reduced}")

