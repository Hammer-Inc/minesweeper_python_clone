import pygame
import traceback as tb
all = [
	'Display'
]
class Display():
	colour = None
	def __init__(self,glo):
		self.g = glo
		pygame.init()
		self.clear()
		pygame.display.set_caption(self.g.title)
		self.clock      = pygame.time.Clock()
		self.colour     = Colours()
		self.font       = Fonts()
	def __getattr__(self,name):
		return self.colour[name]
	def __getitem__(self,name):
		if hasattr(self.colour,name):
			return self.colour[name]
		return 'INVALID_DISPLAY_ATTRIBUTE'
	def fill(self,colour,rect = None):
		if type(colour) is str:
			colour = self.colour[colour]
		self.display.fill(colour,rect)
	def queue(self,obj,rect,area = None):
		#convert the rect to the pygame.Rect type if it isnt
		if type(rect) is tuple or type(rect) is list:
			if len(rect) == 2 and type(obj) is pygame.Surface:
				rect = pygame.Rect(rect,obj.get_size())
			elif len(rect) == 4:
				rect = pygame.Rect(rect)
		else:
			try:
				rect = pygame.Rect(rect)
			except Exception:
				if not area is None:
					rect = pygame.Rect(area)
				else:
					rect = pygame.Rect((0,0,0,0))
		if type(obj) is str:
			obj = self.colour[obj]
		if type(obj) is tuple:
			surf = pygame.Surface(rect.size)
			surf.fill(obj)
			obj = surf
		if type(obj) is pygame.Surface:
			self.lstRefresh.append([obj,rect,area])
		else:
			#if an invalid object is passed as a surface render it anyway
			self.queue("error",rect)
	def cancel(self):
		self.lstRefresh = []
		self.lstClean   = []
	def clear(self):
		self.display = pygame.display.set_mode((self.g.dsp_window_width,self.g.dsp_window_height),pygame.FULLSCREEN*self.g.dsp_screen_mode)
		self.display.fill(self.g.background)
		pygame.display.update()
		self.lstRefresh = []
		self.lstClean   = []
	def render(self,text,colour,font,**position):
		if type(colour) is str: colour = self.colour[colour]
		txt     = self.font[font].render(text,self.g.dsp_use_antialias,colour)
		recttxt = txt.get_rect()
		for key in position:
			exec('recttxt.' + key + '= position[key]')
		return txt,recttxt
	def update(self):
		#blit pair to the screen, update the rects in lstClean, and lstRefresh
		#update lstClean to the rects in lstRefresh
		#clear lstRefresh
		for pair in self.lstRefresh:
			self.display.blit(*pair)
		self.lstClean.extend(x[1] for x in self.lstRefresh)
		pygame.display.update(self.lstClean)
		self.lstClean   = list(x[1] for x in self.lstRefresh)
		self.lstRefresh = []


class Fonts():
	pygame.font.init()
	default		= pygame.font.SysFont("ariel",10)
	title		= pygame.font.SysFont("AR CARTER",50)
	text		= pygame.font.SysFont("AR CARTER",20,1)
	menu_title	= pygame.font.SysFont("AR CARTER",25,1)
	optionfont	= pygame.font.SysFont("AR CARTER",20)
	uitext		= pygame.font.SysFont("Times New Roman",15)
	nodefont	= pygame.font.SysFont("Times New Roman",20)
	def __getitem__(self,name):
		return eval('self.' + name)
	def __getattr__(self,name):
		return self.default



class Colours(object):
	lightgreen 	= (100,255,100)
	green 		= (0,255,0)
	darkgreen	= (0,100,0)
	
	white 		= (255,255,255)
	lightgrey 	= (200,200,200)
	grey  		= (100,100,100)
	darkgrey  	= (50,50,50)
	black 		= (0,0,0)
	
	lightred 	= (255,100,100)
	red   		= (255,0,0)
	darkred 	= (100,0,0)
	
	lightblue 	= (100,100,255)
	blue  		= (0,0,255)
	darkblue	= (0,0,100)

	lightorange = (255,200,100)
	orange		= (255,165,0)
	darkorange	= (200,120,0)
	
	error = (100,50,200)
	def __getattr__(self,name):
		exec('self.' + name + '= self.error')
		return self.error
	def __setattr__(self,name,value):
		if name in dir(self) or not type(value) is tuple or not len(value) == 3: return
		exec('self.'+name+'=value')
	def __getitem__(self,name):
		return self.__getattribute__(name)
	def __setitem__(self,name,value):
		self.__setattribute__(name,value)