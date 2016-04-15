${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/pip install pytub
cd $OPENSHIFT_TMP_DIR
 
cat <<'EOF'  >> youtube_download_py.py
from pytube import YouTube
import os,sys
# not necessary, just for demo purposes
from pprint import pprint

def youtube_download(video_url,load_dir='/tmp/'):
	yt = YouTube()

	# Set the video URL.
	yt.url = "http://www.youtube.com/watch?v=Ik-RsDGPI5Y"

	# Once set, you can see all the codec and quality options YouTube has made
	# available for the perticular video by printing videos.
	
	pprint(yt.videos)
	

	# The filename is automatically generated based on the video title.
	# You can override this by manually setting the filename.

	# view the auto generated filename:
	from __future__ import print_function
	print(yt.filename)

	#Pulp Fiction - Dancing Scene [HD]

	# set the filename:
	#yt.filename = 'Dancing Scene from Pulp Fiction'

	# You can also filter the criteria by filetype.

	pprint(yt.filter('flv'))

	#[<Video: Sorenson H.263 (.flv) - 240p>,
	# <Video: H.264 (.flv) - 360p>,
	# <Video: H.264 (.flv) - 480p>]
	
	# notice that the list is ordered by lowest resolution to highest. If you
	# wanted the highest resolution available for a specific file type, you
	# can simply do:
	print(yt.filter('mp4')[-1])
	#<Video: H.264 (.mp4) - 720p>
	
	# you can also get all videos for a given resolution
	pprint(yt.filter(resolution='480p'))

	#[<Video: H.264 (.flv) - 480p>,
	#<Video: VP8 (.webm) - 480p>]

	# to select a video by a specific resolution and filetype you can use the get
	# method.

	video = yt.get('mp4', '720p')

	# NOTE: get() can only be used if and only if one object matches your criteria.
	# for example:

	pprint(yt.videos)

	#[<Video: MPEG-4 Visual (.3gp) - 144p>,
	# <Video: MPEG-4 Visual (.3gp) - 240p>,
	# <Video: Sorenson H.263 (.flv) - 240p>,
	# <Video: H.264 (.flv) - 360p>,
	# <Video: H.264 (.flv) - 480p>,
	# <Video: H.264 (.mp4) - 360p>,
	# <Video: H.264 (.mp4) - 720p>,
	# <Video: VP8 (.webm) - 360p>,
	# <Video: VP8 (.webm) - 480p>]

	# Notice we have two H.264 (.mp4) available to us.. now if we try to call get()
	# on mp4..

	video = yt.get('mp4')
	# MultipleObjectsReturned: get() returned more than one object -- it returned 2!

	# In this case, we'll need to specify both the codec (mp4) and resolution
	# (either 360p or 720p).

	# Okay, let's download it!
	#video.download()

	# Downloading: Pulp Fiction - Dancing Scene.mp4 Bytes: 37561829
	# 37561829  [100.00%]

	# Note: If you wanted to choose the output directory, simply pass it as an
	# argument to the download method.
	#video.download('/tmp/')
	video.download(load_dir)

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

nohup sh -c " ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/python youtube_download_py.py 'https://www.youtube.com/watch?v=v1Knirup-T4'"> $OPENSHIFT_LOG_DIR/python_ftp_sync.log /dev/null 2>&1 &  
tail -f  $OPENSHIFT_LOG_DIR/python_ftp_sync.log
