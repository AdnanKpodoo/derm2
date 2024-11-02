
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . . 

# Install system dependencies required by MySQL connector and other libraries
#RUN apt-get update && apt-get install -y \
#default-libmysqlclient-dev build-essential

# Install Python dependencies
#RUN pip install --no-cache-dir mysql-connector-python streamlit pandas streamlit-lottie json requests

# Expose the port on which Streamlit will run
EXPOSE 8501

# Command to run your Streamlit app
CMD ["streamlit", "run", "skinderna_app.py"]