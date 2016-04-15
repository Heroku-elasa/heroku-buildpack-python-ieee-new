__author__ = 's'
# import sys
class my_uploadr():

    def upload_mega(self,email,password,file_name,destinatio):


        import crypto
        import sys
        sys.modules['Crypto'] = crypto

        os.environ['PYTHON_EGG_CACHE']=os.getcwd()
        pwd = os.path.realpath(__file__).replace('\\','/')
        pwd = pwd[:pwd.rfind("/")]
        pwd=pwd.replace('/',"\\")
        # sys.stderr.write("Path: " + repr(pwd) + "\n")

        sys.path.append(pwd + '\\mega.co.nz\\lib')
        try:
            from mega import Mega
        except:
            import mega
        # Create an instance of Mega.py
        mega = Mega()
        # add the verbose option for print output on some functions
        mega = Mega({'verbose': True})

        # Login to Mega
        m = mega.login(email, password)
        # login using a temporary anonymous account
        m = mega.login()

        # Get user details
        details = m.get_user()

        # Get account disk quota
        quota = m.get_quota()

        # Get account balance (Pro accounts only)
        balance = m.get_balance()
        # specify unit output kilo, mega, gig, else bytes will output

        # Get account storage space
        space = m.get_storage_space(kilo=True)
        # Get account files
        files = m.get_files()

        #Upload a file, and get its public link
        file = m.upload(file_name)
        m.get_upload_link(file)
        # see mega.py for destination and filename options

        # Upload a file to a destination folder
        dest_file_name=destinatio.split('/')[-1]
        des_dir=destinatio.split(dest_file_name)[0]
        # folder = m.find('my_mega_folder')
        folder = m.find(des_dir)
        up=m.upload(file_name, folder[0])

        public_url=m.get_upload_link(file_name)

        #Import a file from URL, optionally specify destination folder

        m.import_public_url('https://mega.co.nz/#!utYjgSTQ!OM4U3V5v_W4N5edSo0wolg1D5H0fwSrLD3oLnLuS9pc')
        folder_node = m.find('Documents')[1]
        m.import_public_url('https://mega.co.nz/#!utYjgSTQ!OM4U3V5v_W4N5edSo0wolg1D5H0fwSrLD3oLnLuS9pc', dest_node=folder_node)

        #Create a folder

        m.create_folder('new_folder')

        #Rename a file or a folder

        file = m.find('myfile.doc')
        m.rename(file, 'my_file.doc')

        #Moving a file or a folder into another folder

        file = m.find('myfile.doc')
        folder = m.find('myfolder')
        m.move(file[0], folder)

        #Search account for a file, and get its public link

        file = m.find('myfile.doc')
        m.get_link(file)

        #Trash or destroy a file from URL or its ID

        m.delete(file[0])
        m.delete_url('https://mega.co.nz/#!utYjgSTQ!OM4U3V5v_W4N5edSo0wolg1D5H0fwSrLD3oLnLuS9pc')

        m.destroy(file[0])
        m.destroy_url('https://mega.co.nz/#!utYjgSTQ!OM4U3V5v_W4N5edSo0wolg1D5H0fwSrLD3oLnLuS9pc')

        files = m.find('myfile.doc')
        if files:
            m.delete(files[0])

        #Add/remove contacts

        m.add_contact('test@email.com')
        m.remove_contact('test@email.com')


        #Download a file from URL or file obj, optionally specify destination folder

        file = m.find('myfile.doc')
        m.download(file)
        m.download_url('https://mega.co.nz/#!utYjgSTQ!OM4U3V5v_W4N5edSo0wolg1D5H0fwSrLD3oLnLuS9pc')
        m.download(file, '/home/john-smith/Desktop')
        # specify optional download filename (download_url() supports this also)
        m.download(file, '/home/john-smith/Desktop', 'myfile.zip')
        return public_url

if __name__=='__main__':
    import os

    email='ss3@elec-lab.tk';password='ss123456';
    localpath=os.getcwd().replace("\\","/")+'/small_test_file.txt';
    file_name=os.getcwd().replace("\\","/")+'/small_test_file.txt';
    remotepath='/'+localpath.split('/')[-1]

    fh = open("small_test_file.txt","w")
    fh.write("Small test file")
    fh.close()
    my_uploadr().upload_mega(email,password,file_name,remotepath)