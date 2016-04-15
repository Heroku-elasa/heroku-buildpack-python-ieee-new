${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/pip install youtube-dl
cd $OPENSHIFT_TMP_DIR

cat <<'EOF'  >> youtube_download_youtube_dl1.py
from subprocess import call
import os,sys
try:
        video_urls = sys.argv[1:]
		#video_dir = sys.argv[2:]
except:
        video_urls = input('Enter (space-separated) video URLs: ')
		#video_urls = input('Enter (space-separated) video Dir: ')
		
#command = "${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/youtube-dl https://www.youtube.com/watch?v=NG3WygJmiVs -c"
command = "${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/youtube-dl"+ video_urls "-c"

call(command.split(), shell=False)
EOF
cat <<'EOF'  >> youtube_download_youtube_dl.py
import youtube_dl

import os,sys

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


	def my_hook(d):
		if d['status'] == 'finished':
			print('Done downloading, now converting ...')

def youtube_download(video_url,load_dir='/tmp/'):
	

	
	

	ydl_opts = {
		'format': 'bestaudio/best',
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192',
		}],
		'logger': MyLogger(),
		'progress_hooks': [my_hook],
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		#ydl.download(['http://www.youtube.com/watch?v=BaW_jenozKc'])
		ydl.download([video_url])
	

def main():
    print("\n--------------------------")
    print (" Youtube Video Downloader")
    print ("--------------------------\n")

    try:
		home_=os.eviron['OPENSHIF_HOME_DIR'];
		video_dir=home_+'/ap-root/runtime/srv/tmp/'
	except:
		video_dir=os.eviron['TMP'];
	try:
        video_urls = sys.argv[1:]
		#video_dir = sys.argv[2:]
    except:
        video_urls = input('Enter (space-separated) video URLs: ')
		#video_urls = input('Enter (space-separated) video Dir: ')

    for u in video_urls:
        youtube_download(u)
    print("\n Done. in:"+video_dir)

if __name__ == '__main__':
    main()
	
EOF

nohup sh -c " ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/python youtube_download_youtube_dl.py 'https://www.youtube.com/watch?v=v1Knirup-T4'"> $OPENSHIFT_LOG_DIR/youtube_download_youtube_dl.log /dev/null 2>&1 &  
tail -f  $OPENSHIFT_LOG_DIR/youtube_download_youtube_dl.log
