from PIL import Image
import common
import os

#main image processing function
def imageConverter(bot,message,downloaded_file,width,height,fileSize):
    fileName = common.generateFileName(message.from_user.username)+".png"
    with open(fileName, 'wb') as new_file:
        new_file.write(downloaded_file)
        initialImage = Image.open(fileName)

        #compute file size
        if(fileSize<1024):
            fileSizeTxt = str(fileSize)+" B"
        elif(fileSize>=1024 and fileSize<10**6):
            fileSizeTxt = str(round(fileSize/1024,2))+ " KB"
        else:
            fileSizeTxt = str(round(fileSize/10**6,2))+ " MB"

        statReply = "*Current dimensions*: "+str(width)+" X "+str(height)+" px\n*File size*: "+fileSizeTxt
        print(statReply)
        bot.reply_to(message,statReply,parse_mode="Markdown")

        if(width!=512 and height!=512):
            #compute new dimensions``
            widthNew,heightNew = common.getNewDimensions(width,height)
            newImageSize = (widthNew,heightNew)

            modifiedImage = initialImage.resize(newImageSize)
            modifiedImage.save(fileName)
            newFileSize = os.stat("./"+fileName).st_size

            result = open("./"+fileName,"rb")
            bot.send_document(message.chat.id,result)
            result = common.operationSuccess(widthNew,heightNew,round(newFileSize/1024,2))
            bot.send_message(message.chat.id,result,parse_mode="Markdown")
            
        else:
            result = open("./"+fileName,"rb")
            bot.send_document(message.chat.id,result)
            result = common.operationSuccess(width,height,round(fileSize/1024,2))
            bot.send_message(message.chat.id,result,parse_mode="Markdown")