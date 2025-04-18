import asyncio
from playwright.async_api import async_playwright

class YouTubeSearch:
    def __init__(self):
        self.base_url = 'https://www.youtube.com/results?search_query='

    async def search(self, query, max_results=5):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            search_url = f"{self.base_url}{query}"
            await page.goto(search_url)
            await page.wait_for_selector('ytd-video-renderer')

            videos = []
            video_elements = await page.query_selector_all('ytd-video-renderer')

            for video in video_elements[:max_results]:
                title = await video.query_selector('a#video-title')
                title_text = await title.inner_text()
                url = await title.get_attribute('href')

                videos.append({'title': title_text, 'url': f"https://www.youtube.com{url}"})

            await browser.close()
            return videos
    
    async def search_playlists(self, query, max_results=5):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            search_url = f"https://www.youtube.com/results?search_query={query}+playlist"
            await page.goto(search_url)
            await page.wait_for_selector('ytd-playlist-renderer')

            playlists = []
            playlist_elements = await page.query_selector_all('ytd-playlist-renderer')

            for playlist in playlist_elements[:max_results]:
                title = await playlist.query_selector('a#video-title')
                title_text = await title.inner_text()
                url = await title.get_attribute('href')

                playlists.append({'title': title_text, 'url': f"https://www.youtube.com{url}"})

            await browser.close()
            return playlists
