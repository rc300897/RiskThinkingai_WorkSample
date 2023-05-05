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

Filename second_dag.py is the complet DAG pipeline.

## Configuration used for Airflow

* Local Executor for parallelization of tasks. (Tasks read_data_process and task read_data_and_calculate_rolling_mean_and_rolling_median start simentaneously.)
* Postgres database was used to store metadata from the airflow.
* Airflow was installed locally and scheduler, webserver were run on localhost and port 8080.
* Python version 3.9 was used along with airflow.
* All the modules were installed using pip install.

## References
* https://stackoverflow.com/questions/69231797/airflow-dag-fails-when-pythonoperator-with-error-negsignal-sigkill
* https://stackoverflow.com/questions/57668584/airflow-scheduler-does-not-appear-to-be-running-after-execute-a-task
* https://airflow.apache.org/docs/apache-airflow/stable/howto/set-up-database.html
* https://rollbar.com/blog/python-operationalerror/#:~:text=OperationalError%20is%20a%20class%20of,method%20are%20incorrect%20or%20invalid.
* https://www.youtube.com/watch?v=AZfJ8buL5II&t=168s
* https://www.youtube.com/watch?v=LL5WP_T-jvA&t=99s
