FROM python:3.7.7-slim

EXPOSE 5000

COPY ./ ./

RUN pip install --no-cache-dir -r requirements.txt 

CMD ["python", "./twitter.py", " > ./trump.txt"]
