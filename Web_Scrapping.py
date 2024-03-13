import requests
from bs4 import BeautifulSoup
import datetime

# Define target website URL and days to look back
base_url = "https://www.example.com/jobs"  # Replace with target site
days_back = 3  # Number of days to look back for recent jobs

# Generate formatted date string for comparison
today = datetime.date.today()
threshold_date = today - datetime.timedelta(days=days_back)
threshold_date_str = threshold_date.strftime('%Y-%m-%d')  # YYYY-MM-DD format

def extract_recent_jobs(url):
  """Extracts job postings from the given URL and checks for recent dates

  Args:
      url: The URL of the job posting page

  Returns:
      list: A list of dictionaries containing job details (title, date, etc.) for recent jobs
  """
  jobs = []
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')

  # Find all job postings (replace 'job-listing' with appropriate class/tag)
  job_listings = soup.find_all('div', class_='job-listing')

  for job in job_listings:
    # Extract job details (title, date, etc.) based on the website's HTML structure
    job_title = job.find('h3').text.strip()
    # Replace with selector for finding the date posted
    date_posted = job.find('span', class_='posted-date').text.strip()

    # Check if the job was posted within the specified timeframe
    if date_posted >= threshold_date_str:
      jobs.append({
          'title': job_title,
          'date': date_posted,
          # Add other job details as needed
      })

  return jobs

# Iterate through pagination if website uses multiple pages for listings
all_jobs = []
next_page_url = base_url  # Assuming pagination starts at base URL

while next_page_url:
  # Call extract_recent_jobs function to get jobs from current page
  current_page_jobs = extract_recent_jobs(next_page_url)
  all_jobs.extend(current_page_jobs)

  # Find the next page URL (replace logic based on website's pagination)
  next_page_link = soup.find('a', rel='next')
  if next_page_link:
    next_page_url = next_page_link['href']
  else:
    next_page_url = None  # No more pages

# Process and utilize the extracted jobs data (all_jobs)
print(f"Found {len(all_jobs)} jobs posted in the last {days_back} days")
# You can further process or store the jobs data (all_jobs) in a database, CSV, etc.
