How the Script Works

User Input: The script prompts you to enter a starting date and an ending date in the format YYYY-MM-DD.
Data Fetching: It fetches the debt data from the Treasury.gov API in 100-day increments to handle large date ranges efficiently.
Data Processing: The fetched data is combined into a single DataFrame for processing.
Summarization: It calculates the starting and ending debt amounts, the number of days between the dates, and the total debt added during that period.
Output:
Prints a summary of the debt information to the console.
Saves the summary to a CSV file named debt_summary.csv.
Requirements
Make sure you have the required Python packages installed:


pip install pandas requests

How to Run the Script
Save the script to a file, for example, debt_tracker.py.

Run the script using the command:

python debt_tracker.py
Enter the starting and ending dates when prompted.

Example Output

Enter the starting date (YYYY-MM-DD): 2023-01-01
Enter the ending date (YYYY-MM-DD): 2023-01-31
Fetching data from 2023-01-01 to 2023-01-31

US Treasury Federal Debt Tracking.
Starting Date: 2023-01-03
Ending Date: 2023-01-31
Starting Debt: $31,346,897,528,636.54
Ending Debt: $31,455,791,287,015.85
Number of Days: 28
Total Debt Added: $108,893,758,379.31

Summary saved to 'debt_summary.csv'.
Note: The actual debt figures and dates will vary based on the data returned by the API for the specified date range.

Error Handling
Invalid Date Format: If you enter the dates in an incorrect format, the script will prompt an error.
Start Date After End Date: The script checks to ensure the starting date is before the ending date.
No Data Fetched: If no data is returned for the specified date range, the script will inform you.
