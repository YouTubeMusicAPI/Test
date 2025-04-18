import httpx
from selectolax.parser import HTMLParser

MOBILE_URL = "https://m.youtube.com/results?search_query="

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Linux; Android 10; Pixel 5) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Mobile Safari/537.36"
    )
}

async def search_youtube(query: str, limit: int = 5):
    url = MOBILE_URL + query.replace(" ", "+")
    print(f"Searching: {url}")

    async with httpx.AsyncClient(timeout=5) as client:
        r = await client.get(url, headers=HEADERS)
        print("Status Code:", r.status_code)

        html = HTMLParser(r.text)
        results = []

        for a in html.css("a"):
            href = a.attributes.get("href", "")
            if not href.startswith("/watch"):
                continue

            # Title may be wrapped inside span/div
            title = a.text(strip=True)
            if not title:
                span = a.css_first("span")
                if span:
                    title = span.text(strip=True)

            if not title:
                continue

            video_url = f"https://www.youtube.com{href}"
            results.append({"title": title, "url": video_url})
            print(f"[FOUND] {title} -> {video_url}")

            if len(results) >= limit:
                break

        return results
