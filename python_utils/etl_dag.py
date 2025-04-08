import requests
import json
from datetime import datetime
from datetime import timedelta
import boto3
from airflow import DAG
from airflow.operators.python import PythonOperator

def get_weather_data(**kwargs):
    """
    Fetches weather information for ten belgian cities: 'responses',
    which is a list of dictionaries with the weather conditions for each location.
    responses is then pushed to the airflow context, allowing other functions to retrieve
    the information and use it.
    """

    root_url = "https://api.openweathermap.org"
    endpoint = "data/2.5/weather"
    api_key = "***********************" # Enter you weather API
    cities = [
        "Antwerp",
        "Bruges",
        "Brussels",
        "Charleroi",
        "Ghent",
        "Leuven",
        "Liege",
        "Mons",
        "Namur",
        "Ostend",
    ]

    responses = []
    # end request for each city
    for city in cities:
        params = {"q": city, "APPID": api_key, "units": "metric"}
        response = requests.get(f"{root_url}/{endpoint}", params=params)
        if response.status_code == 200:
            responses.append(response.json())

    # Push responses to the airflow context
    kwargs['ti'].xcom_push(key='weather_data', value=json.dumps(responses))
    


def format_response(response):
    """converts the weather data from the API
    response into a format compatible with aws DynamoDB.

    Parameters:
    responses - json: weather API response containing weather conditions

    """

    city = response.get("name")
    dt = str(response.get("dt"))
    latitude = str(response.get("coord").get("lat"))
    longitude = str(response.get("coord").get("lon"))
    weather = response.get("weather")[0].get("main")
    description = response.get("weather")[0].get("description")
    cloud_percentage = str(response.get("clouds").get("all"))
    temperature = str(response.get("main").get("temp"))
    feels_like = str(response.get("main").get("feels_like"))
    min_temp = str(response.get("main").get("temp_min"))
    max_temp = str(response.get("main").get("temp_max"))
    wind_speed = str(round(response.get("wind").get("speed") * 60 * 60 / 1000, 2))
    humidity = str(response.get("main").get("humidity"))

    item = {
        "name": {"S": city},
        "commune": {"S": city},
        "dt": {"N": dt},
        "latitude": {"S": latitude},
        "longitude": {"S": longitude},
        "weather": {"S": weather},
        "description": {"S": description},
        "cloud_pct": {"S": cloud_percentage},
        "temperature": {"S": temperature},
        "feels_like": {"S": feels_like},
        "min_temp": {"S": min_temp},
        "max_temp": {"S": max_temp},
        "wind_speed": {"N": wind_speed},
        "humidity": {"S": humidity},
    }
    return item


def push_data(**kwargs):
    """
    Accesses the weather data from the airflow context, transforms it and
    pushes it into the DynamoDB 'raw_weather_data' table.
    """

    # Get data from aiflow context
    ti = kwargs['ti']
    data_json = ti.xcom_pull(task_ids='get_data', key='weather_data')
    
    responses = json.loads(data_json)

    # Create client to connect to the table
    dynamo_client = boto3.client("dynamodb", region_name="us-west-2")

    for raw_item in responses:
        formated_item = format_response(raw_item) # transform the data in a format accepted by aws
        dynamo_client.put_item(TableName="raw_weather_data", Item=formated_item) # push item
    dynamo_client.close()


# airflow DAG

default_args = {
    'start_date': datetime(2025, 1, 1),
}

with DAG('weather_pipeline',  schedule=timedelta(minutes=5), default_args=default_args, catchup=False) as dag:

    get_data = PythonOperator(
        task_id = 'get_data',
        python_callable=get_weather_data,
        dag=dag
    )

    transform_load = PythonOperator(
        task_id='transform_load',
        python_callable=push_data,
        dag=dag
    )

    # Set task dependencies
    get_data >> transform_load

