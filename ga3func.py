import httpx

# Task 1: Sentiment Analysis API Call
def analyze_sentiment(text):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": "Bearer dummy_api_key"}
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Analyze the sentiment of the following text and classify it as GOOD, BAD, or NEUTRAL."},
            {"role": "user", "content": text}
        ]
    }
    response = httpx.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

# Task 2: Generate Random US Addresses
def generate_addresses():
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": "Bearer dummy_api_key"}
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Respond in JSON"},
            {"role": "user", "content": "Generate 10 random addresses in the US"}
        ],
        "response_format": "json"
    }
    response = httpx.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

# Task 3: Extract Text from Invoice Image
def extract_invoice_text(image_base64):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": "Bearer dummy_api_key"}
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": [
                {"type": "text", "text": "Extract text from this image."},
                {"type": "image_url", "image_url": f"data:image/png;base64,{image_base64}"}
            ]}
        ]
    }
    response = httpx.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

# Task 4: Generate Text Embeddings
def generate_text_embeddings(text_list):
    url = "https://api.openai.com/v1/embeddings"
    headers = {"Authorization": "Bearer dummy_api_key"}
    payload = {
        "model": "text-embedding-3-small",
        "input": text_list
    }
    response = httpx.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

# Task 5: Generate AI-Based Image Descriptions
def generate_image_description(image_base64):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": "Bearer dummy_api_key"}
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": [
                {"type": "text", "text": "Describe this image."},
                {"type": "image_url", "image_url": f"data:image/png;base64,{image_base64}"}
            ]}
        ]
    }
    response = httpx.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

# Task 6: Summarize a Given Text
def summarize_text(text):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": "Bearer dummy_api_key"}
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Summarize the following text."},
            {"role": "user", "content": text}
        ]
    }
    response = httpx.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

# Task 7: Translate Text to Spanish
def translate_to_spanish(text):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": "Bearer dummy_api_key"}
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Translate the following text to Spanish."},
            {"role": "user", "content": text}
        ]
    }
    response = httpx.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

# Task 8: Generate a Short Story
def generate_short_story(prompt):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": "Bearer dummy_api_key"}
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Generate a short story based on the following prompt."},
            {"role": "user", "content": prompt}
        ]
    }
    response = httpx.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

# Task 9: Classify Text into Categories
def classify_text(text):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": "Bearer dummy_api_key"}
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Classify the following text into categories such as Technology, Health, Sports, or Politics."},
            {"role": "user", "content": text}
        ]
    }
    response = httpx.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()
