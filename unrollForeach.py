import sys
import re
import os
import copy
from pprint import pprint

#
#To Handle : 
# \foreach \x in {0,...,11}
#    \foreach \y in {0,...,7}  
#    {
#      \foreach \z in {0,...,7}  
#        \node[fill=blue!75] at (\x,\y){} ;
#    }
#\foreach \k in {0,...,7}  
#    \node[fill=blue!75] at (\k,\k){} ;
#The next foreach is also taken inside \x one



def replaceVarsinForeach(foreachHead, block):
    # print foreachHead, block
    unrolledBlocks=""
    x=re.findall("\\\\foreach(.*)in[\s]*{(.*?)}", foreachHead)
    if(x):
        x = x[0]
        varss = x[0].strip()
        rangeOfVars = x[1].strip()
        if(rangeOfVars.__contains__("...")):
            x = rangeOfVars.split(",")
            start = float(x[0])
            if(isinstance(x[1],float)):
                step=float(x[1])-float(x[0])
            else:
                step=1
            end = float(x[-1])
            # print varss, start, end, step
            for val in range(int(start), int(end+step), step):
                remainblock=copy.copy(block)
                # print ("\\"+varss.strip(), val, remainblock)
                remainblock = re.sub("\\"+varss.strip(), str(val), remainblock)
                # print "++++++++++++++++++"
                unrolledBlocks += remainblock + "\n"
                # print "++++++++++++++++++"

        else:
            
            varList=x[0].split("/")
            var_index_to_name ={}
            for index, var in enumerate(varList):
                var_index_to_name[index] = var.strip().strip("\\")
            # print var_index_to_name
            for x in rangeOfVars.split(","):
                remainblock=copy.copy(block)
                for index, val in enumerate(x.split("/")):
                    remainblock = re.sub("\\\\"+var_index_to_name[index], val, remainblock)
                # print "++++++++++++++++++"
                # print remainblock
                unrolledBlocks += remainblock + "\n"
                # print "++++++++++++++++++"
    # print unrolledBlocks
    # sys.exit(1)
    return unrolledBlocks


# mapForWhereEnd={}
def parseAndHandleForEach(inputTikzBlock):
    # print "***************", inputTikzBlock, "***************"

    regexForForeach = re.compile("\\\\foreach.*?in[\s]*{.*?}[\s]*", re.MULTILINE)
    # print(re.findall(regexForForeach, inputTikzBlock))
    restBlock=""
    lastIndexOffset = 0
    for x in re.finditer(regexForForeach, inputTikzBlock):
        block=""
        multipleForeach=False
        paraenthesis = 0
        startswithParaenthesis = False
        if(inputTikzBlock[x.end(0)] == '{'):
            lastIndexOffset = 1
            block+="{"
            paraenthesis=1
            startswithParaenthesis=True

        # block+=inputTikzBlock[x.start(0):x.end(0)]
        startOffset = 0
        if(startswithParaenthesis):
            startOffset += 1
        for k in inputTikzBlock[x.end(0)+startOffset:]:
            lastIndexOffset+=1
            block+=k
            if(k=="{"):
                paraenthesis+=1
            elif(k=="}"):
                paraenthesis-=1
                if(paraenthesis==0 and startswithParaenthesis):
                    break
            
                # # if(startswithParaenthesis):
                # #     break
                # if(len(re.findall("foreach", block))>0):
                #     multipleForeach=True
                #     continue

            # elif(k=="\\n" and paraenthesis==0):
            #     if(len(re.findall("foreach", block))>0):
            #         multipleForeach=True
            #         continue
            #     break
            elif(k==";" and paraenthesis==0):
                break
            
        # print "=========================="
        # print inputTikzBlock[x.start(0): x.end(0)]
        # print "=========================="
        # print "********"
        # print block
        # replaceVarsinForeach()
        # sys.exit(1)
        # mapForWhereEnd[x.start(0)]=x.end(0)+ len(block)
        # print  replaceVarsinForeach(inputTikzBlock[x.start(0): x.end(0)], block) + inputTikzBlock[x.end(0)+lastIndexOffset:]
        # sys.exit(1)
        # print block
        return inputTikzBlock[:x.start(0)] + replaceVarsinForeach(inputTikzBlock[x.start(0): x.end(0)], block) + inputTikzBlock[x.end(0)+lastIndexOffset:]
        # if(multipleForeach):

        # print "--------------------------------"
                




# fileName = "TestCases/rg-v2.tex"
fileName="TestCases/edge-editing-v2.tex"
with open(fileName) as inputFile:
    fileContent = inputFile.read()
regextToGetTikzPictureCode = re.compile("\\\\end[\s]*{tikzpicture}", re.MULTILINE)

z = []
for x in regextToGetTikzPictureCode.split(fileContent):
    if(x.__contains__("tikzpicture")):
        z.append(x)
count = -1
for x in z:
    for y in (re.split("\\\\begin{tikzpicture}", x)):
        count += 1
        if(count%2==1):
            print "==========================================="
            print("\n\nCalling parseAndHandleForEach for")
            print(y)
            print "==========================================="
            z = parseAndHandleForEach(y)
            # print "\n\n-----START-----\n", z, "\n-----END-----\n\n"
            # sys.exit(1)
            while(z.count("foreach")>0):
                x = parseAndHandleForEach(z)
                z = x
                # print "\n\n-----START-----\n", z, "\n-----END-----\n\n"
            print z