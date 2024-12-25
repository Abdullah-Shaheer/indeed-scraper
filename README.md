# Indeed Job Scraper

## Overview

The **Indeed Job Scraper** is a Python script that allows you to scrape job listings from Indeed.com based on a keyword provided by the user. The scraper handles pagination, collects detailed job information, and saves the data in multiple formats such as CSV, Excel, and JSON. It is designed to be fully automated but also includes handling for situations where Captchas are encountered.

## Features

- **Keyword Support**: Scrapes job listings based on a keyword provided by the user. The scraper will search for jobs related to the given keyword.
- **Pagination Handling**: The scraper automatically navigates through all pages of job listings and extracts job details from each one.
- **Job Information Extraction**: For each job listing, the following information is scraped:
  - **Job Title**
  - **Rating**
  - **Salary**
  - **Company Name**
  - **Company Info (Link)**
  - **Company Location**
  - **Number of Reviews**
  - **Job Description**
- **Automation**: The entire scraping process is automated, making it easy to collect data without manual intervention.
- **Captcha Handling**: If the scraper encounters a CAPTCHA, it will stop and display the message: 
"Captcha encountered. Solve it manually."

## Libraries Used

- `random`: For generating random values to avoid detection.
- `time`: For adding delays between actions to mimic human behavior.
- `selenium`: For controlling the browser and handling dynamic content.
- `webdriver`: For interacting with browsers.
- `beautifulsoup`: For parsing HTML and extracting relevant data.
- `fake_useragent`: To simulate random user agents for avoiding blocks.
- `re`: For regular expression-based data extraction.
- `pandas`: For saving the scraped data in CSV and Excel formats.

## Installation

3. Ensure that you have **Chrome** and **ChromeDriver** installed. You can download the appropriate version of ChromeDriver from:  
   [ChromeDriver Download](https://sites.google.com/a/chromium.org/chromedriver/)

## Usage

1. Run the script and enter the keyword you wish to search for jobs:
    
    ```bash
    main.py
    ```

2. The script will automatically:
    - Search Indeed for the provided keyword.
    - Navigate through pagination to scrape all job listings.
    - Extract relevant job information.
    - Save the data to `Indeed Data.xlsx` and `Indeed Data.csv`.

3. If CAPTCHA is encountered during scraping, the script will stop and display the message:
    
    ```mathematica
    Captcha encountered. Solve it manually.
    ```
## Challenges

* **Cloudflare Protection**: One of the main challenges was dealing with Cloudflare protection, which can block requests from automated scripts. This project uses Selenium to simulate real browsing behavior, but if CAPTCHA appears, the scraper stops and prompts the user to solve it manually.

## Example Output

The scraper collects the following information for each job:

```python
{
  'Job Title': 'Software Engineer',
  'Rating': '4.5',
  'Salary': '$100,000 - $120,000',
  'Company Name': 'TechCorp',
  'Company Info': 'https://www.techcorp.com',
  'Company Location': 'New York, NY',
  'Number of Reviews': '200',
  'Job Description': 'Develop software solutions...'
}

