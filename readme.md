# Weather Data Retrieval Tool

This tool allows users to retrieve weather data from frost.met.no and displays the average temperature for a selected date and time range.

### Getting Started

To use this tool, you will need to have a client ID from frost.met.no. If you don't have one, you can create one by visiting the website and following the instructions provided.

Once you have your client ID, the tool will check for the existence of a file named "metno_client_id.txt" in the same directory as the script. If the file does not exist, the tool will prompt you to create one and enter your client ID.

The tool also has a gui GUI built using tkinter library which allows user to select date and time range and can search for locations, it returns the average temp between the two times

The tool uses the following libraries:

    tkinter
    tkcalendar
    datetime
    requests
    os
    webbrowser

Please make sure these libraries are installed before running the script, there is a requirements.txt filee you can use.
### Usage

To run the script, open a terminal, navigate to the directory where the script is located, and enter python main.py.

Once the script is running, enter the date and time range for which you want to retrieve weather data and click on the "Retrieve Data" button. The average temperature for the selected date and time range will be displayed.

Note that this script is only for demonstration purposes, and it's not intended for production use. You should check the usage and pricing policies of frost.met.no and make sure to not exceed the usage limits.
### Contributions

If you would like to contribute to this project, feel free to fork the repository and submit a pull request with your changes.
### Support

If you have any questions or need help getting the script to work, please open an issue in this repository and I'll do my best to assist you.