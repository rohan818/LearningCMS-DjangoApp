import requests
import json
import csv

# Compact JSON payload for the POST request
json_payload = {"from":0,"size":50,"post_filter":{"bool":{"must":[{"bool":{"should":[{"term":{"object_type.keyword":"course"}}]}},{"bool":{"should":[{"term":{"offered_by":"OCW"}}]}},{"bool":{"should":[{"term":{"topics":"Engineering"}}]}}]}},"query":{"bool":{"should":[{"bool":{"filter":{"bool":{"must":[{"term":{"object_type":"course"}}]}}}}]}},"aggs":{"agg_filter_topics":{"filter":{"bool":{"should":[{"bool":{"filter":{"bool":{"must":[{"bool":{"should":[{"term":{"object_type.keyword":"course"}}]}},{"bool":{"should":[{"term":{"offered_by":"OCW"}}]}}]}}}}]}},"aggs":{"topics":{"terms":{"field":"topics","size":10000}}}},"agg_filter_department_name":{"filter":{"bool":{"should":[{"bool":{"filter":{"bool":{"must":[{"bool":{"should":[{"term":{"object_type.keyword":"course"}}]}},{"bool":{"should":[{"term":{"offered_by":"OCW"}}]}},{"bool":{"should":[{"term":{"topics":"Engineering"}}]}}]}}}}]}},"aggs":{"department_name":{"terms":{"field":"department_name","size":10000}}}},"agg_filter_level":{"filter":{"bool":{"should":[{"bool":{"filter":{"bool":{"must":[{"bool":{"should":[{"term":{"object_type.keyword":"course"}}]}},{"bool":{"should":[{"term":{"offered_by":"OCW"}}]}},{"bool":{"should":[{"term":{"topics":"Engineering"}}]}}]}}}}]}},"aggs":{"level":{"nested":{"path":"runs"},"aggs":{"level":{"terms":{"field":"runs.level","size":10000},"aggs":{"courses":{"reverse_nested":{}}}}}}}},"agg_filter_course_feature_tags":{"filter":{"bool":{"should":[{"bool":{"filter":{"bool":{"must":[{"bool":{"should":[{"term":{"object_type.keyword":"course"}}]}},{"bool":{"should":[{"term":{"offered_by":"OCW"}}]}},{"bool":{"should":[{"term":{"topics":"Engineering"}}]}}]}}}}]}},"aggs":{"course_feature_tags":{"terms":{"field":"course_feature_tags","size":10000}}}}}}

# URL for the POST request
url = "https://open.mit.edu/api/v0/search/"

# Headers for the POST request
headers = {"Content-Type": "application/json"}

# Performing the POST request
response = requests.post(url, json=json_payload, headers=headers)

# Checking if the request was successful
if response.status_code == 200:
    print("Request was successful.")
    # Print the response JSON, or process it as needed
    print(response.json())
else:
    print(f"Request failed with status code: {response.status_code}")



# Extract courses from the response
courses = response['hits']['hits']

# Prepare data structure for extracted information
extracted_data = []

for course in courses:
    # Initialize a dictionary to hold the extracted information for each course
    course_data = {}
    
    # Directly accessible keys
    direct_keys = ['coursenum', 'title', 'short_description']
    for key in direct_keys:
        course_data[key] = course['_source'].get(key, None)
    
    # Extracting first element of 'level' and 'instructors'
    course_data['level'] = course['_source']['runs'][0]['level'][0] if course['_source']['runs'][0]['level'] else None
    course_data['instructor'] = course['_source']['runs'][0]['instructors'][0] if course['_source']['runs'][0]['instructors'] else None
    
    # Semester and year are nested within 'runs'
    course_data['semester'] = course['_source']['runs'][0].get('semester', None)
    course_data['year'] = course['_source']['runs'][0].get('year', None)

    # Extract 'slug' and create 'courseurl'
    course_data['course_url'] = "https://ocw.mit.edu/" + course['_source']['runs'][0]['slug']
    
    # Append the extracted data to the list
    extracted_data.append(course_data)

# Save extracted data to a JSON file
with open('courses_data.json', 'w') as json_file:
    json.dump(extracted_data, json_file, indent=4)

# Save extracted data to a CSV file
csv_columns = ['coursenum', 'semester', 'year', 'level', 'title', 'instructor', 'short_description', 'course_url']
csv_file = "courses_data.csv"
try:
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in extracted_data:
            writer.writerow(data)
except IOError:
    print("I/O error")

# The script saves extracted data into 'courses_data.json' and 'courses_data.csv'.
