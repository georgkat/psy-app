# 
FROM python:3.9

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./. /code/.

#
CMD ["cd", "code"]

#
CMD ["uvicorn", "main:app", "--reload", "--port", "8000"]