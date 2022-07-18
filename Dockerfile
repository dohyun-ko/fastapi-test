FROM python:3.10

COPY ./recommend ./recommend

WORKDIR ./recommend

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "-m", "gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--access-logfile", "./gunicorn-access.log", "main:app", "--preload", "--bind", "0.0.0.0:8000", "--workers", "2"]