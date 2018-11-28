import asyncio
import sys

import time
import win32pipe, win32file, pywintypes
import threading

#not required
import random

class pipeClient():
    def __init__(self,pipeName):
        self.pipeName=pipeName
        self.pipe = win32file.CreateFile(self.pipeName, win32file.GENERIC_READ | win32file.GENERIC_WRITE, 0, None, win32file.OPEN_EXISTING, 0, None)        
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

    async def pipeReader(self):
        while True:
            reader = pipeReader(self.pipe)
            reader.start()
            if reader.reader != None:
                reader.reader=reader.reader.decode("utf-16")
                print(f"message: {reader.reader}")
            # try:
            #     print("BLAHH")
            #     resp =  win32file.ReadFile(self.pipe, 64*1024)
            #     print(f"message: {resp}")
            #     await asyncio.sleep(0.5)
            # except pywintypes.error as e:
            #     pass
    

    async def pipeWriter(self,data):
        try:
            # convert to bytes
            some_data = data.encode('utf-16')
            print(some_data)
            thread = threading.Thread(target=win32file.WriteFile, args=[self.pipe, some_data])
            thread.start()
            #win32file.WriteFile(handle, some_data)
            await asyncio.sleep(0.5)
        except pywintypes.error as e:
            pass
    
    def start(self):
        self.loop.run_forever()


class pipeReader(threading.Thread):   
    def __init__(self,pipe):
        self.logger=logger
        self.reader = None
        self.pipe = pipe
        threading.Thread.__init__(self)

    def run(self):  
        while self.reader == None:
            try: 
                resp =  win32file.ReadFile(self.pipe, 64*1024)
                resp = list(resp)
                resp[1] = resp[1].decode('utf-16')
                reader.reader = resp
            except pywintypes.error as e:
                print("[Pipe Reader] Ouch..  that did not work as intended...")