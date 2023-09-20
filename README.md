# RazerStatusRows

## Overview
RGB lighting can enhance aesthetics, but why limit it to just that? Razer Blade keyboards offer individually lit RGB keys, and with OpenRazer on Linux, you can take control of each key's lighting programmatically. That's where RazerStatusRows comes in – it adds functionality to your Razer keyboard's lighting by displaying real-time status information.

With RazerStatusRows, you can transform your keyboard lighting into a functional status indicator. Currently, it supports the following features:

### Battery Status
- The top row of your keyboard shows the remaining battery percentage.
- Different colors are used to represent specific battery percentage intervals.
- A charging animation displays when your laptop is connected to a charger.

### Temperature Status
- The second row of your keyboard displays the temperature.
- The color gradient represents temperature levels, with hotter temperatures displaying as intense reds.

Stay tuned for more features and enhancements!

## Installation

Follow these simple steps to install and use RazerStatusRows:

1. **Install OpenRazer**: Ensure you have OpenRazer installed on your Linux system.

2. **Clone the Git Repository**: Clone this repository to your local machine.

3. **Install Required Python Packages**: Use pip to install the necessary Python packages. You can install them with the following command:
   ```
   pip install -r requirements.txt
   ```

4. **Run the Python Script**: Execute the Python script by running the following command:
   ```
   python RazerStatusRows.py
   ```

5. **Auto-Start Configuration**: Customize auto-start options according to your preferences to have RazerStatusRows automatically run when you log in.

## Configuration

You can customize RazerStatusRows by adjusting the following configuration options located in the script:

- **BATTERY_HIGH_THRESHOLD**: Set the battery percentage threshold above which the battery indicator will display in green. The default is `0.69`.

- **BATTERY_LOW_THRESHOLD**: Set the battery percentage threshold below which the battery indicator will display in red. By default, it is calculated as `1 - BATTERY_HIGH_THRESHOLD`.

- **SLEEP_INTERVAL**: Configure the interval (in seconds) at which RazerStatusRows updates the keyboard lighting to reflect the current status. The default is `0.5` seconds.

To customize these options, open the Python script and modify the corresponding variables at the beginning of the script. Remember to save your changes before running the script.

---

Enjoy the enhanced functionality and aesthetics of your Razer keyboard with RazerStatusRows!

Feel free to contribute to this project and make it even better. If you encounter any issues or have suggestions, please open an issue on GitHub.

Happy customizing!
