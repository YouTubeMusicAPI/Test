import asyncio
from Yt.Search import YouTubeSearch

async def main():
    search_query = input("Enter search query: ")
    print("Searching for songs...")

    youtube_search = YouTubeSearch()
    songs = await youtube_search.search(search_query)

    if songs:
        print("\nSongs found:")
        for song in songs:
            print(f"Title: {song['title']}\nURL: {song['url']}\n")
    else:
        print("No songs found.")

    print("\nSearching for playlists...")
    playlists = await youtube_search.search_playlists(search_query)

    if playlists:
        print("\nPlaylists found:")
        for playlist in playlists:
            print(f"Title: {playlist['title']}\nURL: {playlist['url']}\n")
    else:
        print("No playlists found.")

if __name__ == '__main__':
    asyncio.run(main())
