import aiohttp
import urllib.parse
import asyncio
import json
from pdf2image import convert_from_bytes

def pdf_to_images(pdf_bytes,resolution=300):
    images = convert_from_bytes(pdf_bytes, dpi=resolution)
    paths = []
    for i in range(len(images)):
        images[i].save('page'+ str(i) +'.jpg', 'JPEG')
        paths.append('page'+ str(i) +'.jpg')
    return paths


async def make_request(HREF="/نتائج 2023",state=0):
    url = 'https://center.mlazemna.com'
    payload = {
        "action": "get",
        "items": {
            "href": HREF,
            "what": 1
        }
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/json;charset=utf-8',
        'Origin': 'https://center.mlazemna.com',
        'Referer': 'https://center.mlazemna.com',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Te': 'trailers',
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url,headers=headers,json=payload) as response:
            response_data = await response.text()
            items = json.loads(response_data)["items"]
            for item in items:
                if urllib.parse.unquote(item["href"]).startswith(payload["items"]["href"]):
                    href = urllib.parse.unquote(item["href"])
                    text = href.replace(payload["items"]["href"],"")
                    if "قتيبة للبنين الثانية" in text and state == 4:
                        url = url + item["href"]
                        return await downloadPdf(url)
                    elif "تطبيقي" in text and state == 3:
                        return await make_request(href,4)
                    elif "القادسية" in text and (state == 2 or state == 1):
                        return await make_request(href,3)
                    elif ("تطبيقي" in text or "علمي" in text) and state == 1:
                        return await make_request(href,2)
                    elif "الدور الاول" in text and "التمهيدي" not in text and state == 0:
                        return await make_request(href,1)
                    
            return False

async def downloadPdf(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                pdfBytes = b""
                while True:
                    chunk = await response.content.read(1024)  # Adjust the chunk size as per your needs
                    if not chunk:
                        break
                    pdfBytes += chunk
                "حيدر نذير صالح"
                return pdf_to_images(pdfBytes)


print(asyncio.run(make_request()))