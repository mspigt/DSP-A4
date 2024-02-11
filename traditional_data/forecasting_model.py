import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, make_scorer

def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

def impute_missing_values(data):
    data_for_model = data.copy()
    median_percentage = data_for_model['percentage of users last year'].median()
    data_for_model['percentage of users last year'].fillna(median_percentage, inplace=True)
    return data_for_model

def encode_categorical_features(data):
    categorical_features = ['country', 'drug']
    one_hot_encoder = OneHotEncoder(sparse=False)
    encoded_features = one_hot_encoder.fit_transform(data[categorical_features])
    encoded_features_df = pd.DataFrame(encoded_features, columns=one_hot_encoder.get_feature_names_out(categorical_features))
    data_for_model = pd.concat([data.drop(columns=categorical_features), encoded_features_df], axis=1)
    return data_for_model

def split_data(data_for_model):
    X = data_for_model[data_for_model['year'] != 2023].drop(columns=['litre/day per 1 000 inhabitants'])
    y = data_for_model[data_for_model['year'] != 2023]['litre/day per 1 000 inhabitants']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

def hyperparameter_tuning(X_train, y_train):
    model = XGBRegressor(objective ='reg:squarederror', random_state=42)
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [3, 5, 7],
        'learning_rate': [0.01, 0.1],
        'subsample': [0.8, 1.0],
        'colsample_bytree': [0.8, 1.0],
    }
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=3, scoring='neg_mean_squared_error', verbose=1, n_jobs=-1)
    grid_search.fit(X_train, y_train)
    best_model = grid_search.best_estimator_
    return best_model

def cross_validation(best_model, X, y):
    scorer = make_scorer(mean_squared_error, greater_is_better=False)
    cv_scores = cross_val_score(best_model, X, y, cv=5, scoring=scorer)
    rmse_scores = np.sqrt(-cv_scores)
    average_rmse = np.mean(rmse_scores)
    return average_rmse

def evaluate_model(best_model, X_test, y_test):
    y_pred = best_model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    return mae, mse, rmse, r2

def predict_2023_values(best_model, data_for_model, data):
    X_2023 = data_for_model[data_for_model['year'] == 2023].drop(columns=['litre/day per 1 000 inhabitants'])
    predicted_2023_values = best_model.predict(X_2023)
    data.loc[(data['year'] == 2023) & (data['litre/day per 1 000 inhabitants'].isnull()), 'litre/day per 1 000 inhabitants'] = predicted_2023_values
    return data

def calculate_consumption_change(data):
    data['consumption change'] = data.groupby(['country', 'drug'])['litre/day per 1 000 inhabitants'].pct_change()
    data.drop(columns=['Unnamed: 0'], inplace=True)
    return data

def save_updated_data(data, file_path):
    updated_file_path_with_change = 'combined_drug_data_updated_with_predictions_and_change.csv'
    data.to_csv(updated_file_path_with_change, index=False)
    return updated_file_path_with_change

# Usage example:
file_path = 'combined_drug_data_updated.csv'
data = load_data(file_path)
data_for_model = impute_missing_values(data)
data_for_model = encode_categorical_features(data_for_model)
X_train, X_test, y_train, y_test = split_data(data_for_model)
best_model = hyperparameter_tuning(X_train, y_train)
average_rmse = cross_validation(best_model, X_train, y_train)
mae, mse, rmse, r2 = evaluate_model(best_model, X_test, y_test)
data = predict_2023_values(best_model, data_for_model, data)
data = calculate_consumption_change(data)
updated_file_path_with_change = save_updated_data(data, file_path)

print(f"Cross-validated RMSE: {average_rmse:.2f}")
print(f"Mean Absolute Error (MAE): {mae:.2f}")
print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"R-squared (R²): {r2:.2f}")
print(f"Updated dataset with consumption change saved to {updated_file_path_with_change}")