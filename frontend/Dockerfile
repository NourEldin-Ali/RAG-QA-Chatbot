FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy all project files to the working directory
COPY . .

# Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt

# Expose the default Streamlit port
EXPOSE 8501

# Specify the command to run the Streamlit application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]