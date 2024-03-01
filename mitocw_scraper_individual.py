# MIT OCW course info scraper to extract information of individual course  using its url

import requests
from bs4 import BeautifulSoup
import json
import unicodedata

def scrape_course_info(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract course details
        course_banner = soup.find('div', id='course-banner')
        course_details = course_banner.find('span', class_='course-number-term-detail').text.split(' | ')
        course_code, semester, level = course_details

        # Extract and normalize course description, then truncate to first sentence
        course_description_tag = soup.find('div', id='expanded-description')
        course_description = course_description_tag.text.strip()

        # Construct course info JSON
        course_info = {
            'CourseCode': course_code,
            'Semester': semester,
            'Level': level,
            'CourseDescription': course_description
        }

        return json.dumps(course_info, indent=4)
    else:
        return 'Failed to fetch the webpage'

# URL to scrape
#url = 'https://ocw.mit.edu/courses/7-016-introductory-biology-fall-2018/'
url = "https://ocw.mit.edu/courses/1-00-introduction-to-computers-and-engineering-problem-solving-spring-2012/"

# Call the function and print the result
print(scrape_course_info(url))
