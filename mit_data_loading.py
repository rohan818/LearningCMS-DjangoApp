import json
import psycopg2
from datetime import datetime
import re  # Import the regular expressions module

json_file_path = '/code/courses_data.json'

# Database connection parameters
db_name = "postgres"
db_user = "postgres"
db_password = "postgres"
db_host = "22387ec73dc8"
db_port = "5432"

def load_json_data(file_path):
    """Load JSON data from a file."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def clean_text(text):
    """Clean the text by keeping only alphabets, digits, and full stops."""
    # Replace any character not a letter, digit, or full stop with a space
    return re.sub(r'[^a-zA-Z0-9\.]', ' ', text)

def generate_slug(title):
    """Generate a cleaned and formatted slug from a title."""
    # Remove characters other than alphabets or digits
    cleaned_title = re.sub(r'[^a-zA-Z0-9]', '', title)
    # Convert to lowercase and replace spaces with hyphens
    slug = cleaned_title.lower().replace(" ", "-")
    return slug

def insert_courses_data(data):
    """Insert courses data into the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            dbname=db_name, 
            user=db_user, 
            password=db_password, 
            host=db_host, 
            port=db_port
        )
        cur = conn.cursor()

        for item in data:
            title = item['title']
            short_description = clean_text(item['short_description'])  # Clean the description
            slug = generate_slug(title)
            created = datetime.now()
            
            owner_id = 1
            subject_id = 2
            
            cur.execute(
                "INSERT INTO courses_course (title, overview, slug, created, owner_id, subject_id) VALUES (%s, %s, %s, %s, %s, %s)",
                (title, short_description, slug, created, owner_id, subject_id)
            )

        conn.commit()
        cur.close()
        conn.close()

        print("Data inserted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    courses_data = load_json_data(json_file_path)
    insert_courses_data(courses_data)

if __name__ == "__main__":
    main()
