import requests
from bs4 import BeautifulSoup

class YouTubeSearch:
    def __init__(self):
        self.base_url = "https://www.youtube.com/results"

    def search(self, query, max_results=5):
        # YouTube search URL format
        url = f"{self.base_url}?search_query={query}"

        # Send HTTP request
        response = requests.get(url)

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all video elements
        video_results = []
        for video in soup.find_all('a', {'href': True}):
            href = video['href']
            
            if '/watch?v=' in href:  # This is a video
                video_url = f"https://www.youtube.com{href}"
                title = video.get('title')
                
                video_results.append({
                    'title': title,
                    'url': video_url
                })
                
                if len(video_results) >= max_results:
                    break

        return video_results

    def search_playlists(self, query, max_results=5):
        # YouTube search URL format for playlists
        url = f"{self.base_url}?search_query={query}&sp=EgIQAw%253D%253D"  # sp=EgIQAw%253D%253D restricts search to playlists

        # Send HTTP request
        response = requests.get(url)

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all playlist elements
        playlist_results = []
        for video in soup.find_all('a', {'href': True}):
            href = video['href']
            
            if '/playlist?list=' in href:  # This is a playlist
                playlist_url = f"https://www.youtube.com{href}"
                title = video.get('title')
                
                playlist_results.append({
                    'title': title,
                    'url': playlist_url
                })
                
                if len(playlist_results) >= max_results:
                    break

        return playlist_results
