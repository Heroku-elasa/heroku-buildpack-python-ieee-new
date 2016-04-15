import requests,json

class Mediafire_Folder:
	def __init__(self,session_token,folder_key):
		self.folder_key = folder_key
		self.response_format = 'json'
		self.session_token = session_token

	def get_info(self):
		parameters = {'session_token':self.session_token,'response_format':self.response_format,'folder_key':self.folder_key}
		r = requests.get("http://www.mediafire.com/api/folder/get_info.php",params = parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			return json['folder_info']

	def delete(self):
		parameters = {'session_token':self.session_token,'response_format':self.response_format,'folder_key':self.folder_key}
		r = requests.get("http://www.mediafire.com/api/folder/delete.php",params = parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			print "Deleted " + self.folder_key

	def move(self,folder_key_dst=''):
		parameters = {'session_token':self.session_token,'response_format':self.response_format,'folder_key_src':self.folder_key,'folder_key_dst':folder_key_dst}
		r = requests.get("http://www.mediafire.com/api/folder/move.php",params = parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			print "Moved " + self.folder_key +" to " + folder_key_dst

	def update(self,foldername='',description='',tags='',privacy='',privacy_recursive='',note_subject='',note_description=''):
		parameters = {'session_token':self.session_token,'response_format':self.response_format,'folder_key':self.folder_key,'foldername':foldername,'description':description,'tags':tags,'privacy':privacy,'privacy_recursive':privacy_recursive,'note_subject':note_subject,'note_description':note_description}
		r = requests.get("http://www.mediafire.com/api/folder/update.php",params = parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			print "Updated " + foldername
			

	def attach_foreign(self): #Not tested
		parameters = {'session_token':self.session_token,'response_format':self.response_format,'folder_key':self.folder_key}
		r = requests.get("http://www.mediafire.com/api/folder/attach_foreign.php",params = parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			print 'Succesfully attached ' + self.folder_key

	def detach_foreign(self): #Not tested
		parameters = {'session_token':self.session_token,'response_format':self.response_format,'folder_key':folder_key}
		r = requests.get("http://www.mediafire.com/api/folder/detach_foreign.php",params = parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			print 'Succesfully detached ' + self.folder_key

	def get_depth(self):
		parameters = {'session_token':self.session_token,'response_format':self.response_format,'folder_key':self.folder_key}
		r = requests.get("http://www.mediafire.com/api/folder/get_depth.php",params = parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			print json['folder_depth']
			return json['folder_depth']['depth']

	def get_siblings(self,content_filter='all',start='',limit=''): #Don't know what this does
		parameters = {'session_token':self.session_token,'response_format':self.response_format,'folder_key':self.folder_key,'content_filter':content_filter,'start':start,'limit':limit}
		r = requests.get("http://www.mediafire.com/api/folder/get_siblings.php",params = parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			print json

	def search(self,search_text):
		parameters = {'session_token':self.session_token,'response_format':self.response_format,'folder_key':self.folder_key,'search_text':search_text}
		r = requests.get("http://www.mediafire.com/api/folder/search.php",params = parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			return json['results']
