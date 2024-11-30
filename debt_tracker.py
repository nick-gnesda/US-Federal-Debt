
import requests
import pandas as pd
from datetime import datetime, timedelta
from io import StringIO  # For handling CSV text

def fetch_debt_data(start_date, end_date):
    # Define the API base URL
    API_BASE_URL = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/debt_to_penny"
    
    # List to hold all data
    all_data = []
    
    # Loop through date ranges in 100-day increments
    current_start_date = start_date
    while current_start_date <= end_date:
        # Calculate the current end date (100 days later)
        current_end_date = min(current_start_date + timedelta(days=100), end_date)
    
        # Format dates as strings
        start_str = current_start_date.strftime("%Y-%m-%d")
        end_str = current_end_date.strftime("%Y-%m-%d")
    
        # Build the API URL with filters
        url = (
            f"{API_BASE_URL}?format=csv"
            f"&filter=record_date:gte:{start_str},record_date:lte:{end_str}"
            f"&page[size]=100"
        )
    
        # Fetch the data
        print(f"Fetching data from {start_str} to {end_str}")
        response = requests.get(url, headers={"Accept": "text/csv"})
    
        # Check if the request was successful
        if response.status_code == 200:
            # Read the data into a DataFrame using StringIO
            df = pd.read_csv(StringIO(response.text))
            all_data.append(df)
        else:
            print(f"Failed to fetch data for {start_str} to {end_str}: {response.status_code}")
    
        # Move to the next date range
        current_start_date = current_end_date + timedelta(days=1)
    
    # Combine all data into a single DataFrame
    if all_data:
        full_data = pd.concat(all_data, ignore_index=True)
        return full_data
    else:
        return pd.DataFrame()  # Return empty DataFrame if no data

def summarize_data(data):
    # Ensure the `record_date` column is in datetime format
    data['record_date'] = pd.to_datetime(data['record_date'])
    
    # Sort the data by date in ascending order
    data.sort_values(by='record_date', inplace=True)
    
    # Extract the relevant columns
    starting_date = data['record_date'].iloc[0]
    ending_date = data['record_date'].iloc[-1]
    starting_debt = data['tot_pub_debt_out_amt'].iloc[0]
    ending_debt = data['tot_pub_debt_out_amt'].iloc[-1]
    
    # Calculate the number of days and total debt added
    total_days = (ending_date - starting_date).days
    total_debt_added = ending_debt - starting_debt
    
    # Display results
    print(f"\nUS Treasury Federal Debt Tracking.")
    print(f"Starting Date: {starting_date.date()}")
    print(f"Ending Date: {ending_date.date()}")
    print(f"Starting Debt: ${starting_debt:,.2f}")
    print(f"Ending Debt: ${ending_debt:,.2f}")
    print(f"Number of Days: {total_days}")
    print(f"Total Debt Added: ${total_debt_added:,.2f}")
    
    # Save the summarized data to a new CSV file
    summary = {
        "Starting Date": [starting_date.date()],
        "Ending Date": [ending_date.date()],
        "Starting Debt": [starting_debt],
        "Ending Debt": [ending_debt],
        "Number of Days": [total_days],
        "Total Debt Added": [total_debt_added]
    }
    summary_df = pd.DataFrame(summary)
    summary_df.to_csv("debt_summary.csv", index=False)
    
    print("\nSummary saved to 'debt_summary.csv'.")

def main():
    # Get start and end dates from user input
    start_date_str = input("Enter the starting date (YYYY-MM-DD): ")
    end_date_str = input("Enter the ending date (YYYY-MM-DD): ")
    
    # Convert input strings to datetime objects
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    except ValueError:
        print("Error: Please enter dates in the format YYYY-MM-DD.")
        return
    
    # Check that start date is before end date
    if start_date > end_date:
        print("Error: Starting date must be before ending date.")
        return
    
    # Fetch data
    data = fetch_debt_data(start_date, end_date)
    
    if data.empty:
        print("No data fetched.")
        return
    
    # Summarize data
    summarize_data(data)

if __name__ == "__main__":
    main()

