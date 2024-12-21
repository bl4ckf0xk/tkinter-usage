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
        self.bar_width = 20  # Increased bar width for better visibility
        self.spacing = 10    # Spacing between bars
        self.canvas_width = max(900, len(traffic_data["Elm Avenue/Rabbit Road"]) * (self.bar_width * 2 + self.spacing) + 100)
        self.canvas_height = 600
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

    def draw_histogram(self):
        """
        Draws the histogram with bars, labels, and axes.
        """
        # Dimensions and parameters
        x_start = 80
        y_base = 500
        y_max_height = 400  # The maximum height for the bars in pixels

        # Draw the bars for each hour
        hours = range(24)  # Hours from 00 to 23
        for i, hour in enumerate(hours):
            # Elm Avenue/Rabbit Road bar
            elm_freq = self.traffic_data["Elm Avenue/Rabbit Road"][i]
            elm_height = (elm_freq / self.max_frequency) * y_max_height
            x0_elm = x_start + i * (self.bar_width * 2 + self.spacing)
            y0_elm = y_base - elm_height
            x1_elm = x0_elm + self.bar_width
            y1_elm = y_base
            self.canvas.create_rectangle(x0_elm, y0_elm, x1_elm, y1_elm, fill="green")
            self.canvas.create_text((x0_elm + x1_elm) // 2, y0_elm - 10, text=str(elm_freq), anchor=tk.S, font=("Arial", 9))

            # Hanley Highway/Westway bar
            hanley_freq = self.traffic_data["Hanley Highway/Westway"][i]
            hanley_height = (hanley_freq / self.max_frequency) * y_max_height
            x0_hanley = x1_elm + 5  # Small spacing between bars for the same hour
            y0_hanley = y_base - hanley_height
            x1_hanley = x0_hanley + self.bar_width
            y1_hanley = y_base
            self.canvas.create_rectangle(x0_hanley, y0_hanley, x1_hanley, y1_hanley, fill="red")
            self.canvas.create_text((x0_hanley + x1_hanley) // 2, y0_hanley - 10, text=str(hanley_freq), anchor=tk.S, font=("Arial", 9))

            # Hour labels on the x-axis
            self.canvas.create_text((x0_elm + x1_hanley) // 2, y1_elm + 20, text=f"{hour:02d}", anchor=tk.N, font=("Arial", 10))

        # Draw x-axis and y-axis
        self.canvas.create_line(50, y_base, self.canvas_width, y_base, arrow=tk.LAST)  # X-axis
        self.canvas.create_line(50, y_base, 50, 50, arrow=tk.FIRST)  # Y-axis

        # Add labels for axes
        self.canvas.create_text(self.canvas_width // 2, 580, text="Hours 00:00 to 24:00", anchor=tk.CENTER, font=("Arial", 12))
        self.canvas.create_text(20, 275, text="Frequency of Vehicles", anchor=tk.CENTER, angle=90, font=("Arial", 12))

    def add_legend(self):
        """
        Adds a legend to the histogram.
        """
        # Add legend for Elm Avenue/Rabbit Road
        self.canvas.create_rectangle(self.canvas_width - 250, 70, self.canvas_width - 230, 90, fill="green")
        self.canvas.create_text(self.canvas_width - 200, 80, text="Elm Avenue/Rabbit Road", anchor=tk.W, font=("Arial", 10))

        # Add legend for Hanley Highway/Westway
        self.canvas.create_rectangle(self.canvas_width - 250, 100, self.canvas_width - 230, 120, fill="red")
        self.canvas.create_text(self.canvas_width - 200, 110, text="Hanley Highway/Westway", anchor=tk.W, font=("Arial", 10))

    def run(self):
        """
        Runs the Tkinter main loop to display the histogram.
        """
        self.setup_window()
        self.draw_histogram()
        self.add_legend()
        self.root.mainloop()


# Example usage
if __name__ == "__main__":
    # Example data for two junctions
    traffic_data = {
        "Elm Avenue/Rabbit Road": [12, 14, 16, 18, 23, 25, 27, 29, 33, 31, 29, 27, 25, 21, 19, 16, 14, 12, 18, 21, 23, 19, 16, 9],
        "Hanley Highway/Westway": [10, 12, 14, 16, 19, 22, 25, 29, 32, 33, 31, 29, 27, 25, 23, 20, 18, 15, 17, 22, 24, 20, 14, 8],
    }
    date = "15/06/2024"
    app = HistogramApp(traffic_data, date)
    app.run()
