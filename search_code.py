import requests
import re
import time

# Ваш GitHub Personal Access Token
github_token = ""

def search_github_for_code_element(name, signature="", content_type="function"):
    """Ищет в GitHub файлы, содержащие указанные элементы кода: функции или классы."""
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3.text-match+json',
    }
    if content_type == "function":
        query = f'"{name}"+"{signature}" in:file language:python'
    elif content_type == "class":
        query = f'class "{name}" in:file language:python'
    else:
        print(f"Unsupported content_type: {content_type}")
        return []

    url = f"https://api.github.com/search/code?q={query}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        print(f"Error searching GitHub: {response.status_code}")
        return []

def extract_function_signatures_from_file(file_path):
    """Извлекает названия функций и их сигнатуры из файла с исходным кодом."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return re.findall(r'def (\w+)\((.*?)\):', content, re.DOTALL)

def extract_classes_from_file(file_path):
    """Извлекает названия классов и их содержимое из файла с исходным кодом."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    # Используем регулярное выражение для поиска классов и сохраняем весь блок класса
    class_pattern = re.compile(r'class (\w+)(\(.*?\))?:\s*\n((?:\s+(?:def|class|@|\w).+\n)+)', re.MULTILINE)
    return class_pattern.findall(content)

local_file_path = ''

# Поиск и вывод результатов для функций
function_signatures = extract_function_signatures_from_file(local_file_path)
for function_name, function_signature in function_signatures:
    matches = search_github_for_code_element(function_name, function_signature, content_type="function")
    for match in matches:
        print(f"Found {function_name} in {match['repository']['html_url']}/blob/{match['sha']}/{match['path']}")

class_definitions = extract_classes_from_file(local_file_path)


for class_name, class_args, _ in class_definitions:
    class_matches = search_github_for_code_element(class_name, content_type="class")
    for match in class_matches:
        print(f"Found class {class_name} in {match['repository']['html_url']}/blob/{match['sha']}/{match['path']}")
# Поиск и вывод результатов для классов
