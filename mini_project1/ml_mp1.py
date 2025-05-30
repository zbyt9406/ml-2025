# -*- coding: utf-8 -*-
"""ml_MP1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/12p_1SWJ5G_NFOszEQwgUfiSy0u7uHZz2
"""

#پیش بینی آب و هوا مبنتی بر یادگیری ماشین

!pip install --upgrade --no-cache-dir gdown
!gdown 18O248Vc5mnWoB21w77NIlFYlbPDsE9tw

import pandas as pd
import numpy as np

df = pd.read_csv("weather_prediction_dataset.csv")

france_cities = ["TOURS"]

columns_to_keep = ["DATE", "MONTH"] + [col for col in df.columns if any(city in col for city in france_cities)]
df_france = df[columns_to_keep]

df_france.to_csv("weather_prediction_dataset_france.csv", index=False)

print("Filtered dataset saved as 'weather_prediction_dataset_france.csv'")

from google.colab import files

# Download the filtered dataset
files.download("weather_prediction_dataset_france.csv")

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np

file_path = "weather_prediction_dataset_france.csv"
df = pd.read_csv(file_path)

df.fillna(df.mean(), inplace=True)

relevant_features = ["DATE", "MONTH", "TOURS_temp_mean", "TOURS_humidity",
                     "TOURS_pressure", "TOURS_wind_speed"]
df_selected = df[relevant_features]

scaler = MinMaxScaler()
df_scaled = df_selected.copy()
df_scaled.iloc[:, 2:] = scaler.fit_transform(df_selected.iloc[:, 2:])

df_scaled.to_csv("weather_prediction_dataset_france_final.csv", index=False)

print("Preprocessing completed! Saved:")
print("- 'weather_prediction_dataset_france_final.csv' (scaled data)")

# Download the preprocessed dataset
files.download("weather_prediction_dataset_france_final.csv")

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

file_path = "weather_prediction_dataset_france_final.csv"
df = pd.read_csv(file_path)

df['DATE'] = pd.to_datetime(df['DATE'], format='%Y%m%d')

test_data = df[df['DATE'].dt.year == 2009]
train_data = df[df['DATE'].dt.year != 2009]

train_data = train_data.drop(columns=['DATE', 'MONTH'])
test_data = test_data.drop(columns=['DATE', 'MONTH'])

X_train, Y_train = train_data.iloc[:, :-1], train_data.iloc[:, -1]
X_test, Y_test = test_data.iloc[:, :-1], test_data.iloc[:, -1]

scaler_X = MinMaxScaler()
X_train_scaled = scaler_X.fit_transform(X_train)
X_test_scaled = scaler_X.transform(X_test)

scaler_Y = MinMaxScaler()
Y_train_scaled = scaler_Y.fit_transform(Y_train.values.reshape(-1, 1))
Y_test_scaled = scaler_Y.transform(Y_test.values.reshape(-1, 1))

def create_sliding_window(data_X, data_Y, window_size, overlap):
    step = window_size - overlap
    X, Y = [], []
    for i in range(0, len(data_X) - window_size + 1, step):
        X.append(data_X[i:i+window_size, :])
        Y.append(data_Y[i+window_size-1, :])
    return np.array(X), np.array(Y)

window_size = 5
overlap = 4

Y_test_scaled = np.clip(Y_test_scaled, 0, 1)

X_train_windowed, Y_train_windowed = create_sliding_window(X_train_scaled, Y_train_scaled, window_size, overlap)
X_test_windowed, Y_test_windowed = create_sliding_window(X_test_scaled, Y_test_scaled, window_size, overlap)

np.save("X_train.npy", X_train_windowed)
np.save("Y_train.npy", Y_train_windowed)
np.save("X_test.npy", X_test_windowed)
np.save("Y_test.npy", Y_test_windowed)

print("🚀 Sliding window train/test data created successfully!")

