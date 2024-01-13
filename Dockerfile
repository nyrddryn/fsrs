# Use the official Python image with the desired version (3.10.6)
FROM python:3.10.6

# Set the working directory inside the container
WORKDIR /app

# Copy your application code to the container
COPY . .

# Install any necessary dependencies (you may need to adjust this based on your project)
RUN pip install flask flask-cors 
# Expose the port your Flask app will run on
EXPOSE 5001

# Define the command to run your Flask app
CMD ["python", "main.py"]
