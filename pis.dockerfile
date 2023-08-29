FROM python:3.9.13
WORKDIR /PIS_projekt_azil/
COPY requirements.txt req.txt
RUN pip3 install -r req.txt
COPY . .
EXPOSE 8080
CMD ["python3", "main.py"]