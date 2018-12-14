from utils import config
from utils import Object
import asyncio
import time
import datetime
from utils import logger

from utils import pipeClient


class ledyBotChat:
    def __init__(self):
        self.l = logger.logs("ledyBotChat")
        self.l.logger.info("Starting")
        loop = asyncio.get_event_loop()
        loop.create_task(self.ledyCommands())
        #config.events.onMessage += self.startLedyBot
        #config.events.onMessage += self.stopLedyBot
        #config.events.onMessage += self.connectDSLedyBot
        #config.events.onMessage += self.disconnectDSLedyBot
        

        self.l.logger.info("Started")
        self.ledyPipeObj = pipeClient.pipeClient(r"\\.\pipe\Demo")
        #self.ledyPipeObj.start()

    async def ledyCommands(self):
        config.events.addCommandType(commandType="ledyDsStart",commandHandler=self.startLedyBot)
        config.events.addCommandType(commandType="ledyDsStop",commandHandler=self.stopLedyBot)
        config.events.addCommandType(commandType="ledyDsConnect",commandHandler=self.connectDSLedyBot)
        config.events.addCommandType(commandType="ledyDsDisconnect",commandHandler=self.disconnectDSLedyBot)
        config.events.addCommandType(commandType="ledyDsRefresh",commandHandler=self.refreshLedyBot)
        #config.events.addCommandType(commandType="ledyDsStart",commandHandler=self.startLedyBot)



    async def startLedyBot(self,message,command):
        # if (message.Message.Contents == "!START") & await self.roleChecker(["Normal"],message.Message.Roles) == True:
        #     self.l.logger.info("Starting Ledybot")
        await self.ledyPipeObj.pipeWriter("startgtsbot")

    async def stopLedyBot(self,message,command):
        # if (message.Message.Contents == "!STOP") & await self.roleChecker(["Normal"],message.Message.Roles) == True:
        #     self.l.logger.info("Starting Ledybot")
        await self.ledyPipeObj.pipeWriter("stopgtsbot")
            
    async def connectDSLedyBot(self,message,command):
        # if (message.Message.Contents == "!CONNECT") & await self.roleChecker(["Normal"],message.Message.Roles) == True:
        #     self.l.logger.info("Starting Ledybot")
            await self.ledyPipeObj.pipeWriter("connect3ds")

    async def disconnectDSLedyBot(self,message,command):
        # if (message.Message.Contents == "!DISCONNECT") & await self.roleChecker(["Normal"],message.Message.Roles) == True:
        #     self.l.logger.info("Starting Ledybot")
        await self.ledyPipeObj.pipeWriter("disconnect3ds")   

    async def refreshLedyBot(self,message,command):
        # if (message.Message.Contents == "!DISCONNECT") & await self.roleChecker(["Normal"],message.Message.Roles) == True:
        #     self.l.logger.info("Starting Ledybot")
        splitMsg = message.Message.Contents.split(" ")
        if len(splitMsg) == 3:
            await self.ledyPipeObj.pipeWriter("refresh {0} {1}".format(splitMsg[1],splitMsg[2])) 
        elif len(splitMsg) == 2:
            await self.ledyPipeObj.pipeWriter("refresh {0} {1}".format(splitMsg[1],splitMsg[2])) 
        elif len(splitMsg) == 1:
            await self.ledyPipeObj.pipeWriter("refresh") 
        await self.ledyPipeObj.pipeReader()    

    async def tradequeueLedyBot(self,message,command):
        # if (message.Message.Contents == "!DISCONNECT") & await self.roleChecker(["Normal"],message.Message.Roles) == True:
        #     self.l.logger.info("Starting Ledybot")
        await self.ledyPipeObj.pipeWriter("tradequeue")       


#refresh [mode] [filename]

#connect3ds 

#disconnect3ds

#startgtsbot 

#stopgtsbot 