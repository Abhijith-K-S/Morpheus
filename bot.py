from concurrent.futures import process
from fileinput import filename
import key
import telebot
import subprocess
from PIL import Image
import os

api_token = key.API_TOKEN
bot = telebot.TeleBot(api_token,parse_mode=None)

bot.remove_webhook()
print("Morpheus v1.2 => Online")

#commands
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if(message.text=="start"):
	    bot.reply_to(message, "Send me a image/video/gif to make sticker/animated sticker")
    else:
        bot.reply_to(message, "1.To make regular sticker, send an image in *png* or *jpg* format \n\n2.To make animated sticker send a *gif* file or a video file in *mp4* or *webm* format \n\nNote: If the duration of the video file is more than 3 seconds, the file will be trimmed to the first 3 seconds",parse_mode="Markdown")


#other cases
@bot.message_handler(content_types=['text','audio','sticker','video_note','voice','location','contact','new_chat_members','left_chat_member','new_chat_title','new_chat_photo','delete_chat_photo','group_chat_created','supergroup_chat_created','channel_chat_created','migrate_to_chat_id','migrate_from_chat_id','pinned_message'])
def improper(message):
    bot.reply_to(message,"*Please send a valid file!!*",parse_mode="Markdown")


#images as documents
@bot.message_handler(content_types=['document'])
def documentAnalyzer(message):
    print(message.document.file_id)
    fileID = message.document.file_id
    print('fileID =', fileID)
    file_info = bot.get_file(fileID)
    print('file.file_path =', file_info.file_path)

    fileExtension = file_info.file_path.lower()
    downloaded_file = bot.download_file(file_info.file_path)
    
    if(fileExtension.endswith(('.png','.jpg','.jpeg'))):
        imageConverter(message,downloaded_file)

    elif(fileExtension.endswith(('.mp4'))):
        videoConverter(message,downloaded_file,"mp4")
    
    elif(fileExtension.endswith(('.webm'))):
        videoConverter(message,downloaded_file,".webm")

    else:
        bot.reply_to(message,"*Please send a valid file!!*",parse_mode="Markdown")


#handling videos
@bot.message_handler(content_types=['video','animation'])
def video(message):
    if(message.content_type=='video'):
        fileID = message.video.file_id
    else:
        fileID = message.animation.file_id

    print('fileID =',fileID)
    file_info = bot.get_file(fileID)
    print('file.file_path = ',file_info.file_path)

    downloaded_file = bot.download_file(file_info.file_path)
    filename = file_info.file_path.lower()

    videoConverter(message,downloaded_file,filename[filename.rfind('.')+1:])


#video processing function
def videoConverter(message,downloaded_file,fileExtension):
    fileName = "video."+fileExtension
    with open(fileName,'wb') as new_file:
        new_file.write(downloaded_file)

    widthNew=0
    heightNew=0
    timeDuration=0.00

    processCommand = "ffmpeg -y -i "+fileName

    findDimensions = subprocess.Popen("ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 "+fileName,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    output,err = findDimensions.communicate()

    if(err):
        bot.reply_to(message,"Error!")
        return
    else:
        dimensions = output.decode()
        index = dimensions.index("x")
        width = dimensions[0:index]
        height = dimensions[index+1:]
        fileSize = os.stat("./video."+fileExtension).st_size
        
        if(fileSize<1024):
            fileSizeTxt = str(fileSize)+" B"
        elif(fileSize>=1024 and fileSize<10**6):
            fileSizeTxt = str(round(fileSize/1024,2))+ " KB"
        else:
            fileSizeTxt = str(round(fileSize/10**6,2))+ " MB"

        statReply = "*Current dimensions*: "+width+" X "+height+" px\n*File size*: "+fileSizeTxt
        print(statReply)
        bot.reply_to(message,statReply,parse_mode="Markdown")


        if(width!=512 and height!=512):
            widthNew,heightNew = getNewDimensions(int(width),int(height))
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
            processCommand = processCommand+" -ss 00:00:00 -to 00:00:02.80"
    
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
    operationSuccess(message.chat.id,widthNew,heightNew,round(newFilesize/1024,2))


#handling images
@bot.message_handler(content_types=['photo'])
def photo(message):
    fileID = message.photo[-1].file_id
    print('fileID =', fileID)
    file_info = bot.get_file(fileID)
    print('file.file_path =', file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)

    imageConverter(message,downloaded_file)


#main image processing function
def imageConverter(message,downloaded_file):
    with open("image.png", 'wb') as new_file:
        new_file.write(downloaded_file)
        initialImage = Image.open("image.png")
        width,height = initialImage.size
        fileSize = os.stat("./image.png").st_size

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
            widthNew,heightNew = getNewDimensions(width,height)
            newImageSize = (widthNew,heightNew)

            modifiedImage = initialImage.resize(newImageSize)
            modifiedImage.save("image.png")
            newFileSize = os.stat("./image.png").st_size

            result = open("./image.png","rb")
            bot.send_document(message.chat.id,result)
            operationSuccess(message.chat.id,widthNew,heightNew,round(newFileSize/1024,2))
            
        else:
            result = open("./image.png","rb")
            bot.send_document(message.chat.id,result)
            operationSuccess(message.chat.id,width,height,round(fileSize/1024,2))


#function to get new dimensions
def getNewDimensions(width,height):
    if(width>height):
        widthNew = 512
        heightNew = round((height*512)/width)

    elif(height>width):
        heightNew = 512
        widthNew = round((width*512)/height)

    elif(width==height):
        heightNew = 512
        widthNew = 512
    
    return widthNew,heightNew


#print details
def operationSuccess(id,width,height,size):
    result = "*File processing successful*\n*New dimensions*: "+str(width)+" X "+str(height)+" px\n*New file size*: "+str(size)+" KB"
    print(result)
    bot.send_message(id,result,parse_mode="Markdown")


bot.infinity_polling()