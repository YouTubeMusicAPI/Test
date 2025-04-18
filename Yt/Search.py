import httpx
import re
import json

def search_youtube_fastest(query: str, limit: int = 5):
    url = f"https://m.youtube.com/results?search_query={query.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36",
    }

    with httpx.Client(http2=True, timeout=3.0) as client:
        response = client.get(url, headers=headers)

    # Fastest regex way to extract ytInitialData
    match = re.search(r"var ytInitialData = ({.*?});", response.text)
    if not match:
        return []

    try:
        data = json.loads(match.group(1))
        videos = []
        sections = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"]
        for sec in sections:
            items = sec.get("itemSectionRenderer", {}).get("contents", [])
            for item in items:
                video = item.get("videoRenderer")
                if video:
                    title = "".join([t.get("text", "") for t in video["title"]["runs"]])
                    video_id = video["videoId"]
                    url = f"https://www.youtube.com/watch?v={video_id}"
                    videos.append({"title": title, "url": url})
                if len(videos) >= limit:
                    break
            if len(videos) >= limit:
                break
        return videos
    except Exception as e:
        return []
