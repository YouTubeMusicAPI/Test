import aiohttp
from bs4 import BeautifulSoup
from .Models import YouTubeResult
import asyncio


async def search_duckduckgo(query: str):
    search_url = f"https://duckduckgo.com/html/?q=site:youtube.com+{query}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(search_url, headers=headers) as response:
                response.raise_for_status()  # Raise exception for bad HTTP responses
                html = await response.text()
                return html
    except aiohttp.ClientError as e:
        print(f"Error while fetching search results: {e}")
        return None


def parse_results(html: str):
    soup = BeautifulSoup(html, 'html.parser')
    results = []

    for a_tag in soup.find_all('a', class_='result__a'):
        title = a_tag.get_text(strip=True)
        url = a_tag.get('href')

        if "youtube.com/watch" in url:
            # Ensure full URL path
            full_url = url if url.startswith("http") else f"https://www.youtube.com{url}"
            results.append(YouTubeResult(title=title, url=full_url))

    return results


async def Search(query: str):
    html = await search_duckduckgo(query)
    
    if html is None:
        return []  # Return an empty list if no HTML was fetched

    return parse_results(html)


# Example usage in an async event loop
if __name__ == "__main__":
    query = "Chandni"
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(Search(query))

    for result in results:
        print(f"Title: {result.title}, URL: {result.url}")
