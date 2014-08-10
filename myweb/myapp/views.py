from django.shortcuts import render

# Create your views here.

'''
from django.http import HttpResponse
def index(req):
	return HttpResponse('<h1>hello world</h1>')
'''

from django.shortcuts import render_to_response
from subprocess import *
from django.http import HttpResponse

class App(object):
	def __init__(self):
		self.music = "off"
		self.cmd_out = ""
		self.light = "off"

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
		Popen(args)

	def ir_tv(self, key):
		tv_map = {"Power":"KEY_POWER", "Mute":"KEY_MUTE", "OK":"KEY_OK", "Ch+":"KEY_UP",\
			"Ch-":"KEY_DOWN", "Vol+":"KEY_VOLUMEUP", "Vol-":"KEY_VOLUMEDOWN"}
		if not key in tv_map:
			print "error: %s" %(key)

		print "send tv key: %s" %(tv_map[key])
		cmd = "/home/pi/tv/send_tv_key.sh" + " " + tv_map[key]
		args = cmd.split(" ")
		Popen(args)

	def switch_light(self):
		if cmp(self.light, "off") == 0:
			self.light = "on"
		else:
			self.light = "off"

	def exec_command(self, command):
		args = command.split(" ")
		if command == "clear":
			self.cmd_out = ""
			return
		try:
			p = Popen(args=args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
			self.cmd_out = p.stdout.read()
		except:
			self.cmd_out = "command error"



my_app = App()

def index(req):
	global my_app
	print req.POST
	
	if req.POST.has_key('weibo'):
		print "weibo"
		content = req.POST['weibo_content']
		my_app.post_weibo(content)
		return HttpResponse("<h3>content:</h3>%s<h3>Post success!</h3>" %content)

	elif req.POST.has_key('music'):
		print "music"
		my_app.update_music_status()
		return render_to_response("index.html", {"app":my_app})

	elif req.POST.has_key('tv'):
		key_value = req.POST['tv']
		print key_value
		my_app.ir_tv(key_value)
		return render_to_response("index.html", {"app":my_app})

	elif req.POST.has_key('lights'):
		print "light"
		my_app.switch_light()
		return render_to_response("index.html", {"app":my_app})

	elif req.POST.has_key('command'):
		content = req.POST['command_line']
		print content
		my_app.exec_command(content)
		return render_to_response("index.html", {"app":my_app})

	else:
		return render_to_response("index.html", {"app":my_app})


