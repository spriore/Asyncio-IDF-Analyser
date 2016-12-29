# Asyncio-IDF-Analyser
Using asyncio to analyse terms IDF's with respect to search queries.  
Steps:  
1. Break list of search queries into terms.  
2. Use aiohttp to scrape Google SERP for queries.  
3. Use bs4 to make list of SERP results.  
4. Use aiohttp to scrape SERP results.  
5. Check if term(s) is/are present.  
6. Math.  
7. Export to CSV.
