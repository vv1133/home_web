from django.shortcuts import render

# Create your views here.

'''
from django.http import HttpResponse
def index(req):
	return HttpResponse('<h1>hello world</h1>')
'''

from django.shortcuts import render_to_response
from subprocess import Popen
from django.http import HttpResponse

class App(object):
	def __init__(self):
		self.music = "off"

	def update_music_status(self):
		if cmp(self.music, "off") == 0:
			print "music start..."
			self.music = "on"
			cmd = "/home/pi/music/play.py"
			args = cmd.split(" ")
			self.music_proc = Popen(args)
		else:
			print "music stop..."
			self.music = "off"
			Popen.terminate(self.music_proc)

	def post_weibo(self, content):
		cmd = "/home/pi/post_weibo/post.py" + "+"\
			+ "%s    --From Raspberry"%(content)
		args = cmd.split("+")
		print "post weibo..."
		self.post_weibo = Popen(args)


my_app = App()

def index(req):
	global my_app
	if req.POST.has_key('weibo'):
		print "weibo"
		content = req.POST['weibo_content']
		my_app.post_weibo(content)
		return HttpResponse("<h3>content:</h3>%s<h3>Post success!</h3>" %content)
	elif req.POST.has_key('music'):
		print "music"
		my_app.update_music_status()
		return render_to_response("index.html", {"app":my_app})
	else:
		return render_to_response("index.html", {"app":my_app})

