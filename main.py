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


def get_weather_data_average(api_key, location, from_date, to_date):
    """Retrieves the weather data from the Met.no API for the given location and date and time range"""
    start_date = from_date.strftime("%Y-%m-%dT%H")
    end_date = to_date.strftime("%Y-%m-%dT%H")
    url = f"https://frost.met.no/observations/v0.jsonld?sources={location}&elements=air_temperature,wind_speed,precipitation_amount&referencetime={start_date}/{end_date}"
    try:
        response = requests.get(url, auth=HTTPBasicAuth(api_key, ''))
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


def on_select_station(event):
    """Handles the event when a weather station is selected from the list"""
    w = event.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    print(value)
    station_id, station_name, station_type = value.split("   |   ")
    location_label.config(text=station_id)
    location_label_name.config(text=station_name)


def put_to_clipboard(value):
    root = tk.Tk()
    root.withdraw()
    root.clipboard_clear()
    root.clipboard_append(value)
    root.update()
    root.destroy()


def search_stations():
    """Searches for weather stations by municipality and displays the results in a list"""
    municipality = municipality_entry.get()
    if not municipality:
        messagebox.showerror("Error", "Please enter a municipality name.")
        return
    try:
        stations = get_weather_stations(client_id, municipality)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while searching for weather stations: {e}")
        return

    if not stations:
        messagebox.showerror("Error", f"No weather stations found for municipality {municipality}.")
        return

    station_list.delete(0, tk.END)

    for station in stations:
        station_list.insert(tk.END, f"{station['id']}   |   {station['name']}   |   ({station['@type']})")


def get_weather_stations(api_key, municipality):
    """Retrieves the list of weather stations from the Met.no API for the given municipality"""
    url = f'https://frost.met.no/sources/v0.jsonld?municipality={municipality}'
    response = requests.get(url, auth=HTTPBasicAuth(api_key, ''))
    data = json.loads(response.text)
    return data['data']

# GUI code here
root = tk.Tk()

location_label = tk.Label(root)
location_label.grid(row=1, column=0, padx=10, pady=10)
location_label.config(text=location)

location_label_name = tk.Label(root)
location_label_name.grid(row=1, column=1, padx=10, pady=10)
location_label_name.config(text=location_name)

startdate = datetime.today() - timedelta(days=2)
cal = Calendar(root, selectmode='day', year=startdate.year, month=startdate.month, day=startdate.day)
cal.grid(row=1, column=0, rowspan=3,columnspan = 2, padx=10, pady=10)

time_selector = tk.ttk.Combobox(root, values=[f"{i:02d}:00" for i in range(24)])
time_selector.grid(row=1, column=3, padx=10, pady=10)
time_selector.current(11)

time_selector_to = tk.ttk.Combobox(root, values=[f"{i:02d}:00" for i in range(24)])
time_selector_to.grid(row=1, column=4, padx=10, pady=10)
time_selector_to.current(14)

municipality_entry = tk.Entry(root)
municipality_entry.grid(row=2, column=3, padx=10, pady=10)

search_button = tk.Button(root, text="Search", command=search_stations)
search_button.grid(row=2, column=4, padx=10, pady=10)

station_list = tk.Listbox(root, width=50)
station_list.grid(row=3, column=3, columnspan=2, padx=10, pady=10)
station_list.bind('<<ListboxSelect>>', on_select_station)

search_button = tk.Button(root, text="Get avgtemp", command=grad_date_time)
search_button.grid(row=5, column=0, padx=10, pady=10)

output_text = tk.Label(root)
output_text.grid(row=6, column=0,columnspan=4, padx=10, pady=10)

root.mainloop()
