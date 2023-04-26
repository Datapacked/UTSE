import re

import requests


def torrentgalaxysearch(searchterm="avatar", pagenum=1, mode="desc", args="id"):
	#'id' is date for some reason?
	possible_args = ['size', 'seeders', 'id', 'name']
	if args not in possible_args:
		args = 'id'
	template = f"https://torrentgalaxy.to/torrents.php?search={searchterm.replace(' ', '+')}&sort=id&order={mode}&page={pagenum}&sort={args}"
	h = requests.get(template)
	text = h.text

	#NOTE: Following line is the full torrentgalaxy torrent URL grabber, the uncommented line grabs the incomplete ones
	#LoT = re.findall('href=\"/torrent/(.*?)\"', h.text)

	#Gets torrent URL and name, profile link, torrent file link, magnet link, and size
	LoTID = [[f"https://torrentgalaxy.to/torrent/{'/'.join(i)}/", i[1]] for i in re.findall('href="/torrent/([0-9]+)/([0-9a-zA-Z\-]+)"', text)]
	LoTUID = re.findall('profile/[0-9a-zA-Z]+', text)
	LoTFL = [f"https://watercache{i}" for i in re.findall('https://watercache(.*?)\'>', text)]
	LoML = [f"magnet:{i}announce"for i in re.findall('magnet:(.*?)announce', text)]
	LoTS = [i.replace(',', '') for i in re.findall('<font color=\'green\'><b>(.*?)</b></font>', text)]
	LoTL = [i.replace(',', '') for i in re.findall('<font color=\'#ff0000\'><b>(.*?)</b></font>', text)]
	LoTSi = re.findall('<span class=\'badge badge-secondary txlight\' style=\'border-radius:4px;\'>(.*?)</span>', text)
	return {"torrent": list(zip(*LoTID))[0], "torrentname": list(zip(*LoTID))[1], "username": LoTUID, "torrentDL": LoTFL, "magnet": LoML, "seeders": LoTS, "leechers": LoTL, "size": LoTSi}