print("X_train shape:", X_train_windowed.shape)
print("Y_train shape:", Y_train_windowed.shape)
print("X_test shape:", X_test_windowed.shape)
print("Y_test shape:", Y_test_windowed.shape)

#MLR

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error

X_train = np.load("X_train.npy")
Y_train = np.load("Y_train.npy")
X_test = np.load("X_test.npy")
Y_test = np.load("Y_test.npy")

X_train = X_train.reshape(X_train.shape[0], -1)
X_test = X_test.reshape(X_test.shape[0], -1)

mlr = LinearRegression()
mlr.fit(X_train, Y_train)

Y_pred_train = np.clip(mlr.predict(X_train), 0, 1)
Y_pred_test = np.clip(mlr.predict(X_test), 0, 1)

Y_train_pred_inv = scaler_Y.inverse_transform(Y_pred_train)
Y_test_pred_inv = scaler_Y.inverse_transform(Y_pred_test)
Y_train_actual_inv = scaler_Y.inverse_transform(Y_train)
Y_test_actual_inv = scaler_Y.inverse_transform(Y_test)

train_rmse = np.sqrt(mean_squared_error(Y_train_actual_inv, Y_train_pred_inv))
test_rmse = np.sqrt(mean_squared_error(Y_test_actual_inv, Y_test_pred_inv))
train_mae = mean_absolute_error(Y_train_actual_inv, Y_train_pred_inv)
test_mae = mean_absolute_error(Y_test_actual_inv, Y_test_pred_inv)
train_mse = mean_squared_error(Y_train_actual_inv, Y_train_pred_inv)
test_mse = mean_squared_error(Y_test_actual_inv, Y_test_pred_inv)

print(f"Train RMSE: {train_rmse:.4f}, Test RMSE: {test_rmse:.4f}")
print(f"Train MAE: {train_mae:.4f}, Test MAE: {test_mae:.4f}")
print(f"Train MSE: {train_mse:.4f}, Test MSE: {test_mse:.4f}")

#MPR

from sklearn.preprocessing import MinMaxScaler, PolynomialFeatures
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, mean_absolute_error

X_train = np.load("X_train.npy")
Y_train = np.load("Y_train.npy")
X_test = np.load("X_test.npy")
Y_test = np.load("Y_test.npy")

X_train = X_train.reshape(X_train.shape[0], -1)
X_test = X_test.reshape(X_test.shape[0], -1)

def train_polynomial_regression(X_train, Y_train, X_test, scaler_Y, degree=2, alpha=5):
    poly = PolynomialFeatures(degree=degree, interaction_only=False)
    X_train_poly = poly.fit_transform(X_train)
    X_test_poly = poly.transform(X_test)

    scaler_X = MinMaxScaler()
    X_train_poly = scaler_X.fit_transform(X_train_poly)
    X_test_poly = scaler_X.transform(X_test_poly)

    model = Ridge(alpha=alpha)
    model.fit(X_train_poly, Y_train)

    Y_train_pred = scaler_Y.inverse_transform(model.predict(X_train_poly).reshape(-1, 1))
    Y_test_pred = scaler_Y.inverse_transform(model.predict(X_test_poly).reshape(-1, 1))

    return model, Y_train_pred, Y_test_pred


mpr_model, Y_train_pred_inv, Y_test_pred_inv = train_polynomial_regression(
    X_train, Y_train, X_test, scaler_Y, degree=2, alpha=5)

Y_train_actual_inv = scaler_Y.inverse_transform(Y_train_windowed.reshape(-1, 1))
Y_test_actual_inv = scaler_Y.inverse_transform(Y_test_windowed.reshape(-1, 1))


train_rmse = np.sqrt(mean_squared_error(Y_train_actual_inv, Y_train_pred_inv))
test_rmse = np.sqrt(mean_squared_error(Y_test_actual_inv, Y_test_pred_inv))
train_mae = mean_absolute_error(Y_train_actual_inv, Y_train_pred_inv)
test_mae = mean_absolute_error(Y_test_actual_inv, Y_test_pred_inv)
train_mse = mean_squared_error(Y_train_actual_inv, Y_train_pred_inv)
test_mse = mean_squared_error(Y_test_actual_inv, Y_test_pred_inv)

