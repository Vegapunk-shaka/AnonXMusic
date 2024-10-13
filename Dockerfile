# Base image with both Python 3.10 and Node.js 19
FROM nikolaik/python-nodejs:python3.10-nodejs19

# Update package list and install ffmpeg
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app/

# Copy all the project files into the container's working directory
COPY . .

# Install Python dependencies
RUN pip3 install --no-cache-dir -U -r requirements.txt

# Expose the port (Koyeb automatically assigns a PORT, but this helps for local testing)
EXPOSE 8080

# Use the start script to launch the application
CMD ["bash", "start"]
