import httpx
import re
import json

BASE_URL = "https://www.youtube.com/results?search_query="
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

async def search_youtube(query: str, limit: int = 1):
    url = BASE_URL + query.replace(" ", "+")
    print(f"Searching: {url}")

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(url, headers=HEADERS)
            if r.status_code != 200:
                print(f"Error: Received status code {r.status_code}")
                return []

            print("Status Code:", r.status_code)

            # More reliable pattern to find ytInitialData
            match = re.search(r"var ytInitialData = ({.*?});", r.text) or \
                    re.search(r'window\["ytInitialData"\]\s*=\s*({.*?});', r.text)

            if not match:
                print("ytInitialData not found in response")
                return []

            try:
                data = json.loads(match.group(1))
            except Exception as e:
                print("JSON parsing error:", e)
                return []

            try:
                results = []
                # Navigate to the video results section
                videos = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]\
                    ["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]

                for item in videos:
                    video_data = item.get("videoRenderer")
                    if not video_data:
                        continue

                    title = video_data.get("title", {}).get("runs", [{}])[0].get("text", "Unknown Title")
                    video_id = video_data.get("videoId")
                    if not video_id:
                        continue

                    url = f"https://www.youtube.com/watch?v={video_id}"
                    results.append({"title": title, "url": url})
                    if len(results) >= limit:
                        break

                return results
            except Exception as e:
                print("Parsing error:", e)
                return []

    except httpx.RequestError as e:
        print(f"Request error: {e}")
        return []


