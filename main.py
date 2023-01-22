import requests
import datetime as dt
import os

NUTRITIONIX_APP_ID = os.environ["NUTRITIONIX_APP_ID"]
NUTRITIONIX_APP_KEY = os.environ["NUTRITIONIX_APP_KEY"]
NUTRITIONIX_API_URL = "https://trackapi.nutritionix.com"
EXERCISE_ENDPOINT = f"{NUTRITIONIX_API_URL}/v2/natural/exercise"
SHEETY_ENDPOINT = "https://api.sheety.co/60014b6b16339df255298504d4b57e49/myWorkouts/workouts"
SHEETY_KEY = os.environ["SHEETY_KEY"]

GENDER = "male"
WEIGHT = 70.0
HEIGHT = 180.0
AGE = 50

def exercise_data(user_input):
    headers = {
        "x-app-id": NUTRITIONIX_APP_ID,
        "x-app-key": NUTRITIONIX_APP_KEY,
        "x-remote-user-id": "0",
        "Content-Type": "application/json"
    }
    data = {
        "query": user_input,
        "gender": GENDER,
        "weight_kg": WEIGHT,
        "height_cm": HEIGHT,
        "age": AGE
    }
    response = requests.post(url=EXERCISE_ENDPOINT, json=data, headers=headers)
    response.raise_for_status()
    print(response.json())
    return response.json()["exercises"]

def post_exercise(exercises):
    headers = {
        "Authorization": SHEETY_KEY,
        "Content-Type": "application/json"
    }

    workout_date = dt.datetime.today().strftime("%d/%m/%Y")
    workout_time = dt.datetime.now().strftime("%X")

    for exercise in exercises:
        print(f"Name: {exercise['name']}\n"
              f"Duration: {exercise['duration_min']}\n"
              f"Calories: {exercise['nf_calories']}")
        data = {
            "workout":
                {
                    "date": workout_date,
                    "time": workout_time,
                    "exercise": exercise['name'].title(),
                    "duration": exercise['duration_min'],
                    "calories": exercise['nf_calories']
                }
        }

        response = requests.post(url=SHEETY_ENDPOINT, json=data, headers=headers)
        response.raise_for_status()
        print(response.text)


user_input = input("Tell me which exercise did you do? ")
exercises = exercise_data(user_input)
post_exercise(exercises)
