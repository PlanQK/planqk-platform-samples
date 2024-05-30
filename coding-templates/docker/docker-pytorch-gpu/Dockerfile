FROM nvidia/cuda:12.1.0-base-ubuntu20.04

RUN apt update && \
    apt install -y --no-install-recommends python3-pip && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Run the command to start the application
CMD ["python3", "-m", "src"]