print(f"Train RMSE: {train_rmse:.4f}, Test RMSE: {test_rmse:.4f}")
print(f"Train MAE: {train_mae:.4f}, Test MAE: {test_mae:.4f}")
print(f"Train MSE: {train_mse:.4f}, Test MSE: {test_mse:.4f}")

#KNN
from sklearn.neighbors import KNeighborsRegressor

X_train = np.load("X_train.npy")
Y_train = np.load("Y_train.npy")
X_test = np.load("X_test.npy")
Y_test = np.load("Y_test.npy")

X_train = X_train.reshape(X_train.shape[0], -1)
X_test = X_test.reshape(X_test.shape[0], -1)

scaler_Y = MinMaxScaler()
Y_train = scaler_Y.fit_transform(Y_train)
Y_test = scaler_Y.transform(Y_test)

def train_knn(X_train, Y_train, X_test, scaler_Y, n_neighbors=5):
    knn = KNeighborsRegressor(n_neighbors=n_neighbors)
    knn.fit(X_train, Y_train.ravel())

    Y_train_pred = scaler_Y.inverse_transform(knn.predict(X_train).reshape(-1, 1))
    Y_test_pred = scaler_Y.inverse_transform(knn.predict(X_test).reshape(-1, 1))

    return knn, Y_train_pred, Y_test_pred

knn_model, Y_train_pred_inv, Y_test_pred_inv = train_knn(X_train, Y_train, X_test, scaler_Y, n_neighbors=5)

Y_train_actual_inv = scaler_Y.inverse_transform(Y_train)
Y_test_actual_inv = scaler_Y.inverse_transform(Y_test)

train_rmse = np.sqrt(mean_squared_error(Y_train_actual_inv, Y_train_pred_inv))
test_rmse = np.sqrt(mean_squared_error(Y_test_actual_inv, Y_test_pred_inv))
train_mae = mean_absolute_error(Y_train_actual_inv, Y_train_pred_inv)
test_mae = mean_absolute_error(Y_test_actual_inv, Y_test_pred_inv)
train_mse = mean_squared_error(Y_train_actual_inv, Y_train_pred_inv)
test_mse = mean_squared_error(Y_test_actual_inv, Y_test_pred_inv)

print(f"KNN Train RMSE: {train_rmse:.4f}, Test RMSE: {test_rmse:.4f}")
print(f"KNN Train MAE: {train_mae:.4f}, Test MAE: {test_mae:.4f}")
print(f"KNN Train MSE: {train_mse:.4f}, Test MSE: {test_mse:.4f}")

# MLP

from tensorflow import keras

X_train = np.load("X_train.npy")
Y_train = np.load("Y_train.npy")
X_test = np.load("X_test.npy")
Y_test = np.load("Y_test.npy")

X_train = X_train.reshape(X_train.shape[0], -1)
X_test = X_test.reshape(X_test.shape[0], -1)

def train_mlp(X_train, Y_train, X_test, scaler_Y, epochs=100, batch_size=32):
    input_dim = X_train.shape[1]

    model = keras.Sequential([
        keras.layers.Input(shape=(input_dim,)),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(32, activation='relu'),
        keras.layers.Dense(1, activation='linear')
    ])

    model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001),
                  loss='mse',
                  metrics=['mae'])

    model.fit(X_train, Y_train, epochs=epochs, batch_size=batch_size, verbose=1, validation_split=0.1)

    Y_train_pred = scaler_Y.inverse_transform(model.predict(X_train).reshape(-1, 1))
    Y_test_pred = scaler_Y.inverse_transform(model.predict(X_test).reshape(-1, 1))

    return model, Y_train_pred, Y_test_pred

