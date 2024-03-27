import requests
import re
import time


github_token = "qqqqqqqq"


def search_github_for_function_signature(function_name, function_signature):

    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3.text-match+json',
    }
   
    query = f'"{function_name}"+"{function_signature}" in:file language:python'
    url = f"https://api.github.com/search/code?q={query}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        print(f"Error searching GitHub: {response.status_code}")
        return []

def extract_function_signatures_from_file(file_path):
   
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    pattern = re.compile(r'def (\w+)\((.*?)\):', re.DOTALL)
    return pattern.findall(content)

local_file_path = '/path'
function_signatures = extract_function_signatures_from_file(local_file_path)

for function_name, function_signature in function_signatures:
    matches = search_github_for_function_signature(function_name, function_signature)
    for match in matches:
        print(f"Found {function_name} in {match['repository']['html_url']}/blob/{match['sha']}/{match['path']}")

