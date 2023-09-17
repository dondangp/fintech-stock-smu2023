# Install app.
FROM python:3.10-bullseye

# Create app directory.
WORKDIR /usr/local/src/app

# Build code for production.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Bundle app source.
COPY . .

# Run app.
CMD [ "sh", "-c", "streamlit run --server.port $PORT fintech.py" ]
