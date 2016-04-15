import pymediafire
import mediafire
class main_dropbox:
    def __init__(self,app_key,app_secret,access_token,loalpath,remotepath):
        self.app_key=app_key;self.app_secret=app_secret;
        self.access_token=access_token;
        self.loalpath=loalpath;self.remotepath=remotepath
    def main_dropbox(self):

        import dropbox
        from dropbox import session
        # # from session import BaseSession
        # s=session.BaseSession

        # Get your app key and secret from the Dropbox developer website
        # app_key = 'INSERT_APP_KEY'
        # app_secret = 'INSERT_APP_SECRET'
        flow = dropbox.client.DropboxOAuth2FlowNoRedirect(self.app_key, self.app_secret)

        # Have the user sign in and authorize this token
        authorize_url = flow.start()
        print '1. Go to: ' + authorize_url
        print '2. Click "Allow" (you might have to log in first)'
        print '3. Copy the authorization code.'

        # code = raw_input("Enter the authorization code here: ").strip()
        # # This will fail if the user enters an invalid authorization code
        # access_token, user_id = flow.finish(code)

        client = dropbox.client.DropboxClient(self.access_token)
        print 'linked account: ', client.account_info()

        # fh = open("small_test_file.txt","w")
        # fh.write("Small test file")
        # fh.write("Small test file")
        # fh.close()

        #uploading file
        f = open(localpath, 'rb')
        response = client.put_file(remotepath, f)
        print "/n uploaded:", response

        # link=dropbox.client.DropboxClient(access_token).share('/magnum-opus.txt')
        link=client.share(remotepath)
        print "/n share_link:", link
        return link

    def download(self):
        #downloading files
        f, metadata = client.get_file_and_metadata('/magnum-opus.txt')
        out = open('magnum-opus.txt', 'wb')
        out.write(f.read())
        out.close()
        print metadata


def my_dropbox(email, password, localpath, remotepath):
    from dbupload import DropboxConnection
    from getpass import getpass

    # email = raw_input("Enter Dropbox email address:")
    # password = getpass("Enter Dropbox password:")

    # Create a little test file
    # fh = open("small_test_file.txt","w")
    # fh = open("small_test_file.txt","w")
    # fh.write("Small test file")
    # fh.write("Small test file")
    # fh.close()
    remote_file=remotepath.split('/')[-1]
    remote_dir=remotepath.split(remote_file)[0]

    try:
    # Create the connection
        conn = DropboxConnection(email, password)

        # Upload the file
        uploader=conn.upload_file(localpath,remote_dir,remote_file)
        public_url=conn.get_download_url(remote_dir,remote_file)
    except:
        print("Upload failed")
    else:
        print("Uploaded small_test_file.txt to the root of your Dropbox")
if __name__ == '__main__':
    import os
    email='ss3@elec-lab.tk';password='ss123456';

    localpath=os.getcwd().replace("\\","/")+'/small_test_file.txt';
    remotepath='/'+localpath.split('/')[-1]

    fh = open("small_test_file.txt","w")
    fh.write("Small test file")
    fh.close()
    # my_dropbox( email, password, localpath, remotepath)

    email ="ss3@elec-lab.tk"
    password = "ss123456"
    application_id = "43325"
    api_key = "m7x4m6p224t9m0j4iqr4k82ipfocbe76c7amqqqn"
    from pymediafire import MediaFireSession
    # test_user = mediafire.Mediafire_User(email,password,application_id,api_key)
    #
    # ss=test_user.get_session_token()
    # ss4=test_user.get_info()
    # # ss1=test_user.folder_create('tt')
    # ss2=test_user.upload(localpath)
    # # ss=u'57e32d07364c28d417d34832c62e7d7023124c31837745de4debc7c4d3944727471408723e67bb0266246edd1ebfa15004db6bad6db987afde399394708387637b5ea41d11ebcdc7'
    # # ss2=u'afhlmywov9n'
    # test_file=mediafire.Mediafire_File(ss,ss2)
    #
    # link=test_file.get_links('')
    # d_link=test_file.download()

    test_user=pymediafire.MediaFireSession(email,password,application_id,api_key)
    s=test_user.create_folder('test')
    # s1=test_user.load_folder()
    # fo='test'
    # s3=test_user.load_folder(fo)
    # s2=test_user.upload(s,localpath)
    s2=test_user.upload(s,localpath)

    # access_token='Ap8LK01GJbsAAAAAAAAABpqZnhsSpLwvdFgL69ROiQ98N3S-PPwbylCf2Cc5Fxhc'
    # main_dropbox(app_key,app_secret,access_token,localpath,remotepath)