import asyncio
from playwright.async_api import async_playwright

async def search_duckduckgo(query: str):
    search_url = f"https://duckduckgo.com/html/?q=site:youtube.com+{query}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Go to DuckDuckGo search page
        await page.goto(search_url)

        # Wait for results to load
        await page.wait_for_selector('a.result__a')

        # Extract the results
        links = await page.eval_on_selector_all('a.result__a', 'elements => elements.map(element => element.href)')

        await browser.close()

        return links


async def main():
    query = "Chandni"
    results = await search_duckduckgo(query)
    if results:
        for url in results:
            print(f"Found result: {url}")
    else:
        print("No results found.")

# Run the main function
asyncio.run(main())
