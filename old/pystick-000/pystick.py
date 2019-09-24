#!/usr/bin/env python

import os, sys, getopt, signal
import gobject, gtk, pango

# ------------------------------------------------------------------------
# This is open source sticker program. Written in python. 

GAP = 4                 # Gap in pixels
TABSTOP = 4
FGCOLOR  = "#000000"
BGCOLOR  = "#ffff88"              

version = 1.0
verbose = False
# Where things are stored (backups, orgs, macros)
config_dir = os.path.expanduser("~/.pystick")

class stickWin():

    def __init__(self, me, head, text):

        window = Gtk.Window(Gtk.WindowType.POPUP)
        window.set_transient_for(me)
        window.set_decorated(False)
        window.set_position(Gtk.WindowPosition.CENTER)
        window.set_default_size(100, 100)
        window.set_flags(Gtk.CAN_FOCUS | Gtk.SENSITIVE)
        #window.connect("motion-notify-event", self.area_motion)        
        window.set_property("destroy-with-parent", True )
        yy = stickDoc(head, text)
        window.add(yy)
        window.show_all()
    
        
class stickDoc(Gtk.DrawingArea):

    def __init__(self, head, text):
    
        self.head = head
        self.text = text
        self.gap = GAP
        
        # Parent widget                 
        GObject.GObject.__init__(self)
        self.set_flags(Gtk.CAN_FOCUS | Gtk.CAN_DEFAULT| Gtk.SENSITIVE | Gtk.PARENT_SENSITIVE)

        self.set_events(  Gdk.EventMask.POINTER_MOTION_MASK |
                    Gdk.EventMask.POINTER_MOTION_HINT_MASK |
                    Gdk.EventMask.BUTTON_PRESS_MASK |
                    Gdk.EventMask.BUTTON_RELEASE_MASK |
                    Gdk.EventMask.KEY_PRESS_MASK |
                    Gdk.EventMask.KEY_RELEASE_MASK |
                    Gdk.EventMask.FOCUS_CHANGE_MASK )

        self.colormap = Gtk.widget_get_default_colormap()
        self.fgcolor  = self.colormap.alloc_color(FGCOLOR)              
        self.bgcolor  = self.colormap.alloc_color(BGCOLOR)              
         
        self.modify_bg(Gtk.StateType.NORMAL, self.bgcolor)
        self.pangolayout = self.create_pango_layout("a")
        
        self.connect("motion-notify-event", self.area_motion)
        self.connect("button-press-event", self.area_button)
        self.connect("expose-event", self.area_expose_cb)
        self.connect("destroy", self.OnExit)

    def area_button(self, area, event):
        self.grab_focus()
        return True

    def area_motion(self, area, event):    
        print "motion event", event.get_state(), event.x, event.y        
        if event.get_state() & Gdk.ModifierType.BUTTON1_MASK:            
            print "drag"

    def setfont(self, fam, size):
    
        fd = Pango.FontDescription()
        fd.set_family(fam)
        fd.set_size(size * Pango.SCALE); 
        self.pangolayout.set_font_description(fd)

        # Get Pango steps
        self.cxx, self.cyy = self.pangolayout.get_pixel_size()
        
        # Get Pango tabs
        self.tabarr = Pango.TabArray(80, False)
        for aa in range(self.tabarr.get_size()):
            self.tabarr.set_tab(aa, Pango.TabAlign.LEFT, aa * TABSTOP * self.cxx * Pango.SCALE)
                
        self.pangolayout.set_tabs(self.tabarr)
        ts = self.pangolayout.get_tabs()
        
        if ts != None: 
            al, self.tabstop = ts.get_tab(1)
        self.tabstop /= self.cxx * Pango.SCALE
                        
    def get_height(self):
        rect = self.get_allocation()
        return rect.height

    def get_width(self):
        rect = self.get_allocation()
        return rect.width
      
    def area_expose_cb(self, area, event):

        #print "area_expose_cb()", event.area.width, event.area.height
        
        # We have a window, goto start pos
        hhh = self.get_height()
        xlen = len(self.text)

        style = self.get_style()
        self.gc = style.fg_gc[Gtk.StateType.NORMAL]
        
        gcx = Gdk.GC(self.window); gcx.copy(self.gc)
        #gcr = Gdk.GC(self.window); gcr.copy(self.gc)
        #colormap = Gtk.widget_get_default_colormap()        
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
        
        # Resize if needed:
        rqx = cxx2 + 4 * self.gap; rqy = cyy2 + 2 * self.gap
        aa, bb = self.get_size_request()
        if aa != rqx or bb != rqy:
            self.set_size_request(rqx, rqy)

    def OnExit(self, aa):
        Gtk.main_quit()


def help():

    print 
    print "PyStick version: ", version
    print 
    print "Usage: " + os.path.basename(sys.argv[0]) + " [options] [[filename] ... [filenameN]]"
    print 
    print "Options:"
    print 
    print "            -d level  - Debug level 1-10. (Limited implementation)"
    print "            -v        - Verbose (to stdout and log)"
    print "            -c        - Dump Config"
    print "            -h        - Help"
    print

def area_motion(self, area, event):    
    print "window motion event", event.get_state(), event.x, event.y        
    if event.get_state() & Gdk.ModifierType.BUTTON1_MASK:            
        print "drag"

# Start of program:

if __name__ == '__main__':

    try:
        if not os.path.isdir(config_dir):
            os.mkdir(config_dir)
    except: pass
    
    # Let the user know it needs fixin'
    if not os.path.isdir(config_dir):
        print "Cannot access config dir:", config_dir
        sys.exit(1)

    opts = []; args = []
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hv")
    except getopt.GetoptError, err:
        print "Invalid option(s) on command line:", err
        sys.exit(1)

    #print "opts", opts, "args", args
    
    for aa in opts:
        if aa[0] == "-d":
            try:
                pgdebug = int(aa[1])
            except:
                pgdebug = 0

        if aa[0] == "-h": help();  exit(1)
        if aa[0] == "-v": verbose = True            
        #if aa[0] == "-x": clear_config = True            
        #if aa[0] == "-c": show_config = True            
        #if aa[0] == "-t": show_timing = True

    if verbose:
        print "PyStick running on", "'" + os.name + "'", \
            "GTK", Gtk.gtk_version, "PyGtk", Gtk.pygtk_version

    www = Gdk.Screen.width(); hhh = Gdk.Screen.height();
    

    window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
    #window.set_decorated(False)
    #window.set_position(Gtk.WindowPosition.CENTER)
    #window.set_default_size(100, 100)
    window.set_flags(Gtk.CAN_FOCUS | Gtk.SENSITIVE)
     
    yy = stickWin(window, "Hello World", "This is a sticky\n"
        "With new longer and longer and longer and longer and longer and longer and longer lines\n"
                        "Done.")
    window.show_all()
           
    Gtk.main()





