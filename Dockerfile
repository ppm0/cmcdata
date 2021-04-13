FROM python:3
WORKDIR /app
ADD *.py /app/
ADD requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "./cmc.py"]
