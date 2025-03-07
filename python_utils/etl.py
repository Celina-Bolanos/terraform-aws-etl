import requests
import boto3
import time


def get_weather_data():
    """
    Fetches weather information for ten belgian cities
    Returns a list of dictionaries with the weather conditions for each location
    """

    root_url = "https://api.openweathermap.org"
    endpoint = "data/2.5/weather"
    api_key = "YOU API GOES HERE"
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

    for city in cities:
        params = {"q": city, "APPID": api_key, "units": "metric"}
        response = requests.get(f"{root_url}/{endpoint}", params=params)
        if response.status_code == 200:
            responses.append(response.json())

    return responses


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


def push_data(responses):
    """
    Pushes formated data into the DynamoDB 'raw_weather_data' table

    Parameters
    table_name -str: name of the target table
    responses - list of api responses to be pushed to the table
    """

    dynamo_client = boto3.client("dynamodb", region_name="us-west-2")

    for raw_item in responses:
        formated_item = format_response(raw_item)
        dynamo_client.put_item(TableName="raw_weather_data", Item=formated_item)
    dynamo_client.close()


if __name__ == "__main__":
    i = 0
    while i <= 10: # Optinally change to "while True" to make it run constantly every 5 mins
        api_responses = get_weather_data()
        push_data(api_responses)
        i += 1
        print(f"Added data {i} time(s).")
        time.sleep(500)
