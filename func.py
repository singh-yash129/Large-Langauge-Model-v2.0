from fastapi import FastAPI, File, Form, UploadFile, HTTPException
import openai
import pandas as pd
import zipfile
import io
import os
import requests
import json
import ga1func, ga2func, ga3func, ga4func, ga5func

# Initialize FastAPI app
app = FastAPI()

# Set your AIPROXY_TOKEN
AIPROXY_TOKEN = os.environ("AIPROXY_TOKEN")
AIPROXY_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"


TASK_IMPLEMENTATIONS = {
    "get_vscode_version": ga1func.get_vscode_version,
    "count_wednesdays": ga1func.count_wednesdays,
    "run_npx_command": ga1func.run_npx_command,
    "make_http_request": ga1func.make_http_request,
    "google_sheets_formula": ga1func.google_sheets_formula,
    "excel_formula": ga1func.excel_formula,
    "extract_csv_from_zip": ga1func.extract_csv_from_zip,
    "sort_json": ga1func.sort_json,
    "multi_cursor_to_json": ga1func.multi_cursor_to_json,
    "extract_hidden_value": ga1func.extract_hidden_value,
    "sum_css_values": ga1func.sum_css_values,
    "process_encoded_files": ga1func.process_encoded_files,
    "use_github": ga1func.use_github,
    "replace_text_in_files": ga1func.replace_text_in_files,
    "list_large_files": ga1func.list_large_files,
    "move_and_rename_files": ga1func.move_and_rename_files,
    "compare_files": ga1func.compare_files,
    "sql_ticket_sales": ga1func.sql_ticket_sales,
    "find_git_repo_size": ga1func.find_git_repo_size,
    "check_file_integrity": ga1func.check_file_integrity,
    "extract_all_text_from_html": ga1func.extract_all_text_from_html,
    "generate_markdown": ga2func.generate_markdown,
    "compress_image": ga2func.compress_image,
    "deploy_github_pages": ga2func.deploy_github_pages,
    "google_colab_test": ga2func.google_colab_test,
    "image_library_colab": ga2func.image_library_colab,
    "deploy_vercel_api": ga2func.deploy_vercel_api,
    "create_github_action": ga2func.create_github_action,
    "push_docker_image": ga2func.push_docker_image,
    "run_fastapi_server": ga2func.run_fastapi_server,
    "run_llamafile": ga2func.run_llamafile,
    "analyze_sentiment": ga3func.analyze_sentiment,
    "generate_addresses": ga3func.generate_addresses,
    "extract_invoice_text": ga3func.extract_invoice_text,
    "generate_text_embeddings": ga3func.generate_text_embeddings,
    "generate_image_description": ga3func.generate_image_description,
    "summarize_text": ga3func.summarize_text,
    "translate_to_spanish": ga3func.translate_to_spanish,
    "generate_short_story": ga3func.generate_short_story,
    "classify_text": ga3func.classify_text,
    "count_ducks_on_page6": ga4func.count_ducks_on_page6,
    "fetch_low_rated_movies": ga4func.fetch_low_rated_movies,
    "fetch_wikipedia_outline": ga4func.fetch_wikipedia_outline,
    "get_islamabad_forecast": ga4func.get_islamabad_forecast,
    "get_max_latitude_lima": ga4func.get_max_latitude_lima,
    "get_hn_go_post": ga4func.get_hn_go_post,
    "get_newest_berlin_github_user": ga4func.get_newest_berlin_github_user,
    "generate_github_action": ga4func.generate_github_action,
    "extract_student_marks": ga4func.extract_student_marks,
    "pdf_to_markdown": ga4func.pdf_to_markdown,
    "clean_excel_and_compute_margin": ga5func.clean_excel_and_compute_margin,
    "count_unique_student_ids": ga5func.count_unique_student_ids,
    "count_successful_get_requests": ga5func.count_successful_get_requests,
    "find_top_data_consumer": ga5func.find_top_data_consumer,
    "aggregate_sales_by_city": ga5func.aggregate_sales_by_city,
    "sum_sales_from_json": ga5func.sum_sales_from_json,
    "count_oi_occurrences": ga5func.count_oi_occurrences,
    "reconstruct_scrambled_image": ga5func.reconstruct_scrambled_image,
    "calculate_average_temperature": ga5func.calculate_average_temperature,
    "extract_emails_from_text": ga5func.extract_emails_from_text
}


