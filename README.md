# Coding_Challenge
The focus of this coding challenge is building a lightweight test framework that uses Selenium or Webdriver.io as core technology. 

## step 1

Create a virtual environment (optional but recommended):

```bash
python -m venv venv
# On Mac:
source venv/bin/activate 
# On Windows:
 venv\Scripts\activate
```

## step 2 

Install the required libraries.

```bash
pip install pytest selenium webdriver_manager
```

## step 3

Install the required libraries.

```bash
pytest test_ryanair.py
```

# Using Docker (optional)

## step 1

Create a Dockerfile in the project directory:

```docker
FROM python:3.9

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["pytest"]
```
## step 2

Create a docker-compose.yml file:

```docker
version: "3"
services:
  test:
    build: .
```


## step 3 

Create a requirements.txt file:

```docker
pytest
selenium
```

## step 4 

To run the test case from a Docker container, execute the following commands:

```bash
docker-compose build
docker-compose run test
```






