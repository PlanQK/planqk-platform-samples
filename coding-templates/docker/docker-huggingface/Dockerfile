FROM python:latest

# Set the working directory to /app
WORKDIR /app

COPY requirements.txt /app/requirements.txt

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

RUN python download-model.py

# Run the command to start the application
CMD ["python", "main.py"]
