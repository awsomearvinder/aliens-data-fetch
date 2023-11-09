import json
import re
import aiohttp
import asyncio

async def get_html(session, entry, sem):
    async with sem:
        async with session.get(entry['link']) as resp:
            req_counter = 0
            while req_counter <= 10:
                try:
                    entry['link_html'] = await resp.text()
                    print(json.dumps(entry))
                    return
                except Exception:
                    req_counter += 1
                    print(f"failed request {entry['occurence']}")
                    continue

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
    
async def main():
    with open("data-no-empties.txt", "r") as file:
        l = []
        for line in file:
            obj = json.loads(line)
            for entry in obj["data"]:
                link = re.match(".*href=\'(.*)\' rel", entry[0]).groups()[0]
                l.append({
                          "link": f"https://nuforc.org/{link}",
                          "occurence": entry[1],
                          "city": entry[2],
                          "state": entry[3],
                          "country": entry[4],
                          "shape": entry[5],
                          "summary": entry[6],
                          "reported": entry[7],
                          "posted": entry[8],
                          "image": entry[9],
                })
        async with aiohttp.ClientSession() as session:
            sem = asyncio.Semaphore(70)
            await asyncio.gather(*[get_html(session, entry, sem) for entry in l])
asyncio.run(main())
