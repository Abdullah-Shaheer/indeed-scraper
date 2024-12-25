import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
import pandas as pd


def get_page_source(url):
    print(f"Navigating to {url}")
    ua = UserAgent()
    user_agent = ua.random

    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument(f"user-agent={user_agent}")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    try:
        driver.get(url)
        time.sleep(random.uniform(2, 5))  # Anti-bot delay

        try:
            if "captcha" in driver.page_source.lower() or "additional verification required" in driver.page_source.lower():
                print("Captcha encountered! Solve it manually.")
                WebDriverWait(driver, 120).until(ec.presence_of_element_located((By.XPATH, "//a[@class='gnav-header-1rg2zl5 e71d0lh0']")))
            if driver.find_element(By.XPATH, "//a[@class='gnav-header-1rg2zl5 e71d0lh0']"):
                print('There is no captcha on the page.')
            elif "request blocked" in driver.page_source.lower():
                print("Our request has been blocked.")
                return None

        except Exception as e:
            print("")
        try:
            pop_up = driver.find_element(By.XPATH,
                                         "//div[@class='dd-privacy-allow mosaic-provider-app-download-promos-service-1h5ugo2 eu4oa1w0']")
            if pop_up:
                print("There is a pop up on the page which might stop some elements from loading.Remove that pop up.")
                print("Scraping is stopped for 10 seconds.")
                time.sleep(10)
        except:
            print("")

        for _ in range(3):
            body = driver.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(random.uniform(1, 2))

        WebDriverWait(driver, 20).until(
            ec.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(5)
        page_source = driver.page_source
        # print("Page source retrieved successfully.")
        # print(page_source)
        return page_source

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        driver.quit()


def get_links(page_source):
    links = []
    soup = BeautifulSoup(page_source, "lxml")

    try:
        a_tags = soup.find_all("a", class_="jcs-JobTitle css-1baag51 eu4oa1w0")
        for a in a_tags:
            link = "https://www.indeed.com" + a["href"]
            links.append(link)
    except Exception as e:
        print(f"An error occured: {e}")
    except NoSuchElementException:
        print("No such element exception !")
    return links


def handle_pagination(base_url):
    all_links = []
    page_number = 0
    while True:
        current_url = f"{base_url}&start={page_number * 10}"
        print(f"Fetching page: {current_url}")
        page_source = get_page_source(current_url)
        if not page_source:
            break
        links = get_links(page_source)
        if not links:
            print("No more job links found.")
            break
        soup = BeautifulSoup(page_source, "lxml")
        next_button = soup.find("a", {'data-testid': 'pagination-page-next'})
        if not next_button:
            print("No more next button. Breaking")
            break
        all_links.extend(links)
        page_number += 1
        time.sleep(1)
    return all_links


def scrape_data(link, page_so):
    print(f"Going to scrape data from the job link:- {link}")
    list_to_store = []
    # Initiating Vars
    job_title = None
    company_name = None
    company_link = None
    pay = None
    rating = None
    location_of_company = None
    review = None
    job_description = None

    soup = BeautifulSoup(page_so, "lxml")

    try:
        loc = soup.find("div", class_="css-si0l7l e37uo190")
        job_title = loc.find("h2", {"data-testid": "simpler-jobTitle"}).text.strip()

    except AttributeError:
        job_title = soup.find("h1", {'class': 'jobsearch-JobInfoHeader-title css-1b4cr5z e1tiznh50'}).text.strip()
    print("Job Title:", job_title)

    try:
        lack = soup.find("div", class_="css-si0l7l e37uo190")
        if lack:
            loc1 = lack.find("div", class_="css-r2tgr9 e37uo190")
            if loc1:
                company_info = loc1.find("span").find("a")
                if company_info:
                    company_name = company_info.text.strip()
                    company_link = company_info.get("href", "Link not available")
                else:
                    raise AttributeError("Company info not found in first selector")
            else:
                raise AttributeError("loc1 not found")
        else:
            raise AttributeError("lack not found")
    except AttributeError:
        try:
            so = soup.find("span", class_="css-1saizt3 e1wnkr790")
            if so:
                company_link_element = so.find("a")
                if company_link_element:
                    company_name = company_link_element.text.strip()
                    company_link = company_link_element.get("href", "Link not available")
                else:
                    raise AttributeError("Company link element not found in second selector")
            else:
                raise AttributeError("so not found")
        except AttributeError:
            try:
                company = soup.find(
                    "span",
                    class_="jobsearch-JobInfoHeader-companyNameSimple css-yxyogu e1wnkr790",
                )
                if company:
                    company_name = company.text.strip()
                    company_link = company.get("href", "Link not available")
                else:
                    raise AttributeError("Company not found in third selector")
            except AttributeError:
                company_name = "Not Available"
                company_link = "Not Available"

    print("Company Name:", company_name)
    print("Company Link:", company_link)

    try:
        pay = soup.find("span", class_='js-match-insights-provider-4pmm6z e1wnkr790').text.strip()
    except AttributeError:
        print("Unable to find pay")
        pay = "Not available"
    if pay.lower() == "full-time" or pay.lower() == "part-time" or pay.lower() == "half-time":
        pay = "Not Available"

    print(f"Salary:- {pay}")

    try:
        lack1 = soup.find("div", class_="css-si0l7l e37uo190").find("div", class_="css-r2tgr9 e37uo190")
        rate_div = lack1.find("div", class_="css-1unnuiz e37uo190")
        rating = rate_div.find("span", class_="css-1b6omqv esbq1260").text.strip()

    except AttributeError:
        try:
            rating = soup.find("span", class_='css-ppxtlp e1wnkr790').text.strip()
        except AttributeError:
            rating = soup.find("span", class_='css-1b6omqv esbq1260').text.strip()
    print("Rating:", rating)

    try:
        location_div = soup.find("div", class_='css-1y8ffjx eu4oa1w0').find('div', class_='css-1weaggb e37uo190')
        location_of_company = location_div.text.strip() if location_div else None
        if location_of_company:
            extra = soup.find("span", class_="css-1b6omqv esbq1260")
            if extra and extra.text in location_of_company:
                location_of_company = re.sub(re.escape(extra.text), "", location_of_company).strip()
            if location_of_company.lower().endswith("remote"):
                location_of_company = location_of_company[:-6]
            #
            if location_of_company.lower().endswith('hybrid work'):
                location_of_company = location_of_company[:-11]
            additional_div = soup.find("div", class_="css-17cdm7w eu4oa1w0")
            if additional_div and additional_div.text in location_of_company:
                location_of_company = re.sub(re.escape(additional_div.text), "", location_of_company).strip()

    except AttributeError:
        try:
            fallback_div = soup.find("div", {'data-testid': 'inlineHeader-companyLocation'}).find('div')
            location_of_company = fallback_div.text.strip() if fallback_div else "Location not found"
        except AttributeError:
            try:
                location_of_company = soup.find("div", {'data-testid': 'job-location'}).text.strip()
            except AttributeError:
                try:
                    location_of_company = soup.find("div", class_='css-17cdm7w eu4oa1w0').text.strip()
                except:
                    location_of_company = "Not Available"
    print("Location:", location_of_company)

    try:
        review = soup.find("span", class_="css-1cxc9zk e1wnkr790").text.strip()
    except AttributeError:
        try:
            review = "Review count not found"
        except AttributeError:
            review = "Not Available"
    print("Review Count:", review)

    try:
        job_description = soup.find("div", {"id": "jobDescriptionText"}).text.strip()

    except AttributeError:
        try:
            job_description = soup.find('div',
                                    class_='jobsearch-JobComponent-description css-16y4thd eu4oa1w0').find('div').text.strip()
        except AttributeError:
            job_description = "Not Available"

    list_to_store.append({'Job Title': job_title if job_title else "Not Available",
                          'Rating': rating if rating else "Not Available",
                          'Salary': pay if pay else "Not Available",
                          'Company Name': company_name if company_name else "Not Available",
                          'Company Info': company_link if company_link else "Not Available",
                          'Company Location': location_of_company if location_of_company else "Not Available",
                          'Number of Reviews': review if review else "Not Available",
                          'Job Description': job_description if job_description else "Not Available"})

    return list_to_store


if __name__ == "__main__":
    key_word = str(input("Enter the keyword for scraping jobs (separated by +):-  "))
    main_list = []
    base_url = f"https://www.indeed.com/jobs?q={key_word}"
    links = handle_pagination(base_url)
    for link in links:
        page_sor = get_page_source(url=link)
        lst = scrape_data(link, page_sor)
        main_list.extend(lst)

    df = pd.DataFrame(main_list)
    df.to_excel('Indeed Data.xlsx', index=False)
    df.to_csv('Indeed Data.csv', index=False)
    print("Data Saved to CSV and EXCEL")
