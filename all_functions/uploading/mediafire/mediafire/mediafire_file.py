import requests,json

class Mediafire_File:
    def __init__(self,session_token,quick_key):
        self.quick_key = quick_key
        self.response_format = 'json'
        # self.response_format = 'xml'
        self.session_token = session_token

    def get_info(self):
        parameters = {'session_token':self.session_token,'response_format':self.response_format,'quick_key':self.quick_key}
        r = requests.get("http://www.mediafire.com/api/file/get_info.php",params = parameters)
        json = r.json()['response']
        if (json['result'] == 'Error'):
            print json['message']
        else:
            return json['file_info']

    def delete(self):
        parameters = {'session_token':self.session_token,'response_format':self.response_format,'quick_key':self.quick_key}
        r = requests.get("http://www.mediafire.com/api/file/delete.php",params = parameters)
        json = r.json()['response']
        if (json['result'] == 'Error'):
            print json['message']
        else:
            print "Deleted " + self.quick_key

    def move(self,folder_key=''):
        parameters = {'session_token':self.session_token,'response_format':self.response_format,'quick_key':self.quick_key,'folder_key':folder_key}
        r = requests.get("http://www.mediafire.com/api/file/move.php",params = parameters)
        json = r.json()['response']
        if (json['result'] == 'Error'):
            print json['message']
        else:
            print "Moved " + self.quick_key + " to " + folder_key

    def update(self,filename,description,tags,privacy,note_subject,note_description):
        parameters = {'session_token':self.session_token,'response_format':self.response_format,'quick_key':self.quick_key,'filename':filename,'description':description,'tags':tags,'privacy':privacy,'note_subject':note_subject,'note_description':note_description}
        r = requests.get("http://www.mediafire.com/api/file/update.php",params = parameters)
        json = r.json()['response']
        if (json['result'] == 'Error'):
            print json['message']
        else:
            print "Changed the info for " + self.quick_key

    def update_password(self,password=""):
        parameters = {'session_token':self.session_token,'response_format':self.response_format,'quick_key':self.quick_key,'password':password}
        r = requests.get("http://www.mediafire.com/api/file/update_password.php",params = parameters)
        json = r.json()['response']
        if (json['result'] == 'Error'):
            print json['message']
        else:
            print "Changed the password for " + self.quick_key

    def update_file(self,to_quickkey):
        parameters = {'session_token':self.session_token,'response_format':self.response_format,'from_quickkey':self.quick_key,'to_quickkey':to_quickkey}
        r = requests.get("http://www.mediafire.com/api/file/update_file.php",params = parameters)
        json = r.json()['response']
        if (json['result'] == 'Error'):
            print json['message']
        else:
            print "Update the quickkey for " + self.quick_key +" to " + to_quickkey
            self.quick_key = to_quickkey

    def copy(self,folder_key=''):
        parameters = {'session_token':self.session_token,'response_format':self.response_format,'quick_key':self.quick_key,'folder_key':folder_key}
        r = requests.get("http://www.mediafire.com/api/file/copy.php",params = parameters)
        json = r.json()['response']
        if (json['result'] == 'Error'):
            print json['message']
        else:
            print "Copied " + self.quick_key +" to " + folder_key
            return json['new_quickkeys']

    def get_links(self,link_type=''):
        parameters = {'session_token':self.session_token,'response_format':self.response_format,'quick_key':self.quick_key,'link_type':link_type}
        r = requests.get("http://www.mediafire.com/api/file/get_links.php",params = parameters)
        # r = requests.get("http://www.mediafire.com/api/1%2E2/file/get_links.php",params = parameters)
        print r.text
        json = r.json()['response']
        if (json['result'] == 'Error'):
            print json['message']
        else:
            return json['links']

    def collaborate(self,emails='',duration='',message='',public='no',email_notification='no'):
        parameters = {'session_token':self.session_token,'response_format':self.response_format,'quick_key':self.quick_key,'emails':emails,'duration':duration,'message':message,'public':public,'email_notification':email_notification}
        r = requests.get("http://www.mediafire.com/api/file/collaborate.php",params = parameters)
        json = r.json()['response']
        if (json['result'] == 'Error'):
            print json['message']
        else:
            return json['collaboration_links'][0]['link']

    def one_time_download(self,get_counts_only='no',duration='',email_notification='no',burn_after_use='yes',success_callback_url='',error_calback_url='',bind_ip=''):
        parameters = {'session_token':self.session_token,'response_format':self.response_format,'quick_key':self.quick_key,'get_counts_only':get_counts_only,'duration':duration,'email_notification':email_notification,'success_callback_url':success_callback_url,'error_calback_url':error_calback_url,'bind_ip':bind_ip,'burn_after_use':burn_after_use}
        r = requests.get("http://www.mediafire.com/api/file/one_time_download.php",params = parameters)
        json = r.json()['response']
        if (json['result'] == 'Error'):
            print json['message']
        else:
            return {'link':json['one_time_download'],'token':json['token']}

    def configure_one_time_download(self,token,duration='',email_notification='no',burn_after_use='yes',success_callback_url='',error_calback_url='',bind_ip=''): #Doesn't work for some reason
        parameters = {'session_token':self.session_token,'response_format':self.response_format,'token':token,'duration':duration,'email_notification':email_notification,'success_callback_url':success_callback_url,'error_calback_url':error_calback_url,'bind_ip':bind_ip,'burn_after_use':burn_after_use}
        r = requests.get("http://www.mediafire.com/api/file/configure_one_time_download.php",params = parameters)
        json = r.json()['response']
        if (json['result'] == 'Error'):
            print json['message']
        else:
            print "Succesfully changed the " + token + " one time download"

    def download(self):
        parameters = {'session_token':self.session_token,'response_format':self.response_format,'quick_key':self.quick_key}
        r = requests.get("http://www.mediafire.com/api/file/get_links.php",params = parameters)
        json = r.json()['response']
        if (json['result'] == 'Error'):
            print json['message']
        else:
            return json['links'][0]['direct_download']
