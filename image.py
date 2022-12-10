from PIL import Image
import common
import os
import time
import psutil

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

        newFileSize = fileSize

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

    # Get a list of processes that have the file open
    open_procs = []
    for proc in psutil.process_iter():
        try:
            files = proc.open_files()
            if any(file.path == fileName for file in files):
                open_procs.append(proc)
        except psutil.AccessDenied:
            continue

    # Print the list of processes that have the file open
    if open_procs:
        print(f"The following processes have '{fileName}' open:")
        for proc in open_procs:
            print(f"- PID {proc.pid}: {proc.name()}")
    else:
        print(f"No processes have '{fileName}' open.")
        os.remove(fileName)
