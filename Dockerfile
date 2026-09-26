# 1. Use an official lightweight Python image
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Download the spaCy NLP model during the build process
RUN python -m spacy download en_core_web_sm

# 6. Copy the rest of your application code
COPY . .

# 7. Expose the port FastAPI runs on
EXPOSE 8000

# 8. Define the command to run the API
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]