import asyncio
from Yt.Search import Search  # Replace 'YourModuleName' with the name of your actual module where the search function is defined.

async def test_search():
    query = "Chandni"  # Replace with the song or video name you want to search for
    results = await Search(query)

    if results:
        for idx, result in enumerate(results, start=1):
            print(f"Result {idx}: {result.title} - {result.url}")
    else:
        print("No results found.")

if __name__ == "__main__":
    asyncio.run(test_search())
