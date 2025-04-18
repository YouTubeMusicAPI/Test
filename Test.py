from Yt.Search import search_youtube_fastest

query = input("Enter search query: ")
results = search_youtube_fastest(query)

if not results:
    print("No results found.")
else:
    for result in results:
        print(f"\n🎵 Title: {result['title']}\n🔗 URL: {result['url']}")
