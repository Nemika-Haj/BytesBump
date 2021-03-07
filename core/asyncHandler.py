import aiohttp

async def get(url, json=True):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return (await response.json()) if json else (await response.text())