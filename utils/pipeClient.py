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
    def __init__(self,pipeName,returnHandler):
        self.pipeName=pipeName
        self.returnHandler=returnHandler
        self.pipe = open(pipeName, 'r+b', 0)       
        self.loop = asyncio.get_event_loop()
        #self.loop.create_task(self.pipeHandler())
        #self.loop.create_task(self.pipeReader())
        #self.loop.create_task(self.pipeWriter())

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

    async def continuousPipeReader(self):
        while True:
            self.reader = pipeReader(self.pipe)
            self.reader.start()
            count = 0
            while self.reader.reader == None:
                count+=1
                if self.reader.reader != None:
                    #await self.returnHandler(self.reader.reader)
                    print(f"message: {self.reader.reader}")
                await asyncio.sleep(0.5)
                if count == 5:
                    print("tooo Long")
                    #self.reader.join()
                    #print(self.reader.is_alive())
                    await asyncio.sleep(55)
            # try:
            #     print("BLAHH")
            #     resp =  win32file.ReadFile(self.pipe, 64*1024)
            #     print(f"message: {resp}")
            #     await asyncio.sleep(0.5)
            # except pywintypes.error as e:
            #     pass

    async def pipeReader(self): #for whatever reason this reads but however it doesnt get the first two characters
        print("Starting read")
        n = struct.unpack('I', self.pipe.read(4))[0]    # Read str length
        resp = self.pipe.read(n)                           # Read str
        print(type(resp))
        self.pipe.seek(0) 
        print(resp) 
        resp = resp.decode('utf-16')      
        #resp[1] = resp[1].decode('utf-16')
        print(resp)
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
        #self.logger=logger
        self.reader = None
        self.pipe = pipe
        threading.Thread.__init__(self)

    def run(self):  
        while self.reader == None:
            try: 
                n = struct.unpack('I', self.pipe.read(4))[0]    # Read str length
                resp = self.pipe.read(n)                           # Read str
                self.pipe.seek(0)        
                resp[1] = resp[1].decode('utf-16')
                self.reader = resp
                print(resp)
                time.sleep(5)
            except pywintypes.error as e:
                print("[Pipe Reader] Ouch..  that did not work as intended...")