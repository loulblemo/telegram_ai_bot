import openai
import json

openai.api_key = json.load(open("auth.json", 'rb'))["openai_key"]
chat_model = "gpt-4o-mini"

def chat(messages):

    response = openai.chat.completions.create(
        model=chat_model,
        messages=messages,
        max_tokens=200, 
        temperature=0.8,
        top_p=0.5
    )

    return response.choices[0].message.content


def reply(message):

    bot_names = ["@davinci_ai_telegram_bot", "Leo", "Leonardo"]

    if any(name in message.lower() for name in bot_names):

        system_prompt1 = f"""
IDENTITY:

You are Leonardo Da Vinci, the famous Italian inventor. When you reply to messages you always reply like if you where Leonardo Da Vinci and never break character, no matters what the content of the message is.

Your task is to reply or comment to the last message with a short thought provoking message in the style of Leonardo Da Vinci.

Always reply in the same language as the input message.
"""

    prompt = f"""

the message that was sent to you message:

'''
{message} 
'''

Your thought provoking reply:
"""

    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]

    return chat(messages)