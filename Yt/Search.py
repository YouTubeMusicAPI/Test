import requests
from bs4 import BeautifulSoup

class YouTubeSearch:
    def __init__(self):
        self.base_url = 'https://www.youtube.com/results?search_query='
    
    def search(self, query, max_results=5):
        search_url = f"{self.base_url}{query}"
        response = requests.get(search_url)
        
        # Print the raw HTML to inspect
        print("Raw HTML:\n", response.text[:1000])  # Print first 1000 characters of HTML

        soup = BeautifulSoup(response.text, 'html.parser')
        videos = []

        for video in soup.find_all('a', {'class': 'yt-uix-tile-link'}):
            title = video.get('title')
            url = f"https://www.youtube.com{video.get('href')}"
            videos.append({'title': title, 'url': url})

            if len(videos) >= max_results:
                break
        
        return videos
    
    def search_playlists(self, query, max_results=5):
        search_url = f"https://www.youtube.com/results?search_query={query}+playlist"
        response = requests.get(search_url)
        
        # Print the raw HTML to inspect
        print("Raw HTML:\n", response.text[:1000])  # Print first 1000 characters of HTML
        
        soup = BeautifulSoup(response.text, 'html.parser')
        playlists = []

        for playlist in soup.find_all('a', {'class': 'yt-uix-tile-link'}):
            title = playlist.get('title')
            url = f"https://www.youtube.com{playlist.get('href')}"
            playlists.append({'title': title, 'url': url})

            if len(playlists) >= max_results:
                break
        
        return playlists
