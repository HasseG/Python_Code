# Base image
FROM python:3.11-slim

# Set working dir in container
WORKDIR /home/hasseg/Projects/Python_Code/DiscordBot

# Copy all files to container
COPY . .

# Install dependencies
RUN python3 -m venv venv && \
    . venv/bin/activate && \
    pip install --no-cidache-dir -r requirements.txt

# Define command to run bot
CMD [ "/bin/bash", "-c", "source venv/bin/activate && python3 main.py" ]