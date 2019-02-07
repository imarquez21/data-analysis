import os
import datetime
import argparse
import tarfile
import sys
from shutil import copyfile

def extract(tar_url, extract_path='.'):
    tar = tarfile.open(tar_url, 'r')
    memberList = []
    finallist = []
    for item in tar:
        if item.name.find(".tgz") != -1 or item.name.find(".tar.gz") != -1:
            item.name = item.name.split('/')[1]
            memberList.append(item)
        if item.name.endswith(".out"):
            finallist.append(item)
            item.name = item.name.split('/')[-1]

    tar.extractall(path=extract_path, members=memberList)
    for fname in memberList:
        fname = extract_path + fname.name
        try:
            extract(fname, extract_path=extract_path)
        except Exception as e:
            name = os.path.basename(sys.argv[0])
            print("EXCEPTION", e, name[:name.rfind('.')], fname)
        os.remove(fname)
    tar.extractall(path=extract_path, members=finallist)
    tar.close()

    return 0


def process_directory(tars_dir, outdir):

    print "Validating if file in "+str(tars_dir)+" is compressed."

    for root, dirs, files in os.walk(tars_dir):
        for filename in files:
            try:
                if filename.endswith(".tgz"):
                    extract(root + "/" + filename, extract_path=outdir)
                elif filename.endswith(".out"):
                    if not os.path.exists(outdir):
                        os.makedirs(outdir)
                    src = dir + "/" + filename
                    copyfile(src, '%s/%s' % (outdir, src.split('/')[-1]))
            except Exception as e:
                name = os.path.basename(sys.argv[0])
    print("EXCEPTION", e, name[:name.rfind('.')], filename)

    return 0


def main():

    print "Script start"
    print datetime.datetime.now()

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", type=str, required=True, help="Directory from where compressed files will be extracted.")
    parser.add_argument("-o", "--outdir", type=str, required=True,
                        help="Directory where uncompressed files will be extracted to.")

    args = vars(parser.parse_args())

    tars_dir = args["dir"]
    outdir = args["outdir"]

    process_directory(tars_dir, outdir)

    print "Script End"
    print datetime.datetime.now()

    return 0

if __name__ == '__main__':
    main()
