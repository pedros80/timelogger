#!/usr/bin/env python
""" 
time_logger.py

Store start and stop times for named tasks and calculate the previous time
spent on them.

requires - python 2.x, Tkinter and MySQLdb.
run python setup_logger.py to start
change username and password in Logger() at bottom of script

See also README.md and LICENSE.txt

"""

__author__ = "Peter Somerville"
__email__ = "peterwsomerville@gmail.com"
__version__ = "1.0.1"
__date__ = "21/5/12"


import Tkinter as tk
import MySQLdb as mdb
import datetime
import sys

class ScrolledList(tk.Frame):
    def __init__(self, options, parent=None):
        tk.Frame.__init__(self, parent, bg="black")
        self.pack(expand=tk.YES, fill=tk.BOTH)                
        self.makeWidgets(options)
    def makeWidgets(self, options):                 
        sbary = tk.Scrollbar(self)
        sbarx = tk.Scrollbar(self)
        list = tk.Listbox(self, relief=tk.SUNKEN, width=35, height=12,bg="black",fg="white")
        sbary.config(command=list.yview)                 
        sbarx.config(command=list.xview,orient=tk.HORIZONTAL)
        list.config(yscrollcommand=sbary.set,xscrollcommand=sbarx.set)           
        sbary.pack(side=tk.RIGHT, fill=tk.Y)           
        sbarx.pack(side=tk.BOTTOM, fill=tk.X)
        list.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH) 
        self.listbox = list


