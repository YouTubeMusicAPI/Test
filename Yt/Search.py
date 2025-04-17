import aiohttp
from bs4 import BeautifulSoup
from .Models import YouTubeResult  # Ensure this is correctly imported
import asyncio

async def search_duckduckgo(query: str):
    search_url = f"https://duckduckgo.com/html/?q=site:youtube.com+{query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(search_url, headers=headers) as response:
            html = await response.text()

            # Print the raw HTML to debug the issue
            print(f"Raw HTML: {html[:500]}")  # Print the first 500 characters to check

            return html


def parse_results(html: str):
    soup = BeautifulSoup(html, 'html.parser')
    results = []

    for a_tag in soup.find_all('a', class_='result__a'):
        title = a_tag.get_text()
        url = a_tag.get('href')

        if "youtube.com/watch" in url:
            results.append(YouTubeResult(title=title, url=f"https://www.youtube.com{url}"))

    return results


async def Search(query: str):
    html = await search_duckduckgo(query)
    return parse_results(html)

# Test the search function directly
async def main():
    query = "Chandni"  # Replace with your test query
    results = await Search(query)
    print(f"Results: {results}")

# Running the test
if __name__ == "__main__":
    asyncio.run(main())
