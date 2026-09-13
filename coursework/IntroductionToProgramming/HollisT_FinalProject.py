# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Course: DSC510
# Week: 11
# Assignment: Final Project
# Author: Tim Hollis
# Date: 11/20/2025
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Data Source: OpenWeather API (https://openweathermap.org/api)

# Dependencies:
#    - Python 3
#    - requests library (install with: pip install requests)
#    - Tkinter (included with Python standard library)

# Setup Instructions:
#    1. Get an API key from OpenWeatherMap (https://openweathermap.org/api)
#    2. Replace 'YOUR_API_KEY_HERE' in the code with your actual API key
#    3. Install dependencies: pip install requests
#    4. Run the program: python HollisT_FinalProject.py

# Usage:
#    - Enter either a city/state or ZIP code,
#    - select units, and click the appropriate lookup button. Weather results
#    - will be displayed in a popup window.

# Important Notes:
#    - API key is REQUIRED from OpenWeather (free tier available)
#    - One Call 3.0 API requires credit card registration even for free tier
#    - Program is US-only and requires a 2-letter state code for city lookups
#    - Input validation ensures proper city, state, and ZIP formats
#    - Exception handling provides user-friendly error messages
#    - State must be 2-letter code (e.g., "CA", "NY", "TX")
#    - ZIP code must be exactly 5 digits

# API Key Configuration:
#    - Replace 'YOUR_API_KEY_HERE' on line 46 with your actual OpenWeather API
#    key


import tkinter as tk
from tkinter import ttk, messagebox
import requests
import datetime

API_KEY = 'YOUR_API_KEY_HERE' # Replace with your actual OpenWeather API key
BASE_GEO_DIRECT = 'https://api.openweathermap.org/geo/1.0/direct'
BASE_GEO_ZIP = 'https://api.openweathermap.org/geo/1.0/zip'
BASE_GEO_REVERSE = 'https://api.openweathermap.org/geo/1.0/reverse'
BASE_ONECALL = 'https://api.openweathermap.org/data/3.0/onecall'
BASE_ONECALL_OVERVIEW = 'https://api.openweathermap.org/data/3.0/onecall/overview'
US_COUNTRY_CODE = 'US'


# ------------------ API Functions ------------------

def get_lat_lon_by_city_state(city, state):
    """Perform GEO direct lookup for city + state in the US."""
    params = {
        'q': f'{city},{state},{US_COUNTRY_CODE}',
        'limit': 1,
        'appid': API_KEY,
    }
    try:
        resp = requests.get(BASE_GEO_DIRECT, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if not data:
            messagebox.showerror(
                'Error', f'No results found for {city}, {state}. Please check spelling.')
            return None

        item = data[0]
        lat = float(item['lat'])
        lon = float(item['lon'])
        api_city = item.get('name', '').title()
        api_state = item.get('state', state).upper()

        if api_city.lower() != city.lower():
            messagebox.showinfo(
                'Notice', f'The city you entered was changed to: {api_city}, {api_state}')

        resolved = f"{api_city}, {api_state}"
        return lat, lon, resolved

    except requests.exceptions.HTTPError as e:
        messagebox.showerror('API Error', f'HTTP error occurred: {e}')
        return None
    except requests.exceptions.ConnectionError:
        messagebox.showerror(
            'Network Error',
            'Unable to connect to weather service.\nPlease check your internet connection.')
        return None
    except requests.exceptions.Timeout:
        messagebox.showerror(
            'Timeout',
            'The request timed out. Service might be slow.')
        return None
    except requests.exceptions.RequestException as e:
        messagebox.showerror('Request Error',
                             f'An error occurred with the request: {e}')
        return None
    except Exception as e:
        messagebox.showerror('Error', f'Unexpected error: {e}')
        return None


def get_lat_lon_by_zip(zip_code):
    """Perform GEO lookup for US ZIP code and get state information."""
    params = {
        'zip': f'{zip_code},{US_COUNTRY_CODE}',
        'appid': API_KEY,
    }
    try:
        resp = requests.get(BASE_GEO_ZIP, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        lat = float(data['lat'])
        lon = float(data['lon'])
        city_name = data.get('name', 'Unknown').title()

        # Reverse Geo call to get the state code
        reverse_params = {
            'lat': lat,
            'lon': lon,
            'limit': 1,
            'appid': API_KEY
        }
        reverse_resp = requests.get(
            BASE_GEO_REVERSE,
            params=reverse_params,
            timeout=10)
        reverse_resp.raise_for_status()
        reverse_data = reverse_resp.json()

        if reverse_data:
            location_info = reverse_data[0]
            state_code = location_info.get('state', '')
            location_name = f"{city_name}, {state_code}" if state_code else f"{city_name}, US"
        else:
            location_name = f"{city_name}, US"

        return lat, lon, location_name

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            messagebox.showerror(
                'Not Found', f'ZIP code {zip_code} not found.')
        else:
            messagebox.showerror('API Error', f'HTTP error: {e}')
        return None
    except requests.exceptions.ConnectionError:
        messagebox.showerror('Network Error',
                             'Unable to connect to weather service.')
        return None
    except requests.exceptions.Timeout:
        messagebox.showerror('Timeout', 'The request timed out.')
        return None
    except requests.exceptions.RequestException as e:
        messagebox.showerror('Request Error', f'Request failed: {e}')
        return None
    except Exception as e:
        messagebox.showerror('Error', f'Unexpected error: {e}')
        return None


def get_weather(lat, lon, units):
    """Fetch current weather using One Call API."""
    params = {
        'lat': lat,
        'lon': lon,
        'exclude': 'minutely,hourly,alerts',
        'appid': API_KEY,
    }
    if units in {'imperial', 'metric'}:
        params['units'] = units

    try:
        resp = requests.get(BASE_ONECALL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        current = data.get('current', {})
        daily = data.get('daily', [])
        today = daily[0] if daily else {}

        return {
            'temp': current.get('temp'),
            'pressure': current.get('pressure'),
            'humidity': current.get('humidity'),
            'clouds': current.get('clouds'),
            'desc': current.get('weather', [{}])[0].get('description', 'N/A'),
            'high': today.get('temp', {}).get('max', 'N/A'),
            'low': today.get('temp', {}).get('min', 'N/A'),
            'rain_chance': int(today.get('pop', 0) * 100),
        }
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            messagebox.showerror(
                'Authorization Error', 'API Key Error: 401 Unauthorized.\n\n'
                'NOTE: The "One Call 3.0" API requires a subscription '
                '(credit card on file) even for the free tier.\n'
                'Please check the API Key permissions.')
        else:
            messagebox.showerror('API Error', f'Weather lookup failed: {e}')
        return None
    except requests.exceptions.ConnectionError:
        messagebox.showerror(
            'Network Error',
            'Check your internet connection.')
        return None
    except requests.exceptions.Timeout:
        messagebox.showerror('Timeout', 'Weather request timed out.')
        return None
    except requests.exceptions.RequestException as e:
        messagebox.showerror('Request Error', f'Error fetching weather: {e}')
        return None
    except Exception as e:
        messagebox.showerror('Error', f'Unexpected error: {e}')
        return None


def get_weather_overview(lat, lon, units):
    """Fetch AI-generated weather overview for today."""
    params = {
        'lat': lat,
        'lon': lon,
        'appid': API_KEY,
    }
    if units in {'imperial', 'metric'}:
        params['units'] = units

    try:
        resp = requests.get(BASE_ONECALL_OVERVIEW, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        return {
            'date': data.get('date', 'N/A'),
            'overview': data.get('weather_overview', 'No overview available.'),
            'units': data.get('units', 'N/A')
        }
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            messagebox.showerror(
                'Authorization Error',
                'One Call Overview 3.0 requires a valid subscription.')
        else:
            messagebox.showerror('API Error', f'Overview lookup failed: {e}')
        return None
    except requests.exceptions.ConnectionError:
        messagebox.showerror(
            'Network Error',
            'Could not connect for AI Overview.')
        return None
    except requests.exceptions.Timeout:
        messagebox.showerror('Timeout', 'Overview request timed out.')
        return None
    except Exception as e:
        # Non-critical failure: just log to console or ignore so main weather
        # still shows
        print(f"Overview failed: {e}")
        return None


def get_forecast(lat, lon, units):
    """Fetch 7-day forecast with highs, lows, and chance of rain."""
    params = {
        'lat': lat,
        'lon': lon,
        'exclude': 'minutely,hourly,alerts',
        'appid': API_KEY,
    }
    if units in {'imperial', 'metric'}:
        params['units'] = units

    try:
        resp = requests.get(BASE_ONECALL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        daily = data.get('daily', [])

        forecast = []
        for day in daily[:7]:
            forecast.append({
                'date': day.get('dt'),
                'high': day.get('temp', {}).get('max', 'N/A'),
                'low': day.get('temp', {}).get('min', 'N/A'),
                'rain_chance': int(day.get('pop', 0) * 100),
                'desc': day.get('weather', [{}])[0].get('description', 'N/A')
            })
        return forecast
    except requests.exceptions.RequestException as e:
        # If main weather loaded but forecast fails, just show error
        messagebox.showerror(
            'Forecast Error',
            f'Could not retrieve forecast: {e}')
        return None
    except Exception as e:
        messagebox.showerror('Error', f'Forecast parsing failed: {e}')
        return None

# ------------------ Display Functions ------------------


def show_weather(location, units, weather, overview_data=None, forecast=None):
    """Display weather report in a popup window."""
    unit_label = {'imperial': '°F', 'metric': '°C', 'kelvin': 'K'}[units]

    # Base daily report

    report = (
        f'Location: {location}\n'
        f'Conditions: {weather["desc"].title()}\n'
        f'Current Temp: {weather["temp"]}{unit_label}\n'
        f'High: {weather["high"]}{unit_label}\n'
        f'Low: {weather["low"]}{unit_label}\n'
        f'Pressure: {weather["pressure"]} hPa\n'
        f'Humidity: {weather["humidity"]}%\n'
        f'Clouds: {weather["clouds"]}%\n'
        f'Chance of Rain: {weather["rain_chance"]}%\n'
    )

    # Overview section (long text, should wrap)

    overview_text = None
    if overview_data:
        overview_text = overview_data['overview']

    # Forecast section (short lines, no wrapping, with colored symbols)

    forecast_lines = None
    if forecast:
        symbol_map = {
            "Clear Sky": ("☀", "sun"),
            "Sunny": ("☀", "sun"),
            "Few Clouds": ("☁", "cloud"),
            "Scattered Clouds": ("☁", "cloud"),
            "Broken Clouds": ("☁", "cloud"),
            "Overcast": ("☁", "cloud"),
            "Light Rain": ("☂", "rain"),
            "Moderate Rain": ("☂", "rain"),
            "Heavy Rain": ("⛆", "rain"),
            "Thunderstorm": ("⚡", "storm"),
            "Snow": ("❄", "snow"),
            "Sleet": ("❄", "snow"),
            "Fog": ("🌫", "fog"),
            "Mist": ("🌫", "fog"),
        }

        forecast_lines = []
        for day in forecast:
            date_str = datetime.datetime.fromtimestamp(
                day['date']).strftime('%a %b %d')
            desc = day['desc'].title()
            symbol, tag = symbol_map.get(desc, ("•", "default"))
            line_text = (
                f"{date_str}: {symbol} {desc}, "
                f"High {day['high']}{unit_label}, "
                f"Low {day['low']}{unit_label}, "
                f"Rain {day['rain_chance']}%"
            )
            forecast_lines.append((line_text, tag))

    # Pass sections separately to popup

    show_weather_popup(report, overview_text, forecast_lines)


def show_weather_popup(report, overview_text=None, forecast_lines=None):
    """Popup window with dynamic sizing based on content."""
    popup = tk.Toplevel(root)
    popup.title("Weather Report")
    popup.configure(bg="#f5f5f5")

    # Dynamic sizing based on content

    has_overview = overview_text is not None
    has_forecast = forecast_lines is not None

    if has_overview and has_forecast:
        # All three sections - full size
        popup.geometry("750x550")
    elif has_overview or has_forecast:
        # Two sections - medium size
        popup.geometry("750x450")
    else:
        # Only daily summary - compact size
        popup.geometry("400x300")

    # Main container that will hold everything

    main_container = ttk.Frame(popup)
    main_container.pack(fill="both", expand=True, padx=15, pady=10)

    # Handle case with only daily summary (no overview, no forecast)

    if not has_overview and not has_forecast:
        summary_header = tk.Label(
            main_container,
            text="🌤️ Daily Summary",
            font=("Calibri", 12, "bold"),
            bg="#d0ebff",
            anchor="w"
        )
        summary_header.pack(fill="x", pady=(0, 5))

        daily_label = tk.Label(
            main_container,
            text=report,
            font=("Calibri", 11),
            bg="#f5f5f5",
            justify="left",
            anchor="nw"
        )
        daily_label.pack(fill="both", expand=True)

        # Close button at bottom

        close_btn = ttk.Button(
            main_container,
            text="Close",
            command=popup.destroy)
        close_btn.pack(pady=15)
        return

    # Handle cases with overview and/or forecast

    if has_overview:
        # Side-by-side layout for overview cases

        top_frame = ttk.Frame(main_container)
        top_frame.pack(fill="both", expand=True)

        # Daily summary (left column)

        summary_header = tk.Label(
            top_frame,
            text="🌤️ Daily Summary",
            font=("Calibri", 12, "bold"),
            bg="#d0ebff",
            anchor="w"
        )
        summary_header.grid(row=0, column=0, sticky="w", pady=(0, 5))

        daily_label = tk.Label(
            top_frame,
            text=report,
            font=("Calibri", 11),
            bg="#f5f5f5",
            justify="left",
            anchor="nw",
            wraplength=320
        )
        daily_label.grid(row=1, column=0, sticky="nw", padx=(0, 10))

        # Overview (right column)

        overview_header = tk.Label(
            top_frame,
            text="📖 Weather Overview",
            font=("Calibri", 12, "bold"),
            bg="#fff3bf",
            anchor="w"
        )
        overview_header.grid(row=0, column=1, sticky="w", pady=(0, 5))

        overview_label = tk.Label(
            top_frame,
            text=overview_text,
            font=("Calibri", 11),
            bg="#f5f5f5",
            justify="left",
            anchor="nw",
            wraplength=320
        )
        overview_label.grid(row=1, column=1, sticky="nw")

        top_frame.columnconfigure(0, weight=1)
        top_frame.columnconfigure(1, weight=1)
        top_frame.rowconfigure(1, weight=1)

    else:
        # Only daily summary but with forecast coming - single centered box

        summary_header = tk.Label(
            main_container,
            text="🌤️ Daily Summary",
            font=("Calibri", 12, "bold"),
            bg="#d0ebff",
            anchor="w"
        )
        summary_header.pack(fill="x", pady=(0, 5))

        daily_label = tk.Label(
            main_container,
            text=report,
            font=("Calibri", 11),
            bg="#f5f5f5",
            justify="left",
            anchor="nw"
        )
        daily_label.pack(fill="both", expand=True)

    # Forecast section (if requested)

    if has_forecast:
        separator = ttk.Separator(main_container, orient="horizontal")
        separator.pack(fill="x", pady=15)

        forecast_header = tk.Label(
            main_container,
            text="📅 7-Day Forecast",
            font=("Calibri", 12, "bold"),
            bg="#d3f9d8",
            anchor="w"
        )
        forecast_header.pack(fill="x", pady=(0, 5))

        forecast_box = tk.Text(
            main_container,
            wrap="none",
            font=("Calibri", 11),
            bg="#f5f5f5",
            height=8,
            width=90
        )
        forecast_box.pack(pady=5, anchor="n")

        # Define tag colors for condition symbols

        forecast_box.tag_configure("sun", foreground="#E67E22")  # orange
        forecast_box.tag_configure("cloud", foreground="#5C6B73")  # slate gray
        forecast_box.tag_configure("rain", foreground="#1E88E5")  # blue
        forecast_box.tag_configure("storm", foreground="#8E24AA")  # purple
        forecast_box.tag_configure("snow", foreground="#00ACC1")  # teal
        forecast_box.tag_configure("fog", foreground="#7A7A7A")  # medium gray
        forecast_box.tag_configure("default", foreground="#333333")  # dark

        # Insert each forecast line separately with newline

        for line_text, tag in forecast_lines:
            forecast_box.insert("end", line_text + "\n", tag)

        forecast_box.config(state="disabled")

    # Close button - always at the bottom

    close_btn = ttk.Button(main_container, text="Close", command=popup.destroy)
    close_btn.pack(pady=15)


# ------------------ GUI Workflow ------------------

def lookup_city():
    """Handle city/state lookup workflow with tailored error messages."""
    city = city_entry.get().strip()
    state = state_entry.get().strip().upper()
    units = unit_var.get()

    if not city and state:
        messagebox.showerror(
            'Error', 'You must enter a city name when searching by city.')
        city_entry.focus_set()
        return
    if city and not state:
        messagebox.showerror(
            'Error',
            'You must enter a 2-letter state code when searching by city.')
        state_entry.focus_set()
        return
    if not city and not state:
        messagebox.showerror(
            'Error', 'You must enter both a city and a state.')
        city_entry.focus_set()
        return
    if city.isdigit():
        messagebox.showerror(
            'Error',
            'It looks like you entered a ZIP code. Please use the ZIP Lookup option instead.'
        )
        zip_entry.focus_set()
        return
    if len(state) != 2 or not state.isalpha():
        messagebox.showerror(
            'Error',
            'State must be a valid 2-letter code (e.g., TX, CA).'
        )
        state_entry.focus_set()
        return

    coords = get_lat_lon_by_city_state(city, state)
    if coords:
        lat, lon, name = coords
        weather = get_weather(lat, lon, units)
        if weather:
            overview_data = None
            forecast = None
            if city_overview_var.get():  # AI overview checkbox
                overview_data = get_weather_overview(lat, lon, units)
            if city_forecast_var.get():  # 7-day forecast checkbox
                forecast = get_forecast(lat, lon, units)
            show_weather(name, units, weather, overview_data, forecast)
            status_var.set(f'Weather retrieved for {name}')


def lookup_zip():
    """Handle ZIP code lookup workflow with tailored error messages."""
    zip_code = zip_entry.get().strip()
    units = unit_var.get()

    if not zip_code:
        messagebox.showerror(
            'Error', 'You must enter a ZIP code when using ZIP Lookup.')
        zip_entry.focus_set()
        return
    if not zip_code.isdigit() or len(zip_code) != 5:
        messagebox.showerror('Error', 'ZIP code must be exactly 5 digits.')
        zip_entry.focus_set()
        return

    coords = get_lat_lon_by_zip(zip_code)
    if coords:
        lat, lon, name = coords
        weather = get_weather(lat, lon, units)
        if weather:
            overview_data = None
            forecast = None
            if zip_overview_var.get():  # AI overview checkbox
                overview_data = get_weather_overview(lat, lon, units)
            if zip_forecast_var.get():  # 7-day forecast checkbox
                forecast = get_forecast(lat, lon, units)
            show_weather(name, units, weather, overview_data, forecast)
            status_var.set(f'Weather retrieved for {name}')


def exit_program():
    """Exit the program gracefully with a farewell message that auto-closes."""
    goodbye_window = tk.Toplevel(root)
    goodbye_window.title("Goodbye")
    goodbye_window.geometry("300x120")
    goodbye_window.configure(bg='#f0f8ff')
    goodbye_window.update_idletasks()
    x = root.winfo_x() + (root.winfo_width() - 300) // 2
    y = root.winfo_y() + (root.winfo_height() - 120) // 2
    goodbye_window.geometry(f"300x120+{x}+{y}")
    label = ttk.Label(
        goodbye_window,
        text="Thanks for using\nThe Weather Program!\nBye for now!",
        font=('Calibri', 12),
        justify='center',
        background='#f0f8ff'
    )
    label.pack(expand=True, pady=25)
    goodbye_window.deiconify()
    goodbye_window.focus_force()
    goodbye_window.after(
        3000,
        lambda: [goodbye_window.destroy(), root.destroy()]
    )


# ------------------ GUI Setup ------------------

root = tk.Tk()
root.title('Weather Program')
root.configure(bg='#f5f5f5')
root.geometry('450x650')

# Styles

style = ttk.Style()
style.configure('TLabel', font=('Calibri', 11), background='#f5f5f5')
style.configure('TButton', font=('Calibri', 11))
style.configure('TEntry', font=('Calibri', 11))
style.configure('TCheckbutton', font=('Calibri', 10), background='#f5f5f5')
style.configure(
    'Title.TLabel',
    font=(
        'Calibri',
        20,
        'bold'),
    background='#f5f5f5')
style.configure(
    'Header.TLabelframe.Label',
    font=(
        'Calibri',
        14,
        'bold'),
    background='#f5f5f5')
style.configure(
    'OR.TLabel',
    font=(
        'Calibri',
        12,
        'italic'),
    background='#f5f5f5')
style.configure('Status.TLabel', font=('Calibri', 10), background='#e0e0e0')

# Title

title_label = ttk.Label(root, text='Weather Program', style='Title.TLabel')
title_label.grid(row=0, column=0, columnspan=2, pady=15)

# City Frame

city_frame = ttk.LabelFrame(root, text='City Lookup')
city_frame.grid(row=1, column=0, columnspan=2, padx=15, pady=10, sticky='ew')
city_frame.configure(labelanchor='n')

ttk.Label(
    city_frame,
    text='City:').grid(
        row=0,
        column=0,
        padx=8,
        pady=8,
    sticky='w')
city_entry = ttk.Entry(city_frame, width=20)
city_entry.grid(row=0, column=1, padx=8, pady=8)

ttk.Label(
    city_frame,
    text='State (2 letters):').grid(
        row=1,
        column=0,
        padx=8,
        pady=8,
    sticky='w')
state_entry = ttk.Entry(city_frame, width=20)
state_entry.grid(row=1, column=1, padx=8, pady=8)

city_overview_var = tk.BooleanVar()
city_overview_check = ttk.Checkbutton(
    city_frame,
    text='Include AI Weather Summary',
    variable=city_overview_var)
city_overview_check.grid(row=2, column=0, columnspan=2, pady=8)

city_forecast_var = tk.BooleanVar()
city_forecast_check = ttk.Checkbutton(
    city_frame,
    text='Include 7-Day Forecast',
    variable=city_forecast_var)
city_forecast_check.grid(row=3, column=0, columnspan=2, pady=8)

city_lookup_btn = ttk.Button(
    city_frame,
    text='Lookup City',
    command=lookup_city)
city_lookup_btn.grid(row=4, column=0, columnspan=2, pady=12)

# OR Separator

or_label = ttk.Label(root, text='─ OR ─', style='OR.TLabel')
or_label.grid(row=2, column=0, columnspan=2, pady=10)

# ZIP Frame

zip_frame = ttk.LabelFrame(root, text='ZIP Lookup')
zip_frame.grid(row=3, column=0, columnspan=2, padx=15, pady=10, sticky='ew')
zip_frame.configure(labelanchor='n')

ttk.Label(
    zip_frame,
    text='ZIP Code:').grid(
        row=0,
        column=0,
        padx=8,
        pady=8,
    sticky='w')
zip_entry = ttk.Entry(zip_frame, width=20)
zip_entry.grid(row=0, column=1, padx=8, pady=8)

zip_overview_var = tk.BooleanVar()
zip_overview_check = ttk.Checkbutton(
    zip_frame,
    text='Include AI Weather Summary',
    variable=zip_overview_var)
zip_overview_check.grid(row=1, column=0, columnspan=2, pady=8)

zip_forecast_var = tk.BooleanVar()
zip_forecast_check = ttk.Checkbutton(
    zip_frame,
    text='Include 7-Day Forecast',
    variable=zip_forecast_var)
zip_forecast_check.grid(row=2, column=0, columnspan=2, pady=8)

zip_lookup_btn = ttk.Button(zip_frame, text='Lookup ZIP', command=lookup_zip)
zip_lookup_btn.grid(row=3, column=0, columnspan=2, pady=12)

# Units Dropdown

ttk.Label(
    root,
    text='Units:').grid(
        row=4,
        column=0,
        padx=15,
        pady=15,
    sticky='e')
unit_var = tk.StringVar(value='imperial')  # default to Fahrenheit
unit_menu = ttk.OptionMenu(
    root,
    unit_var,
    'imperial',
    'imperial',
    'metric',
    'kelvin')
unit_menu.grid(row=4, column=1, padx=15, pady=15, sticky='w')

# Exit Button

exit_btn = ttk.Button(root, text='Exit', command=exit_program)
exit_btn.grid(row=6, column=0, columnspan=2, pady=20, sticky="ew")

# Status Bar

status_var = tk.StringVar(value='Ready')
status_bar = ttk.Label(root, textvariable=status_var, style='Status.TLabel',
                       relief='sunken', anchor='w')
status_bar.grid(row=7, column=0, columnspan=2, sticky='ew', padx=10, pady=5)

# Keyboard shortcut: press Esc to exit

root.bind('<Escape>', lambda event: exit_program())


# ------------------Call to Main ------------------

def main():
    """Main function to start the GUI application."""
    root.mainloop()


if __name__ == "__main__":
    main()

