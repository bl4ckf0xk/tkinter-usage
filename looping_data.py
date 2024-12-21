import tkinter as tk


class HistogramApp:
    def __init__(self, traffic_data, date):
        """
        Initializes the histogram application with the traffic data and selected date.
        """
        self.traffic_data = traffic_data
        self.date = date
        self.root = tk.Tk()
        self.canvas = None

    def setup_window(self):
        """
        Sets up the Tkinter window and canvas for the histogram.
        """
        self.root.title(f"Traffic Data Histogram - {self.date}")
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="white")
        self.canvas.pack()

    def draw_histogram(self):
        """
        Draws the histogram with axes, labels, and bars.
        """
        if not self.traffic_data:
            print("No data available to display the histogram.")
            return

        # Convert string values to integers
        numeric_data = {key: int(value) for key, value in self.traffic_data.items()}

        max_value = max(numeric_data.values())
        bar_width = 40
        spacing = 20
        x_start = 50
        y_base = 500

        # Draw bars
        for i, (key, value) in enumerate(numeric_data.items()):
            bar_height = int((value / max_value) * 400)  # Scale bar height
            x0 = x_start + i * (bar_width + spacing)
            y0 = y_base - bar_height
            x1 = x0 + bar_width
            y1 = y_base

            self.canvas.create_rectangle(x0, y0, x1, y1, fill="blue")
            self.canvas.create_text((x0 + x1) // 2, y1 + 15, text=key, anchor=tk.N)

        # Draw axes
        self.canvas.create_line(40, y_base, 750, y_base, arrow=tk.LAST)  # X-axis
        self.canvas.create_line(50, 50, 50, y_base, arrow=tk.FIRST)       # Y-axis


    def add_legend(self):
        """
        Adds a legend to the histogram.
        """
        self.canvas.create_text(600, 50, text="Blue Bars: Traffic Data", fill="blue", font=("Arial", 12))

    def run(self):
        """
        Runs the Tkinter main loop to display the histogram.
        """
        self.setup_window()
        self.draw_histogram()
        self.add_legend()
        self.root.mainloop()


class MultiCSVProcessor:
    def __init__(self):
        """
        Initializes the application for processing multiple CSV files.
        """
        self.current_data = None

    def load_csv_file(self, file_path):
        """
        Loads a CSV file and processes its data.
        """
        # Helper function for parsing time
        def parse_time(time_str):
            hours, minutes, seconds = map(int, time_str.split(':'))
            return hours, minutes

        try:
            with open(f"traffic_data{file_path}.csv", 'r') as file:
                lines = file.readlines()

            # Read headers
            columns = lines[0].strip().split(',')
        except FileNotFoundError:
            print(f"Error: No file found for the date {file_path}.csv")
            return None

        # Variables
        vehicle_count = truck_count = elec_count = two_wheeled_vehicle_count = 0
        buses_heading_north_count = no_turn_count = bicycle_count = over_speed_limit_count = 0
        elm_junction_count = hanley_junction_count = elm_junc_scooter_count = 0
        vehicles_by_hour = {}
        rain_hours = 0
        rain_minutes = 0
        rain_times = []
        previous_weather = None

        for line in lines[1:]:
            row = dict(zip(columns, line.strip().split(',')))
            vehicle_count += 1

            if row['VehicleType'].strip() == 'Truck':
                truck_count += 1
            if row.get('elctricHybrid', '').strip() == 'True':
                elec_count += 1
            if row['VehicleType'].strip() in ['Bicycle', 'Motorcycle', 'Scooter']:
                two_wheeled_vehicle_count += 1
            if (row['VehicleType'].strip() == 'Buss' and
                row['JunctionName'].strip() == 'Elm Avenue/Rabbit Road' and
                row['travel_Direction_out'].strip() == 'N'):
                buses_heading_north_count += 1
            if row['travel_Direction_in'].strip() == row['travel_Direction_out'].strip():
                no_turn_count += 1
            if row['VehicleType'].strip() == 'Bicycle':
                bicycle_count += 1
            if int(row['JunctionSpeedLimit']) < int(row['VehicleSpeed']):
                over_speed_limit_count += 1
            if row['JunctionName'].strip() == 'Elm Avenue/Rabbit Road':
                elm_junction_count += 1
                if row['VehicleType'].strip() == 'Scooter':
                    elm_junc_scooter_count += 1

            # Track vehicles by hour for Hanley Highway/Westway
            if row['JunctionName'].strip() == 'Hanley Highway/Westway':
                hanley_junction_count += 1
                hour = row['timeOfDay'].split(':')[0]
                vehicles_by_hour[hour] = vehicles_by_hour.get(hour, 0) + 1

            # Calculate rain durations
            if row['Weather_Conditions'] in ('Light Rain', 'Heavy Rain'):
                time_of_day = parse_time(row['timeOfDay'])
                rain_times.append(time_of_day)
            elif row['Weather_Conditions'] not in ('Light Rain', 'Heavy Rain') and previous_weather in ('Light Rain', 'Heavy Rain'):
                time_in_minutes = [(time[0] * 60 + time[1]) for time in rain_times]
                if time_in_minutes:
                    range_minutes = max(time_in_minutes) - min(time_in_minutes)
                    rain_hours += range_minutes // 60
                    rain_minutes += range_minutes % 60
                    if rain_minutes >= 60:
                        rain_hours += 1
                        rain_minutes -= 60
                    rain_times.clear()
            previous_weather = row['Weather_Conditions']

        # Final calculations
        truck_percentage = round((truck_count * 100) / vehicle_count) if vehicle_count else 0
        avg_bike_per_hour = round(bicycle_count / 24)
        elm_junc_scooter_percentage = int((elm_junc_scooter_count * 100) / elm_junction_count) if elm_junction_count else 0
        peak_hour = max(vehicles_by_hour.items(), key=lambda x: x[1]) if vehicles_by_hour else ('0', 0)
        formatted_peak_hours = f"Between {peak_hour[0]}:00 and {int(peak_hour[0]) + 1}:00"
        formatted_rain_duration = f"{rain_hours} hours and {rain_minutes} minutes"

        # Display outcomes
        results = [
            f"The total number of vehicles recorded for this date is {vehicle_count}",
            f"The total number of trucks recorded for this date is {truck_count}",
            f"The total number of electric vehicles for this date is {elec_count}",
            f"The total number of two-wheeled vehicles for this date is {two_wheeled_vehicle_count}",
            f"The total number of Buses leaving Elm Avenue/Rabbit Road heading North is {buses_heading_north_count}",
            f"The total number of vehicles through both junctions not turning left or right is {no_turn_count}",
            f"The percentage of all vehicles recorded that are Trucks for this date is {truck_percentage}%",
            f"The average number of Bikes per hour for this date is {avg_bike_per_hour}",
            f"The total number of vehicles recorded as over the speed limit for this date is {over_speed_limit_count}",
            f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {elm_junction_count}",
            f"The total number of vehicles recorded through Hanley Highway/Westway junction is {hanley_junction_count}",
            f"{elm_junc_scooter_percentage}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.",
            f"The highest number of vehicles in an hour on Hanley Highway/Westway is {peak_hour[1]}",
            f"The most vehicles through Hanley Highway/Westway were recorded {formatted_peak_hours}",
            f"The number of hours of rain for this date is {formatted_rain_duration}"
        ]

        for result in results:
            print(result)

        self.save_results_to_file(file_path, results)
        return results

    def save_results_to_file(self, file_path, results):
        """
        Saves the results to a text file.
        """
        try:
            with open(f"results.txt", "a") as file:
                for line in results:
                    file.write(line + "\n")
            print(f"Results saved to 'results.txt'.")
        except Exception as e:
            print(f"Error saving results: {e}")

    def process_files(self):
        """
        Main loop for processing multiple CSV files based on user input.
        """
        while True:
            print("Enter the date for the file you want to process (format: DDMMYYYY).")
            date = input("Date (e.g., 21122024): ").strip()
            
            if len(date) != 8 or not date.isdigit():
                print("Invalid date format. Please try again.")
                continue
            
            results = self.load_csv_file(date)
            if results:
                # Display the histogram
                histogram_data = {
                    "Trucks": results[1].split()[-1],
                    "Two-Wheelers": results[3].split()[-1],
                    "Overspeed": results[8].split()[-1],
                    "Bicycles (Avg/Hour)": results[7].split()[-1],
                }
                app = HistogramApp(histogram_data, date)
                app.run()

            load_another = input("Do you want to load another file? (yes/no): ").strip().lower()
            if load_another == "no":
                print("Exiting the program. Goodbye!")
                break


# Main program entry point
if __name__ == "__main__":
    processor = MultiCSVProcessor()
    processor.process_files()
