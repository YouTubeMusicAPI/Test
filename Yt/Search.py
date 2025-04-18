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

    print("Raw HTML Response:")
    print(response.text[:1000])  # Print first 1000 chars to avoid too much output

    # Look for any JavaScript variable containing global data
    match = re.search(r"window\.WIZ_global_data\s*=\s*(\{.*?\});", response.text)
    if not match:
        print("No global data found")
        return []

    try:
        data = json.loads(match.group(1))
        print("Extracted Data:", json.dumps(data, indent=4))  # Print the global data for inspection
        # Process the data further here
        videos = []  # Extract video details from the data if available
        # You'll need to explore the extracted global data structure to find video information.
        return videos
    except Exception as e:
        print(f"Error extracting global data: {e}")
        return []

# Example usage
query = input("Enter search query: ")
videos = search_youtube_fastest(query)

if videos:
    print("Found Videos:")
    for video in videos:
        print(f"Title: {video['title']}")
        print(f"URL: {video['url']}")
else:
    print("No videos found.")
