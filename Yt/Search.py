import httpx
import re
import json

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

        if "ytInitialData" not in r.text:
            print("ytInitialData not found in response")
            return []

        data_raw = re.search(r"var ytInitialData = ({.*?});</script>", r.text)
        if not data_raw:
            print("ytInitialData regex failed")
            return []

        try:
            data = json.loads(data_raw.group(1))
        except Exception as e:
            print("Failed to parse JSON:", e)
            return []

        # Traverse YouTube response data
        try:
            results = []
            videos = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]\
                ["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]

            for video in videos:
                video_data = video.get("videoRenderer")
                if not video_data:
                    continue

                video_id = video_data.get("videoId")
                title_runs = video_data.get("title", {}).get("runs", [])
                if not title_runs:
                    continue

                title = title_runs[0]["text"]
                url = f"https://www.youtube.com/watch?v={video_id}"

                results.append({"title": title, "url": url})
                if len(results) >= limit:
                    break

            return results

        except Exception as e:
            print("Error parsing results:", e)
            return []
