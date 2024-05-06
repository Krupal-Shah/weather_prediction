import pandas as pd
from sklearn.multioutput import MultiOutputRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
import numpy as np

def back_training(weather, model, predictors, start=3650, step=90):
    all_predictions = []

    for i in range(start, weather.shape[0], step):
        train = weather.iloc[:i,:]
        test = weather.iloc[i:(i+step),:]
        assert train[predictors].isna().sum().sum() == 0
        assert train[predictors].isin([np.inf, -np.inf]).sum().sum() == 0

        model.fit(train[predictors], train[['target_max', 'target_min']])

        preds = model.predict(test[predictors])

        preds = pd.DataFrame(preds, columns=['target_max', 'target_min'], index=test.index)
        combined = pd.concat([test[['target_max', 'target_min']], preds], axis=1) # Concatenate real test data with predictions to calculate error
        all_predictions.append(combined)

    return pd.concat(all_predictions)

def compute_rolling(weather, horizon, col):
    label = f"{col}_rolling_{horizon}"

    weather[label] = weather[col].rolling(horizon).mean()
    # weather[f"{label}_pct"] = pct_diff(weather[label], weather[col])
    return weather

def main():
    print("Reading the data ...")
    df = pd.read_csv('weather_data.csv', low_memory=False)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df['snow_ground'] = pd.to_numeric(df['snow_ground'], errors='coerce')
    df['wind_speed'] = pd.to_numeric(df['wind_speed'], errors='coerce')
    df.fillna(method='ffill', inplace=True)

    # Setting the location
    print("Setting the location ...")
    id = [27793,]
    df = df[df["id"].isin(id)]
    df = df.drop(columns=["id"])
    df = df.drop(columns=["name"])
    df = df.drop(columns=["location"])

    # Setting the target columns
    print("Setting the parameters ...")
    df["target_max"] = df.shift(-1)['max_temp']
    df["target_min"] = df.shift(-1)['min_temp']
    df = df.ffill()
    # model = MultiOutputRegressor(RandomForestRegressor(n_estimators=100, random_state=42))
    model = MultiOutputRegressor(Ridge(random_state=42, alpha=0.1))
    # predictors = df.columns[~df.columns.isin(['target_max', 'target_min'])]

    # print("Training the model...")
    # df.fillna(0, inplace=True)
    # predictions = back_training(df, model, predictors)

    # print("Calculating the error...")
    # predictions.columns = ['Actual Max', 'Actual Min', 'Predicted Max', 'Predicted Min']

    # print("Max Temp MAE: ", mean_absolute_error(predictions["Actual Max"], predictions["Predicted Max"]))
    # print("Min Temp MAE: ", mean_absolute_error(predictions["Actual Min"], predictions["Predicted Min"]))

    # print("Improving the model...")
    print("Adding rolling features...")
    rolling_horizons = [3, 7, 14]
    for horizon in rolling_horizons:
        for col in ["max_temp", "min_temp", "rain", "snow", "precip", "snow_ground", "wind_speed"]:
            df = compute_rolling(df, horizon, col)
    df.dropna(inplace=True)

    print("Training the model...")
    predictors = df.columns[~df.columns.isin(['target_max', 'target_min'])]
    predictions = back_training(df, model, predictors)

    print("Calculating the error...")
    predictions.columns = ['Target Max', 'Target Min', 'Predicted Max', 'Predicted Min']

    print("Max Temp MAE: ", mean_absolute_error(predictions["Target Max"], predictions["Predicted Max"]))
    print("Min Temp MAE: ", mean_absolute_error(predictions["Target Min"], predictions["Predicted Min"]))
    print("Done!\n")

    print("Predicting tomorrows temperature ...")

    # Predicting tomorrow's temperature
    yesterday = predictions.iloc[-1, :]  # Assuming 'predictions' DataFrame contains predicted values
    new_row = {'max_temp': yesterday['Predicted Max'], 'min_temp': yesterday['Predicted Min']}
    df = df.iloc[-1:, :]
    df = df.append(new_row, ignore_index=True)
    df.drop(columns=['target_max', 'target_min'], inplace=True)

    # Fill missing values using forward fill
    df.fillna(0, inplace=True)
    df['snow_ground'] = df['snow_ground'].ffill()
    print(df)

    # Assuming 'model' is your trained model and 'predictors' are the features used for prediction
    predictions = model.predict(df)
    print(predictions)
    
main()