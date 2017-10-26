from main import *
import utilities as utils
import objects
class Quit(Exception):
	pass
class GameOver(Exception):
	pass
@ConfigGLO
class State(object):
	BreakException 	= Exception
	Use__loop__		= True
	def __init__(self, *args):
		self.glo.display.clear()
		self.init(*args)
		try:
			while True:
				self.loop()
				self.__loop__()
				self.glo.display.update()
				self.glo.display.clock.tick(self.glo.dsp_max_frames)
				gc.collect()
		except self.BreakException:
			return
	def __loop__(self):
		for Item in self.UI:
			if self.UI[Item]['Open']:
				curitem = self.UI[Item]
				for btn in curitem['Buttons']:
					btn.update()
				for txt in curitem['Text']:
					self.glo.display.queue(*txt)
				for event in pygame.event.get([pygame.MOUSEBUTTONUP,pygame.KEYDOWN,pygame.QUIT]):
					pygame.event.post(event)
					if event.type == pygame.MOUSEBUTTONUP:
						if curitem['Hide']:
							if not curitem['Base'].rect.collidepoint(pygame.mouse.get_pos()):
								curitem['Open'] = False
								self.glo.display.queue(self.glo.background,curitem['Base'].rect)
								curitem['Button'].recolour(curitem['Button'].colour,curitem['Button'].showpress)
					elif event.type == pygame.QUIT:
						raise Quit
					elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
						if curitem['Hide']:
							curitem['Open'] = False
							self.glo.display.queue(self.glo.background,curitem['Base'].rect)
							curitem['Button'].recolour('curitem'['Button'].colour,curitem['Button'].showpress)
						else:
							self.Exit('ESC_KEY')
					

		pygame.event.clear()
	def init(self):
		pass
	def loop(self):
		raise self.BreakException
	def Exit(self,caller = None):
		self.glo.display.clear()
		raise self.BreakException
		raise Exception('Loop exit call failed')
class MainMenu(State):
	BreakException = Quit
	def init(self):
		self.UI = {}
		self.GameOptions  = {'width':10,'height':10,'bombs':10}
		
		textStart 	= self.glo.display.render("New Game","grey","text",centery = 70,left = 10)
		textOptions	= self.glo.display.render("Game Options","grey","text",centery = 140,left = 10)
		textExit	= self.glo.display.render("Quit","grey","text",centery = 210,left = 10)
		
		butStart	= utils.Button("green",self.NewGame,2,left = 0,top = 50,width=150,height=40)
		butOptions	= utils.Button("orange",self.dispOptions,2,left = 0, top = 120,width = 150,height = 40)
		butExit		= utils.Button("red",self.Exit,2,left = 0,top = 190,width=150,height=40)
		sideBar		= utils.Button("darkgrey",lambda me:None,False,left = 0,top = 0,width=150,height=self.glo.dsp_window_height)
		self.UI["Base"] = {'Open':True,'Text':[textStart,textOptions,textExit],'Buttons':[sideBar,butStart,butExit,butOptions],'Base':sideBar,'Button':None,'Hide':False}
		
		#Game option menu
		title		= self.glo.display.render('Game Settings',"lightorange","menu_title",top = 50,centerx = 250)
		
		opsideBar 	= utils.Button("darkorange",lambda me:None,False,left = 150,top = 0,width=200,height=self.glo.dsp_window_height)
		mclevel		= utils.MultipleChoice(self.LevelChanged,'Difficulty',['Easy','Medium','Hard','Debug','Custom'],0,(175,100),150)
		butWidth	= utils.TButton("Width","lightorange",self.cgs,1,left= 175,top=mclevel.rect.bottom + 20, width = 30,height = 10)
		butHeight	= utils.TButton("Height","lightorange",self.cgs,1,left= 205,top=mclevel.rect.bottom + 20, width = 30,height = 10)
		butBombs	= utils.TButton("Bombs","lightorange",self.cgs,1,left= 235,top=mclevel.rect.bottom + 20, width = 30,height = 10)
		self.UI['opmenu1']	={'Open':False,'Text':[title],'Buttons':[opsideBar,mclevel,butWidth,butHeight,butBombs],'Base':opsideBar,'Button':butOptions,'Hide':True}
	def loop(self):		
		pass
	def NewGame(self,caller =None):
		pygame.event.clear()
		gui = GameUI(self.GameOptions)
	def dispOptions(self,caller=None):
		self.UI['opmenu1']['Open'] = True
		caller.recolour(self.UI['opmenu1']['Base'].colour,False)
		pygame.event.clear()
	def cgs(self,caller):
		self.GameOptions[caller.text.lower()] = tkSimpleDialog.askinteger("Set "+caller.text,caller.text + ":",initialvalue = self.GameOptions[caller.text.lower()],minvalue=1,maxvalue= 900*(caller.text=="Bombs")+30*(not caller.text=="Bombs"))
	def LevelChanged(self,caller):
		if not caller.selOption == "Custom":
			self.GameOptions.update(self.glo.game_level_presets[caller.selOption])
		
		
class GameUI(State):
	BreakException = GameOver
	def init(self,gameOpt):
		self.UI = {}
		self.GameOptions  = gameOpt
		self.Game 	= objects.Manager(self)

		textmenu 	= self.glo.display.render("Menu","white","uitext",centery=10,centerx = 25)
		textbombs	= self.glo.display.render("Total Bombs: " + `self.GameOptions['bombs']`,"white","uitext",centery=10,left = 160)
		texttiles	= self.glo.display.render("Tiles: " + `self.GameOptions['width']*self.GameOptions['height']`,"white","uitext",centery=10,left = 170 + textbombs[1].width)
		
		topbar		= utils.Button("darkgrey",lambda me:None,False,left = 0,top = 0,width=self.glo.dsp_window_width,height=20)
		butMenu		= utils.Button("lightgrey",self.ShowMenu,2,left=0,top=0,width=150,height=20)
		
		self.UI["Base"] = {'Open':True,'Text':[textmenu,textbombs,texttiles],'Buttons':[topbar,butMenu],'Base':topbar,'Button':None,'Hide':False}
		#PauseMenu
		textExit	= self.glo.display.render("Quit","grey","text",centery = 70,left = 10)
		
		butExit		= utils.Button("red",self.Exit,False,left = 0,top = 50,width=150,height=40)
		sidebar		= utils.Button("grey",lambda me:None,False,left = 0,top = 20,width=150,height=self.glo.dsp_window_height-20)
		self.UI["Paused"] = {'Open':False,'Text':[textExit],'Buttons':[sidebar,butExit],'Base':sidebar,'Button':butMenu,'Hide':True}
		self.glo.display.fill("lightblue")
	def loop(self):
		if not self.UI['Paused']['Open']:
			self.Game.update()
	def ShowMenu(self,caller=None):
		self.UI['Paused']['Open'] = True
		caller.recolour(self.UI['Paused']['Base'].colour,False)
		pygame.event.clear()