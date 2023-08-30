import typing as T
import uuid
import requests
from .base import BaseTranslationClient


class AzureTranslateClient(BaseTranslationClient):
    key: str
    endpoint: str
    location: str
    api_version: str

    def __init__(self, key: str, location: str, endpoint: str, api_version: str = None, **kwargs) -> None:
        super().__init__(
            content_language_key='azure_code'
        )
        self.key = key
        self.location = location
        self.endpoint = endpoint
        self.api_version = api_version or '3.0'

    def _translate(
        self,
        text: str,
        from_language_code: str,
        to_language_code: str
    ):
        if not text:
            return ""

        translations = self._call_api(
            texts=[text],
            from_language=from_language_code,
            to_languages=[to_language_code]
        )
        return translations[0].get(to_language_code)

    def _translate_batch(
        self,
        texts: T.List[str],
        from_language_code: str,
        to_language_code: str
    ):
        translations = self._call_api(
            texts=texts,
            from_language=from_language_code,
            to_languages=[to_language_code]
        )
        return [translation.get(to_language_code) for translation in translations]

    def _call_api(
        self,
        texts: T.List[str],
        from_language: str,
        to_languages: T.List[str]
    ):
        params = {
            'api-version': self.api_version,
            'from': from_language,
            'to': to_languages
        }

        headers = {
            'Ocp-Apim-Subscription-Key': self.key,
            # location required if you're using a multi-service or regional (not global) resource.
            'Ocp-Apim-Subscription-Region': self.location,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        body = [{
            'text': text
        } for text in texts]

        request = requests.post(
            self.endpoint,
            params=params,
            headers=headers,
            json=body
        )
        request.raise_for_status()

        response = request.json()
        translations = [{lang["to"]: lang["text"] for lang in translation["translations"]} for translation in response]

        return translations
