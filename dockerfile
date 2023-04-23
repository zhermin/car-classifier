FROM python:3.10.11-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code to the container
COPY . .

# Expose port 4000
EXPOSE 4000

# Run the FastAPI app
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4000" ]