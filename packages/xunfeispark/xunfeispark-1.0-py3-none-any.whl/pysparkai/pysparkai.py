# Description: SparkAI class for chatbot
# Author: Shibo Li, MiQroEra Inc
# Date: 2023-08-30
# Version: v0.1


import os
from .auth_websocket_client import ChatbotClient


class PySparkAI:
    """
    PySparkAI class for chatbot
    """

    def __init__(self, api_key, api_secret, app_id, spark_url, domain):
        self.API_KEY = api_key or os.getenv("SPARK_AI_API_KEY")
        self.API_SECRET = api_secret or os.getenv("SPARK_AI_API_SECRET")
        self.APP_ID = app_id or os.getenv("SPARK_AI_APP_ID")
        self.SPARK_URL = spark_url or os.getenv("SPARK_AI_SPARK_URL")
        self.domain = domain or os.getenv("SPARK_AI_DOMAIN")

        # Initialize the client
        self.client = ChatbotClient(
            self.APP_ID, self.API_KEY, self.API_SECRET, self.SPARK_URL, self.domain)

    def chat(self, messages, temperature=None, max_tokens=None):
        """
        The method is to define a chatbot.
        :param messages: The messages of the chatbot.
        :param temperature: The temperature of the chatbot.
        :param max_tokens: The max_tokens of the chatbot.
        :return: The response of the chatbot.
        """
        user_input = messages[-1]["content"]
        response = self.client.get_response(
            user_input, temperature=temperature, max_tokens=max_tokens)
        response_message = {
            "message": response,
            "role": "assistant"
        }
        token_counts = {
            'question_tokens': self.client.usage_questions_tokens,
            'prompt_tokens': self.client.usage_prompt_tokens,
            'completion_tokens': self.client.usage_completion_tokens,
            'total_tokens': self.client.usage_total
        }
        return {
            "choices": [response_message],
            "usage": token_counts
        }