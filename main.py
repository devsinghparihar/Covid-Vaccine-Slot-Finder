import requests
import json
import datetime
import eel
# initialzing eel
eel.init('web')

# initialzing prequistes
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',}
# for getting next 7 days --------------------------------------------------
numdays = 7
base = datetime.datetime.today()
date_list = [base + datetime.timedelta(days=x) for x in range(numdays)]
date_str = [x.strftime("%d-%m-%Y") for x in date_list]
# --------------------------------------------------------------------------

@eel.expose
def starter(pincode1 ,age1):
    extracter(pincode1, age1)
@eel.expose
def extracter(pincode, age):
    data = []
    for INP_DATE in date_str:
        url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pincode}&date={INP_DATE}"
        response = requests.get(url, headers=headers)
        if response.ok:
            resp_json = response.json()
            if resp_json["centers"]:
                data.append("Available on: {}".format(INP_DATE))
                data.append("\n")

                for center in resp_json["centers"]:
                    for session in center["sessions"]:
                        if session["min_age_limit"] <= age:
                            data.append("Center: ")
                            data.append(center["name"])
                            data.append("\n")
                            data.append("Block name: ")
                            data.append(center["block_name"])
                            data.append("\n")

                            data.append("Price: ")
                            data.append(center["fee_type"])
                            data.append("\n")

                            data.append("Available Capacity: ")
                            data.append(session["available_capacity"])
                            data.append("\n")
                            if (session["vaccine"] != ''):
                                data.append("Vaccine Name: ")
                                data.append(session["vaccine"])
                                data.append("\n")


                            data.append("\n\n")

            else:

                data.append("No available slots on {}".format(INP_DATE))
                data.append("\n")

    dataString = ''.join(str(e) for e in data)
    eel.currentStatus(dataString)



if __name__ == '__main__':
    eel.start('index.html', size=(1280, 768))