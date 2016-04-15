
#pip install inbox
#dasinbox.py 0.0.0.0 4467

from inbox import Inbox

inbox = Inbox()

@inbox.collate
def handle(to, sender, subject, body):
    ...

# Bind directly.
inbox.serve(address='0.0.0.0', port=4467)

if __name__ == '__main__':
    inbox.dispatch()
	
