from bs4 import BeautifulSoup, NavigableString

from ..content_languages import get_content_language


def translate(
    text: str,
    from_language: str,
    to_language: str
):
    from .. import translation_manager
    return translation_manager.translate(
        text,
        get_content_language(from_language),
        get_content_language(to_language)
    )

def _translateHTML(
    node,
    from_language: str,
    to_language: str
):
    if isinstance(node, NavigableString):
        key = node.string.strip()
        value = node.string
        if key:
            # TODO: Implement your translate function
            value = value.replace(key, translate(key, from_language, to_language))
            node.replace_with(value)
    else:
        for child in node.children:
            _translateHTML(
                child,
                from_language,
                to_language
            )

def translateHTML(
    html: str,
    from_language: str,
    to_language: str
):
    soup = BeautifulSoup(html, "html.parser")
    
    for node in soup.children:
        _translateHTML(
            node,
            from_language,
            to_language
        )

    return str(soup.prettify())
