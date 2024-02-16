from libmso import mso, SimpleObject
import argparse


# add arguments for file

parser = argparse.ArgumentParser(
                    prog='MSOTEST',
                    description='What the does',
                    epilog='Tex')

parser.add_argument('filename', nargs="?")
args = parser.parse_args()

if not args.filename:
    # create a simpleobject
    newsimpobj = SimpleObject("stest", [1,2,2,31,2,5,12,5,2,5,214,1,243,1,325,1,4,124,13,5,34215345,234,5,3245,2345,145,25,1345,13251,234,513,45])
    # save
    mso.save(newsimpobj, "simotest.mso")
else:
    try:
        obj = mso.read(args.filename)
        print(obj.name)
        print(obj.data)
    except Exception as e:
        print(e)