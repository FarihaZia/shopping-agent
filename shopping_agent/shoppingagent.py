# shopping_agent_simple.py

from agents import Agent, Runner, function_tool
from connection import config
import requests
from datetime import datetime
import rich


API_URL = "https://template-03-api.vercel.app/api/products"


@function_tool
def get_all_products() -> list:
    response = requests.get(API_URL)
    data = response.json().get("data", [])
    
    
    result = []
    for item in data:
        result.append({
            "name": item["productName"],
            "price": item["price"],
            "category": item["category"]
        })
    return result


@function_tool
def search_products(keyword: str) -> list:
    response = requests.get(API_URL)
    data = response.json().get("data", [])
    
    keyword = keyword.lower()
    result = []

    for item in data:
        name = item["productName"].lower()
        desc = item["description"].lower()
        if keyword in name or keyword in desc:
            result.append({
                "name": item["productName"],
                "price": item["price"],
                "category": item["category"]
            })
    
    if not result:
        return [{"message": f"No products found for '{keyword}'"}]
    
    return result


@function_tool
def search_products(query: str) -> list:
    response = requests.get(API_URL)
    data = response.json().get("data", [])
    
    query = query.lower()
    result = []

    for item in data:
        category = item["category"].lower()

        if category in query:
            result.append({
                "name": item["productName"],
                "price": item["price"],
                "category": item["category"]
            })

    
    if not result:
        for item in data:
            if query in item["productName"].lower() or query in item["description"].lower():
                result.append({
                    "name": item["productName"],
                    "price": item["price"],
                    "category": item["category"]
                })

    if not result:
        return [{"message": "No products found."}]
    
    return result


@function_tool
def filter_by_max_price(max_price: int) -> list:
    response = requests.get(API_URL)
    data = response.json().get("data", [])
    
    result = []

    for item in data:
        if item["price"] <= max_price:
            result.append({
                "name": item["productName"],
                "price": item["price"]
            })

    if not result:
        return [{"message": f"No products found under price {max_price}"}]

    return result


agent = Agent(
    name="ShoppingAgent",
    instructions="You are a helpful shopping assistant. You can find, filter, and search for products using different tools.",
    tools=[get_all_products, search_products, search_products, filter_by_max_price]
)


query = "show me men's shoes under 8000"

result = Runner.run_sync(agent, query, run_config=config)

print("Final Output:", result.final_output)
