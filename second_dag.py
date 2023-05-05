try:

    from datetime import timedelta, datetime
    from airflow import DAG

    from airflow.operators.python_operator import PythonOperator
    from airflow.operators.bash import BashOperator
    import pandas as pd
    import numpy as np
    import os 
    import glob

    from datetime import datetime

    # Setting up Triggers
    from airflow.utils.trigger_rule import TriggerRule

    print("All Dag modules are ok ......")

except Exception as e:
    print("Error  {} ".format(e))


def read_data_process():
    directory_path = "/Users/rahulchalla/airflow/data/Stocks_data"
    files_path_processed ="/Users/rahulchalla/airflow/data/processed_data/processed_data.parquet"

    dfs = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".csv"):
                df = pd.read_csv(os.path.join(root,file))
                df['Symbol'] = file[:-3]
                if root[-4:] == "etfs":
                    df['Security Name'] = "etfs"
                elif root[-6:] == "stocks":
                    df['Security Name'] = "stock"
                dfs.append(df)
    comb_df = pd.concat(dfs,ignore_index= True)
    comb_df.to_parquet(files_path_processed,index = False)  

def read_data_and_calculate_rollingmean_and_rollingmedian():
    directory_path = "/Users/rahulchalla/airflow/data/Stocks_data"
    files_path_aggregated = "/Users/rahulchalla/airflow/data/aggregated_data/aggregated_data.parquet"
    dfs = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".csv"):
                df = pd.read_csv(os.path.join(root,file))
                df['Symbol'] = file[:-3]
                if root[-4:] == "etfs":
                    df['Security Name'] = "etfs"
                elif root[-6:] == "stocks":
                    df['Security Name'] = "stock"
                rollings = df['Volume'].rolling(30)
                df['vol_moving_avg'] = rollings.mean()
                df['adj_close_rolling_med'] = rollings.median()
                dfs.append(df)
    comb_df = pd.concat(dfs,ignore_index= True)
    comb_df.to_parquet(files_path_aggregated,index = False)

def ml_model_build_and_train():
    files_path_aggregated = "/Users/rahulchalla/airflow/data/aggregated_data/aggregated_data.parquet"
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_absolute_error, mean_squared_error
    import pickle

    data = pd.read_parquet(files_path_aggregated)
    # Assume `data` is loaded as a Pandas DataFrame
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)

    # Remove rows with NaN values
    data.dropna(inplace=True)
    Data1 = data.sample(frac = 0.05, random_state=42)

    # Select features and target
    features = ['vol_moving_avg', 'adj_close_rolling_med']
    target = 'Volume'

    X = Data1[features]
    y = Data1[target]

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X.values, y.values, test_size=0.2, random_state=42)

    # Create a RandomForestRegressor model
    model = RandomForestRegressor(n_estimators=100, random_state=42)

    # Train the model
    model.fit(X_train, y_train)

    # Train the model
    y_pred = model.predict(X_test)

    # Calculate the Mean Absolute Error and Mean Squared Error
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)

    # Saving the trained model.
    model_save_path = "/Users/rahulchalla/airflow/data/models/randomforestmodel_stocksdata/randomforest_model_stock_volume_prediction.sav"
    pickle.dump(model, open(model_save_path, 'wb'))



        









    


def on_failure_callback(context):
    print("Fail works  !  ")


with DAG(dag_id="second_dag",
         schedule_interval="@once",
         default_args={
             "owner": "airflow",
             "start_date": datetime(2023, 4, 30),
             "retries": 1,
             "retry_delay": timedelta(minutes=1),
             'on_failure_callback': on_failure_callback,
             'email': ['rahulchalla30@gmail.com'],
             'email_on_failure': False,
             'email_on_retry': False,
         },
         catchup=False) as dag:
    
    task_start = BashOperator(
    task_id='start',
    bash_command='date'
    )

    

    read_data_process = PythonOperator(
        task_id = "read_data_process",
        python_callable=read_data_process,
    )

    read_data_and_calculate_rollingmean_and_rollingmedian = PythonOperator(
        task_id = "read_data_and_calculate_rollingmean_and_rollingmedian",
        python_callable=read_data_and_calculate_rollingmean_and_rollingmedian
    )

    ml_model_build_and_train = PythonOperator(
        task_id = "ml_model_build_and_train",
        python_callable = ml_model_build_and_train
    )

    

    


task_start >> [read_data_process,read_data_and_calculate_rollingmean_and_rollingmedian] >> ml_model_build_and_train