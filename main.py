from tasks import (
    generate_data, format_markdown, count_wednesdays, sort_contacts,
    extract_recent_logs, index_markdown_titles, extract_email_sender,
    extract_credit_card, find_similar_comments, compute_gold_sales
)
from phaseB_tasks import (
    process_data, delete_data, fetch_data_from_api, clone_and_commit, run_sql_query, scrape_website,
    resize_image, transcribe_audio, markdown_to_html, filter_csv
)

from fastapi import FastAPI, HTTPException
import os
import openai

app = FastAPI()

@app.post("/run")
async def run_task(task: str):
    """Parses the task description and executes the closest matching function."""
    task_map = {
        "generate_data": generate_data,
        "format_markdown": format_markdown,
        "count_wednesdays": count_wednesdays,
        "sort_contacts": sort_contacts,
        "extract_recent_logs": extract_recent_logs,
        "index_markdown_titles": index_markdown_titles,
        "extract_email_sender": extract_email_sender,
        "extract_credit_card": extract_credit_card,
        "find_similar_comments": find_similar_comments,
        "compute_gold_sales": compute_gold_sales,
        "fetch_data_from_api": fetch_data_from_api,
        "clone_and_commit": clone_and_commit,
        "run_sql_query": run_sql_query,
        "scrape_website": scrape_website,
        "resize_image": resize_image,
        "transcribe_audio": transcribe_audio,
        "markdown_to_html": markdown_to_html,
        "filter_csv": filter_csv
    }

    if task in task_map:
        return {"message": task_map[task]()}

    # Use AI to find the closest matching task
    openai.api_key = os.environ["AIPROXY_TOKEN"]
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Identify the correct function name from this list: " + str(list(task_map.keys()))},
            {"role": "user", "content": f"Task description: {task}"}
        ]
    ).choices[0].message.content.strip()

    predicted_task = response["choices"][0]["message"]["content"].strip()

    if predicted_task in task_map:
        return {"message": task_map[predicted_task]()}
    
    return {"error": "Could not understand the task"}

@app.get("/read")
async def read_file(path: str):
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    with open(path, "r") as f:
        return {"content": f.read()}

@app.post("/process")
async def run_process_task(path: str):
    try:
        result = process_data(path)
        return {"message": "File processed successfully", "data": result}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

@app.post("/delete")
async def run_delete_task(path: str):
    try:
        delete_data(path)
        return {"message": "File deletion blocked"}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
