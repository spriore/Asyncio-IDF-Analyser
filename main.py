import numpy, pandas, re, aiohttp, asyncio, itertools
from bs4 import BeautifulSoup

#Insert list of search queries
 queries = [] 

#Term Handelers
queries = list(set(queries))
terms = set(itertools.chain.from_iterable(str.split(query.lower(), " ") for query in queries))

#aiohttp Headers
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"} 

async def fetch(session, url):
    async with session.get(url, headers = headers) as response:
        return await response.text()

async def google(loop, query):
    urlset = []
    google = "https://www.google.com/search?q=" + query.replace(" ", "+") + "&num=100&start=0"
    async with aiohttp.ClientSession(loop=loop) as session:
        html = await fetch(session, google)
    soup = BeautifulSoup(html, "lxml")
    for script in soup.find_all("div", class_="srg"):
        for link in script.find_all("h3", class_="r"):
            urlset.append( link.find('a').get('href') )
    return urlset
        
async def idf(loop, query):
    tf = pandas.DataFrame()
    urlset = await google(loop, query)
    for url in urlset:
        async with aiohttp.ClientSession(loop=loop) as session:
            try:
                html = await fetch(session, url)
            except Exception as inst:
                print(query, url, str(type(inst)), str(inst))
                continue

        soup = BeautifulSoup(html, "lxml")
        for script in soup(["head", "script", "style", "link", "meta"]):
            script.extract()
        text   = soup.get_text(separator = " ")

        #Term frequency counts
        counts = dict.fromkeys(terms, 0)
        for t in terms: 
            if re.search(r"("+ t +")", text):
                counts[t] = 1

        #Add TFi to TF table
        tfi      = pandas.Series(counts)
        tfi.name = url
        tf       = tf.append(tfi)

    #Calculate IDF scores and TFIDF values
    m   = len(tf)
    idf = numpy.log( m / tf[tf!=0].count(axis = 0) )
    idfs.loc[term] = idf
    
idfs = pandas.DataFrame(index = queries, columns = terms)

loop = asyncio.get_event_loop()
tasks = [idf(loop, query) for query in queries]
fut = asyncio.gather(*tasks)
loop.run_until_complete(fut)
loop.close()
    
idfs.to_csv("idsf.csv")

print("complete")
