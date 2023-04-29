import random
import re
import xml.etree.ElementTree as ET

import requests


def anirenasearch(searchterm="uzaki", pagenum=1):
	return_template = {"torrent": object, "torrentname": object, "username": object, "torrentDL": object, "magnet": object, "seeders": object, "leechers": object, "size": object}
	for i in return_template:
		return_template[i] = []
	flag = True
	if flag:
		#template url, the random integer is there for some reason, i don't know why
		template = f"https://www.anirena.com/rss.php?s={searchterm.replace(' ', '+')}&t={random.randint(0, 100)}&start={100 * pagenum - 1}"
		r = requests.get(template)
		with open('anirena.tmp.rss', 'w') as tmpfile:
			tmpfile.write(r.text)
	tree = ET.parse('anirena.tmp.rss')
	root = tree.getroot()
	items = root.find('channel').findall('item')
	torrent = None
	for i in items:
		#getting torrent names
		tname = i.find('title').text
		#getting usernames
		username = i.find('creator').text
		#getting torrent file DL links
		tDL = i.find('link').text
		#getting torent descriptions
		desc = i.find('description').text
		#getting relevant torrent description infos from torrent descriptions using regex black magic
		desc_info = re.findall('\d+(?:\.\d+)?', desc)[0:2] + re.findall('\d+(?:\.\d+)?\s*(?:[KMGTP]B|\b)', desc)
		#getting magnet links
		magnet = i.find('{http://xmlns.ezrss.it/0.1/}torrent')[-1].text
		#splitting info accordingly
		seeders, leechers, size = desc_info
		#putthing all of that into arrays
		return_template['torrent'].append("/none")
		return_template['torrentname'].append(tname)
		return_template['username'].append(username)
		return_template['torrentDL'].append(tDL)
		return_template['magnet'].append(magnet)
		return_template['seeders'].append(seeders)
		return_template['leechers'].append(leechers)
		return_template['size'].append(size)
	return return_template