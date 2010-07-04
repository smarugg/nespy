import wx
import os
import thread
global pygame # when we import it, let's keep its proper name!

class SDLThread:
    def __init__(self,screen):
        self.m_bKeepGoing = self.m_bRunning = False
        self.screen = screen
        self.color = (255,0,0)
        self.rect = (10,10,100,100)

    def Start(self):
        self.m_bKeepGoing = self.m_bRunning = True
        thread.start_new_thread(self.Run, ())

    def Stop(self):
        self.m_bKeepGoing = False

    def IsRunning(self):
        return self.m_bRunning

    def Run(self):
        while self.m_bKeepGoing:
            e = pygame.event.poll()
            if e.type == pygame.MOUSEBUTTONDOWN:
                self.color = (255,0,128)
                self.rect = (e.pos[0], e.pos[1], 100, 100)
                print e.pos
            self.screen.fill((0,0,0))
            self.screen.fill(self.color,self.rect)
            pygame.display.flip()
        self.m_bRunning = False;

class SDLPanel(wx.Panel):
    def __init__(self,parent,ID,tplSize):
        global pygame
        wx.Panel.__init__(self, parent, ID, size=tplSize)
        self.Fit()
        os.environ['SDL_WINDOWID'] = str(self.GetHandle())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        import pygame # this has to happen after setting the environment variables.
        pygame.display.init()
        window = pygame.display.set_mode(tplSize)
        self.thread = SDLThread(window)
        self.thread.Start()

    def __del__(self):
        self.thread.Stop()

class MyFrame(wx.Frame):
    def __init__(self, parent, ID, strTitle, tplSize):
        wx.Frame.__init__(self, parent, ID, strTitle, size=tplSize)
        self.pnlSDL = SDLPanel(self, -1, tplSize)
        
        #housekeeping
        self.currentDirectory = os.getcwd()
        
        #create status bar
        statusBar = self.CreateStatusBar()
        
        #create menu bar and itemse
        menuBar = wx.MenuBar()
        firstOption = wx.Menu()
        secondOption = wx.Menu()
        thirdOption = wx.Menu()
        
        #define some identifiers
        ID_OPEN = 1
        ID_EXIT = 2
        
        ID_CPU = 3
        ID_PAUSE = 4
        
        ID_DISASSEMBLY = 5
        ID_MEMORY = 6
        
        #first menu options (File)    
        firstOption.Append(ID_OPEN, "Open Rom", "Open a NES rom located on your computer")
        firstOption.Append(ID_EXIT, "Exit", "Close nespy")
        
        #second menu options (CPU)
        secondOption.Append(ID_CPU, "Reset", "Reset execution of the current rom")
        secondOption.Append(ID_PAUSE, "Pause", "Pause execution of the current rom")
        
        #third menu options (Debug)
        thirdOption.Append(ID_DISASSEMBLY, "Disassembly", "Show the disassembly of the current rom")
        thirdOption.Append(ID_MEMORY, "Memory", "View the memory of the current rom")
        
        #add menu items to menubar
        menuBar.Append(firstOption, "File")
        menuBar.Append(secondOption, "CPU")
        menuBar.Append(thirdOption, "Debug")
        
        self.SetMenuBar(menuBar)
        
        #Define the code to be run when a menu option is selected
        #wx.EVT_MENU(self, ID_EXIT, self.OnExit)
        wx.EVT_MENU(self, ID_OPEN, self.OnOpen)
        wx.EVT_MENU(self, ID_EXIT, self.OnExit)
        

        #self.Fit()
     
    #method handling opening of rom files from menu
    def OnOpen(self, e):
        #the limitation of file types
        wildcard = "NES rom (*.nes)|*.nes|" \
                    "All files (*.*)|*.*"    
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=self.currentDirectory,
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            print "You chose the following file(s):"
            for path in paths:
                print path
        dlg.Destroy()    
            
     
    #method handling exiting of program from menu
    def OnExit(self, e):
        self.Close(True)
        
        
        

app = wx.PySimpleApp()
frame = MyFrame(None, wx.ID_ANY, "nespy 0.1", (640,480))
frame.Show()
app.MainLoop()