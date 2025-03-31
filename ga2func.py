import markdown
import PIL.Image as Image
import io
import docker
import requests
import fastapi
from fastapi import FastAPI
import uvicorn
import yaml
import os
import subprocess
from Prebuilt import gunc

def generate_markdown():
    md_content = gunc('q-markdown')
    return md_content

def compress_image(image_path, output_path, max_size=1500):
    img = Image.open(image_path)
    img.save(output_path, format='PNG', optimize=True)
    return os.path.getsize(output_path)

def deploy_github_pages():
    command = "git push origin main"
    os.system(command)
    return "GitHub Pages deployed"

def google_colab_test():
    return "Run the given Python script on Google Colab"

def image_library_colab():
    return "Upload and process the image in Google Colab"

def deploy_vercel_api():
    return "Deploy FastAPI on Vercel with student marks API"

def create_github_action():
    action_yaml = """
jobs:
  test:
    steps:
      - name: Run Action
        run: echo "Hello, world!"
    """
    with open(".github/workflows/action.yml", "w") as f:
        f.write(action_yaml)
    return "GitHub Action created"

def push_docker_image():
    client = docker.from_env()
    image = client.images.build(path=".", tag="my_image:latest")
    client.images.push("my_dockerhub_username/my_image")
    return "Docker image pushed"

def run_fastapi_server():
    app = FastAPI()
    @app.get("/api")
    def get_students():
        return {"students": [{"studentId": 1, "class": "1A"}]}
    uvicorn.run(app, host="0.0.0.0", port=8000)
    return "FastAPI server running"

def run_llamafile():
    os.system("./llamafile --serve &")
    subprocess.run(["ngrok", "http", "8000"])
    return "Llamafile running with ngrok tunnel"

# Call functions as needed

