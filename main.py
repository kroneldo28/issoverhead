import requests
from datetime import datetime
import smtplib
import time


CITY = "Douala"
MY_LAT = 4.051056
MY_LONG = 9.767869
MY_EMAIL = "ronel.dev@yahoo.com"
with open("password.txt") as password:
    my_password = password.read()

to_email = "kouakep.dev@gmail.com"
subject_mail = "Subject:ISS in the sky [Look up 👆🏾]\n\n"
message = f"Look up in the sky. The Iss is over your head in {CITY}"
signature = "\nSent with python.\nRonel"


# Your position is within +5 or -5 degrees of the ISS position.
def iss_near_me():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    return MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5


def is_nighttime():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now()
    return time_now.hour <= sunrise or time_now.hour >= sunset


# If the ISS is close to my current position
while True:
    # BONUS: run the code every 60 seconds
    time.sleep(60)
    if iss_near_me() and is_nighttime():
        with smtplib.SMTP("smtp.mail.yahoo.com", 587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=my_password)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=to_email, msg=subject_mail + message + signature)
