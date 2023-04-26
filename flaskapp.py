from flask import Flask, render_template

import anirena
import nyaa
import torrentgalaxy

app = Flask(__name__, static_folder='static')

@app.route('/all/<searchterm>/<page>')
@app.route('/all/<searchterm>')
def table(searchterm, page = 0):
	page = int(page)
	an = anirena.anirenasearch(searchterm, page)
	ny = nyaa.nyaasearch(searchterm, page)
	to = torrentgalaxy.torrentgalaxysearch(searchterm, page)
	arr = []
	#rotates from columns to rows
	for (t, tname, uname, tdl, m, s, l, si) in zip(*an.values()):
		arr.append([t, tname, uname, tdl, m, s, l, si])
	for (t, tname, uname, tdl, m, s, l, si) in zip(*ny.values()):
		arr.append([t, tname, uname, tdl, m, s, l, si])
	for (t, tname, uname, tdl, m, s, l, si) in zip(*to.values()):
		arr.append([t, tname, uname, tdl, m, s, l, si])
	return render_template('index.html', data=arr)

app.run(debug=True)