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
        self.l.logger.info("Starting")
        self.l.logger.info("Starting")
        self.l.logger.info("Starting")
        self.l.logger.info("Starting")
        self.l.logger.info("Starting")
        self.l.logger.info("Starting")
        self.l.logger.info("Starting")
        self.l.logger.info("Starting")
        self.l.logger.info("Starting")
        

        self.l.logger.info("Started")
        self.ledyPipeObj = pipeClient.pipeClient(r"\\.\pipe\Demo")
        self.ledyPipeReaderObj = pipeClient.pipeClient(r"\\.\pipe\Demo1")
        loop.create_task(self.ledyReader())
        #self.ledyPipeObj.start()

    async def ledyReader(self):
        while True:
            commandOutput = await self.ledyPipeReaderObj.pipeReader()
            commandOutput = await self.messageFix(commandOutput)
            print("reader...")

            self.l.logger.info("[but] {0}".format(commandOutput))

    async def messageFix(self,message):
        if message.split(":")[0] == "g": #msg fix
                message = "ms{0}".format(message)
        elif message.split(":")[0] == "mmand": #command fix
            message = "co{0}".format(message)
        return message


    async def ledyCommands(self):
        config.events.addCommandType(commandType="ledyDsStart",commandHandler=self.startLedyBot)
        config.events.addCommandType(commandType="ledyDsStop",commandHandler=self.stopLedyBot)
        config.events.addCommandType(commandType="ledyDsConnect",commandHandler=self.connectDSLedyBot)
        config.events.addCommandType(commandType="ledyDsDisconnect",commandHandler=self.disconnectDSLedyBot)
        config.events.addCommandType(commandType="ledyDsRefresh",commandHandler=self.refreshLedyBot)
        config.events.addCommandType(commandType="ledyDsTradequeue",commandHandler=self.tradequeueLedyBot)
        config.events.addCommandType(commandType="ledyDsViewqueue",commandHandler=self.viewqueueLedyBot)
        #config.events.addCommandType(commandType="ledyDsStart",commandHandler=self.startLedyBot)



    async def startLedyBot(self,message,command):
        # if (message.Message.Contents == "!START") & await self.roleChecker(["Normal"],message.Message.Roles) == True:
        #     self.l.logger.info("Starting Ledybot")
        await self.ledyPipeObj.pipeWriter("startgtsbot")

    async def stopLedyBot(self,message,command):
        # if (message.Message.Contents == "!STOP") & await self.roleChecker(["Normal"],message.Message.Roles) == True:
        #     self.l.logger.info("Starting Ledybot")
        await self.ledyPipeObj.pipeWriter("stopgtsbot")
        commandOutput = await self.ledyPipeObj.pipeReader()
        commandOutput = await self.messageFix(commandOutput)
        botRoles= {"":0}
        await self.processMsg(message=commandOutput,username="Bot",channel=message.Message.Channel,server=message.Message.Server,service=message.Message.Service,roleList=botRoles)       

            
    async def connectDSLedyBot(self,message,command):
        # if (message.Message.Contents == "!CONNECT") & await self.roleChecker(["Normal"],message.Message.Roles) == True:
        #     self.l.logger.info("Starting Ledybot")
        await self.ledyPipeObj.pipeWriter("connect3ds")
        commandOutput = await self.ledyPipeObj.pipeReader()
        commandOutput = await self.messageFix(commandOutput)
        botRoles= {"":0}
        await self.processMsg(message=commandOutput,username="Bot",channel=message.Message.Channel,server=message.Message.Server,service=message.Message.Service,roleList=botRoles)       
  

    async def disconnectDSLedyBot(self,message,command):
        # if (message.Message.Contents == "!DISCONNECT") & await self.roleChecker(["Normal"],message.Message.Roles) == True:
        #     self.l.logger.info("Starting Ledybot")
        await self.ledyPipeObj.pipeWriter("disconnect3ds")   
        commandOutput = await self.ledyPipeObj.pipeReader()
        commandOutput = await self.messageFix(commandOutput)
        botRoles= {"":0}
        await self.processMsg(message=commandOutput,username="Bot",channel=message.Message.Channel,server=message.Message.Server,service=message.Message.Service,roleList=botRoles)       
  

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
        commandOutput = await self.ledyPipeObj.pipeReader()
        commandOutput = await self.messageFix(commandOutput)
        botRoles= {"":0}
        await self.processMsg(message=commandOutput,username="Bot",channel=message.Message.Channel,server=message.Message.Server,service=message.Message.Service,roleList=botRoles)       
    

    async def tradequeueLedyBot(self,message,command):
        # if (message.Message.Contents == "!DISCONNECT") & await self.roleChecker(["Normal"],message.Message.Roles) == True:
        #     self.l.logger.info("Starting Ledybot")
        await self.ledyPipeObj.pipeWriter("togglequeue")
        commandOutput = await self.ledyPipeObj.pipeReader()  
        commandOutput = await self.messageFix(commandOutput)
        botRoles= {"":0}
        await self.processMsg(message=commandOutput,username="Bot",channel=message.Message.Channel,server=message.Message.Server,service=message.Message.Service,roleList=botRoles)       

    async def viewqueueLedyBot(self,message,command):
        # if (message.Message.Contents == "!DISCONNECT") & await self.roleChecker(["Normal"],message.Message.Roles) == True:
        #     self.l.logger.info("Starting Ledybot")
        await self.ledyPipeObj.pipeWriter("viewqueue")
        commandOutput = await self.ledyPipeObj.pipeReader()  
        commandOutput = await self.messageFix(commandOutput)
        botRoles= {"":0}
        await self.processMsg(message=commandOutput,username="Bot",channel=message.Message.Channel,server=message.Message.Server,service=message.Message.Service,roleList=botRoles)       
        
        


    async def processMsg(self,username,message,roleList,server,channel,service):
        print("ya... {0}".format(message))
        formatOptions = {"%authorName%": username, "%channelFrom%": channel, "%serverFrom%": server, "%serviceFrom%": service,"%message%":"message","%roles%":roleList}
        message = Object.ObjectLayout.message(Author=username,Contents=message,Server=server,Channel=channel,Service=service,Roles=roleList)
        objDeliveryDetails = Object.ObjectLayout.DeliveryDetails(Module="Command",ModuleTo="Site",Service=service,Server=server,Channel=channel)
        objSendMsg = Object.ObjectLayout.sendMsgDeliveryDetails(Message=message, DeliveryDetails=objDeliveryDetails, FormattingOptions=formatOptions,messageUnchanged="None")
        config.events.onMessageSend(sndMessage=objSendMsg)     


#refresh [mode] [filename]

#connect3ds 

#disconnect3ds

#startgtsbot 



#stopgtsbot 

'''
whats missing:
    trade commnad
        to add trades i think?

    remove command
        remove trades???

    responding to any message that may come through

'''

ledy = ledyBotChat()