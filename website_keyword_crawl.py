#Python 3.x
#Website keyword crawler v1.1
#Created by rickvg @ https://github.com/rickvg

import urllib.request
import re
import threading
from multiprocessing import Queue


def findkeywordlvl(strwebsiteinp, strmatch, queueget):
    if strmatch.startswith("src="):
        strmatch = strmatch[5:len(strmatch)]
    elif strmatch.startswith("href="):
        strmatch = strmatch[6:len(strmatch)]

    if not (strmatch.endswith(".jpg")) or (strmatch.endswith(".png")) or (strmatch.endswith(".bmp")) or (strmatch.endswith(".gif")):
        if strmatch.startswith("//"):
            strwebsite2 = "http:" + strmatch
        elif strmatch.startswith("/"):
            strwebsite2 = strwebsiteinp + strmatch
        else:
            strwebsite2 = strmatch
        if ("\\" not in strwebsite2):
            try:
                print(strwebsite2)
                strcontent = urllib.request.urlopen(strwebsite2).read()
                match2 = re.findall(re.escape(strKeyword), str(strcontent))
                match3 = re.findall("href=[\'\"]http\://[A-z0-9_\-\./]+|href=[\'\"]\/[A-z0-9_\-\./]+|href=[\'\"]www[A-z0-9_\-\./]+",str(strcontent))
                match3 = match3 + re.findall("src=[\'\"]http\://[A-z0-9_\-\./]+|src=[\'\"]\/[A-z0-9_\-\./]+|src=[\'\"]www[A-z0-9_\-\./]+",str(strcontent))
                if match2:
                    strPrint = strwebsite2 + " has " + str(len(match2)) + " matches with keyword: " + strKeyword + "\n"
                    print(strPrint)
                    strFile.write(strPrint)
                else:
                    print("No matches for:", strwebsite2)
                queueget.put([strwebsite2, match3])
                return [strwebsite2, match3]
            except Exception as ex:
                errormsg = "Exception {0} occurred. Reason:\n{1!r}"
                message = errormsg.format(type(ex).__name__, ex.args)
                print(message)
                strFile2.write(message)

strWebsite = input("Enter website (Format http://domain.com):\n")
strKeyword = input("Enter keyword to search for:\n")
intLevel = int(input("Select levels to scan. Choose 1, 2 or 3 - 3 might contain errors:\n"))
filename = strWebsite[7:len(strWebsite)] + " positives.log"
filename2 = strWebsite[7:len(strWebsite)] + " errors.log"
strFile = open(filename, 'w')
strFile2 = open(filename2, 'w')

strContent = urllib.request.urlopen(strWebsite).read()
match2 = re.findall(re.escape(strKeyword), str(strContent))
match3 = []

if match2:
    strPrint = strWebsite + " has " + str(len(match2)) + " matches with keyword: " + strKeyword + "\n"
    print(strPrint)
    strFile.write(strPrint)
else:
    print("No matches for:", strWebsite)

if intLevel == 1:
    print("Finished scanning website for keywords")
elif intLevel in range(2, 4):
    regex1 = r"src=[\'\"]http\://[A-z0-9_\-\./]+|src=[\'\"]\/[A-z0-9_\-\./]+|src=[\'\"]www[A-z0-9_\-\./]+"
    regex2 = r"href=[\'\"]http\://[A-z0-9_\-\./]+|href=[\'\"]\/[A-z0-9_\-\./]+|href=[\'\"]www[A-z0-9_\-\./]+"

    results = []

    match = re.findall(re.compile(regex2), str(strContent))
    matchsrc = re.findall(re.compile(regex1), str(strContent))
    match = match + matchsrc

    q = Queue()
    threads = []

    i = 0
    while i < len(match):
        if threading.active_count() < 10:
            t = threading.Thread(target=findkeywordlvl, args =(strWebsite, match[i],q))
            t.start()
            threads.append(t)
            i += 1

    for p in threads:
        p.join()
    while not q.empty():
        results.append(q.get_nowait())

    print(results)

    threads = []
    j = 0
    if intLevel == 3:
        for i in range(0,len(results)):
            while j < len(results[i][1]):
                if threading.active_count() < 10:
                    threads.append(threading.Thread(target=findkeywordlvl, args=(results[i][0],results[i][1][j],q)))
                    threads[j].start()
                    j += 1
        for p in threads:
            p.join()
else:
    print("Wrong level. Try again.")

strFile.close()
strFile2.close()
