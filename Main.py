import asyncio
from Yt.Search import search_youtube

async def main():
    query = input("Enter search query: ")
    results = await search_youtube(query)
    for result in results:
        print(f"Title: {result['title']}\nURL: {result['url']}\n")

if __name__ == "__main__":
    asyncio.run(main())
