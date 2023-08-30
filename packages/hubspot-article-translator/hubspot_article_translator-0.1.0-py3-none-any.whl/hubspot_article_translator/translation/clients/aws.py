from boto3.session import Session

from .base import BaseTranslationClient


class AWSTranslateClient(BaseTranslationClient):
    client = None

    def __init__(self, aws_session: Session, **kwargs) -> None:
        super().__init__(
            content_language_key='aws_code'
        )
        self.client = aws_session.client('translate')

    def _translate(
        self,
        text: str,
        from_language_code: str,
        to_language_code: str
    ):
        if not text:
            return ""

        response = self.client.translate_text(
            Text=text,
            SourceLanguageCode=from_language_code,
            TargetLanguageCode=to_language_code,
        )

        if (
            not response or
            not response.get('TranslatedText')
        ):
            raise Exception("Unable to translate text")

        return response['TranslatedText']
