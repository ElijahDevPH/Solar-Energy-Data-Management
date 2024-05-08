import json
import os
import datetime
import logging

# Set up logging to track events and errors
logging.basicConfig(filename='solar_energy_log.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def print_menu():
    # Printing the main menu using a loop over a dictionary
    menu_options = {
        1: 'Enter new data',
        2: 'Show all data',
        3: 'Edit data entry',
        4: 'Calculate averages and suggest improvements',
        5: 'Save data to file',
        6: 'Load data from file',
        7: 'Show statistics',
        8: 'Data Visualization',
        9: 'Efficiency Analysis',
        10: 'Seasonal Analysis',
        11: 'Settings',
        12: 'Help',
        13: 'Advanced Filter View',
        14: 'Exit'
    }
    print("\n|       Solar Energy Data Management       |")
    print("\n--------------------------------------------")
    for key in menu_options:  # Looping through dictionary items
        print(f"{key}. {menu_options[key]}")  # Printing each menu option
    print("\n--------------------------------------------")

def get_integer_input(prompt, error_message="Invalid input. Please enter a valid number."):
    # Using a while loop to repeatedly prompt for input until valid input is received
    while True:

        try:
            value = int(input(prompt))  # Convert input to an integer data type
            logging.info(f"Integer input received: {value}")
            return value
        except ValueError:  # Handle incorrect input that cannot be converted to an integer
            logging.error("Invalid integer input")
            print(error_message)

def get_float_input(prompt, min_value=None, error_message="Invalid input. Please enter a valid number."):
    # Using a while loop to ensure correct float input
    while True:

        try:
            value = float(input(prompt))
            if min_value is not None and value < min_value:  # Check if value is less than the minimum value
                raise ValueError(f"Value must be at least {min_value}.")
            logging.info(f"Float input received: {value}")
            return value
        except ValueError as e:
            logging.error("Invalid float input")
            print(f"{error_message} {e}")

def get_weather_input():
    # Looping until valid weather input is received
    valid_weathers = ['Clear', 'Rainy', 'Cloudy']
    while True:
        weather = input("Enter the predominant weather condition (Clear, Rainy, Cloudy): ").capitalize()
        if weather in valid_weathers:  # Condition checking if the input is within allowed values
            logging.info(f"Weather input received: {weather}")
            return weather
        logging.warning("Invalid weather condition attempted")
        print("Invalid weather condition. Please enter 'Clear', 'Rainy', or 'Cloudy'.")

def get_user_input(data):
    # Collecting multiple entries from user input using a loop
    num_weeks = get_integer_input("Enter the number of weeks of data you will input: ", "Enter a positive integer.")

    for _ in range(num_weeks):  # Using a for loop to iterate through the number of weeks
        week = input("Enter the week identifier (e.g., 'Week 1'): ")
        total_energy = get_float_input(f"Enter total solar energy produced in {week} (in kWh): ", min_value=0)
        weather = get_weather_input()
        data.append({'week': week, 'total_energy': total_energy, 'weather': weather})  # Appending a dictionary to a list
    return data

def show_data(data):
    # Checking if the data list is empty using a condition
    if not data:
        print("No data available.")
        logging.info("Displayed empty data list")
    for index, entry in enumerate(data, start=1):  # Using enumerate to get index and value
        print(f"{index}. Week: {entry['week']}, Energy: {entry['total_energy']} kWh, Weather: {entry['weather']}")

def edit_data(data):
    # Editing data entries selected by user
    if not data:
        print("No data to edit.")
        return data
    show_data(data)
    entry_number = get_integer_input("Enter the number of the entry to edit: ") - 1  # Using -1 to adjust for zero-indexing

    if 0 <= entry_number < len(data):  # Condition to check valid index
        print("Enter new data:")
        data[entry_number]['week'] = input("Week identifier (e.g., 'Week 1'): ")
        data[entry_number]['total_energy'] = get_float_input("Total solar energy (in kWh): ", min_value=0)
        data[entry_number]['weather'] = get_weather_input()
    else:
        print("Invalid entry number.")
        logging.warning("Attempted to edit non-existent entry number")
    return data

def calculate_daily_average(data):
    # Calculate daily average if data is available
    if not data:
        print("No data to calculate.")
        return {}
    daily_data = {entry['week']: entry['total_energy'] / 7 for entry in data}  # Dictionary comprehension to calculate average
    return daily_data

def suggest_improvements(weather):
    # Suggest improvements based on weather conditions using conditions
    if weather in ['Rainy', 'Cloudy']:
        return "Consider using higher efficiency panels or adding more panels to compensate."
    elif weather == 'Clear':
        return "Optimal conditions. Ensure maintenance is up to date for maximum efficiency."
    else:
        return "No specific improvements suggested."

def display_averages_and_suggestions(data):
    # Display data and suggestions if data is available
    if not data:
        print("No data available.")
        return
    daily_avg = calculate_daily_average(data)
    print("\nDaily Solar Energy Production Averages and Suggestions:")
    for entry in data:
        week_avg = daily_avg[entry['week']]
        improvements = suggest_improvements(entry['weather'])
        print(f"{entry['week']}: {week_avg:.2f} kWh/day, Weather: {entry['weather']} - {improvements}")

def save_data(data):
    # Save data to a file if data is not empty
    if not data:
        print("No data to save.")
        return
    filename = input("Enter filename to save data (e.g., 'solar_data.json'): ")
    with open(filename, 'w') as f:  # Using with statement to ensure proper file handling
        json.dump(data, f, indent=4)
    print("Data saved successfully.")
    logging.info(f"Data saved to {filename}")

def load_data():
    # Load data from a file if file exists
    filename = input("Enter filename to load data from (e.g., 'solar_data.json'): ")
    if not os.path.exists(filename):
        print("File does not exist.")
        logging.error("Attempt to load non-existent file")
        return []
    with open(filename, 'r') as f:
        data = json.load(f)
    print("Data loaded successfully.")
    logging.info(f"Data loaded from {filename}")
    return data

def show_statistics(data):
    # Display statistics of the data
    if not data:
        print("No data available for statistics.")
        return

    total_energy = sum(entry['total_energy'] for entry in data)  # Use sum to calculate total energy
    max_energy = max(entry['total_energy'] for entry in data)  # Use max to find the maximum
    min_energy = min(entry['total_energy'] for entry in data)  # Use min to find the minimum
    average_energy = total_energy / len(data)  # Use division to find average

    print(f"Total energy produced: {total_energy} kWh")
    print(f"Maximum energy in a week: {max_energy} kWh")
    print(f"Minimum energy in a week: {min_energy} kWh")
    print(f"Average energy per week: {average_energy:.2f} kWh")
    logging.info("Displayed statistics for data")

def data_visualization(data):
    # Visualize data using simple text-based bar charts
    if not data:
        print("No data available for visualization.")
        return
    print("\nEnergy Production Chart:")
    for entry in data:
        bars = '*' * int(entry['total_energy'] / 10)  # Each '*' represents 10 kWh
        print(f"{entry['week']}: {bars} ({entry['total_energy']} kWh)")
    logging.info("Displayed data visualization")

def efficiency_analysis(data):
    # Perform a simple efficiency analysis
    if not data:
        print("No data available for efficiency analysis.")
        return
    efficiency_ratings = []
    for entry in data:
        rating = entry['total_energy'] / 100  # Simplified efficiency calculation
        efficiency_ratings.append((entry['week'], rating))
    print("\nEfficiency Ratings (per 100 kWh):")
    for week, rating in efficiency_ratings:
        print(f"{week}: {rating:.2f}")
    logging.info("Efficiency analysis performed")

def seasonal_analysis(data):
    # Analyze data by seasons using month extracted from week data
    if not data:
        print("No data available for seasonal analysis.")
        return
    season_data = {'Spring': [], 'Summer': [], 'Autumn': [], 'Winter': []}
    for entry in data:
        month = int(entry['week'].split(' ')[1])  # Extract month from week data assuming format "Week X"
        if 3 <= month <= 5:
            season = 'Spring'
        elif 6 <= month <= 8:
            season = 'Summer'
        elif 9 <= month <= 11:
            season = 'Autumn'
        else:
            season = 'Winter'
        season_data[season].append(entry['total_energy'])
    for season, energies in season_data.items():
        if energies:
            average = sum(energies) / len(energies)  # Calculate average for the season
            print(f"{season} average energy: {average:.2f} kWh")
        else:
            print(f"No data for {season}")
    logging.info("Seasonal analysis completed")

def settings():
    # Placeholder for settings feature
    print("Settings feature not implemented as of now.")

def help_menu():
    # Display help menu with instructions
    print("\nHelp Menu:")
    print("1. Enter data for each week including energy and weather.")
    print("2. Use the edit feature to correct any entry mistakes.")
    print("3. Save your data regularly to avoid loss.")
    print("4. Load previously saved data to continue your work.")
    print("5. View statistics to understand trends.")
    print("6. Visualize data to get a graphical representation of energy production.")
    print("7. Conduct efficiency analysis to rate the energy output.")
    print("8. Perform seasonal analysis to understand energy trends over seasons.")
    print("9. Contact support if you need further assistance.")
    logging.info("Displayed help menu")

def advanced_filter_view(data):
    # Advanced filtering options for viewing specific data
    if not data:
        print("No data available to filter.")
        return
    print("Advanced Filter Options:")
    print("1. Filter by Weather Condition")
    print("2. Filter by Energy Threshold")
    choice = get_integer_input("Select a filter option: ")

    if choice == 1:
        condition = get_weather_input()
        filtered_data = [entry for entry in data if entry['weather'] == condition]  # List comprehension for filtering
        show_data(filtered_data)

    elif choice == 2:
        threshold = get_float_input("Enter energy threshold (kWh): ")
        filtered_data = [entry for entry in data if entry['total_energy'] >= threshold]  # List comprehension for filtering
        show_data(filtered_data)
    logging.info("Performed advanced filtering")

def main():
    # Main function to handle user interaction and use all functions above
    data = []
    while True:  # Main loop to continuously display the menu and respond to user input
        print_menu()
        choice = get_integer_input("Choose an option: ")
        if choice == 1:
            data = get_user_input(data)
        elif choice == 2:
            show_data(data)
        elif choice == 3:
            data = edit_data(data)
        elif choice == 4:
            display_averages_and_suggestions(data)
        elif choice == 5:
            save_data(data)
        elif choice == 6:
            data = load_data()
        elif choice == 7:
            show_statistics(data)
        elif choice == 8:
            data_visualization(data)
        elif choice == 9:
            efficiency_analysis(data)
        elif choice == 10:
            seasonal_analysis(data)
        elif choice == 11:
            settings()
        elif choice == 12:
            help_menu()
        elif choice == 13:
            advanced_filter_view(data)
        elif choice == 14:
            print("Exiting program.")
            break
        else:
            print("Invalid option. Please choose again.")

if __name__ == "__main__":
    main() # to run the main function
