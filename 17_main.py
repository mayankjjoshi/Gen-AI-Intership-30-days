# tool calling 

import os , json
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

menu = {
    "kajusev":180,
    "sevtameta":80,
    "lasniyasak":120,
    "sukibhaji":100,
    "dahithikari":140,
    "dalrice":130,
    "bajrerotla":30,
    "rotli":12,
    "chass":30,
    "taree":10
}

# create tool 

def get_menu():
    res = []
    for item in menu:
        # print(f"{item} - {menu[item]}")
        res.append(f"{item} - {menu[item]}")
    return res

# print(get_menu())
# tool schema

tools = [
    {
        "type":"function",
        "function":{
            "name":"get_menu",
            "description":"get menu of items with price",
            "parameters":{
                "type":"object",
                "properties":{}
            }
        }
    }
]

user_input = input("BOT : ")

messages = [
    {
        "role":"user",
        "content":user_input,
    }
]

msg = client.chat.complete(
    model="mistral-small-latest",
    temperature=0.2,
    messages=messages,
    tools=tools,
    tool_choice="auto",
)

response = msg.choices[0].message

if response.tool_calls:
    messages.append(response)
    for tc in response.tool_calls:
        # print(tc)
        if tc.function.name == "get_menu":
            result = get_menu()
        formatted_result =  json.dumps(result)
        messages.append(
            {
                "role":"tool",
                "content":formatted_result,
                "tool_call_id":tc.id
            }
        )

    # print(messages)
    final = client.chat.complete(
        model="mistral-small-latest",
        temperature=0.2,
        messages=messages
    )

    print(final.choices[0].message.content)

else:
    print(response.content)
