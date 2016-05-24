#Python 3.x
#Website keyword crawler v1.0
#Created by rickvg @ https://github.com/rickvg

import urllib.request
import re

strWebsite = input("Enter website (Format http://domain.com):\n")
strKeyword = input("Enter keyword to search for:\n")
intLevel = int(input("Select levels to scan. Choose 1, 2 or 3 - 3 might contain errors because of websites out of scope.:\n"))
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
elif intLevel >= 2:
    regex1 = r"src=[\'\"]http\://[A-z0-9_\-\./]+|src=[\'\"]\/[A-z0-9_\-\./]+|src=[\'\"]www[A-z0-9_\-\./]+"
    regex2 = r"href=[\'\"]http\://[A-z0-9_\-\./]+|href=[\'\"]\/[A-z0-9_\-\./]+|href=[\'\"]www[A-z0-9_\-\./]+"
    match = re.findall(re.compile(regex2), str(strContent))
    matchsrc = re.findall(re.compile(regex1), str(strContent))
    match = match + matchsrc

    for i in range(0,len(match)):
        if match[i].startswith("src="):
            match[i] = match[i][5:len(match[i])]
        elif match[i].startswith("href="):
            match[i] = match[i][6:len(match[i])]
        print(match[i])
        if (match[i].endswith(".jpg")) or (match[i].endswith(".png")) or (match[i].endswith(".bmp")) or (match[i].endswith(".gif")):
            print("")
        else:
            if match[i].startswith("//"):
                strWebsite2 = "http:" + match[i]
            elif match[i].startswith("/"):
                strWebsite2 = strWebsite + match[i]
            else:
                strWebsite2 = match[i]
            print(strWebsite2)
            if ("\\" not in strWebsite2):
                try:
                    strContent = urllib.request.urlopen(strWebsite2).read()
                    match2 = re.findall(re.escape(strKeyword), str(strContent))

                    if intLevel == 3:
                        match3.append(re.findall("href=[\'\"]http\://[A-z0-9_\-\./]+|href=[\'\"]\/[A-z0-9_\-\./]+|href=[\'\"]www[A-z0-9_\-\./]+", str(strContent)))
                        match3.append(re.findall("src=[\'\"]http\://[A-z0-9_\-\./]+|src=[\'\"]\/[A-z0-9_\-\./]+|src=[\'\"]www[A-z0-9_\-\./]+", str(strContent)))
                    if match2:
                        strPrint = strWebsite2 + " has " + str(len(match2)) + " matches with keyword: " + strKeyword + "\n"
                        print(strPrint)
                        strFile.write(strPrint)
                    else:
                        print("No matches for:", strWebsite2)
                except Exception as ex:
                    errormsg = "Exception {0} occured. Reason:\n{1!r}"
                    message = errormsg.format(type(ex).__name__, ex.args)
                    print(message)
                    strFile2.write(message)
                
    if intLevel == 3:
        for i in range(0,len(match3)):
            for j in range(0,len(match3[i])):
                if match3[i][j].startswith("src="):
                    match3[i][j] = match3[i][j][5:len(match3[i][j])]
                elif match3[i][j].startswith("href="):
                    match3[i][j] = match3[i][j][6:len(match3[i][j])]

                print(match3[i][j])

                if (match3[i][j].endswith(".jpg")) or (match3[i][j].endswith(".png")) or (match3[i][j].endswith(".bmp")) or (match3[i][j].endswith(".ico"))or (match3[i][j].endswith(".gif")):
                    print("")
                else:
                    if match3[i][j].startswith("//"):
                        strWebsite3 = "http:" + match3[i][j]
                    elif match3[i][j].startswith("/"):
                        if strWebsite2.endswith("/"):
                            strWebsite3 = strWebsite2[0:len(strWebsite2)-1] + match3[i][j]
                        else:
                            strWebsite3 = strWebsite2 + match3[i][j]
                        print(strWebsite3)
                    
                    else:
                        strWebsite3 = match3[i][j]
                    if ("\\" not in strWebsite3):
                        try:
                            strContent = urllib.request.urlopen(strWebsite3).read()
                            match4 = re.findall(re.escape(strKeyword), str(strContent))

                            if match4:
                                strPrint = strWebsite3 + " has " + str(len(match4)) + " matches with keyword: " + strKeyword + "\n"
                                print(strPrint)
                                strFile.write(strPrint)
                            else:
                                print("No matches for:", strWebsite3)
                        except Exception as ex:
                            errormsg = "Exception {0} occured. Reason:\n{1!r}"
                            message = errormsg.format(type(ex).__name__, ex.args)
                            print(message)
                            strFile2.write(message)
    else:
        print("")
else:
    print("Wrong level. Try again.")


strFile.close()
strFile2.close()
