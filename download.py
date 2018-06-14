import requests
import re
import time
import json
from tqdm import tqdm

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0'}
url = json.load(open('./track_url.json', 'r'))

def final_url(html):
    reg = '"id":(.*?),"play_path_64":"(.*?)"'
    final_url = re.findall(reg, html.text)
    return final_url

for u in tqdm(url):
    try:
        html = requests.get(u, headers=header)
        f_url = final_url(html)

        for eid, fu in f_url:
            m4a = requests.get(fu)
            with open('./episode/'+eid+'.m4a', 'wb') as f:
                f.write(m4a.content)
            time.sleep(0.2)
    except:
        continue
