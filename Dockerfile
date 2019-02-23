FROM python:3
ADD *.py /
ADD requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "./cmc.py"]