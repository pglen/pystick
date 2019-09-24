#!/usr/bin/env python

import os, sys, getopt, signal
import gobject, gtk, pango

import random, time

GAP = 4                 # Gap in pixels
TABSTOP = 4

FGCOLOR  = "#000000"
BGCOLOR  = "#ffff88"              
FRCOLOR  = "#cccc00"              

TOPSTOP = 50
BUTSTOP = 50

# ------------------------------------------------------------------------
# Collection of windows:

class stickList():

    def __init__(self):
        self.data = []
        pass
        
    def add(self, item):
        self.data.append(item)

# Globals
slist = stickList()
xxx = 0; yyy = 50

# -----------------------------------------------------------------------
# Sleep just a little, but allow the system to breed

def  usleep(msec):

    got_clock = time.clock() + float(msec) / 1000
    #print got_clock
    while True:
        if time.clock() > got_clock:
            break
        Gtk.main_iteration_do(False)        
        
# ------------------------------------------------------------------------
# Sticky window:
                
class stickWin():
    
    def __init__(self, me, head, text):
        
        global xxx, yyy, slist
        
        www = Gdk.Screen.width(); hhh = Gdk.Screen.height();
        
        self.window = window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        #self.window = window = Gtk.Window(Gtk.WindowType.POPUP)
        
        window.set_default_size(10, 10)
        #window.set_decorated(False)
        #window.set_has_frame(True )
        
        window.set_type_hint(Gdk.WindowTypeHint.UTILITY)
        
        window.set_events(  Gdk.EventMask.POINTER_MOTION_MASK |
                    Gdk.EventMask.POINTER_MOTION_HINT_MASK |
                    Gdk.EventMask.BUTTON_PRESS_MASK |
                    Gdk.EventMask.BUTTON_RELEASE_MASK |
                    Gdk.EventMask.KEY_PRESS_MASK |
                    Gdk.EventMask.KEY_RELEASE_MASK |
                    Gdk.EventMask.FOCUS_CHANGE_MASK )
                    
        window.set_accept_focus(True)
        window.connect("key-press-event", self.key_press_event)
        window.connect("button-press-event", self.area_button)
        
        #window.connect("motion-notify-event", self.area_motion)        
        #window.connect("destroy", self.OnExit)

        window.set_flags(Gtk.CAN_FOCUS | Gtk.SENSITIVE)
        #window.set_flags(Gtk.CAN_FOCUS | Gtk.CAN_DEFAULT| Gtk.SENSITIVE | Gtk.PARENT_SENSITIVE)
        window.set_destroy_with_parent(True )
        window.set_transient_for(me)
        
        self.sticky = stickDoc(me, head, text)
        window.add(self.sticky)
        window.show_all()
        
        usleep(1)           # Present window
        Gdk.Window.set_decorations(window.get_window(), Gdk.DECOR_BORDER)

        #Gdk.Window.set_composited(window.get_window(), True )
        #Gdk.Window.set_opacity(window.get_window(), .5)
                
        # Arrange it in peace
        yyy = TOPSTOP; xxx = www / 2
        for ww in slist.data: 
            xx, yy = Gdk.Window.get_position(ww.window.get_window())
            ww, hh = Gdk.Window.get_size(ww.window.get_window())
            #print "position", xx, yy, "size", ww, hh
            if yyy + hh >= hhh - 2 * BUTSTOP:
                xxx += 200
                yyy = TOPSTOP
                if xxx > www - 100:
                    xxx = TOPSTOP
            else: 
                yyy +=  hh + 4
        
        #print  xxx, yyy
        window.move(xxx, yyy)
        slist.add(self)  
            
    def area_button(self, area, event):
        #print "win butt"
        return False 
    
    def key_press_event(self, text_view, event):
        #print "window keypress"
        if event.get_state() & Gdk.ModifierType.MOD1_MASK:       
            if event.keyval == Gdk.KEY_x or event.keyval == Gdk.KEY_X:
                sys.exit(0)            
        return False
                        
    def OnExit(self, aa):
        print "onexit"
        #while Gtk.main_level():
        #    Gtk.main_quit()

# ------------------------------------------------------------------------
# The surface of the yellow sticky

