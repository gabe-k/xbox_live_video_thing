import requests
import json

class XboxAPIClient:

	def __init__(self, auth):
		self.auth = auth

	def get_games_clips_for_title(self, title_id, params=None):
		uri = 'https://gameclipsmetadata.xboxlive.com/public/titles/' + str(title_id) + '/clips?qualifier=created'
		if params:
			for p in params:
				uri += '&' + p + '=' + str(params[p])
		r = self.request('GET', uri)
		return json.loads(r.text)['gameClips']

	def download_game_clip(self, filename, clip):
		uri = None
		for u in clip['gameClipUris']:
			if u['uriType'] == 'Download':
				uri = u['uri']

		r = requests.get(uri, stream=True)
		with open(filename, 'wb') as f:
			for chunk in r.iter_content(chunk_size=1024):
				if chunk:
					f.write(chunk)
					f.flush()

		return r.status_code

	def request(self, verb, uri, contract_version=2):
		return requests.request(verb, uri, headers={'Authorization': self.auth, 'x-xbl-contract-version': contract_version})