import sys
import os
from datetime import datetime, timedelta
from scrapy.cmdline import execute
import argparse

def main(args):
    # Append the current file path
    sys.path.append(os.path.abspath(__file__))

    # Helper function to build the Scrapy command
    def build_command(spider, category=None, time=None,file=None):
        command = [f'scrapy', 'crawl', spider]  # Use a list for better handling of arguments
        if category:
            command += [f'-a', f'category={category}']  # Add category argument
        if time:
            command += [f'-a', f'time={time}']  # Add time argument
        if file:
            command += [f'-s', f'EXPORTER_FILE={file}']  # Specify output file
        return command

    # Handle date range if both start_date and end_date are provided
    if args.start_date and args.end_date:
        # Parse the start and end dates
        start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(args.end_date, "%Y-%m-%d")
        
        # Iterate through each date in the range
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime("%Y-%m-%d")
            print(f"Running spider for date: {date_str}")
            # Build and execute the command with the current date
            execute(build_command(args.spider, args.category,date_str, args.file))
            # Move to the next date
            current_date += timedelta(days=1)
    else:
        # No date range, execute for a single date or without date
        execute(build_command(args.spider, args.category, None , args.file))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Scrapy spider with optional parameters.')
    parser.add_argument('--spider', required=True, help='Name of the Scrapy spider to run')
    parser.add_argument('--category', help='Category to filter items')
    parser.add_argument('--time', help='Specific time or date to crawl for')
    parser.add_argument('--start_date', help='Start date for date range (YYYY-MM-DD)')
    parser.add_argument('--end_date', help='End date for date range (YYYY-MM-DD)')
    parser.add_argument('--file', help='Output file for the scraped data')
    args = parser.parse_args()
    main(args)