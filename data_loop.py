import tkinter as tk


class HistogramApp:
    def __init__(self, traffic_data, date):
        """
        Initializes the histogram application with the traffic data and selected date.
        :param traffic_data: Dictionary containing vehicle frequencies for two junctions per hour
        :param date: Selected date as a string
        """
        self.traffic_data = traffic_data  # {'Elm Avenue/Rabbit Road': [...], 'Hanley Highway/Westway': [...]}
        self.date = date
        self.root = tk.Tk()
        self.canvas = None
        self.bar_width = 20  # Bar width for histogram
        self.spacing = 10    # Spacing between bars
        self.canvas_width = max(900, len(traffic_data["Elm Avenue/Rabbit Road"]) * (self.bar_width * 2 + self.spacing) + 100)
        self.canvas_height = 630
        self.max_frequency = max(
            max(self.traffic_data["Elm Avenue/Rabbit Road"]),
            max(self.traffic_data["Hanley Highway/Westway"])
        )

    def setup_window(self):
        """
        Sets up the Tkinter window and canvas for the histogram.
        """
        self.root.title(f"Histogram of Vehicle Frequency per Hour ({self.date})")
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()

        # Add main heading
        self.canvas.create_text(
            self.canvas_width // 2, 30,
            text=f"Histogram of Vehicle Frequency per Hour ({self.date})",
            font=("Arial", 16, "bold"),
            fill="black"
        )

    def draw_histogram(self):
        """
        Draws the histogram with bars, labels, and axes.
        """
        # Dimensions and parameters
        x_start = 50  # Start position for the bars
        y_base = 540
        y_max_height = 400  # The maximum height for the bars in pixels

        hours = range(24)  # Hours from 00 to 23

        for i, hour in enumerate(hours):
            x_offset = x_start + i * (self.bar_width * 2 + self.spacing)

            # Elm Avenue/Rabbit Road bar
            elm_freq = self.traffic_data["Elm Avenue/Rabbit Road"][i]
            elm_height = (elm_freq / self.max_frequency) * y_max_height
            x0_elm = x_offset
            y0_elm = y_base - elm_height
            x1_elm = x0_elm + self.bar_width
            y1_elm = y_base
            self.canvas.create_rectangle(x0_elm, y0_elm, x1_elm, y1_elm, fill="lawn green")
            self.canvas.create_text((x0_elm + x1_elm) // 2, y0_elm - 10, text=str(elm_freq), anchor=tk.S, font=("Arial", 9, "bold"), fill="lawn green")

            # Hanley Highway/Westway bar
            hanley_freq = self.traffic_data["Hanley Highway/Westway"][i]
            hanley_height = (hanley_freq / self.max_frequency) * y_max_height
            x0_hanley = x1_elm  # No spacing between the green and red bars
            y0_hanley = y_base - hanley_height
            x1_hanley = x0_hanley + self.bar_width
            y1_hanley = y_base
            self.canvas.create_rectangle(x0_hanley, y0_hanley, x1_hanley, y1_hanley, fill="tomato")
            self.canvas.create_text((x0_hanley + x1_hanley) // 2, y0_hanley - 10, text=str(hanley_freq), anchor=tk.S, font=("Arial", 9, "bold"), fill="tomato")

            # Hour labels on the x-axis
            self.canvas.create_text((x0_elm + x1_hanley) // 2, y1_elm + 20, text=f"{hour:02d}", anchor=tk.N, font=("Arial", 10))

        # Add labels for axes
        self.canvas.create_text(self.canvas_width // 2, 600, text="Hours (00:00 to 23:00)", anchor=tk.CENTER, font=("Arial", 12))

    def add_legend(self):
        """
        Adds a legend to the histogram.
        """
        # Add legend for Elm Avenue/Rabbit Road
        self.canvas.create_rectangle(55, 70, 75, 90, fill="lawn green")
        self.canvas.create_text(85, 80, text="Elm Avenue/Rabbit Road", anchor=tk.W, font=("Arial", 10))

        # Add legend for Hanley Highway/Westway
        self.canvas.create_rectangle(55, 100, 75, 120, fill="tomato")
        self.canvas.create_text(85, 110, text="Hanley Highway/Westway", anchor=tk.W, font=("Arial", 10))

    def run(self):
        """
        Runs the Tkinter main loop to display the histogram.
        """
        self.setup_window()
        self.draw_histogram()
        self.add_legend()
        self.root.mainloop()


class MultiCSVProcessor:
    def validate_date_input(self, prompt, min_value, max_value):
        """
        Validates date inputs with range checking.
        """
        while True:
            try:
                value = int(input(prompt))
                if min_value <= value <= max_value:
                    return value
                print(f"Value must be between {min_value} and {max_value}.")
            except ValueError:
                print("Invalid input. Please enter an integer.")

    def process_csv(self, file_name, date):
        """
        Processes a CSV file and generates data for histogram visualization.
        """
        try:
            with open(file_name, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"File not found: {file_name}")
            return None

        headers = lines[0].strip().split(',')
        data = [dict(zip(headers, line.strip().split(','))) for line in lines[1:]]

        # Example: Process the data and generate histogram-compatible data
        traffic_data = {
            "Elm Avenue/Rabbit Road": [0] * 24,
            "Hanley Highway/Westway": [0] * 24
        }

        for row in data:
            hour = int(row["timeOfDay"].split(":")[0])  # Extract hour from "HH:MM"
            if row["JunctionName"] == "Elm Avenue/Rabbit Road":
                traffic_data["Elm Avenue/Rabbit Road"][hour] += 1
            elif row["JunctionName"] == "Hanley Highway/Westway":
                traffic_data["Hanley Highway/Westway"][hour] += 1

        return traffic_data

    def run(self):
        """
        Main loop to handle multiple CSV files.
        """
        while True:
            day = self.validate_date_input("Enter day (1-31): ", 1, 31)
            month = self.validate_date_input("Enter month (1-12): ", 1, 12)
            year = self.validate_date_input("Enter year (2000-2024): ", 2000, 2024)

            date = f"{day:02d}/{month:02d}/{year}"
            file_name = f"traffic_data{day:02d}{month:02d}{year}.csv"

            print(f"Processing file: {file_name}")
            traffic_data = self.process_csv(file_name, date)

            if traffic_data:
                app = HistogramApp(traffic_data, date)
                app.run()  # Display the histogram

            cont = input("Do you want to process another file? (Y/N): ").strip().lower()
            if cont != 'y':
                print("Exiting program.")
                break


# Example usage
if __name__ == "__main__":
    csv_processor = MultiCSVProcessor()
    csv_processor.run()
