from ddgs import DDGS
# ddgs = DDGS()
# results = ddgs.text("Anand Mercantile College Of Science And Technology", max_results=3)
# print(results)

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
    return json.dumps(res)

def web_search(query):
    ddgs = DDGS()
    results = ddgs.text(query, max_results=3)
    if results:
        text = ""
        for result in results:
            text = result['body'] + "/n"
        return text
    else:
        return f"{query} not found"

# web_search("Kismat Kathiywadi")

# print(get_menu())

def price(item):
    if item in menu:
        return f"{item} cost {menu[item]}"
    else:
        return "Item not found"

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
    },
    {
        "type":"function",
        "function":{
            "name":"web_search",
            "description":"Search on web based on any topic which provide through user query",
            "parameters":{
                "type":"object",
                "properties":{
                    "query":{
                    "type":"string",
                    "description":"string query to search on web"
                    }
                },
                "required":["query"]
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"price",
            "description":"Show price of particular dish from menu",
            "parameters":{
                "type":"object",
                "properties":{
                    "item":{
                    "type":"string",
                    "description":"item to search price on menu"
                    }
                },
                "required":["query"]
            }
        }
    },
]

# dispatcher 

def tool_call(name, args):
    if name == "get_menu":
        return get_menu()
    elif name == "web_search":
        return web_search(args["query"])
    elif name == "price":
        return price(args["item"])
    else:
        return "Tool not found"


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
        # if tc.function.name == "get_menu":
        #     result = get_menu()
        # formatted_result =  json.dumps(result)
        print(f"Tool Used : {tc.function.name}")
        print(f"Arguments Used : {tc.function.arguments}")
        
        args = json.loads(tc.function.arguments)
        result = tool_call(tc.function.name,args)
        print("Tool Calling and O/P : ")
        print(f"TOOL NAME : {tc.function.name} => O/P : {result}")
        messages.append(
            {
                "role":"tool",
                "content":result,
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
