import sys
import collections
import os
def getName(text):
    result = ""
    split = text.split("-")
    for a in split:
        try:
            int(a[0])
        except:
            if(a != ""):
                result += a + "-"
    if(result):
        result = result[:-1]
        version = text.split(result)[1][1:]
        version = version.replace("\r", "")
        return (result, version)

def extractVersions(content):
    if(content[len(content) - 1] == ""):
        content = content[:-1]
    result = {}
    for line in content:
        name, version = getName(line)
        result[name] = version
    return result;

def diff(file1, file2):
    showMissing = False
    showDiffs = False
    if(len(sys.argv) == 3):
        showMissing = True
        showDiffs = True
    if("-d" in sys.argv):
        showDiffs = True

    if("-m" in sys.argv):
        showMissing = True

    content1 = os.popen("docker exec -it " + file1 + " rpm -qa").read()
    content2 = os.popen("docker exec -it " + file2 + " rpm -qa").read()
    content1 = content1.split("\n")
    if(content1[len(content1) - 1] == ""):
        content1 = content1[:-1]
    content2 = content2.split("\n")
    if(content2[len(content2) - 1] == ""):
        content2 = content2[:-1]
    
    versions1 = extractVersions(content1)
    versions1 = collections.OrderedDict(sorted(versions1.items()))
    versions2 = extractVersions(content2)
    for package in versions1:
        if(showMissing and package not in versions2):
            print("\033[91m" + package + " \033[0mmissing in \033[93m" + file2)
        elif(showDiffs and package in versions2 and versions1[package] != versions2[package]):
            print("\033[91m" + package + " \033[0mversion \033[96m" + versions1[package] + " \033[0mis different in \033[93m" + file2 + " \033[96m-> " + versions2[package])

diff(sys.argv[1], sys.argv[2])