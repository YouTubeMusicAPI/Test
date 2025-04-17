import aiohttp
from bs4 import BeautifulSoup
from .Models import YouTubeResult
import asyncio

async def search_duckduckgo(query: str):
    search_url = f"https://duckduckgo.com/html/?q=site:youtube.com+{query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(search_url, headers=headers) as response:
            html = await response.text()
            print(f"Raw HTML: {html[:500]}...")  # Print first 500 chars for debugging
            return html


def parse_results(html: str):
    soup = BeautifulSoup(html, 'html.parser')
    results = []

    # Look for links containing 'result__a' class (DuckDuckGo's result links)
    for a_tag in soup.find_all('a', class_='result__a'):
        title = a_tag.get_text()
        url = a_tag.get('href')

        if "youtube.com/watch" in url:
            results.append(YouTubeResult(title=title, url=f"https://www.youtube.com{url}"))

    return results


async def Search(query: str):
    html = await search_duckduckgo(query)
    results = parse_results(html)

    if not results:
        print(f"No results found for '{query}'")
    else:
        print(f"Found {len(results)} results")
    
    return results
