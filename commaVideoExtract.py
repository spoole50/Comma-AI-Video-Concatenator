import os
import ffmpeg

basePath = "/Users/spoole/Desktop/rsync/realdata/"

# for root, dirs, files in os.walk(basePath):
#     for file in files:
#         print(os.path.join(root, file))

dirDict = {}
for dir in os.scandir(basePath):
    try:
        vidFile = dir.path.split('/')[-1][:20]
        vidNum = int(dir.path.split('/')[-1][22:])
        if len(vidFile) == 20:
            if vidFile not in dirDict:
                dirDict[vidFile] = vidNum
            elif vidNum > dirDict[vidFile]:
                dirDict[vidFile] = vidNum
    except ValueError as ve:
        print(f"ValueError: {dir.path}\n{ve}")

# ffmpeg.input('mylist.txt', f='concat', safe=0).output('output.mp4', codec='copy').overwrite_output().run()       
print(dirDict)