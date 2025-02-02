from tasks import (
    format_markdown, count_wednesdays, sort_contacts,
    extract_recent_logs, index_markdown_titles, extract_email_sender,
    extract_credit_card, find_similar_comments, compute_gold_sales
)
from phaseB_tasks import (
    fetch_data_from_api, clone_and_commit, run_sql_query, scrape_website
)

from fastapi import FastAPI, HTTPException
import os

app = FastAPI()

@app.post("/run")
async def run_task(task: str):
    task_map = {
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
        "scrape_website": scrape_website
    }

    if task in task_map:
        result = task_map[task]()
        return {"message": result}
    
    return {"error": "Unknown task"}

@app.get("/read")
async def read_file(path: str):
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    with open(path, "r") as f:
        return {"content": f.read()}