# Function mapping
TASK_FUNCTIONS = {
    "check_file_integrity": ("file_path",),
    "compare_files": ("zip_filename",),
    "count_wednesdays": ("start_date", "end_date"),
    "excel_formula": ("func"),
    "extract_all_text_from_html": ("html_content",),
    "extract_csv_from_zip": ("zip_filename",),
    "extract_hidden_value": ("html_content",),
    "find_git_repo_size": ("repo_path",),
    "get_vscode_version": (),
    "google_sheets_formula": ("func"),
    "list_large_files": ("zip_filename", "min_size", "date"),
    "make_http_request": ("email",),
    "move_and_rename_files": ("zip_filename",),
    "multi_cursor_to_json": ("input_text",),
    "process_encoded_files": ("zip_filename", "symbols"),
    "replace_text_in_files": ("zip_filename",),
    "run_npx_command": ("filename",),
    "sort_json": ("json_list",),
    "sql_ticket_sales": ("db_path",),
    "sum_css_values": ("html_content",),
    "use_github": ("repo_url", "email"),
    "compress_image": ("image_path", "output_path", "max_size"),
    "create_github_action": (),
    "deploy_github_pages": (),
    "deploy_vercel_api": (),
    "generate_markdown": (),
    "google_colab_test": (),
    "image_library_colab": (),
    "push_docker_image": (),
    "run_fastapi_server": (),
    "run_llamafile": (),
    "analyze_sentiment": ("text",),
    "classify_text": ("text",),
    "extract_invoice_text": ("image_base64",),
    "generate_addresses": (),
    "generate_image_description": ("image_base64",),
    "generate_short_story": ("prompt",),
    "generate_text_embeddings": ("text_list",),
    "summarize_text": ("text",),
    "translate_to_spanish": ("text",),
    "count_ducks_on_page6": (),
    "extract_student_marks": ("pdf_path",),
    "fetch_low_rated_movies": (),
    "fetch_wikipedia_outline": ("country",),
    "generate_github_action": (),
    "get_hn_go_post": (),
    "get_islamabad_forecast": ("api_key",),
    "get_max_latitude_lima": (),
    "get_newest_berlin_github_user": (),
    "pdf_to_markdown": ("pdf_path",),
    "aggregate_sales_by_city": ("file_path",),
    "calculate_average_temperature": ("json_file",),
    "clean_excel_and_compute_margin": ("file_path", "date_filter", "product_filter", "country_filter"),
    "count_oi_occurrences": ("json_file",),
    "count_successful_get_requests": ("log_file",),
    "count_unique_student_ids": ("file_path",),
    "extract_emails_from_text": ("file_path",),
    "find_top_data_consumer": ("log_file",),
    "reconstruct_scrambled_image": ("image_file", "mapping_file"),
    "sum_sales_from_json": ("file_path",)
}

# Function to call respective task function (dummy implementation)
def execute_task(task_name, **kwargs):
    function = TASK_IMPLEMENTATIONS.get(task_name)
    if function:
        return function(**kwargs)  # ✅ Call actual function
    return "Unknown task"


prompt = f"""
You are an AI assistant trained to solve data science assignments efficiently. Given a user question, determine if:
1. The question can be answered directly with your knowledge.
2. The question requires executing a function from a predefined list.

**Rules:**
- If a function is needed, return a JSON object in this format:
  {{
      "function": "function_name",
      "parameters": {{ "param1": "value1", "param2": "value2" }}
  }}
- Only use function names from this list: {json.dumps(list(TASK_FUNCTIONS.keys()))}.
- Ensure all required parameters for the function are included.
- If the function does not require parameters, return `"parameters": {{}}`.
- **Do NOT answer in plain text** if a function is available.

**Example Outputs:**
1. **Direct Answer:**
   *User:* What is 2 + 2?  
   *Response:* "4"

2. **Function Call Required:**
   *User:* "What is the output of 'code -s' in VS Code?"  
   *Response:*  
   ```json
   {{
       "function": "get_vscode_version",
       "parameters": {{}}
   }}
   ```
3. **Function Call Required**
   *User:* "Download the provided README.md file. In the directory where you downloaded it, make sure it is called README.md, and run 'npx -y prettier@3.4.2 README.md | sha256sum'. What is the output?"   
      *Response:*  
   ```json
   {{
       "function": "run_npx_command",
       "parameters": {{
           "filename": "README.md"

       }}
   }}
   ```
 4.**Function Call Required**
   *User:* "Running `uv run --with httpie -- https [URL]` installs the Python package `httpie` and sends a HTTPS request to the URL.
   - Send a HTTPS request to `https://httpbin.org/get` with the URL encoded parameter `email` set to your email.
   - What is the JSON output of the command? (Paste only the JSON body, not the headers)"   
      *Response:*  

{{
    "function": "make_http_request",
    "parameters": {{
       
     
            "email": "hjshj@gmail.com"
        
    }}
}}
"""

@app.post("/api/")
async def answer_question(question: str = Form(...), file: UploadFile = File(None)):
    try:
        if(file):
            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)

        headers = {
            "Authorization": f"Bearer {AIPROXY_TOKEN}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "system", "content": prompt},{"role": "user","content":f'Question{question}'}]
        }
        response = requests.post(AIPROXY_URL, json=data, headers=headers)
        response_json = response.json()
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response_json.get("error", "Unknown error"))
        print("Response Status Code:", response.status_code)
        print("Raw Response Text:", response.text)


        print("Raw AI response:", response_json)

        ai_response = response_json["choices"][0]["message"]["content"].strip()
        print(ai_response)
        if ai_response.startswith("```json"):
            ai_response = ai_response.replace("```json", "").replace("```", "").strip()
        # If GPT-4o Mini suggests a function call, execute it
        print(ai_response)
        try:
            parsed_response = json.loads(ai_response)
            if "function" in parsed_response and parsed_response["function"] in TASK_FUNCTIONS:
                task_name = parsed_response["function"]
                task_params = parsed_response.get("parameters", {})
              
                return {"answer": execute_task(task_name, **task_params)}
        except json.JSONDecodeError:
            pass  # If response isn't JSON, assume it's a direct answer
        
        return {"answer": ai_response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