mlp_model, Y_train_pred_inv, Y_test_pred_inv = train_mlp(
    X_train, Y_train, X_test, scaler_Y, epochs=100, batch_size=32)

Y_train_actual_inv = scaler_Y.inverse_transform(Y_train.reshape(-1, 1))
Y_test_actual_inv = scaler_Y.inverse_transform(Y_test.reshape(-1, 1))

train_rmse = np.sqrt(mean_squared_error(Y_train_actual_inv, Y_train_pred_inv))
test_rmse = np.sqrt(mean_squared_error(Y_test_actual_inv, Y_test_pred_inv))
train_mae = mean_absolute_error(Y_train_actual_inv, Y_train_pred_inv)
test_mae = mean_absolute_error(Y_test_actual_inv, Y_test_pred_inv)
train_mse = mean_squared_error(Y_train_actual_inv, Y_train_pred_inv)
test_mse = mean_squared_error(Y_test_actual_inv, Y_test_pred_inv)

print(f"MLP Train RMSE: {train_rmse:.4f}, Test RMSE: {test_rmse:.4f}")
print(f"MLP Train MAE: {train_mae:.4f}, Test MAE: {test_mae:.4f}")
print(f"MLP Train MSE: {train_mse:.4f}, Test MSE: {test_mse:.4f}")

#CNN

def create_sliding_window(X, Y, window_size=5, step=1):
    X_windowed, Y_windowed = [], []
    for i in range(0, len(X) - window_size + 1, step):
        X_windowed.append(X[i:i+window_size])
        Y_windowed.append(Y[i+window_size-1])
    return np.array(X_windowed), np.array(Y_windowed)

def train_cnn(X_train, Y_train, X_test, scaler_Y, epochs=100, batch_size=32):
    time_steps, num_features = X_train.shape[1], X_train.shape[2]

    model = keras.Sequential([
        keras.layers.Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(time_steps, num_features)),
        keras.layers.Conv1D(filters=32, kernel_size=3, activation='relu'),
        keras.layers.Flatten(),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(1, activation='linear')
    ])

    model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001),
                  loss='mse',
                  metrics=['mae'])

    model.fit(X_train, Y_train, epochs=epochs, batch_size=batch_size, verbose=1, validation_split=0.1)

    Y_train_pred = scaler_Y.inverse_transform(model.predict(X_train))
    Y_test_pred = scaler_Y.inverse_transform(model.predict(X_test))

    return model, Y_train_pred, Y_test_pred


window_size, step = 5, 1
X_train_windowed, Y_train_windowed = create_sliding_window(X_train, Y_train, window_size, step)
X_test_windowed, Y_test_windowed = create_sliding_window(X_test, Y_test, window_size, step)

X_train_windowed = X_train_windowed.reshape((X_train_windowed.shape[0], window_size, X_train.shape[1]))
X_test_windowed = X_test_windowed.reshape((X_test_windowed.shape[0], window_size, X_test.shape[1]))

cnn_model, Y_train_pred_inv, Y_test_pred_inv = train_cnn(
    X_train_windowed, Y_train_windowed, X_test_windowed, scaler_Y, epochs=100, batch_size=32)

Y_train_actual_inv = scaler_Y.inverse_transform(Y_train_windowed.reshape(-1, 1))
Y_test_actual_inv = scaler_Y.inverse_transform(Y_test_windowed.reshape(-1, 1))

train_rmse = np.sqrt(mean_squared_error(Y_train_actual_inv, Y_train_pred_inv))
test_rmse = np.sqrt(mean_squared_error(Y_test_actual_inv, Y_test_pred_inv))
train_mae = mean_absolute_error(Y_train_actual_inv, Y_train_pred_inv)
test_mae = mean_absolute_error(Y_test_actual_inv, Y_test_pred_inv)
train_mse = mean_squared_error(Y_train_actual_inv, Y_train_pred_inv)
test_mse = mean_squared_error(Y_test_actual_inv, Y_test_pred_inv)

