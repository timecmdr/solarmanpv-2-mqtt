# FROM arm32v7/python:3
# Above image stopped working with error needing SMBUS so using alexellis2 base image.
FROM python
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
