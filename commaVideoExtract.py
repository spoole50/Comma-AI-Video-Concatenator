import os
import ffmpeg
from scp import SCPClient

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

# print(dirDict)

for date in dirDict:
    with open(f'./{date}_vidList.txt', 'w', encoding='utf-8') as vidList:
        for i in range(dirDict[date]):
            vidFile = f"/realdata/{date}--{i}/fcamera.hevc"
            # vidFile = os.path.abspath(vidFile)
            vidList.write(f"file '{os.getcwd()}{vidFile}'\n")

ffmpeg.input('/Users/spoole/Desktop/rsync/2022-11-28--16-43-50_vidList.txt', f='concat', safe=0, r=20)\
    .output('./testOut.mp4', codec='copy', map=0, vtag='hvc1').run(quiet=True)