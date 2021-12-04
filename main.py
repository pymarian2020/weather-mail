import requests
import smtplib
import os


# Coordinates of your location
latitude = 52.5200
longitude = 10.4515
#Api key for openweathermap.org
api_key = os.environ.get("API_AUTH_KEY")

parameters = {
    "appid": api_key,
    "lat": latitude,
    "lon": longitude,
    "exclude": "minutely,daily,current",
    "units": "metric",
}

response = requests.get("https://api.openweathermap.org/data/2.5/onecall", params=parameters)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]
will_rain = False
for hour_data in weather_slice:
    condition_code = int(hour_data["weather"][0]["id"])
    if condition_code < 700:
        will_rain = True

if will_rain:
    sender_email = os.environ.get("EMAIL")
    password = "sender_email_password"
    receiver_email = "your_mail@gmail.com"

    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email,
                        msg=f"Subject: Its going to rain!")
