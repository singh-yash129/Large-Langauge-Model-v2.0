# Use an official lightweight Python image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy project files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the FastAPI default port
EXPOSE 8000

# Command to run the FastAPI app with Uvicorn
CMD ["uvicorn", "func:app", "--host", "0.0.0.0", "--port", "8000"]
