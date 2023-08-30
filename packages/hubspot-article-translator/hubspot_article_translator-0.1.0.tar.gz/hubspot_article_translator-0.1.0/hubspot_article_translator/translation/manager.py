import typing as T
import logging

from .clients.base import BaseTranslationClient

logger = logging.getLogger()


class TranslationManager(object):
    clients: T.List[BaseTranslationClient]

    def __init__(
        self
    ) -> None:
        self.clients = []

    def add_clients(
        self,
        *clients: BaseTranslationClient
    ):
        self.clients.extend(clients)

    def get_supported_clients(
        self,
        from_language: dict,
        to_language: dict,
    ) -> T.List[BaseTranslationClient]:
        return [
            client for client in self.clients if client.supports_translation(
                from_language=from_language,
                to_language=to_language
            )
        ]

    def translate(
        self,
        text: str,
        from_language: dict,
        to_language: dict
    ):
        for client in self.get_supported_clients(
            from_language=from_language,
            to_language=to_language
        ):
            try:
                translated_text = client.translate(
                    text=text,
                    from_language=from_language,
                    to_language=to_language
                )
                return translated_text
            except Exception as e:
                logger.exception(e)
                continue

        raise Exception("No clients were able to complete the translation")

    def translate_batch(
        self,
        texts: T.List[str],
        from_language: dict,
        to_language: dict
    ):
        for client in self.get_supported_clients(
            from_language=from_language,
            to_language=to_language
        ):
            try:
                translated_text = client.translate_batch(
                    texts=texts,
                    from_language=from_language,
                    to_language=to_language
                )
                return translated_text
            except Exception as e:
                logger.exception(e)
                continue

        raise Exception("No clients were able to complete the translation")
