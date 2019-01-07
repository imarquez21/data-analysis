#!/usr/bin/python
import os
import re
import sys
import argparse
import glob
import tarfile
import json
import psycopg2
import logging
import time
import csv
import datetime
#from dotenv import load_dotenv
#from dotenv import find_dotenv

#load_dotenv(dotenv_path='.get_br.env', verbose=True)

log_filename = "csvgen.br"
log_path = "log"
cache_path = "cache"
date = datetime.datetime.today().strftime('%Y%m%d')

if not os.path.exists(log_path):
    os.makedirs(log_path)

logFormatter = logging.Formatter("%(asctime)s %(process)d %(levelname)-5.5s %(message)s")
log = logging.getLogger()
log.setLevel(logging.INFO)
fileHandler = logging.FileHandler("{0}/{1}.log".format(log_path, log_filename))
fileHandler.setFormatter(logFormatter)
log.addHandler(fileHandler)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
log.addHandler(consoleHandler)

log.info("CSV Generator - BISMark bitrate - Init log.")

try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse

def argparse_match1(s, pat=re.compile(r"20[0-9]{6}")):
    if not pat.match(s):
        raise argparse.ArgumentTypeError
    return s

parser = argparse.ArgumentParser(description='CSV Generator - BISMark bitrate')
# parser.add_argument('-d','--date', metavar='date', nargs=1,
#                    help='Date in time in the format YYYYMMDD.', type=argparse_match1)
# parser.add_argument('-a','--days-after', metavar='daysafter', nargs=1,
#                    help='Number of days after.')
# parser.add_argument('-b','--days-before', metavar='daysbefore', nargs=1,
#                    help='Number of days before.')

parser.add_argument('-f','--input-file', metavar='inputfile', nargs=1,
                   help='Input file (.dat) with device list.')



args = parser.parse_args()

# if len(sys.argv)<3:
#   parser.print_help()
#   print "Example:",os.path.basename(__file__),"-d $(date +%Y%m%d) -b 2 -f inputlist.dat"
#   sys.exit(1)


pattern = '%Y%m%d %H:%M:%S'

if args.input_file:
  filename = args.input_file[0]
  if os.path.isfile(filename):
    log.info( "Processig file: "+filename )
  else:
    print "File "+filename+" does not exist"
    sys.exit(1)
else:
  print "-f (--input-file) required"
  sys.exit(1)

# print args.date
# start = None
# finish = None
# startn = 0
# finishn = 0
# if args.date:
#   date = args.date[0]+" 00:00:00"
#   if args.days_before:
#     startn = int(args.days_before[0])
#   start = int(time.mktime(time.strptime(date, pattern))) - (startn * 3600 * 24)
#   if args.days_after:
#     finishn = int(args.days_after[0])
#   finish = int(time.mktime(time.strptime(args.date[0]+" 23:59:59", pattern))) + (finishn * 3600 * 24)
# #  print "\nQuerying data between:"
# #  print "\t"+time.strftime('%Y%m%d %H:%M:%S ', time.localtime(start))
# #  print "\t"+time.strftime('%Y%m%d %H:%M:%S ', time.localtime(finish))
# else:
#   print "Please provide a date (-d) in the format YYYYMMDD."
#   parser.print_help()
#   sys.exit(1)

log.info("Querying data between:")
# log.info("\t"+time.strftime('%Y%m%d %H:%M:%S Start', time.localtime(start)))
# log.info("\t"+time.strftime('%Y%m%d %H:%M:%S End', time.localtime(finish)))

def id_to_macaddr(ids):
  ids=ids.strip("PI")
  i=ids.lower()
  ret = i[:2]+":"+i[2:4]+":"+i[4:6]+":"+i[6:8]+":"+i[8:10]+":"+i[10:]
  return ret

f = open(filename, "rU")
if not f:
  sys.exit(1)

log.info("Connecting to "+os.getenv("PSQL_DB")+" ...")
try:
    conn = psycopg2.connect("dbname='"+os.getenv("PSQL_DB")+"' user='"+os.getenv("PSQL_USER")+"' host='"+os.getenv("PSQL_HOST")+"' password='"+os.getenv("PSQL_PASS")+"'")
    conn.set_session(autocommit=True)
    log.info("Done.")
except:
    log.error("Unable to connect to the database. Exiting...")
    sys.exit(1)

cur = conn.cursor()

# n = ( ( finish - start ) / ( 3600 * 24 ) ) + 1

lines = f.readlines()
with open(date+'_bitarate.csv', 'wb') as csvfile:
  w = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
  header = ["Device_ID", "Source_IP", "Destination_IP", "Event_date", "Avg", "Std", "Min", "Max", "Median", "Direction"]
  w.writerow(header)
  for l in lines:
    row = []
    log.info("Processing PI"+l.strip()+" ...")
    row.append("PI"+l.strip())
    device_mac = id_to_macaddr(l.strip())
    row.append(device_mac)
    cur.execute("select deviceid,srcip,dstip,eventstamp,average,std,minimum,maximum,median,direction from m_bitrate where deviceid = %s",[device_mac])
    out1 = cur.fetchone()
    while out1 is not None:
        w.writerow(out1)
        out1 = cur.fetchone()

cur.close()
conn.close()


    # for i in range(n):
    #   s=time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(start + ((i * ( 3600 * 24 ) ))))
    #   f=time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(start + ((i * ( 3600 * 24 ) ) + (3600 * 24 - 1) )))
    #   log.info ("Day "+str(i+1)+" "+s+"- "+f)
    #   cur.execute("select max(average) from m_bitrate where deviceid = %s AND eventstamp > %s AND eventstamp <= %s AND direction = 'dw'", (id_to_macaddr(l.strip()), s,f))
    #   out1=cur.fetchone()
    #   row.append('None' if out1[0]==None else out1[0])
    # for i in range(n):
    #   s=time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(start + ((i * ( 3600 * 24 ) ))))
    #   f=time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(start + ((i * ( 3600 * 24 ) ) + (3600 * 24 - 1) )))
    #   log.info ("Day "+str(i+1)+" "+s+"- "+f)
    #   cur.execute("select max(average) from m_bitrate where deviceid = %s AND eventstamp > %s AND eventstamp <= %s AND direction = 'up'", (id_to_macaddr(l.strip()), s,f))
    #   out1=cur.fetchone()
    #   row.append('None' if out1[0]==None else out1[0])
    # w.writerow(row)
# cur.close()
# conn.close()

