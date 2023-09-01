# Description: This file implements a wrapper for the AI Chatbot API.
# Author: Shibo Li, MiQroEra Inc
# Date: 2023-08-30
# Version: v0.1


import threading
import base64
import hashlib
import hmac
import json
from urllib.parse import urlparse, urlencode
from datetime import datetime
from time import mktime
from wsgiref.handlers import format_date_time
import websocket
from .api_utils import gen_params
from .error_codes import get_error_message


class ChatbotClient:
    """
    ChatbotClient is a wrapper for the AI Chatbot API.
    """

    def __init__(self, appid, api_key, api_secret, spark_url, domain):
        """
        :param appid: The appid of the AI Chatbot API.
        :param api_key: The api_key of the AI Chatbot API.
        :param api_secret: The api_secret of the AI Chatbot API.
        :param spark_url: The spark_url of the AI Chatbot API.
        :param domain: The domain of the AI Chatbot API.
        """
        self.appid = appid
        self.api_key = api_key
        self.api_secret = api_secret
        self.spark_url = spark_url
        self.domain = domain
        self.answer = ""
        self.ws_param = self.Ws_Param(appid, api_key, api_secret, spark_url)
        self.usage_questions_tokens = 0
        self.usage_prompt_tokens = 0
        self.usage_completion_tokens = 0
        self.usage_total = 0

    class Ws_Param:
        """
        Ws_Param is a wrapper for the websocket parameters.
        """

        def __init__(self, APPID, APIKey, APISecret, Spark_url):
            self.APPID = APPID
            self.APIKey = APIKey
            self.APISecret = APISecret
            self.host = urlparse(Spark_url).netloc
            self.path = urlparse(Spark_url).path
            self.Spark_url = Spark_url

        def create_url(self):
            """
            The method is to create the url for the websocket.
            :return: The url for the websocket.
            """
            now = datetime.now()
            date = format_date_time(mktime(now.timetuple()))

            signature_origin = f"host: {self.host}\ndate: {date}\nGET {self.path} HTTP/1.1"
            signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                     digestmod=hashlib.sha256).digest()
            signature_sha_base64 = base64.b64encode(
                signature_sha).decode(encoding='utf-8')

            authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'
            authorization = base64.b64encode(
                authorization_origin.encode('utf-8')).decode(encoding='utf-8')

            v = {
                "authorization": authorization,
                "date": date,
                "host": self.host
            }
            url = self.Spark_url + '?' + urlencode(v)
            return url

    def on_message(self, ws, message):
        """
        The method is to handle the message received from the websocket.
        :param ws: The websocket object.
        :param message: The message received from the websocket.
        :return: None
        """
        data = json.loads(message)
        code = data['header']['code']
        if code != 0:
            error_message = get_error_message(code)
            print(f'请求错误: {code}, {error_message}')
            ws.close()
        else:
            choices = data["payload"]["choices"]
            status = choices["status"]
            content = choices["text"][0]["content"]
            self.answer += content
            if 'usage' in data['payload']:
                question_tokens = data['payload']['usage']['text']['question_tokens']
                prompt_tokens = data['payload']['usage']['text']['prompt_tokens']
                completion_tokens = data['payload']['usage']['text']['completion_tokens']
                total_tokens = data['payload']['usage']['text']['total_tokens']
                self.usage_questions_tokens += question_tokens
                self.usage_prompt_tokens += prompt_tokens
                self.usage_completion_tokens += completion_tokens
                self.usage_total += total_tokens
                if status == 2:
                    ws.close()

    def on_error(self, ws, error):
        print("### error:", error)

    @staticmethod
    def on_close(ws, one, two):
        # print("")
        pass

    def on_open(self, ws):
        threading.Thread(target=self.run, args=(ws,)).start()

    def run(self, ws):
        data = json.dumps(gen_params(
            appid=self.appid,
            domain=self.domain,
            question=ws.question,
            temperature=ws.temperature,
            max_tokens=ws.max_tokens
        )
        )
        ws.send(data)

    def get_response(self, question, temperature=0.5, max_tokens=2048):
        """
        The method is to get the response from the AI Chatbot API.
        :param question: The question to be asked.
        :param temperature: The temperature of the AI Chatbot API.
        :param max_tokens: The max_tokens of the AI Chatbot API.
        :return: The response from the AI Chatbot API.
        """
        self.answer = ""

        if not question.strip():
            print("请您输入有效内容。")
            return

        websocket.enableTrace(False)
        ws_url = self.ws_param.create_url()
        ws = websocket.WebSocketApp(
            ws_url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        ws.appid = self.appid
        ws.domain = self.domain
        ws.question = question
        ws.temperature = temperature or 0.7  # default 0.7
        ws.max_tokens = max_tokens or 4096   # default 4096
        ws.on_open = self.on_open
        threading.Timer(10, ws.close).start()
        ws.run_forever()
        return self.answer