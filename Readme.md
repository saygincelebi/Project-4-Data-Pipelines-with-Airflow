##**Project: Data Pipelines with Airflow**## 

A music streaming company, Sparkify, has decided that it is time to introduce more automation and monitoring to their data warehouse ETL pipelines and come to the conclusion that the best tool to achieve this is Apache Airflow.

They have decided to bring you into the project and expect you to create high grade data pipelines that are dynamic and built from reusable tasks, can be monitored, and allow easy backfills. They have also noted that the data quality plays a big part when analyses are executed on top the data warehouse and want to run tests against their datasets after the ETL steps have been executed to catch any discrepancies in the datasets.

The source data resides in S3 and needs to be processed in Sparkify's data warehouse in Amazon Redshift. The source datasets consist of JSON logs that tell about user activity in the application and JSON metadata about the songs the users listen to.

###Datasets###

For this project, we have worked with two datasets. These are the s3 links for each:

Log data: s3://udacity-dend/log_data
Song data: s3://udacity-dend/song_data

###Structure###
The project  package contains three major components for the project:

- The dag
- The operators folder
- The helper class for the SQL transformations

**DAG parameters:**

- The DAG does not have dependencies on past runs
- DAG has schedule interval set to hourly
- On failure, the task are retried 3 times
- Retries happen every 5 minutes
- Catchup is turned off
- Email are not sent on retry

###Flow###
Task dependencies are set as following:
[![Flow](https://video.udacity-data.com/topher/2019/January/5c48a861_example-dag/example-dag.png "Flow")](https://video.udacity-data.com/topher/2019/January/5c48a861_example-dag/example-dag.png "Flow")

###Project Files###
- **dags/Sparkify_Dag.py**: Directed Acyclic Graph definition with imports, tasks and task dependencies

- **plugins/helpers/sql_queries.py**: Contains Insert SQL statements
- **plugins/operators/create_tables.sql**: Contains SQL Table creations statements

- **plugins/operators/stage_redshift.py**: Operator that copies data from S3 buckets into redshift staging tables
- **plugins/operators/load_dimension.py:** Operator that loads data from redshift staging tables into dimensional tables
- **plugins/operators/load_fact.py:** Operator that loads data from redshift staging tables into fact table
- **plugins/operators/data_quality.py:** Operator that validates data quality in redshift tables

###DAG Configuration###
In the DAG, the default parameters are added according to these guidelines

- The DAG does not have dependencies on past runs
- On failure, the task are retried 3 times
- Retries happen every 5 minutes
- Catchup is turned off
- Do not email on retry

###Data Structure###

Using the song and log datasets, we have created a star schema optimized for queries on song play analysis. This includes the following tables.

####Fact Table####
**songplays** - records in log data associated with song plays i.e. records with page NextSong
songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
####Dimension Tables####
**users** - users in the app
user_id, first_name, last_name, gender, level
**songs** - songs in music database
song_id, title, artist_id, year, duration
**artists** - artists in music database
artist_id, name, location, latitude, longitude
**time** - timestamps of records in songplays broken down into specific units
start_time, hour, day, week, month, year, weekday

####Deployment####
We need to run /opt/airflow/start.sh command to start the Airflow web server, the flow will start at it's scheduled time.