print(f"CNN Train RMSE: {train_rmse:.4f}, Test RMSE: {test_rmse:.4f}")
print(f"CNN Train MAE: {train_mae:.4f}, Test MAE: {test_mae:.4f}")
print(f"CNN Train MSE: {train_mse:.4f}, Test MSE: {test_mse:.4f}")

from tqdm import tqdm

df = pd.read_csv("weather_prediction_dataset.csv")

print("Dataset Columns:", df.columns.tolist())

cities = set()
features = set()
for col in df.columns:
    if "_" in col:
        city, feature = col.split("_", 1)
        cities.add(city)
        features.add(feature)

cities = list(cities)
features = list(features)

feature_columns = [f"{city}_{feature}" for city in cities for feature in features if f"{city}_{feature}" in df.columns]

df = df[['DATE'] + feature_columns]

df['DATE'] = pd.to_datetime(df['DATE'])
df = df.sort_values(by='DATE')

df.fillna(df.mean(), inplace=True)

scaler = MinMaxScaler()
df[feature_columns] = scaler.fit_transform(df[feature_columns])

X = df[feature_columns].values[:-1]
y = df[feature_columns].values[1:]

split_idx = int(0.8 * len(X))
X_train, X_test = X[:split_idx], X[split_idx:]
y_train, y_test = y[:split_idx], y[split_idx:]

beta = np.random.randn(len(feature_columns) + 1, len(feature_columns))
learning_rate = 0.01
threshold = 1e-4
max_epochs = 1000

for epoch in tqdm(range(max_epochs), desc="Training Progress"):
    y_pred = np.dot(np.c_[np.ones(X_train.shape[0]), X_train], beta)
    error = y_pred - y_train
    mse = np.mean(error ** 2)

    gradient = (2 / len(X_train)) * np.dot(np.c_[np.ones(X_train.shape[0]), X_train].T, error)
    beta -= learning_rate * gradient

    y_test_pred = np.dot(np.c_[np.ones(X_test.shape[0]), X_test], beta)
    test_mse = np.mean((y_test_pred - y_test) ** 2)

    tqdm.write(f"Epoch {epoch + 1}: Train MSE={mse:.6f}, Test MSE={test_mse:.6f}")

    if mse < threshold:
        print("Stopping early as training error is below threshold.")
        break

print("Final Weights:", beta)

from sklearn.linear_model import LinearRegression, Ridge, Lasso

df = pd.read_csv("weather_prediction_dataset.csv")

print("Dataset Columns:", df.columns.tolist())

city = "BASEL"
feature_columns = [col for col in df.columns if col.startswith(f"{city}_")]

df = df[['DATE'] + feature_columns]

df['DATE'] = pd.to_datetime(df['DATE'])
df = df.sort_values(by='DATE')

df.fillna(df.mean(), inplace=True)

scaler = MinMaxScaler()
df[feature_columns] = scaler.fit_transform(df[feature_columns])

X = df[feature_columns].values[:-1]
y = df[feature_columns].values[1:]

split_idx = int(0.8 * len(X))
X_train, X_test = X[:split_idx], X[split_idx:]
y_train, y_test = y[:split_idx], y[split_idx:]

models = {
    "Linear Regression": LinearRegression(),
    "Ridge Regression": Ridge(alpha=1.0),
    "Lasso Regression": Lasso(alpha=0.1)
}

results = {}
for name, model in models.items():
    print(f"Training {name}...")
    model.fit(X_train, y_train)
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    train_mse = mean_squared_error(y_train, y_train_pred)
    test_mse = mean_squared_error(y_test, y_test_pred)

    results[name] = {
        "Train MSE": train_mse,
        "Test MSE": test_mse
    }
    print(f"{name}: Train MSE={train_mse:.6f}, Test MSE={test_mse:.6f}")

best_model = min(results, key=lambda x: results[x]["Test MSE"])
print("Best model:", best_model, "with Test MSE:", results[best_model]["Test MSE"])

