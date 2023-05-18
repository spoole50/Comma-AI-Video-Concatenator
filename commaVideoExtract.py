import os
import sys
from argparse import ArgumentParser
import ffmpeg
import timeit
# from scp import SCPClient

def catalogVids(basePath):
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
            # print(f"ValueError: {dir.path}\n{ve}")
            continue
        except Exception as e:
            print(f"Directory Parse Error: {dir.path}\n{e}")
    
    for date in dirDict:
        with open(f'{basePath}/{date}_vidList.txt', 'w', encoding='utf-8') as vidList:
            for i in range(dirDict[date]+1):
                vidFile = f"{basePath}/{date}--{i}/fcamera.hevc"
                vidList.write(f"file '{vidFile}'\n")

def checkVids(basePath):
    dateList = []
    for item in os.scandir(basePath):
        if item.is_file():
            if item.name.endswith('_vidList.txt'):
                dateList.append(item.name)
    if len(dateList) == 0:
        sys.exit('No video files found')
    elif len(dateList) == 1:
        return [dateList[0]]
    elif len(dateList) > 1:
        for idx, date in enumerate(dateList):
            print(f'{idx + 1}. {date.split("_")[0]}')
        for _ in range(3):
            try:
                userChoice = input(f"Choose date/time of video (1-{len(dateList)}) or type 'all':\n")
                if userChoice.lower().strip() == 'all':
                    return dateList
                else:
                    return [dateList[int(userChoice) - 1]]
            except ValueError as ve:
                print("Please enter a vaild option")
                continue
            except Exception as e:
                sys.exit(f"Video Choice Error: {e}")
        sys.exit("Too Many Invalid Choices, Please Try Again")

def concatVid(basePath, vidList):
    # print(f"{basePath}/{vidList}")
    for vid in vidList:
        date = vid.split('_')[0]
        try:
            start = timeit.default_timer()
            ffmpeg.input(f'{basePath}/{vid}', f='concat', safe=0, r=20)\
                .output(f'{basePath}/{date}.mp4', codec='copy', map=0, vtag='hvc1')\
                .run(capture_stdout=True, capture_stderr=True, quiet=True, overwrite_output=True)
            end = timeit.default_timer()
            print(f"{date} Concatenation Complete, Wall-Time {end-start:.2f} seconds")
        except ffmpeg.Error as e:
            sys.exit(f"ffmpg error:\nstdout: {e.stdout.decode('utf-8')}\nstderr: {e.stderr.decode('utf-8')}")
        except Exception as e:
            sys.exit(f"Concat/ffmpg Fatal Error: {e}")

def initParser():
    parser = ArgumentParser()
    parser.add_argument(
        '-d',
        '--dir',
        help='Specify path to directory containing video files, if not default',
        type=str)
    return parser.parse_args()

def main():
    args = initParser()
    if args.dir:
        path = args.dir
    else:
        path = '/data/media/0/realdata/'
    try:
        catalogVids(path)
        vidList = checkVids(path)
        concatVid(path, vidList)
        sys.exit('Success')
    except KeyboardInterrupt:
        sys.exit('\nKeyboardInterrupt')
    except Exception as e:
        sys.exit(f"Error: {e}")

if __name__ == '__main__':
    main()