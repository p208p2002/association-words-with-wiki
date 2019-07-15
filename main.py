# -!- coding: utf-8 -!-
import jieba
import jieba.posseg
# import jieba.analyse
import json
import os
from collections import Counter

class KeyMatch():
    def __init__(self):        
        self.jsonData = '' # 原始json資料
        self.jsonDataWithSplit = [] # 句子分割        
        self.filterFlags = [] # 詞性過濾黑名單
        self.keyMatchRes = []

        # 加載字典
        jieba.initialize('dict/dict.txt.big')
        jieba.load_userdict('dict/mydict')
            
    def split(self, jsonDataPath, filterFlags=[]):
        #
        self.filterFlags = filterFlags
        # 加載wiki json
        print('** 加載 wiki json **')
        self.__loadJson(jsonDataPath)        
        # 將文章分隔成句子
        print('** 開始分割文章 **')
        self.__splitArticleAsSentence(self.jsonData)        
        # 將句子分割成單詞，並且過濾指定詞性
        print('** 開始分割句子成單詞 **')
        self.__splitSentenceAsWords(self.jsonDataWithSplit, self.filterFlags)
        # 合併存檔
        print('** 合併存檔 **')
        self.__mergeSplitDatas()


    def match(self, key=''):        
        # 開始匹配
        print('** 開始關鍵字匹配 **')
        self.__matchKey(key)
        print('** 完成 **')
    
    def getTop(self,n):
        return Counter(self.keyMatchRes).most_common(n)

                    
    def __loadJson(self, jsonDataPath):
        with open(jsonDataPath, 'r',encoding="utf-8") as f:
            data = json.load(f)
        self.jsonData = data
    
    def __splitArticleAsSentence(self, jsonData):
        # 拆分句子
        data = jsonData        
        tmp = ''
        txtSplitAry = []
        
        index = 0
        while(True):
            try:
                for s in data[str(index)]:
                    if(s == '，' or s == '。'):
                        txtSplitAry.append(tmp)
                        tmp = ''
                    else:
                        tmp = tmp + s

                if(tmp != ''):
                    txtSplitAry.append(tmp)
                index += 1

                if(index == 2):
                    break
            except:
                break
        
        self.jsonDataWithSplit = txtSplitAry
    
    def __splitSentenceAsWords(self, jsonDataWithSplit, filterFlags=[]):
        # 分詞&過濾詞性                
        segLists = []
        lenOfJsonDataWithSplit = len(jsonDataWithSplit)
        fileSerialNumber = 0
        for i in range(len(jsonDataWithSplit)):
            seg_list = jieba.posseg.lcut(jsonDataWithSplit[i])

            # 找到刪除目標
            delTarget = []
            for j in seg_list:
                word, flag = j
                if flag in filterFlags:
                    delTarget.append(j)
            
            # 刪除
            for j in delTarget:
                seg_list.remove(j)

            # 存回陣列                              
            segLists.append(seg_list)

            # 階段存檔
            if((i!=0 and i %100 ==0) or (i!=0 and i == lenOfJsonDataWithSplit-1)):                
                # 抽離詞性
                dataOnlyAsWordsWithoutFlags = [] # 不含詞性的資料
                for k in segLists:            
                    onlyWords = []
                    for l in k:                
                        w,f = l
                        onlyWords.append(w)
                    dataOnlyAsWordsWithoutFlags.append(onlyWords)
                
                # 
                segLists = dataOnlyAsWordsWithoutFlags
                del dataOnlyAsWordsWithoutFlags
                
                # 儲存存檔
                segListsStr = str(segLists).replace('pair(','(')
                with open('./splitdata/seg_lists_'+str(fileSerialNumber), 'w', encoding='utf-8') as f:
                    f.write(segListsStr)
                print('save:','seg_lists_'+str(fileSerialNumber),i)
                
                # release mem
                del segLists
                del segListsStr
                segLists = []
                fileSerialNumber += 1
        
        #
        try:
            del segLists
            del segListsStr
        except:
            pass
    
    def __mergeSplitDatas(self):
        fileSN = 0
        fileBaseName = 'seg_lists_'
        fileRootPath = 'splitdata'
        jsonDataAsWords = [] # 讀入的資料存檔
        # 讀入存檔資料
        while(True):            
            try:
                with open(fileRootPath + '/' + fileBaseName + str(fileSN), 'r',encoding="utf-8") as f:
                    data = f.read()
                print('load:',fileSN)
                fileSN += 1

                # 將檔案資料讀入變數
                _jsonDataAsWords = locals()
                exec("jsonDataAsWords="+str(data), globals(), _jsonDataAsWords)
                jsonDataAsWords = jsonDataAsWords + _jsonDataAsWords['jsonDataAsWords']

                #刪除分割檔案
                os.remove(fileRootPath + '/' + fileBaseName + str(fileSN-1))

            except:
                break
        
        # 合併
        with open('./splitdata/seg_lists', 'w', encoding='utf-8') as f:
            f.write(str(jsonDataAsWords))
        del jsonDataAsWords

    def __matchKey(self, key):
        fileName = 'seg_lists'
        fileRootPath = 'splitdata'
        jsonDataAsWords = [] # 讀入的資料存檔
        # 讀入檔案
        with open(fileRootPath + '/' + fileName , 'r',encoding="utf-8") as f:
            data = f.read()

        # 將檔案資料讀入變數
        _jsonDataAsWords = locals()
        exec("jsonDataAsWords="+str(data), globals(), _jsonDataAsWords)
        jsonDataAsWords = jsonDataAsWords + _jsonDataAsWords['jsonDataAsWords']
        del data

        # 與關鍵字匹配
        keyMatchRes = []
        for words in jsonDataAsWords:
            if key in words:
                for i in words:
                    if i != key:
                        keyMatchRes.append(i)
            else:
                continue
        
        self.keyMatchRes = keyMatchRes
        

if __name__ == "__main__":
    # 詞性 nu : no use
    BLACK_LIST_OF_FLAGS = ['c','e','h','k','o','p','u','ud','ug','uj','ul','uv','uz','y','x','nu','z','zg','f','m']
    key = '數學'
    jsonFile = 'wikidata/wiki20180805_fullText.json'    
    km = KeyMatch()
    km.split(jsonDataPath = jsonFile ,filterFlags = BLACK_LIST_OF_FLAGS)
    km.match(key = key)
    print(km.getTop(10))

    # print(jieba.posseg.lcut('如'))
    # print(jieba.posseg.lcut('亦'))
    # print(jieba.posseg.lcut('有著'))




# print(segLists)

# res = jieba.analyse.extract_tags(string, topK=20, withWeight=True, allowPOS=('n','nr','ns','nsf','nt','nz','nl','ng'))
# print(res)