class Logger(tk.Frame):
    def __init__(self, user, pword, host="localhost", master=None,):
        tk.Frame.__init__(self, master)
       
        try:
            self.con = mdb.connect(host, user, pword, 'logger')
            self.cur = self.con.cursor()
        except  mdb.Error, e:
            print "Failed to connect to database"
            sys.exit(1)
        self.grid()
        self.master.title("Log Time Spent On Tasks")
        self.create_widgets()
        self.get_tasks()
        self.current_task = None
        self.start = None
          
        
    def create_widgets(self):
        self.tasks = ScrolledList(self)
        self.tasks.grid(row=0, column=1)
        self.tasks.listbox.bind("<Double-1>", self.task_a)
        self.tasks.listbox.bind("<Return>", self.task_a)
        self.bframe=tk.Frame(self, bg="black")
        self.bframe.grid(row=0, column=0, sticky="nsew")
        
        self.get_tasks_btn = tk.Button(self.bframe, text="All Tasks", command=self.get_tasks, width=8, bg="black", fg="white")
        self.get_tasks_btn.grid(row=0, column=0, sticky=tk.N+tk.W)
        self.get_tasks_btn.bind("<Return>", self.get_tasks_a)
        
        self.stop_btn = tk.Button(self.bframe, text="Stop", command=self.stop, state=tk.DISABLED, width=8, bg="black", fg="white")
        self.stop_btn.grid(row=0, column=2, sticky=tk.N)
        self.stop_btn.bind("<Return>", self.stop_a)
        
        self.start_btn = tk.Button(self.bframe, text="Start", command=self.start, width=8, bg="black", fg="white")
        self.start_btn.grid(row=0, column=1, sticky=tk.W)
        self.start_btn.bind("<Return>", self.start_a)
        

        self.details_btn = tk.Button(self.bframe, text="Task Details", command=self.task, width=8, bg="black", fg="white")
        self.details_btn.grid(row=1, column=0, sticky=tk.W)
        self.details_btn.bind("<Return>", self.task_a)
        
        self.del_task_btn = tk.Button(self.bframe, text="Remove Task", command=self.remove, width=8, bg="black", fg="white")
        self.del_task_btn.grid(row=1, column=1, sticky=tk.E)
        self.del_task_btn.bind("<Return>", self.remove_a)
        
        self.quit_btn = tk.Button(self.bframe, text="Quit", command=self.quit, width=8, bg="red", fg="black")
        self.quit_btn.grid(row=1, column=2)
        self.quit_btn.bind("<Return>", self.quit_a)
        
        self.space = tk.Label(self.bframe, height=4, bg="black", fg="white")
        self.space.grid(row=2, column=0, columnspan=3, sticky=tk.E+tk.W)
        
        self.new_btn = tk.Button(self, text="New Task", command=self.new_task, bg="black", fg="white")
        self.new_btn.grid(row=4, column=0, sticky=tk.W+tk.E)
        self.new_btn.bind("<Return>", self.new_task_a)
        
        self.task_name = tk.Entry(self, bg="grey")
        self.task_name.grid(row=3, column=0, sticky=tk.E+tk.N+tk.S+tk.W)

    
    def task(self):
        if self.tasks.listbox.curselection():
            self.space.config(text="")
            tid = int(self.tasks.listbox.get(self.tasks.listbox.curselection()).split("-")[0])
            self.cur.execute("SELECT SEC_TO_TIME(SUM(TIME_TO_SEC(stop) - TIME_TO_SEC(start))) FROM logs WHERE tid='%d'"%tid)
            row = self.cur.fetchone()
            if row[0] is not None:
                duration = (datetime.datetime.min+row[0]).time()
            else:
                duration = 0
            self.cur.execute("SELECT descript FROM tasks WHERE tid='%d'"%tid)
            task = self.cur.fetchone()[0]
            self.tasks.listbox.delete(0,tk.END)
            self.tasks.listbox.insert(0, "%d - %s - %s"%(tid, task, duration))
            self.space.config(text="Time spent: \n %s"% duration)
            self.del_task_btn.config(state=tk.DISABLED)
            self.details_btn.config(state=tk.DISABLED)
            self.start_btn.config(state=tk.DISABLED)
            self.get_tasks_btn.config(state=tk.NORMAL)
        else:
            self.space.config(text="Select a task first...")
            
    def new_task(self):
        des = self.task_name.get()
        if des is not "":
            self.space.config(text="")
            self.cur.execute("INSERT INTO tasks (descript) VALUES ('%s')"%des)
            self.get_tasks()
            self.task_name.delete(0,tk.END)
        else:
            self.space.config(text="Enter a task description...")
            
    def new_task_a(self, event):
        self.new_task()

    def remove(self):
        if self.tasks.listbox.curselection():
            self.space.config(text="")
            tid = int(self.tasks.listbox.get(self.tasks.listbox.curselection()).split("-")[0])
            try:
                self.cur.execute("DELETE FROM logs WHERE tid='%d'"%tid)
                self.cur.execute("DELETE FROM tasks WHERE tid='%d'"%tid)
            except mdb.Error, e:
                print "Error %d: %s" % (e.args[0],e.args[1])
                sys.exit(1)
            self.get_tasks()
        else:
            self.space.config(text="Select a task to remove...")
        
    def start(self):
        if self.tasks.listbox.curselection() and self.current_task is None:
            self.start_config()
            tid, description = self.tasks.listbox.get(self.tasks.listbox.curselection()).split("-")
            self.space.config(text="Timing - '%s'"%description)
            tid = int(tid)
            self.current_task = tid
            now = datetime.datetime.now()
            now = now.isoformat(' ').split(".")[0]
            self.start = now
            try:
                self.cur.execute("INSERT INTO logs (tid, start) VALUES ('%d', '%s')"%(tid,now))
            except mdb.Error, e:
                print "fail"
                sys.exit(1)
        else:
            self.space.config(text="Select a task to start timing...")
                   
    def stop(self):
        if self.tasks.listbox.curselection() and self.current_task is not None:
            self.stop_config()
            self.space.config(text="")
            tid = self.current_task
            self.current_task = None
            now = datetime.datetime.now()
            now = now.isoformat(' ').split(".")[0]
            self.cur.execute("UPDATE logs SET stop='%s' WHERE tid='%d' AND start='%s'"%(now,tid,self.start))
     
    def get_tasks(self):
        self.tasks.listbox.delete(0,tk.END)
        self.del_task_btn.config(state=tk.NORMAL)
        self.details_btn.config(state=tk.NORMAL)
        self.get_tasks_btn.config(state=tk.DISABLED)
        self.start_btn.config(state=tk.NORMAL)
        try:
            self.cur.execute("SELECT tid, descript FROM tasks ORDER BY tid")
            rows = self.cur.fetchall()
            for row in rows:
                self.tasks.listbox.insert(tk.END, "%d - %s" %(row[0], row[1]))
        except mdb.Error, e:
            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)
            
    def task_a(self, event):
        self.task()
    def remove_a(self, event):
        self.remove()
    def get_tasks_a(self,event):
        self.get_tasks()
    def stop_a(self, event):
        self.stop()
    def start_a(self, event):
        self.start()
    def quit_a(self, event):
        self.quit()

    def stop_config(self):
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.new_btn.config(state=tk.NORMAL)
        self.details_btn.configure(state=tk.NORMAL)
        self.del_task_btn.configure(state=tk.NORMAL)
        self.quit_btn.config(state=tk.NORMAL)

    def start_config(self):
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.new_btn.config(state=tk.DISABLED)
        self.get_tasks_btn.config(state=tk.DISABLED)
        self.details_btn.configure(state=tk.DISABLED)
        self.del_task_btn.configure(state=tk.DISABLED)
        self.quit_btn.config(state=tk.DISABLED)

if __name__ == "__main__":
    # change username and password to match user created after setup_logger.py
    # if host is not localhost add third argument, i.e. call Logger('user','pass','host') 
    log = Logger("logger_u", "this is a dummy pass")
    log.mainloop()