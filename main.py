import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 40.379589 #ENTER YOUR LATITUDE HERE
MY_LONG = -3.706790 #ENTER YOUR LONGITUDE HERE
MY_EMAIL = "ENTER YOUR EMAIL HERE"
MY_PASSWORD = "ENTER YOUR PASSWORD HERE"
SEND_TO = "ENTER EMAIL ADDRESS YOU'RE SENDING THIS TO"


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if iss_longitude in range(int(MY_LONG) - 5, int(MY_LONG) + 5) and iss_latitude in range(int(MY_LAT - 5),
                                                                                            int(MY_LAT) + 5):
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0]) + 1 #ALTER FINAL NUMBER DEPENDING ON TIMEZONE. DEFAULT IS UTC
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0]) + 1 #ALTER FINAL NUMBER DEPENDING ON TIMEZONE. DEFAULT IS UTC

    time_now = datetime.now()

    if time_now.hour >= sunset or time_now.hour <= sunrise:
        return True


is_iss_overhead()
is_night()

while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        with smtplib.SMTP("ENTER SMTP ADDRESS HERE") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=SEND_TO,
                msg="Subject:It's time!\n\nLook up now! 👆👆"
            )

