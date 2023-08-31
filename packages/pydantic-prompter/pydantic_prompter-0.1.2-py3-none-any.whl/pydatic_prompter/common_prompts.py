from models.recommendation import (
    RecommendationResults,
    QueryGPTResponse,
    QuestionGPTResponse,
    RecommendationTitleResponse,
)
from prompts.prompter import Prompter


@Prompter(llm="openai", jinja=True, model_name="gpt-3.5-turbo-16k")
def rank_recommendation_entries(json_entries) -> RecommendationResults:
    """
    >> user: >
        Which of the following JSON entries fit best to the query. order by best fit descending
        Base your answer ONLY on the given YML entries, if you are not sure, or there are no entries

    >> user: >
        The JSON entries:
        {{ json_entries }}

    >> user: {{ user_query }}

    """


@Prompter(llm="openai", jinja=True, model_name="gpt-3.5-turbo")
def search_query(history) -> QueryGPTResponse:
    """
    {{ history }}

    >> user: |
        Generate a Google-like search query text encompassing all previous chat questions and answers
    """


@Prompter(llm="openai", jinja=True, model_name="gpt-3.5-turbo")
def ask_questions(history) -> QuestionGPTResponse:
    """
    >> user: |
        I want to watch something, ask me 1 short question with 2-4 answers, the last answer should be a default
        answer, to try and figure out what I want to watch.
        use simple language.
        Don't ask about specific actor.
        Don't ask about specific movie.
        Don't ask about specific publisher.
        Never ask the same question more than once.
        feel free to be as creative as you can.

    {{ history }}
    """


@Prompter(llm="openai", jinja=True, model_name="gpt-3.5-turbo-16k")
def recommendation_title(json_entries) -> RecommendationTitleResponse:
    """
    >> user: >
        Based on the JSON entries, suggest a minimum 4 words and maximum 6 words title

    >> user: >
        The JSON entries:
        {{ json_entries }}

    """


def text_service_prompt(pydantic_return_cls):
    @Prompter(llm="openai", jinja=True, model_name="gpt-3.5-turbo")
    def _text_service_prompt(
        text, char_limit, formal_style, content_type
    ) -> pydantic_return_cls:
        """
        >> system: You are a talented {{ content_type }} generator
        >> system: |
            You are permitted generate up to {{ char_limit }} characters.
            no more than {{ char_limit }} characters
        >> user: >
            create a {{ content_type }} in {{ formal_style }} style to the following context:
            ###
            {{ text }}
            ###

        """

    return _text_service_prompt


if __name__ == "__main__":
    import logging

    logging.basicConfig()
