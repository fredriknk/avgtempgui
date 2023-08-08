import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime, timedelta, date
import requests
import os
from requests.auth import HTTPBasicAuth
from tkinter import ttk
import json
import webbrowser
import re

location ="SN17850" #Ås
def make_client_id():
    def on_link_click(event):
        webbrowser.open_new("https://frost.met.no/howto.html")

    def on_create_file():
        client_id = client_id_entry.get()
        if not client_id:
            messagebox.showerror("Error", "Please enter a client ID.")
            return None

        with open("metno_client_id.txt", "w") as f:
            f.write(client_id)
        messagebox.showinfo("Success", "File created successfully.")
        root2.destroy()
        return client_id

    root2 = tk.Tk()
    root2.title("Metno Client ID")

    link = tk.Label(root2, text="Gå inn her:", fg="blue", cursor="hand2")
    link.pack()
    link.bind("<Button-1>", on_link_click)

    client_id_label = ttk.Label(root2, text="Lag en id, og skriv inn under:")
    client_id_label.pack()

    client_id_entry = ttk.Entry(root2)
    client_id_entry.pack()

    create_file_button = ttk.Button(root2, text="Create File", command=on_create_file)
    create_file_button.pack()

    root2.mainloop()

path = os.path.dirname(os.path.abspath(__file__))  # path of this file

try:
    id_file = os.path.join(path, 'metno_client_id.txt')
    with open(id_file, 'r') as f:
        client_id = f.read().strip()
except FileNotFoundError:
    print(id_file + ' not found, create one')
    client_id = make_client_id()

location = "SN17850"
location_name = "Ås"


def make_client_id():
    def on_link_click(event):
        webbrowser.open_new("https://frost.met.no/")

    def on_create_file():
        client_id = client_id_entry.get()
        if not client_id:
            messagebox.showerror("Error", "Please enter a client ID.")
            return

        with open("metno_client_id_2.txt", "w") as f:
            f.write(client_id)
        messagebox.showinfo("Success", "File created successfully.")
        root.destroy()

    root2 = tk.Tk()
    root2.title("Metno Client ID")

    link = tk.Label(root2, text="https://frost.met.no/", fg="blue", cursor="hand2")
    link.pack()
    link.bind("<Button-1>", on_link_click)

    client_id_label = ttk.Label(root2, text="Enter your client ID:")
    client_id_label.pack()

    client_id_entry = ttk.Entry(root2)
    client_id_entry.pack()

    create_file_button = ttk.Button(root2, text="Create File", command=on_create_file)
    create_file_button.pack()

    root2.mainloop()

def grad_date_time():
    """Retrieves the weather data for the selected date and time range and displays the average temperature"""
    if not client_id:
        messagebox.showerror("Error", "Client ID not found.")
        return

    selected_date = datetime.strptime(cal.get_date(), '%m/%d/%y')
    from_time = time_selector.get()
    to_time = time_selector_to.get()
    from_datetime = datetime.combine(selected_date, datetime.strptime(from_time, '%H:%M').time())
    to_datetime = datetime.combine(selected_date, datetime.strptime(to_time, '%H:%M').time())
    avg_temp = get_weather_data_average(client_id, location_label.cget("text"), from_datetime, to_datetime)
    put_to_clipboard(f"{avg_temp:.3f}")
    if avg_temp is None:
        output_text.config(text="No weather data available for the selected date and time.")
    else:
        output_text.config(text=f"The average temperature for the selected date and time is: {avg_temp:.3f}")


def get_weather_data_average(client_id, location, from_date, to_date):
    """Retrieves the weather data from the Met.no API for the given location and date and time range"""
    start_date = from_date.strftime("%Y-%m-%dT%H")
    end_date = to_date.strftime("%Y-%m-%dT%H")
    url = f"https://frost.met.no/observations/v0.jsonld?sources={location}&elements=air_temperature,wind_speed,precipitation_amount&referencetime={start_date}/{end_date}"
    try:
        response = requests.get(url, auth=HTTPBasicAuth(client_id, ''))
        if response.status_code != 200:
            raise ValueError(f"Error {response.status_code}: {response.reason}")
        data = response.json()

        temperature_values = [obs["observations"][0]["value"] for obs in data["data"] if obs["observations"]]
        if not temperature_values:
            return None
        avg_temp = sum(temperature_values) / len(temperature_values)
        return avg_temp
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while retrieving weather data: {e}")
        return None



def get_weather_data(client_id, location, from_date=datetime.now()-timedelta(days=2), to_date=datetime.now()-timedelta(days=1)):
    """Retrieves the weather data from the Met.no API for the given location and date and time range"""
    start_date = from_date.strftime("%Y-%m-%dT%H")
    end_date = to_date.strftime("%Y-%m-%dT%H")
    url = f"https://frost.met.no/observations/v0.jsonld?sources={location}&elements=precipitation_amount&referencetime={start_date}/{end_date}"
    try:
        response = requests.get(url, auth=HTTPBasicAuth(client_id, ''))
        if response.status_code != 200:
            raise ValueError(f"Error {response.status_code}: {response.reason}")
        data = response.json()
        return data
    except Exception as e:
        print("Error", f"An error occurred while retrieving weather data: {e}")
        messagebox.showerror("Error", f"An error occurred while retrieving weather data: {e}")
        return None



