FROM python:3.7.0-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /application
COPY requirements.txt /application
RUN python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
COPY . /application
EXPOSE 8000
