FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy all project files to the working directory
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose the default Streamlit port
EXPOSE 5000

# Specify the command to run the application (modify as needed)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
