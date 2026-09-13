
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Course: DSC510
# Week: 6
# Assignment: 6.1 Temperature Assessment Tool
# Author: Tim Hollis
# Date: 10/14/2025
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# === Temperature Conversion ===


def convert_temp(temp, from_unit):
    """Converts temperature between Celsius and Fahrenheit."""
    if from_unit == "C":
        return temp * 9 / 5 + 32  # C to F
    else:
        return (temp - 32) * 5 / 9  # F to C


# === Unit Selection and Validation ===


def get_temperature_unit():
    """Gets and validates temperature unit from user."""
    while True:
        unit = (
            input("Enter temperature unit (C for Celsius, F for Fahrenheit): ")
            .strip()
            .upper()
        )
        if unit in ["C", "F"]:
            return unit
        elif unit == "":
            print("Defaulting to Fahrenheit.")
            return "F"
        else:
            print('Invalid choice. Please enter "C" for Celsius or "F" for Fahrenheit.')


def validate_temperature(temp, unit):
    """Validates if temperature is within reasonable range for the unit."""
    if unit == "C":
        if temp < -90 or temp > 60:
            print(
                f"Warning: {temp}°C is outside typical Earth temperature range (-90°C to 60°C)"
            )
            while True:
                confirm = (
                    input("Do you want to continue anyway? (y/n): ").strip().lower()
                )
                if confirm == "y":
                    return True
                elif confirm == "n":
                    return False
                else:
                    print('Please enter "y" for yes or "n" for no.')
    else:
        if temp < -130 or temp > 140:
            print(
                f"Warning: {temp}°F is outside typical Earth temperature range (-130°F to 140°F)"
            )
            while True:
                confirm = (
                    input("Do you want to continue anyway? (y/n): ").strip().lower()
                )
                if confirm == "y":
                    return True
                elif confirm == "n":
                    return False
                else:
                    print('Please enter "y" for yes or "n" for no.')
    return True


# === Statistical Calculations ===


def calculate_average(temps):
    """Calculates and returns the average temperature."""
    return sum(temps) / len(temps) if temps else 0


# === Temperature Analysis and Output ===


def analyze_temps(temps, unit):
    """Analyzes the temperature list and prints comprehensive results."""
    if not temps:
        print("No temperatures to analyze.")
        return

    alt_unit = "F" if unit == "C" else "C"
    temp_count = len(temps)
    formatted_temps = ", ".join(f"{temp:.1f}°{unit}" for temp in temps)
    highest_temp = max(temps)
    lowest_temp = min(temps)
    average_temp = calculate_average(temps)
    converted_high = convert_temp(highest_temp, unit)
    converted_low = convert_temp(lowest_temp, unit)
    converted_avg = convert_temp(average_temp, unit)
    temp_range = f"{lowest_temp:.1f}°{unit} - {highest_temp:.1f}°{unit}"
    converted_range = (
        f"{converted_low:.1f}°{alt_unit} - {converted_high:.1f}°{alt_unit}"
    )
    sorted_temps = sorted(temps)
    median = (
        sorted_temps[len(sorted_temps) // 2]
        if len(sorted_temps) % 2 == 1
        else (
            sorted_temps[len(sorted_temps) // 2 - 1]
            + sorted_temps[len(sorted_temps) // 2]
        )
        / 2
    )

    print("\n" + "=" * 78)
    print("TEMPERATURE ANALYSIS RESULTS".center(78))
    print("=" * 78)
    print(f"Total temperatures entered: {temp_count}")
    print(f"Temperatures entered: {formatted_temps}")
    print(
        f"Highest temperature: {highest_temp:.1f}°{unit} ({converted_high:.1f}°{alt_unit})"
    )
    print(
        f"Lowest temperature:  {lowest_temp:.1f}°{unit} ({converted_low:.1f}°{alt_unit})"
    )
    print("-" * 78)
    print("Additional Analysis:".center(78))
    print(
        f"\nAverage temperature: {average_temp:.1f}°{unit} ({converted_avg:.1f}°{alt_unit})"
    )
    print(f"Temperature range:   {temp_range} ({converted_range})")
    print(f"Median temperature:  {median:.1f}°{unit}")
    if highest_temp - lowest_temp > 20:
        print("\nNote: Large temperature variation detected.")
    elif highest_temp - lowest_temp < 5:
        print("\nNote: Very consistent temperatures entered.")
    print("=" * 78)
    print("\nThank you for using the Temperature Analysis Tool!")


# === Main Program Execution ===


def main():
    """Main function that runs the Temperature Analysis Tool."""
    temps = []

    print("=" * 78)
    print("TEMPERATURE ANALYSIS TOOL".center(78))
    print("=" * 78)
    print(
        "Please input each temperature individually, and press ENTER to input the next."
    )
    print(
        "When complete, press ENTER with no value to finish input and begin analysis."
    )
    print("Pressing ENTER without adding any temperatures will exit the program.")
    print("Note: If no unit is selected, Fahrenheit will be used by default.\n")

    try:
        unit = get_temperature_unit()

        print(f"\nEntering temperatures in °{unit}")
        print("You can enter decimal values (e.g., 23.5)")
        print("-" * 78)

        while True:
            try:
                temp_input = input(f"Enter temperature (°{unit}): ").strip()
                if temp_input == "":
                    break

                temp = float(temp_input)

                if not validate_temperature(temp, unit):
                    print("Temperature discarded.")
                    continue

                temps.append(temp)
                print(f"✓ Temperature {temp:.1f}°{unit} added. ({len(temps)} total)")

                if len(temps) % 5 == 0:
                    current_avg = calculate_average(temps)
                    print(f"   Running average: {current_avg:.1f}°{unit}")

            except ValueError:
                print("Error: Please enter a valid number or press ENTER to finish.")
            except KeyboardInterrupt:
                print("\n\nProgram interrupted by user.")
                return

        if not temps:
            confirm_exit = (
                input(
                    "\nAre you sure you want to exit? (y to confirm, any other key to return): "
                )
                .strip()
                .lower()
            )
            if confirm_exit == "y":
                print("\nExiting program.")
                return
            else:
                print("\nReturning to temperature entry...")
                main()
                return

        print("\nInput complete. Processing results...")
        analyze_temps(temps, unit)

    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("Please restart the program and try again.")


# === Program Entry Point ===


if __name__ == "__main__":
    main()

