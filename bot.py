import key
import telebot
from PIL import Image
import os

api_token = key.API_TOKEN
bot = telebot.TeleBot(api_token,parse_mode=None)

#commands
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if(message.text=="start"):
	    bot.reply_to(message, "Send me a picture in PNG or JPEG format")
    else:
        bot.reply_to(message, "To use me, send an image that you would like to be made as a sticker (in PNG or JPEG format) and i will return the formatted image")


#other cases
@bot.message_handler(content_types=['text','audio','sticker','video','video_note','voice','location','contact','new_chat_members','left_chat_member','new_chat_title','new_chat_photo','delete_chat_photo','group_chat_created','supergroup_chat_created','channel_chat_created','migrate_to_chat_id','migrate_from_chat_id','pinned_message'])
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
    
    if(file_info.file_path.lower().endswith(('.png','.jpg','.jpeg'))):
        downloaded_file = bot.download_file(file_info.file_path)
        imageConverter(message,downloaded_file)

    else:
        bot.reply_to(message,"*Please send a valid file!!*",parse_mode="Markdown")


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


        if(width>512 or height>512):
            if(width>height):
                widthNew = 512
                heightNew = round((height*512)/width)

            elif(height>width):
                heightNew = 512
                widthNew = round((width*512)/height)

            elif(width==height):
                heightNew = 512
                widthNew = 512

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


#print details
def operationSuccess(id,width,height,size):
    result = "*Image processing successful*\n*New dimensions*: "+str(width)+" X "+str(height)+" px\n*New file size*: "+str(size)+" KB"
    print(result)
    bot.send_message(id,result,parse_mode="Markdown")


bot.infinity_polling()