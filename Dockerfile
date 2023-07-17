# Use an official Python runtime as the base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Set the command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