class stickDoc(Gtk.DrawingArea):

    def __init__(self, me, head, text):
    
        self.me = me
        self.head = head
        self.text = text
        
        self.gap = GAP
        
        # Parent widget                 
        GObject.GObject.__init__(self)
        #self.set_flags(Gtk.CAN_FOCUS | Gtk.CAN_DEFAULT| Gtk.SENSITIVE | Gtk.PARENT_SENSITIVE)
        self.set_flags(Gtk.CAN_FOCUS | Gtk.SENSITIVE)
        
        self.set_events(    Gdk.EventMask.ALL_EVENTS_MASK )
        
        self.colormap = Gtk.widget_get_default_colormap()
        self.fgcolor  = self.colormap.alloc_color(FGCOLOR)              
        self.bgcolor  = self.colormap.alloc_color(BGCOLOR)              
        self.frcolor  = self.colormap.alloc_color(FRCOLOR)              
         
        self.modify_bg(Gtk.StateType.NORMAL, self.bgcolor)
        self.pangolayout = self.create_pango_layout("a")
        
        self.connect("motion-notify-event", self.area_motion)
        self.connect("button-press-event", self.area_button)
        self.connect("expose-event", self.area_expose_cb)
        self.connect("key-press-event", self.key_press_event)        
        #self.connect("destroy", self.OnExit)

    def area_button(self, area, event):
        print "yellow butt"
        self.ex = event.x; self.ey = event.y
        #par = self.get_parent_window()
        #par.raise_()
        #par.show()
        #par.focus()
        return False 

    def area_motion(self, area, event):    
        #print "motion event", event.get_state(), event.x, event.y        
        if event.get_state() & Gdk.ModifierType.BUTTON1_MASK:            
            #print "dragx", self.ex, event.x, "dragy", self.ey, event.y
            par = self.get_parent_window()
            x, y = par.get_position()
            par.move(   int(x + (event.x - self.ex)),
                            int( y + (event.y-self.ey)))

    def key_press_event(self, text_view, event):
        print "widget keypress"
        if event.get_state() & Gdk.ModifierType.MOD1_MASK:       
            if event.keyval == Gdk.KEY_x or event.keyval == Gdk.KEY_X:
                sys.exit(0)            
        return False
        
    def setfont(self, fam, size):
        fd = Pango.FontDescription()
        fd.set_family(fam)
        fd.set_size(size * Pango.SCALE); 
        self.pangolayout.set_font_description(fd)

        # Get Pango steps
        self.cxx, self.cyy = self.pangolayout.get_pixel_size()
        
        # Get Pango tabs
        '''self.tabarr = Pango.TabArray(80, False)
        for aa in range(self.tabarr.get_size()):
            self.tabarr.set_tab(aa, Pango.TabAlign.LEFT, aa * TABSTOP * self.cxx * Pango.SCALE)
        self.pangolayout.set_tabs(self.tabarr)
        ts = self.pangolayout.get_tabs()
        if ts != None: 
            al, self.tabstop = ts.get_tab(1)
        self.tabstop /= self.cxx * Pango.SCALE'''
                        
    def area_expose_cb(self, area, event):
    
        style = self.get_style()
        self.gc = style.fg_gc[Gtk.StateType.NORMAL]
        
        gcx = Gdk.GC(self.window); gcx.copy(self.gc)
        gcx.set_foreground(self.fgcolor)
        
        self.setfont("system", 14)
        self.pangolayout.set_text(self.head)            
        x = 2 * self.gap; y = self.gap
        self.window.draw_layout(gcx, x, y, self.pangolayout, self.fgcolor, self.bgcolor)
        cxx, cyy = self.pangolayout.get_pixel_size()
        
        self.setfont("system", 11)
        self.pangolayout.set_text(self.text)            
        x = 2 * self.gap; y += self.cyy + self.cyy / 2
        self.window.draw_layout(gcx, x, y, self.pangolayout, self.fgcolor, self.bgcolor)
        cxx2, cyy2 = self.pangolayout.get_pixel_size()
        
        #print  cxx, cyy, cxx2, cyy2
        
        # Resize if needed:
        if cxx < cxx2: cxx = cxx2
        rqx = cxx + 4 * self.gap; 
        rqy = cyy + cyy2 + 2 * self.gap
        
        self.ww, self.hh = self.get_size_request()
        if self.ww != rqx or self.hh != rqy:
            self.set_size_request(rqx, rqy)
        
        win = self.get_window()
        ww, hh = Gdk.Window.get_size(win)
        
        #print "ww,hh", ww, hh
        ww -= 1; hh -= 1
            
        gcx.set_foreground(self.frcolor)
        win.draw_line(gcx, 0, 0, ww, 0)
        win.draw_line(gcx, ww, 0, ww, hh)
        win.draw_line(gcx, 0, 0, 0, hh)
        win.draw_line(gcx, 0, hh, ww, hh)
        


