import requests

# URL of the ZIP archive
url = "http://localhost:8042/studies/8a15ce0e-7be9d010-b0954129-02380184-e92766fd/archive"

# Send a GET request to download the file
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Write the content to a file (in binary mode)
    with open('study_archive.zip', 'wb') as file:
        file.write(response.content)
    print("Download complete: study_archive.zip")
else:
    print(f"Failed to download file. Status code: {response.status_code}")
