"""Utility script to seed target mock values directly into Redis"""

import asyncio
import json

from redis.asyncio import Redis

api_definition_payload = {
    "id": "demo",
    "routes": [
        {
            "path": "api/v1/inventory",
            "methods": ["GET"],
            "schema": {
                "type": "object",
                "properties": {
                    "sku": {"type": "str"},
                    "name": {"type": "str"},
                    "quantity": {"type": "int"},
                },
            },
            "behaviours": {"GET": {"action": "decrement", "field": "stock"}},
        }
    ],
}

inventory_state = [
    {"sku": "SKU-992", "name": "Wireless Mouse", "quantity": 42},
    {"sku": "SKU-104", "name": "Mechanical Keyboard", "quantity": 15},
]


async def seed():
    r = Redis(host="localhost", port=6379, decode_responses=True)

    await r.set("api_definition:demo", json.dumps(api_definition_payload))

    await r.set("mock_state:demo:api/v1/inventory", json.dumps(inventory_state))

    print("Database seeding completed")
    await r.aclose()


if __name__ == "__main__":
    asyncio.run(seed())
