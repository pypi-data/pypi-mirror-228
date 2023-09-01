from typing import TypedDict


class TextModelSettings(TypedDict, total=False):
    """
    Change these settings to tweak the model's behavior.

    Heavily inspired by https://platform.openai.com/docs/api-reference/completions/create
    """

    max_tokens: int  # defaults to inf
    temperature: float  # ValueRange(0, 2)
    top_p: float  # ValueRange(0, 1)
    logit_bias: dict[int, int]  # valmap(ValueRange(-100, 100))
    stop: list[str]  # MaxLen(4)
    n: int  # defaults to 1
