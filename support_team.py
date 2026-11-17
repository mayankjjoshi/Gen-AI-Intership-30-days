
import os
import json

from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

# --------------------------------
# COMPANY DATABASE (DEMO)
# --------------------------------

orders = {
    "ORD101": "Shipped - arriving tomorrow",
    "ORD102": "Processing - ships in 2 days"
}

menu = {
    "pizza": 299,
    "pasta": 349,
    "coke": 60
}


# --------------------------------
# TOOLS
# --------------------------------

def track_order(order_id):
    order_id = order_id.upper()

    if order_id in orders:
        return orders[order_id]

    return "Order not found."


def get_menu():
    result = ""

    for k, v in menu.items():
        result += k + " - Rs " + str(v) + "\n"

    return result


def check_price(item):
    item = item.lower()

    if item in menu:
        return item + " costs Rs " + str(menu[item])

    return item + " not on menu"


# --------------------------------
# TOOL EXECUTOR
# --------------------------------

def run_tool(name, args):

    if name == "track_order":
        return track_order(args["order_id"])

    elif name == "get_menu":
        return get_menu()

    elif name == "check_price":
        return check_price(args["item"])

    else:
        return "Unknown tool"


# --------------------------------
# ORDER TOOLS
# --------------------------------

order_tools = [
    {
        "type": "function",
        "function": {
            "name": "track_order",
            "description": "Track an order by its ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "e.g. ORD101"
                    }
                },
                "required": ["order_id"]
            }
        }
    }
]


# --------------------------------
# MENU TOOLS
# --------------------------------

menu_tools = [
    {
        "type": "function",
        "function": {
            "name": "get_menu",
            "description": "Get the full menu with prices",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_price",
            "description": "Get the price of a dish",
            "parameters": {
                "type": "object",
                "properties": {
                    "item": {
                        "type": "string",
                        "description": "Dish name"
                    }
                },
                "required": ["item"]
            }
        }
    }
]


# --------------------------------
# SPECIALIST AGENT
# --------------------------------

def run_specialist(system_prompt, query, tools):

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": query
        }
    ]

    response = client.chat.complete(
        model="mistral-small-latest",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    msg = response.choices[0].message

    if msg.tool_calls:

        # Preserve assistant tool-call message
        messages.append(msg)

        for tc in msg.tool_calls:

            args = json.loads(tc.function.arguments)

            result = run_tool(
                tc.function.name,
                args
            )

            print(f"{tc.function.name} => {result}")

            messages.append({
                "role": "tool",
                "name": tc.function.name,
                "content": str(result),
                "tool_call_id": tc.id
            })

        final = client.chat.complete(
            model="mistral-small-latest",
            messages=messages
        )

        return final.choices[0].message.content

    return msg.content


# --------------------------------
# ROUTER AGENT
# --------------------------------

def route(query):

    r = client.chat.complete(
        model="mistral-small-latest",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": """
                You are a query router.

                Reply with ONE word only:

                order   - Order tracking and delivery questions.
                menu    - Food menu and price questions.
                general - Everything else.
                """
            },
            {
                "role": "user",
                "content": query
            }
        ]
    )

    return r.choices[0].message.content.strip().lower()


# --------------------------------
# MAIN APPLICATION
# --------------------------------

query = input("Customer: ")

category = route(query)

print(f"Routed to: {category} Agent")


if category == "order":

    answer = run_specialist(
        "You are a polite order support agent. Use the track_order tool to help customers.",
        query,
        order_tools
    )

elif category == "menu":

    answer = run_specialist(
        "You are a friendly menu assistant. Use get_menu and check_price to help customers.",
        query,
        menu_tools
    )

else:

    answer = run_specialist(
        "You are a helpful support agent. Answer the customer politely.",
        query,
        []
    )


print("Support:", answer)
