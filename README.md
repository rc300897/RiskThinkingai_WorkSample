# Work Sample on Data processing and ML model build - RiskThinkingAi
Work Sample on Data processing and ML model building 

The entire process is done in the following steps:
1) Step 1 - Read the data, check the data types and create two new columns for Symbol and Security Name and combine all the files into a single parquet file and store in a directory.
2) Step 2 - Read the input data, check the data types, create two new columns for Symbol and Security Name, create two aggregated columns i) volumne moving average for 30 days and ii) adjacent close rolling mean and then finally combine all the files into a single parquet file and store in another directory.
3) Step 3 - Build a RandomForest Regressor model using Scikit-learn and train the model.(Note: I have used only a subset of the cleaned data. I have used about 5% of the total data which was around 1.4 million rows.This data made a model size 8 GB. I couldnt use Total data as my system resources were not powerful enough to train the model on complete data which is 28 million rows.
4) Step 4 - Created an application using Flask to host the machine learning model and send get request using api to get predections.

## Work Included
* The data pipeline was designed using python and Airflow was used to run the pipeline. I created a DAG and run the pipeline to process the data and train the model.
* The configuration used for airflow and its dependencies are included in the airflow config file attached.
* The Dag was written in python using VS Code.
* All the logs for the pipleine tasks are included in the respective folder.
