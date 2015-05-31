#!/usr/bin/python

import os.path
import json

class Game:
    Pod     = dict()
    Setting = dict()

class Setting:
    def __init__(self, filename):
        self.filename = filename
        
        if not self.Read():
            sys.exit("Settings.__init__ CRITICAL Unable to read settings from file: [%s]" % self.filename)

    def Read(self):
        if os.path.isfile(self.filename):
            try:
                fd = open(self.filename, "r")
                setting = dict(json.load(fd))
                for key, val in setting["general"].items():
                    Game.Setting[key]    = val
                for pod in setting["pods"]:
                    Game.Pod[pod["name"]] = pod
                fd.close()
                return(True)
            
            except IOError as e:
                print("Settings.Read ERROR tryin to open [%s]" % (e.info, self.filename))
                return(False)
        else:
            return(False)


if __name__ == "__main__":
    
    s = Setting("./tron.json")
    
    for k, v in Game.Setting.items():
        print("%s: %s" %(k, v))
    for k, v in Game.Pod.items():
        print("%s: %s" % (k, v))