def get_available_elements(client_id):
    """Retrieve the metadata about Frost API elements"""
    url = "https://frost.met.no/elements/v0.jsonld"
    try:
        response = requests.get(url, auth=HTTPBasicAuth(client_id, ''))
        if response.status_code != 200:
            raise ValueError(f"Error {response.status_code}: {response.reason}")
        elements = response.json()
        return [element['id'] for element in elements['data']]
    except Exception as e:
        print("Error", f"An error occurred while retrieving elements: {e}")
        return None


def get_weather_stations(client_id, municipality):
    """Retrieves the list of weather stations from the Met.no API for the given municipality"""
    url = f'https://frost.met.no/sources/v0.jsonld?municipality={municipality}'
    response = requests.get(url, auth=HTTPBasicAuth(client_id, ''))
    data = json.loads(response.text)
    return data['data']

def get_elements_at_location(client_id, location):
    """Retrieve the available elements at a specific location using the Frost API"""
    # Get sources (stations) at the location
    url_sources = f"https://frost.met.no/sources/v0.jsonld?geometry={location}"
    try:
        response_sources = requests.get(url_sources, auth=HTTPBasicAuth(client_id, ''))
        response_sources.raise_for_status()
        sources = response_sources.json()

        # Extract the source IDs
        source_ids = [source['id'] for source in sources['data']]

        # Get the elements for each source
        elements = set()
        for source_id in source_ids:
            url_elements = f"https://frost.met.no/observations/availableTimeSeries/v0.jsonld?sources={source_id}"
            response_elements = requests.get(url_elements, auth=HTTPBasicAuth(client_id, ''))
            response_elements.raise_for_status()
            elements_data = response_elements.json()
            for element in elements_data['data']:
                elements.add(element['elementId'])

        return list(elements)

    except Exception as e:
        print("Error", f"An error occurred while retrieving elements at location: {e}")
        return None

def get_elements_at_location(client_id, location):
    """Retrieve the available elements at a specific location using the Frost API"""
    url_elements = f"https://frost.met.no/observations/availableTimeSeries/v0.jsonld?sources={location}"
    try:
        response_elements = requests.get(url_elements, auth=HTTPBasicAuth(client_id, ''))
        response_elements.raise_for_status()
        elements_data = response_elements.json()
        elements = [element['elementId'] for element in elements_data['data']]
        return elements, elements_data
    except Exception as e:
        print("Error", f"An error occurred while retrieving elements at location: {e}")
        return None



def get_request(client_id, url):
    """
    Retrieves the weather data for the given elements, location, and date and time range
    from the Met.no API
    """
    try:
        response = requests.get(url, auth=HTTPBasicAuth(client_id, ''))
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print("Error", f"An error occurred while retrieving weather data: {e}")
        return None
def replace_referencetime(url, from_date, to_date):
    new_referencetime = f"&referencetime={from_date}/{to_date}"
    return re.sub(r'&referencetime=[^&]*', new_referencetime, url)

elements = ["air_temperature","air_pressure_at_sea_level","min(air_temperature PT1H)","max(air_temperature PT1H)","dew_point_temperature PT1H","specific_humidity PT1H","min(grass_temperature PT1H","mean(volume_fraction_of_water_in_soil PT1H)","wind_speed PT1H","max(wind_speed PT1H)","precipitation_amount P1D"]
elements = ["sum(precipitation_amount PT1H)","relative_humidity","air_temperature"]
# Example usage:
# elements,data = get_available_elements(client_id)
#print(elements)
# elements2,avaliable = get_elements_at_location(client_id,location)
#print(elements2)

url = "https://frost.met.no/observations/v0.jsonld?sources=SN17850&referencetime=2023-01-04T12%3A00%3A00.000Z&elements=water_vapor_partial_pressure_in_air"

from_date = "2023-04-01T12%3A00%3A00.000Z"
to_date = "2023-04-08T12%3A00%3A00.000Z"

url = "https://frost.met.no/observations/v0.jsonld?sources=SN17850:0&referencetime=1944-05-01T00:00:00.000Z/9999-12-31T23:59:59Z&elements=mean(water_vapor_partial_pressure_in_air P1D)&timeoffsets=PT0H&timeresolutions=P1D&timeseriesids=0&performancecategories=C&exposurecategories=2"
data = get_weather(client_id,replace_referencetime(url, from_date, to_date))

url =  "uri": "https://frost.met.no/observations/v0.jsonld?sources=SN17850:0&referencetime=2015-09-21T00:00:00.000Z/9999-12-31T23:59:59Z&elements=mean(air_temperature P1D)&timeoffsets=PT0H&timeresolutions=P1D&timeseriesids=0&performancecategories=C&exposurecategories=1&levels=2.0"
data = get_weather(client_id,replace_referencetime(url, from_date, to_date))

url = "https://frost.met.no/observations/v0.jsonld?sources=SN17850:0&referencetime=2015-09-21T00:00:00.000Z/9999-12-31T23:59:59Z&elements=mean(relative_humidity P1D)&timeoffsets=PT0H&timeresolutions=P1D&timeseriesids=0&performancecategories=C&exposurecategories=1&levels=2.0"
data = get_weather(client_id,replace_referencetime(url, from_date, to_date))

url = "uri": "https://frost.met.no/observations/v0.jsonld?sources=SN17850:0&referencetime=2020-12-02T00:00:00.000Z/9999-12-31T23:59:59Z&elements=mean(soil_temperature P1D)&timeoffsets=PT0H&timeresolutions=P1D&timeseriesids=0&performancecategories=C&exposurecategories=2&levels=10.0"
data = get_weather(client_id,replace_referencetime(url, from_date, to_date))

for type in data["data"]:
    print(type["elementId"] )
    print("\n")
    if not 'validTo' in type.keys():
        print(type["elementId"])