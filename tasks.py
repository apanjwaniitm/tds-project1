import os
import openai

openai.api_key = os.getenv("AIRPOXY_TOKEN")

# Task A2: Format Markdown files using Prettier
import subprocess

def format_markdown():
    # Ensure the file path is correct
    markdown_file_path = r"C:\Users\aakan\tds-project1\data\format.md"
    
    # Check if the markdown file exists
    if not os.path.exists(markdown_file_path):
        raise FileNotFoundError(f"The file at {markdown_file_path} does not exist.")

    # Ensure the full path to npx is used if necessary
    npx_path = r"C:\Program Files\nodejs\npx.cmd"  # Modify if your npx is located elsewhere

    try:
        # Run the npx command using subprocess and the full path to npx
        subprocess.run([npx_path, "prettier@3.4.2", "--write", markdown_file_path], check=True)
        print(f"Markdown file at {markdown_file_path} has been formatted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while formatting the markdown file: {e}")
    except FileNotFoundError as e:
        print(f"File not found: {e}")

# Task A3: Count Wednesdays in data/dates.txt
import datetime

def count_wednesdays():
    """Counts the number of Wednesdays in /data/dates.txt and writes the result to /data/dates-wednesdays.txt."""
    with open(r"C:\Users\aakan\tds-project1\data\dates.txt", "r") as f:
        dates = f.readlines()
    
    count = 0
    for date in dates:
        try:
            # Try to parse in '%Y-%m-%d' format first
            parsed_date = datetime.datetime.strptime(date.strip(), "%Y-%m-%d")
        except ValueError:
            try:
                # If the first format fails, try '%d-%b-%Y' format
                parsed_date = datetime.datetime.strptime(date.strip(), "%d-%b-%Y")
            except ValueError:
                # If both formats fail, skip the line
                continue
        
        if parsed_date.weekday() == 2:  # Wednesday is day 2
            count += 1
    
    with open("data/dates-wednesdays.txt", "w") as f:
        f.write(str(count))
    
    return f"Number of Wednesdays: {count}"

# Task A4: Sort Contacts in data/contacts.json
import json

def sort_contacts():
    """Sorts contacts.json by last_name, then first_name and saves to contacts-sorted.json."""
    with open(r"C:\Users\aakan\tds-project1\data\contacts.json", "r") as f:
        contacts = json.load(f)
    
    sorted_contacts = sorted(contacts, key=lambda x: (x["last_name"], x["first_name"]))
    
    with open("data/contacts-sorted.json", "w") as f:
        json.dump(sorted_contacts, f, indent=4)
    
    return "Contacts sorted successfully"

# Task A5: Extract first line from 10 most recent .log files
import os

def extract_recent_logs():
    """Writes the first line of the 10 most recent .log files in /data/logs/ to /data/logs-recent.txt."""
    log_dir = r"C:\Users\aakan\tds-project1\data\logs\\"
    log_files = sorted(
        [f for f in os.listdir(log_dir) if f.endswith(".log")],
        key=lambda x: os.path.getmtime(os.path.join(log_dir, x)),
        reverse=True
    )[:10]

    with open("data/logs-recent.txt", "w") as out_file:
        for log_file in log_files:
            with open(os.path.join(log_dir, log_file), "r") as f:
                first_line = f.readline().strip()
                out_file.write(first_line + "\n")
    
    return "Logs extracted successfully"

# Task A6: Extract first # Title from markdown files in data/docs
import re

def index_markdown_titles():
    """Creates index.json mapping filenames to their first H1 title."""
    index = {}
    docs_dir = r"C:\Users\aakan\tds-project1\data\docs\\"

    for file in os.listdir(docs_dir):
        if file.endswith(".md"):
            with open(os.path.join(docs_dir, file), "r") as f:
                for line in f:
                    if line.startswith("# "):  # First H1
                        index[file] = line.strip("# ").strip()
                        break

    with open("data/docs/index.json", "w") as f:
        json.dump(index, f, indent=4)
    
    return "Markdown titles indexed successfully"

# Task A7: Extract email sender using LLM
import openai
import os

def extract_email_sender():
    """Extracts sender email from data/email.txt using GPT-4o-Mini."""
    with open(r"C:\Users\aakan\tds-project1\data\email.txt", "r") as f:
        email_content = f.read()

    openai.api_key = os.environ["AIPROXY_TOKEN"]
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "Extract the sender's email address from this email."},
                  {"role": "user", "content": email_content}]
    )

    sender_email = response["choices"][0]["message"]["content"].strip()
    
    with open("data/email-sender.txt", "w") as f:
        f.write(sender_email)
    
    return f"Extracted email: {sender_email}"

# Task A8: Extract credit card number from image
from PIL import Image
import pytesseract

def extract_credit_card():
    """Extracts credit card number from data/credit-card.png using OCR."""
    image = Image.open(r"C:\Users\aakan\tds-project1\data\credit_card.png")
    card_number = pytesseract.image_to_string(image).replace(" ", "").strip()

    with open("data/credit-card.txt", "w") as f:
        f.write(card_number)
    
    return "Credit card number extracted"

# Task A9: Find most similar comments using embeddings
from sentence_transformers import SentenceTransformer, util

def find_similar_comments():
    """Finds the most similar pair of comments from data/comments.txt."""
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    with open(r"C:\Users\aakan\tds-project1\data\comments.txt", "r") as f:
        comments = f.readlines()
    
    embeddings = model.encode(comments, convert_to_tensor=True)
    cosine_scores = util.pytorch_cos_sim(embeddings, embeddings)
    
    max_score = 0
    best_pair = ("", "")
    
    for i in range(len(comments)):
        for j in range(i + 1, len(comments)):
            if cosine_scores[i][j] > max_score:
                max_score = cosine_scores[i][j]
                best_pair = (comments[i].strip(), comments[j].strip())

    with open("data/comments-similar.txt", "w") as f:
        f.write("\n".join(best_pair))
    
    return "Most similar comments extracted"

# Task A10: Compute Total Sales for Gold Tickets in SQLite
import sqlite3

def compute_gold_sales():
    """Computes total sales for Gold tickets in ticket-sales.db."""
    conn = sqlite3.connect(r"C:\Users\aakan\tds-project1\data\ticket-sales.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT SUM(units * price) FROM tickets WHERE type = 'Gold'")
    total_sales = cursor.fetchone()[0] or 0

    with open("data/ticket-sales-gold.txt", "w") as f:
        f.write(str(total_sales))
    
    conn.close()
    return f"Total sales for Gold tickets: {total_sales}"
