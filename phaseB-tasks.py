import requests
from git import Repo
import sqlite3
from bs4 import BeautifulSoup

# Task B3: Fetch Data from API
def fetch_data_from_api(url, save_path):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(save_path, 'w') as file:
                file.write(response.text)
            return "Data fetched successfully"
        else:
            return "Failed to fetch data"
    except Exception as e:
        return f"Error fetching data: {e}"

# Task B4: Clone Git Repo and Commit
def clone_and_commit(repo_url, local_path, commit_message):
    try:
        repo = Repo.clone_from(repo_url, local_path)
        repo.git.add(A=True)
        repo.index.commit(commit_message)
        repo.remote().push()
        return "Git repo cloned and committed successfully"
    except Exception as e:
        return f"Error with Git operation: {e}"

# Task B5: Run SQL Query
def run_sql_query(db_path, query):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception as e:
        return f"Error executing SQL query: {e}"

# Task B6: Scrape Website (Example - Scraping title)
def scrape_website(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string if soup.title else "No title found"
            return f"Website title: {title}"
        else:
            return "Failed to scrape website"
    except Exception as e:
        return f"Error scraping website: {e}"
