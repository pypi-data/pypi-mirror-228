# Hubspot-Article-Translator
Auto translation of Hubspot Knowledgebase Articles powered by Selenium

## Important Disclaimer
This application only performs upserts to **DRAFT** articles. It will never modify an article that is published.

## Demo Videos
https://github.com/noodle-factory/Hubspot-Article-Translator/assets/53892067/da218794-033d-45fd-9d80-330ca62ba9d5

## Installation
1. Install Google Chrome; This module depends on a chrome driver, so selenium can leverage off of it.
2. `pip install hubspot-Article-Translator`

## How to use module
### Configuring Translation APIs
#### AWS API
```python
import boto3
from hubspot_article_translator import translation_manager, AWSTranslateClient


if __name__ == "__main__":
    # Setup Translation Client/s
    boto3.setup_default_session()
    translation_manager.add_clients(
        AWSTranslateClient(
            aws_session=boto3.DEFAULT_SESSION
        )
    )
```

#### Azure API
```python
from hubspot_article_translator import translation_manager, AzureTranslateClient


if __name__ == "__main__":
    # Setup Translation Client/s
    translation_manager.add_clients(
        AzureTranslateClient(
            key="<AZURE_TRANSLATE_KEY>",
            location="<AZURE_TRANSLATE_LOCATION>",
            endpoint="<AZURE_TRANSLATE_ENDPOINT>",
            api_version="<AZURE_TRANSLATE_API_VERSION>"
        )
    )
```

### Executing the translation workflow
```python
import boto3
from selenium import webdriver
from hubspot_article_translator import State, workflow, translation_manager, AWSTranslateClient, AzureTranslateClient


if __name__ == "__main__":
    # Create the selenium Chrome driver
    driver = webdriver.Chrome()

    # Execute the workflow, passing parameters into State object
    workflow.execute(
        driver=driver,
        state=State(
            # Your Hubspot Account Email
            email="<HUBSPOT EMAIL>",

            # Your Hubspot Account Password
            password="<HUBSPOT PASSWORD>",

            # 2FA code from Authenticator App
            code="<HUBSPOT 2FA CODE>",

            # List of article IDs to translate
            article_ids=["<ID OF ARTICLE TO TRANSLATE>", ...],

            # The ID of the knowledge base that the above articles are in
            knowledge_base_id="<ID OF THE KNOWLEDGE BASE>",

            # the source language of articles
            from_language="en",

            # the languages each article will be translated to
            # make sure key aligns with content language codes
            # https://github.com/noodle-factory/Hubspot-Article-Translator/blob/master/hubspot_article_translator/translation/content_languages/content_languages.json
            # make sure value is exactly the name of the language in Hubspot
            to_languages={
                "es": "Spanish",
                "pt-pt": "Portuguese - Portugal",
                "id": "Indonesian"
            },

            # Automatically publish the article once translation is done
            # Note ensure that you have setup all the knowledge base category translations for each language...
            # Otherwise you won't be able to publish the articles
            auto_publish=True|False 
        )
    )

    # Close the selenium Driver
    driver.quit()
```

## Tips & tricks
### Getting all the article IDs
It would be time consuming to get all the article IDs from each page manually. Instead, navigate to the knowledge base articles page, then open the console and paste this command
```js
[...document.querySelectorAll('[data-test-object-id]')].map(e => e.getAttribute('data-test-object-id')).join("|")
```

## Known Limitations
1. This hasn't been tested with other browsers, it will likely only work with Chrome currently
2. The account must be configured with 2FA through the authenticator app, and not a mobile phone number
