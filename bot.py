import key
import telebot
import video
import image

api_token = key.API_TOKEN
bot = telebot.TeleBot(api_token,parse_mode=None)

print("Morpheus v1.3 => Online")

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


#files as documents
@bot.message_handler(content_types=['document'])
def documentAnalyzer(message):
    fileID = message.document.file_id
    file_info = bot.get_file(fileID)

    downloaded_file = bot.download_file(file_info.file_path)
    
    mime_type = message.document.mime_type
    fileType = str(mime_type[:mime_type.rfind('/')])

    if(fileType!="image" and fileType!="video"):
        bot.reply_to(message,"*Please send a valid file!!*",parse_mode="Markdown")

    else:
        width = message.document.thumb.width
        height = message.document.thumb.height
        fileSize = message.document.file_size

        if(fileType=="image"):
            image.imageConverter(bot,message,downloaded_file,width,height,fileSize)

        elif(fileType=="video"):
            fileExtension = str(mime_type[mime_type.rfind('/')+1:])
            video.videoConverter(bot,message,downloaded_file,fileExtension,width,height,fileSize)


#handling videos
@bot.message_handler(content_types=['video','animation'])
def videoAndAnimation(message):
    if(message.content_type=='video'):
        fileID = message.video.file_id
        mime_type = message.video.mime_type
        fileExtension = str(mime_type[mime_type.rfind('/')+1:])
        width = message.video.width
        height = message.video.height
        duration = message.video.duration
        fileSize = message.video.file_size
    else:
        fileID = message.animation.file_id
        mime_type = message.animation.mime_type
        fileExtension = str(mime_type[mime_type.rfind('/')+1:])
        width = message.animation.width
        height = message.animation.height
        duration = message.animation.duration
        fileSize = message.animation.file_size

    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    video.videoConverter(bot,message,downloaded_file,fileExtension,width,height,duration,fileSize)


#handling images
@bot.message_handler(content_types=['photo'])
def photo(message):
    fileID = message.photo[-1].file_id
    width = message.photo[-1].width
    height = message.photo[-1].height
    fileSize = message.photo[-1].file_size

    file_info = bot.get_file(fileID)

    downloaded_file = bot.download_file(file_info.file_path)
    image.imageConverter(bot,message,downloaded_file,width,height,fileSize)