import openai
import json
import time

class GPTHandler:
    def __init__(self, api_key):
        self.api_key = api_key
        self.credits_used = 0
        self.credits_limit = 10000  # Example limit for tracking
        self.cache = {}
        self.variations = {
            'event1': ["Description A1", "Description A2", "Description A3", "Description A4", "Description A5"],
            'event2': ["Description B1", "Description B2", "Description B3", "Description B4", "Description B5"],
            'event3': ["Description C1", "Description C2", "Description C3", "Description C4", "Description C5"],
            'event4': ["Description D1", "Description D2", "Description D3", "Description D4", "Description D5"],
            'event5': ["Description E1", "Description E2", "Description E3", "Description E4", "Description E5"]
        }

    def call_api(self, prompt):
        if self.credits_used >= self.credits_limit:
            return "Credit limit reached. Please try again later."
        if prompt in self.cache:
            return self.cache[prompt]

        # Call to OpenAI API
        openai.api_key = self.api_key
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': prompt}]
        )

        # Check for successful response
        if response:
            self.credits_used += response['usage']['total_tokens']
            self.cache[prompt] = response['choices'][0]['message']['content']
            return self.cache[prompt]
        return "API call failed."

    def get_fallback_description(self, event):
        return self.variations.get(event, ["Default description"])[0]

    def get_template_based_description(self, person_attributes):
        templates = [
            "{name} is a {profession} from {location}.",
            "Meet {name}, a {age}-year-old {profession} living in {location}.",
            "{name}, the {profession}, hails from {location}.",
            "A {profession} named {name} who is {age} years old from {location}.",
            "Introducing {name}, a {profession} aged {age} from {location}."
        ]
        import random
        template = random.choice(templates)
        return template.format(**person_attributes)

    def reset_credits(self):
        self.credits_used = 0

    def cache_status(self):
        return f"Cache size: {len(self.cache)} entries."