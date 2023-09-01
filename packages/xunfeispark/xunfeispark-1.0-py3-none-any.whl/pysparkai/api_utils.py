# Description: This file implements a wrapper for the AI Chatbot API.
# Author: Shibo Li, MiQroEra Inc
# Date: 2023-08-30
# Version: v0.1


def gen_params(appid, domain, question, uid="1234", temperature=0.5, max_tokens=2048, top_k=4, chat_id=None,
               previous_chats=[]):
    """
    Generate parameters for the API request.
    """
    data = {
        "header": {
            "app_id": appid,
            "uid": uid
        },
        "parameter": {
            "chat": {
                "domain": domain,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_k": top_k
            }
        },
        "payload": {
            "message": {
                "text": [{"role": "user", "content": question}]
            }
        }
    }

    if chat_id:
        data["parameter"]["chat"]["chat_id"] = chat_id

    return data