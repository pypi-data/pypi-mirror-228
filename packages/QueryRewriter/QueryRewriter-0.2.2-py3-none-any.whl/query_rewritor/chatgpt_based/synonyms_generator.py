import os
import openai

TEMPLATE = """Generate a JSON dict like {"keyword": ["synonyms"]} comprising the most important keywords extracted from the following query and their most associated synonyms. The query : "$$QUERY$$". Do not provide any further information. If there are no keywords, answer {}."""

class Synonyms_generator:
    def __init__(self, openai_api_key = ""):
        if openai_api_key != "":
            openai.api_key = openai_api_key
        else:
            openai.api_key = os.getenv("OPENAI_API_KEY")
    def generate(self, query = ""):
        prompt = TEMPLATE.replace("$$QUERY$$", query)
        # print(prompt)
        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
        ]
        )
        return eval(completion.choices[0].message["content"])

