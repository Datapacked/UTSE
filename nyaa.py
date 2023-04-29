import re
import xml.etree.ElementTree as ET

import requests


def nyaasearch(searchterm='uzaki', pagenum='1'):
	return_template = {"torrent": object, "torrentname": object, "username": object, "torrentDL": object, "magnet": object, "seeders": object, "leechers": object, "size": object}
	for i in return_template:
		return_template[i] = []
	template = f"https://nyaa.si/?f=0&c=0_0&q={searchterm.replace(' ', '+')}&p={pagenum}"
	r = requests.get(template)
	with open('nyaa.tmp.html', 'w') as nyout:
		ostri = re.sub('<script(.*)>(.*)</script>', '', r.text)
		ostri = re.sub('<meta.*?>', '', ostri)
		ostri = re.sub('<link.*?>', '', ostri)
		ostri = re.sub('<input.*?>', '', ostri)
		ostri = re.sub('<img.*?>', '', ostri)
		ostri = re.sub('<ul class="pagination">.*</ul>', '', ostri)
		ostri = ostri.replace('selected', '').replace('<br>', '').replace('&laquo;', '')
		ostri = re.sub('<!--.*?-->', '', ostri, flags=re.DOTALL)
		nyout.write(ostri)
	tree = ET.parse('nyaa.tmp.html')
	root = tree.getroot()
	#gets the div
	#then the div inside the div
	#then the table inside that div
	#then the tbody inside that table
	tbody = root.find('body')[1][0][0][1]
	for i in tbody:
		#torrent name
		tname = (i[1][-1].text)

		#Torrent file DL link and torrent magnet link
		tfdl = ('https://nyaa.si' + i[2][0].attrib['href'])
		tml = (i[2][1].attrib['href'])

		#Torrent size
		ts = i[3].text

		#Seeders and leechers
		tsc = i[5].text
		tlc = i[6].text
		return_template['torrent'].append("/none")
		return_template['torrentname'].append(tname)
		return_template['username'].append("/none")
		return_template['torrentDL'].append(tfdl)
		return_template['magnet'].append(tml)
		return_template['seeders'].append(tsc)
		return_template['leechers'].append(tlc)
		return_template['size'].append(ts)
	return return_template