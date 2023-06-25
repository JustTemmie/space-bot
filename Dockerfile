# Use a base image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# copy all files into the container
COPY . .

# install dependencies
RUN pip install --default-timeout=900 -r requirements.txt

# install libgl1, required for openCV
RUN apt-get update && apt-get install -y libgl1-mesa-glx

# Run the bot
CMD [ "python", "main.py" ]
