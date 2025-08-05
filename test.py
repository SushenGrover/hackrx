import requests

data = {
    "documents": "C:\\Users\\grove\\Desktop\\coding\\doc_processor\\data\\BAJHLIP23020V012223.pdf",
    "questions": [
        "What is the company name?",
        "What is the most important date in the document?"
    ]
}
resp = requests.post("http://127.0.0.1:8000/hackrx/run", json=data)
print(resp.status_code)
print(resp.json())
