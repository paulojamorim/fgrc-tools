import sys
import glob
import subprocess

def extract_from_gz(files, folder):
    for f in files:
        subprocess.call(["gunzip", f]) 

def main():
    folder  = sys.argv[1]
    arq = glob.glob(folder + "*.gz")
    extract_from_gz(arq, folder)
    print "FIM!"

if __name__ == '__main__':
    main()
