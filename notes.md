# to activate venv virtual environment

source venv/bin/activate

# To run docker image in the production environment locally

## using gunicorn because Flask doesn't provide a production server

docker build -t flask-book-api .
docker run --name flask-book-api -d -p 8000:5000 -rm flask-book-api:latest