df = pd.read_csv("weather_prediction_dataset.csv")

print("Dataset Columns:", df.columns.tolist())

cities = ["BASEL", "BUDAPEST", "DRESDEN"]

all_results = {}

for city in cities:
    print(f"\nProcessing city: {city}")

    feature_columns = [col for col in df.columns if col.startswith(f"{city}_")]

    if not feature_columns:
        print(f"Warning: No columns found for {city}. Skipping...")
        continue

    city_df = df[['DATE'] + feature_columns].copy()

    city_df['DATE'] = pd.to_datetime(city_df['DATE'])
    city_df = city_df.sort_values(by='DATE')

    city_df.fillna(city_df.mean(), inplace=True)

    scaler = MinMaxScaler()
    city_df[feature_columns] = scaler.fit_transform(city_df[feature_columns])

    X = city_df[feature_columns].values[:-1]
    y = city_df[feature_columns].values[1:]

    split_idx = int(0.8 * len(X))
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]

    # Initialize models. if you put alpha's so low like 0.00001, the MSE's would be so close to eachother.
    models = {
        "Linear Regression": LinearRegression(),
        "Ridge Regression": Ridge(alpha=0.00001),
        "Lasso Regression": Lasso(alpha=0.00001)
    }

    results = {}
    for name, model in models.items():
        print(f"Training {name} for {city}...")
        model.fit(X_train, y_train)
        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)

        train_mse = mean_squared_error(y_train, y_train_pred)
        test_mse = mean_squared_error(y_test, y_test_pred)

        results[name] = {
            "Train MSE": train_mse,
            "Test MSE": test_mse
        }
        print(f"{name} ({city}): Train MSE={train_mse:.6f}, Test MSE={test_mse:.6f}")

    all_results[city] = results

for city, results in all_results.items():
    best_model = min(results, key=lambda x: results[x]["Test MSE"])
    print(f"\nBest model for {city}: {best_model} with Test MSE: {results[best_model]['Test MSE']:.6f}")

# 3 other cities

df = pd.read_csv("weather_prediction_dataset.csv")

selected_cities = ["MAASTRICHT", "MUENCHEN", "TOURS"]
selected_features = ["pressure", "humidity", "precipitation"]
feature_columns = [f"{city}_{feature}" for city in selected_cities for feature in selected_features]

for col in feature_columns:
    if col not in df.columns:
        raise ValueError(f"Missing column: {col}")

df = df[['DATE'] + feature_columns].copy()

df['DATE'] = pd.to_datetime(df['DATE'], format='%Y%m%d')
df = df.sort_values(by='DATE')

df.fillna(df.mean(), inplace=True)

scaler = MinMaxScaler()
df[feature_columns] = scaler.fit_transform(df[feature_columns])

city = "MUENCHEN"
city_features = [f"{city}_{feature}" for feature in selected_features]

X = df[city_features].values[:-1]
y = df[city_features].values[1:]

split_idx = int(0.8 * len(X))
X_train, X_test = X[:split_idx], X[split_idx:]
y_train, y_test = y[:split_idx], y[split_idx:]

models = {
    "Linear Regression": LinearRegression(),
    "Ridge Regression": Ridge(alpha=1),
    "Lasso Regression": Lasso(alpha=0.1)
}

results = {}
for name, model in models.items():
    print(f"Training {name} for {city}...")
    model.fit(X_train, y_train)
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    train_mse = mean_squared_error(y_train, y_train_pred)
    test_mse = mean_squared_error(y_test, y_test_pred)

    results[name] = {
        "Train MSE": train_mse,
        "Test MSE": test_mse
    }
    print(f"{name}: Train MSE={train_mse:.6f}, Test MSE={test_mse:.6f}")

best_model = min(results, key=lambda x: results[x]["Test MSE"])
print(f"\nBest model for {city}: {best_model} with Test MSE: {results[best_model]['Test MSE']:.6f}")