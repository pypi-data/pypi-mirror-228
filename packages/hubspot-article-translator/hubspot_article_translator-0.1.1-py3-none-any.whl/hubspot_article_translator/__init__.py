from .translation import *
from .core import (
    State,
    Action,
    LoginAction,
    CaptureArticleAction,
    TranslateArticleAction,
    NavigateToArticleAction,
    ActionBranch
)


workflow = Action(
    LoginAction(),
    ActionBranch(
        NavigateToArticleAction(),
        CaptureArticleAction(),
        TranslateArticleAction(),
        read_key="article_ids",
        write_key="article_id",
    )
)
