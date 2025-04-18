import httpx
from selectolax.parser import HTMLParser

YOUTUBE_SEARCH_URL = "https://www.youtube.com/results?search_query="

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Mobile Safari/537.36"
}

async def search_youtube(query: str, limit: int = 5):
    search_url = YOUTUBE_SEARCH_URL + query.replace(" ", "+")
    print(f"Searching: {search_url}")  # Debug URL

    async with httpx.AsyncClient(timeout=5) as client:
        response = await client.get(search_url, headers=HEADERS)
        print(f"Status Code: {response.status_code}")  # Debug response
        html = HTMLParser(response.text)

        results = []
        for node in html.css("a"):
            href = node.attributes.get("href", "")
            title = node.text(strip=True)
            if "/watch?" in href and title:
                print(f"[FOUND] {title} -> {href}")  # Debug each result
                results.append({
                    "title": title,
                    "url": f"https://www.youtube.com{href}"
                })

            if len(results) >= limit:
                break
        return results
