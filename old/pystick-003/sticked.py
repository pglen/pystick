#!/usr/bin/env python

import os, sys, getopt, signal
import gobject, gtk, pango

import random, time
import yellow, treehand, sutil

class StickEd():
    
    def __init__(self, par, cb, head = None, body = None):
    
        self.cb = cb
        self.window = window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        window.set_title("Python Sticky Editor")
        window.set_position(Gtk.WindowPosition.CENTER)
        
        window.set_modal(True )
        window.set_transient_for(par)
       
        #ic = Gtk.Image(); ic.set_from_stock(Gtk.STOCK_DIALOG_INFO, Gtk.IconSize.BUTTON)
        #window.set_icon(ic.get_pixbuf())
        
        #www = Gdk.Screen.width(); hhh = Gdk.Screen.height();
        www, hhh = sutil.get_screen_wh()
        
        window.set_default_size(www/2, hhh/2)
        
        window.set_flags(Gtk.CAN_FOCUS | Gtk.SENSITIVE)
         
        window.set_events(  Gdk.EventMask.POINTER_MOTION_MASK |
                            Gdk.EventMask.POINTER_MOTION_HINT_MASK |
                            Gdk.EventMask.BUTTON_PRESS_MASK |
                            Gdk.EventMask.BUTTON_RELEASE_MASK |
                            Gdk.EventMask.KEY_PRESS_MASK |
                            Gdk.EventMask.KEY_RELEASE_MASK |
                            Gdk.EventMask.FOCUS_CHANGE_MASK )
         
        # W1           
        window.connect("key-press-event", self.key_press_event)        
        window.connect("button-press-event", self.area_button)        
        
        window.set_icon_from_file("icon.png")
        
        vbox = Gtk.VBox()
        
        self.vspacer(vbox)
        lab1 = Gtk.Label(label="  Header:")
        hbox2 = Gtk.HBox(); hbox2.pack_start(lab1, False )
        vbox.pack_start(hbox2, False )
        self.vspacer(vbox)
 
        hbox3 = Gtk.HBox(); 
        self.spacer(hbox3)
        self.head = Gtk.Entry();
        if head != None: self.head.set_text(head)
        
        hbox3.pack_start(self.head, True, True, 0)
        self.spacer(hbox3)
        vbox.pack_start(hbox3, False )
        hbox4 = Gtk.HBox(); 
        self.spacer(hbox4)
        
        self.vspacer(vbox)
        lab2 = Gtk.Label(label="  Text:")
        hbox2b = Gtk.HBox(); hbox2b.pack_start(lab2, False )
        vbox.pack_start(hbox2b, False )
        self.vspacer(vbox)
   
        self.text = Gtk.TextView();
        self.text.set_border_width(8)
        if body != None: 
            self.text.grab_focus()
            buff = Gtk.TextBuffer(); buff.set_text(body)
            self.text.set_buffer(buff)

        sw = Gtk.ScrolledWindow()
        sw.add(self.text)
        sw.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
       
        self.spacer(hbox4)
        hbox4.pack_start(sw, True, True, 0)
        self.spacer(hbox4)
        
        vbox.pack_start(hbox4, True, True, 0)
        
        hbox = Gtk.HBox()
        
        self.spacer(hbox)
        
        butt1 = Gtk.Button(" _OK ")
        butt1.connect("clicked", self.click_ok, window)
        hbox.pack_end(butt1, False)
        
        butt2 = Gtk.Button(" _Cancel ")
        butt2.connect("clicked", self.click_can, window)
        hbox.pack_end(butt2, False)
       
        vbox.pack_start(hbox, False ) 
       
        window.add(vbox)
        window.show_all()

    def spacer(self, hbox, xstr = "    "):
        lab = Gtk.Label(label=xstr)
        hbox.pack_start(lab, False )
       
    def vspacer(self, vbox):
        lab = Gtk.Label(label=" ")
        vbox.pack_start(lab, False )
        
    def click_ok(self, butt, xx):
        self.cb(self)
        self.window.destroy()
        pass
        
    def click_can(self, butt, xx):
        self.window.destroy()
        pass
    
    def key_press_event(self, win, event):
    
        if event.keyval == Gdk.KEY_Escape:
            self.window.destroy()
    
    def  area_button(self, butt):
        pass
    
    
    
    
    
    
    
    


