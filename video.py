import subprocess
import common
import os

#video processing function
def videoConverter(bot,message,downloaded_file,fileExtension,width,height,fileSize):
    fileName = "video."+fileExtension
    with open(fileName,'wb') as new_file:
        new_file.write(downloaded_file)

    widthNew=0
    heightNew=0
    timeDuration=0.00

    processCommand = "ffmpeg -y -i "+fileName
        
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
        widthNew,heightNew = common.getNewDimensions(int(width),int(height))
        if(widthNew!=512 and widthNew%2!=0):
            widthNew=widthNew+1
        elif(heightNew!=512 and heightNew%2!=0):
            heightNew=heightNew+1
        processCommand = processCommand +" -vf scale="+str(widthNew)+":"+str(heightNew)
    else:
        widthNew = width
        heightNew = height

    tmp = subprocess.Popen("ffprobe -i "+fileName+" -v quiet -show_entries format=duration -hide_banner -of default=noprint_wrappers=1:nokey=1",stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output,err = tmp.communicate()
    if(err):
        bot.reply_to(message,"Error!")
        return
    else:
        duration = output.decode()
        print(duration)
        timeDuration=float(duration)

        if(timeDuration>3.00):
            processCommand = processCommand+" -ss 00:00:00 -to 00:00:02.99"
    
    #trim or resize
    processCommand = processCommand+" tmp."+fileExtension
    modify = subprocess.Popen(processCommand,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output,err = modify.communicate()
    modify.wait()
    print("Trim and resize complete")

    #remove audio stream
    if os.path.exists("tmp2."+fileExtension):
        os.remove("tmp2."+fileExtension)
    processCommand = "ffmpeg -i tmp."+fileExtension+" -c copy -an "+"tmp2."+fileExtension
    modify = subprocess.Popen(processCommand,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output,err = modify.communicate()
    modify.wait()
    print("Audio removal complete")

    #encode to webm
    processCommand = "ffmpeg -y -i tmp2."+fileExtension+" -c:v libvpx-vp9 -crf 25 -b:v 720k -c:a libopus tmp3.webm"
    modify = subprocess.Popen(processCommand,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output,err = modify.communicate()
    modify.wait()
    print("Encoded to webm")

    newFilesize = os.stat("./tmp3.webm").st_size
    print(newFilesize)

    if(newFilesize>262144):
        factor=5
        while(newFilesize>262144):
            if os.path.exists("output.webm"):
                os.remove("output.webm")

            processCommand = "ffmpeg -y -i tmp3.webm -crf "+str(factor)+" -b:v 0 -c:a libopus output.webm"
            modify = subprocess.Popen(processCommand,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            output,err = modify.communicate()
            modify.wait()
            
            newFilesize = os.stat("./output.webm").st_size
            print("newFileSize = "+str(newFilesize))
            factor=factor+5

    else:
        if os.path.exists("output.webm"):
            os.remove("output.webm")

        os.rename("tmp3.webm","output.webm")    

    result = open("./output.webm","rb")
    bot.send_document(message.chat.id,result)
    result = common.operationSuccess(widthNew,heightNew,round(newFilesize/1024,2))
    bot.send_message(message.chat.id,result,parse_mode="Markdown")