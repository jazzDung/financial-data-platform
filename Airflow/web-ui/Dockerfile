#image name financial-data-platform-web-ui

FROM python:3.9 

COPY templates /app/templates
COPY static /app/static
COPY app.py /app

RUN pip install psycopg2 flask vnstock pandas
CMD [“python3”, “app.py”] 
# Or enter the name of your unique directory and parameter set.

Expose 5000
WORKDIR /app
CMD python3 app.py