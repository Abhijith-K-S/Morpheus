from datetime import datetime

#generate unique filename
def generateFileName(username):
    dt_string = datetime.now().strftime("%d%m%Y%H%M%S")
    return username+"_"+dt_string

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
def operationSuccess(width,height,size):
    result = "*File processing successful*\n*New dimensions*: "+str(width)+" X "+str(height)+" px\n*New file size*: "+str(size)+" KB"
    print(result)
    return result