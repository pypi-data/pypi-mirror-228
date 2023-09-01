import httpx

_default_url = "http://localhost:8000/nlp-call"

def set_url(url):
    global _default_url
    _default_url = url

async def call_module_async(module_id, auth_token, input_data, url=None):
    if url is None:
        url = _default_url

    data = {
        "module_id": module_id,
        "auth_token": auth_token,
        "input": input_data
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data)

        if response.status_code == 200:
            result = response.json()
            return result
        else:
            response.raise_for_status()

def call_module(module_id, user_id, input_data, url=None):
    import asyncio

    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(call_module_async(module_id, user_id, input_data, url))
    return result
