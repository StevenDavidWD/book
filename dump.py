import json
import redis

r = redis.Redis()
oa = open('./album.json', 'w')

album_list = list()

album = r.smembers('album')

for a in album:
    a = eval(a.decode('utf-8'))
    album_list.append(a)

# for e in episode:
#     e = eval(e)
#     episode_list.append(e)

# for index, c in enumerate(cover):
#     d = dict()
#     d['url'] = c.decode('utf-8')
#     d['index'] = index
#     cover_list.append(d)

json.dump(album_list, oa, ensure_ascii=False, indent=4)
# json.dump(episode_list, oe, ensure_ascii=False, indent=4)
# json.dump(cover_list, oc, ensure_ascii=False, indent=4)
