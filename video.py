import subprocess
import common
import os

#video processing function
def videoConverter(bot,message,downloaded_file,fileExtension,width,height,duration,fileSize):
    generatedFileName = common.generateFileName(message.from_user.username)
    inputFileName = generatedFileName+"."+fileExtension
    outputFileName = generatedFileName+".webm"

    with open(inputFileName,'wb') as new_file:
        new_file.write(downloaded_file)

    widthNew=0
    heightNew=0

    #the ffmpeg command
    processCommand = "ffmpeg -y -i "+inputFileName
        
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

    #compute new dimensions
    if(width!=512 and height!=512):
        widthNew,heightNew = common.getNewDimensions(int(width),int(height))
        if(widthNew!=512 and widthNew%2!=0):
            widthNew=widthNew+1
        elif(heightNew!=512 and heightNew%2!=0):
            heightNew=heightNew+1
        processCommand = processCommand +" -vf scale="+str(widthNew)+":"+str(heightNew)
    else:
        widthNew = width
        heightNew = height

    #trim to make duration less than 3 seconds
    if(duration>3.00):
        processCommand = processCommand+" -ss 00:00:00 -to 00:00:02.99"
    
    #vp9 encoding
    processCommand = processCommand+" -an -c:v libvpx-vp9 -crf 25 -b:v 720k -c:a libopus "+outputFileName

    modify = subprocess.Popen(processCommand,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output,err = modify.communicate()
    modify.wait()
    print("Encoded to webm")

    newFilesize = os.stat(outputFileName).st_size
    print(newFilesize)  

    result = open(outputFileName,"rb")
    bot.send_document(message.chat.id,result)
    result = common.operationSuccess(widthNew,heightNew,round(newFilesize/1024,2))
    bot.send_message(message.chat.id,result,parse_mode="Markdown")