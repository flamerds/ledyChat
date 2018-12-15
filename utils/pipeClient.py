import asyncio
import sys

import time
import win32pipe, win32file, pywintypes
import threading

import struct
import codecs

#not required
import random

class pipeClient():
    def __init__(self,pipeName):
        self.pipeName=pipeName
        self.pipe = open(pipeName, 'r+b', 0)       


    async def pipeHandler(self): 
        while True:
            try:
                self.pipe=win32file.CreateFile(r'\\.\pipe\Demo', win32file.GENERIC_READ | win32file.GENERIC_WRITE, 0, None, win32file.OPEN_EXISTING, 0, None)
            except pywintypes.error as e:
                if e.args[0] == 2:
                    print("no pipe, trying again in a sec")
                    time.sleep(1)
                elif e.args[0] == 109:
                    print("broken pipe, bye bye")
                    quit = True
            asyncio.sleep(0.5)


    # async def pipeReader(self): #for whatever reason this reads but however it doesnt get the first two characters
    #     print("Starting read")
    #     n = struct.unpack('I', self.pipe.read(4))[0]    # Read str length
    #     resp = self.pipe.read(n)                           # Read str
    #     print(type(resp))
    #     self.pipe.seek(0) 
    #     print(resp) 
    #     resp = resp.decode('utf-16')      
    #     #resp[1] = resp[1].decode('utf-16')
    #     print(resp)
    #     return resp

    async def pipeReader(self): #for whatever reason this reads but however it doesnt get the first two characters
        print("Starting read")
        reader = pipeReader(self.pipe)
        reader.start()
        while reader.reader == None:
            await asyncio.sleep(1)
        resp = reader.reader
        reader.join()
        return resp

    async def pipeWriter(self,data):
        print("blah")
        print("Active Threads: {0}".format(threading.active_count()))
        try:
            # convert to bytes
            #some_data = data.encode('utf-16')
            some_data = data
            print(some_data)
            self.thread = threading.Thread(name='pipeWriter',target=self.write, args=[self.pipe, some_data])
            self.thread.start()
            await asyncio.sleep(2)
            print("YAYYY")
            #win32file.WriteFile(handle, some_data)
        except pywintypes.error as e:
            print("error...")
            pass
    
    def write(self,pipe,data):
        print("writing")
        pipe.write(data.encode('utf-16-le').strip(codecs.BOM_UTF16)) #this can probably be removed as byte order doesnt seem to be a thing when using -le or -be
        pipe.seek(0)
        print("written")


    def start(self):
        self.loop.run_forever()


class pipeReader(threading.Thread):
    def __init__(self,pipe):
        self.reader = None
        self.pipe = pipe
        threading.Thread.__init__(self)

    def run(self):  
        while self.reader == None:
            try: 
                n = struct.unpack('I', self.pipe.read(4))[0]    # Read str length
                resp = self.pipe.read(n)                           # Read str
                self.pipe.seek(0)        
                resp = resp.decode('utf-16')
                self.reader = resp
                time.sleep(5)
            except pywintypes.error as e:
                print("[Pipe Reader] Ouch..  that did not work as intended...")