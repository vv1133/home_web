from django.shortcuts import render

# Create your views here.

'''
from django.http import HttpResponse
def index(req):
	return HttpResponse('<h1>hello world</h1>')
'''

from django.shortcuts import render_to_response
from subprocess import Popen

class App(object):
	def __init__(self):
		self.music = "off"
		self.weibo = ""

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

	def post_weibo(self):
		if self.weibo == "":
			print "post weibo..."
			self.weibo = "success"
		else:
			print "recover"
			self.weibo = ""
			
my_app = App()

def index(req):
	global my_app
	return render_to_response("index.html", {"app":my_app})

def music(req):
	global my_app
	my_app.update_music_status()
	return render_to_response("index.html", {"app":my_app})

def weibo(req):
	global my_app
	my_app.post_weibo()
	return render_to_response("index.html", {"app":my_app})


