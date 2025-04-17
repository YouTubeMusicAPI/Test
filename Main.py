from Yt.Search import YouTubeSearch  # Assuming the search code is saved as YouTubeSearch.py

def test_search(query):
    youtube_search = YouTubeSearch()

    print("Searching for songs...\n")
    songs = youtube_search.search(query)
    if songs:
        for index, song in enumerate(songs, 1):
            print(f"{index}. Title: {song['title']}, URL: {song['url']}")
    else:
        print("No songs found.\n")
    
    print("\nSearching for playlists...\n")
    playlists = youtube_search.search_playlists(query)
    if playlists:
        for index, playlist in enumerate(playlists, 1):
            print(f"{index}. Title: {playlist['title']}, URL: {playlist['url']}")
    else:
        print("No playlists found.\n")

if __name__ == "__main__":
    # Replace with the search query you want to test
    query = input("Enter search query: ")
    test_search(query)
