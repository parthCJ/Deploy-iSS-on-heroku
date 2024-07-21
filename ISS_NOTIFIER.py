import requests
from datetime import datetime
import smtplib
import time

to_address = "your address"
from_address = "your adress"
MY_PASSWORD = "fghffcvfgfccv"
MY_LAT = 4891177 # Your latitude
MY_LONG = 3300726 # Your longitude

def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    #Your position is within +5 or -5 degrees of the iss position.
    if (MY_LAT-5) <= iss_latitude <= (MY_LAT+5) and (MY_LONG-5) <= iss_longitude <= (MY_LONG+5):
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
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True

while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        connection = smtplib.SMTP_SSL("smtp.gmail.com", port=465)
try:
    connection.login(to_address, MY_PASSWORD)
    connection.sendmail(
        from_addr=from_address,
        to_addrs=to_address,
        msg="Subject:Look Up \n\nThe ISS is above you in the sky."
    )
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
finally:
    connection.quit()

