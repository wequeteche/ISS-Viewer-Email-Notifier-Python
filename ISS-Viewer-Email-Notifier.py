# Importing dependencies
import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 0.868230
MY_LONG = 35.122662
MY_GMAIL = "....@gmail.com"
MY_PASSWORD = "...."


# --------------ISS Position vs Local Time----------#
# Iss Current Position
def iss_overhead():
    global MY_LAT, MY_LONG
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    iss_position = response.json()["iss_position"]
    latitude = float(iss_position["latitude"])
    longitude = float(iss_position["longitude"])

    if MY_LAT - 5 <= latitude <= MY_LAT + 5 and MY_LONG - 5 <= longitude <= MY_LONG + 5:
        return True


# Local hour time
hour_time = int(datetime.now().hour)

# local sunrise & sunset time
parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}
response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

run = True
while run:
    if hour_time < sunrise or hour_time > sunset:
        # ----------------Email notification---------------------#
        send_mail = iss_overhead()
        while send_mail:
            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(user=MY_GMAIL, password=MY_PASSWORD)
                connection.sendmail(from_addr=MY_GMAIL,
                                    to_addrs=".....@gmail.com",
                                    msg="Subject:LOOK UP!\n\nInternational Space Station is overhead")
            time.sleep(60)
            send_mail = iss_overhead()
