import requests

url = "http://127.0.0.1:8000/predict/"
file_path = "C:/Users/Rishabh/Downloads/anonmised.zip"

with open(file_path, 'rb') as zip_file:
    files = {'file': ('yourfile.zip', zip_file, 'application/zip')}
    response = requests.post(url, files=files)

print(response.json())
