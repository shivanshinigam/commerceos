import urllib.request
import json
import os

key = os.environ.get('GEMINI_API_KEY')
if not key:
    print("No key")
else:
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
    req = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(req)
        data = json.loads(response.read())
        for model in data.get('models', []):
            if 'gemini' in model['name']:
                print(model['name'])
    except Exception as e:
        print(e)
