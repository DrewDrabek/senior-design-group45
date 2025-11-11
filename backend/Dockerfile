# This is just a test dockerfile that was used for making sure that the application could be containerized and then run
# This might need to change based on the actual structure of the application but might also work since app is the dir of the application
# The requirements.txt will need to be updated to include the dependencies after we add them but we might be able to use items to do that 

# This is the base image for the application
FROM python:3.13
WORKDIR /code

# Install dependencies - this is from the documentation and might need to be changed
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app ./app

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# To run this you will first need to build the image using the command:
# docker build -t my-backend-image .
# Then you can run the container using the command:
# docker run -d -p 8000:8000 --name my-backend-container this starts the container and then does port forwarding so you can access the app on localhost:8000