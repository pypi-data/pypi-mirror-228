import typing as T

from concurrent.futures import ThreadPoolExecutor, as_completed


class BaseTranslationClient(object):

    def __init__(
        self,
        content_language_key: str
    ) -> None:
        self.content_language_key = content_language_key

    def _raise_not_supported_exception(
        self,
        from_language: dict,
        to_language: dict
    ):
        raise Exception(f"{from_language['code']} or {to_language['code']} is not supported")

    def supports_translation(
        self,
        from_language: dict,
        to_language: dict,
        raise_exception: bool = False
    ) -> bool:
        if not (
            from_language.get(self.content_language_key) and
            to_language.get(self.content_language_key)
        ):
            if raise_exception:
                self._raise_not_supported_exception(
                    from_language=from_language,
                    to_language=to_language
                )
            return False
        return True

    def translate(
        self,
        text: str,
        from_language: dict,
        to_language: dict
    ):
        if not text:
            return ""

        self.supports_translation(
            from_language=from_language,
            to_language=to_language,
            raise_exception=True
        )

        return self._translate(
            text=text,
            from_language_code=from_language[self.content_language_key],
            to_language_code=to_language[self.content_language_key]
        )

    def translate_batch(
        self,
        texts: T.List[str],
        from_language: dict,
        to_language: dict
    ):
        self.supports_translation(
            from_language=from_language,
            to_language=to_language,
            raise_exception=True
        )

        try:
            return self._translate_batch(
                texts=texts,
                from_language_code=from_language[self.content_language_key],
                to_language_code=to_language[self.content_language_key]
            )
        except NotImplementedError:
            pass

        # default optimised batch processing
        translations = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            for result in executor.map(
                self._translate,
                texts,
                [from_language[self.content_language_key]] * len(texts),
                [to_language[self.content_language_key]] * len(texts),
            ):
                translations.append(result)
        return translations

    def _translate(
        self,
        text: str,
        from_language_code: str,
        to_language_code: str
    ):
        raise NotImplementedError()

    def _translate_batch(
        self,
        texts: T.List[str],
        from_language_code: str,
        to_language_code: str
    ):
        raise NotImplementedError()
