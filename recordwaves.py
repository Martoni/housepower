
# arecord -d 10 -f S16_LE -c1 -r4000 -D plughw:1 -t wav foobar.wav
import os
import sys
import getopt
import time
import subprocess

def usage():
    print("Usage:")
    print("$ python3 recordwaves.py [options]")
    print("-h, --help   print this help message")
    print("-n, --name   give prefix name of records(default rec)")
    print("-d, --dir    give directory to record wavefiles (default hdata)")
    print("-t, --time   give record time in second (default 60)")


if __name__ == "__main__":
    print("recording current sound")
    if sys.version_info[0] < 3:
        raise Exception("Must be using Python 3")

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hn:t:d:",
                                    ["help", "name=",
                                     "time=", "dir="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    wavename = "rec"
    wavetime = 60
    hdata = "hdata"
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-n", "--name"):
            wavename = arg
        elif opt in ("-t", "--time"):
            wavetime = int(arg)
        elif opt in ("-d", "--dir"):
            hdata = arg

    if not os.path.exists("{}".format(hdata)):
        os.mkdir("{}".format(hdata))
    if not os.path.exists("{}/tmp".format(hdata)):
        os.mkdir("{}/tmp".format(hdata))

    while True:
        epoch_time = int(time.time())
        cmd = ("arecord -d {} -f S16_LE -c1 -r4000 -D plughw:1 -t wav {}/tmp/{}-{}.wav"
                .format(wavetime, hdata, wavename, epoch_time))
        print(cmd)
        subprocess.check_call(cmd.split(" "))
        # move result to hdata
        os.rename("{}/tmp/{}-{}.wav".format(hdata, wavename, epoch_time),
                  "{}/{}-{}.wav".format(hdata, wavename, epoch_time))
        
