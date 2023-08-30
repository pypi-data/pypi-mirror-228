import json
from pathlib import Path

content_languages: dict[str, dict[str, str]] = {}
with open(Path(__file__).parent / "content_languages.json", "r") as file:
    content_languages = json.load(file)


def get_content_language(code: str):
    return content_languages.get(code)

def set_content_language(code: str, content_langauge: dict[str, str]):
    content_languages[code] = content_langauge
