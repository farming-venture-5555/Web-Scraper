# Use the official Playwright image as the base image
FROM mcr.microsoft.com/playwright/playwright:latest

# Set the working directory
WORKDIR /workspace

# Copy the code into the container
COPY . /workspace

# Install any additional dependencies if needed
# RUN apt-get update && apt-get install -y <additional-packages>

# Install Playwright dependencies
RUN playwright install-deps

# Install Python dependencies
RUN pip install -r requirements.txt

# Run the Playwright tests by default
CMD ["python3", "scrapper.py"]