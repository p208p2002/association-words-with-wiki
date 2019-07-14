# -!- coding: utf-8 -!-
import jieba
import jieba.posseg
# import jieba.analyse
import json
from collections import Counter


# print(data['0'])

# print(txtSplitAry)

class KeyMatch():
    def __init__(self, jsonDataPath):
        self.key = '' # match 關鍵字
        self.jsonDataPath = jsonDataPath # json檔案路徑
        self.jsonData = '' # 原始json資料
        self.jsonDataWithSplit = [] # 句子分割
        self.jsonDataAsWords = [] # 拆成單字且過濾後
        self.filterFlags = [] # 詞性過濾黑名單
        self.keyMatchRes = []


        # 加載字典
        jieba.initialize('dict/dict.txt.big')
        jieba.load_userdict('dict/mydict')
            
    def split(self, filterFlags=[]):
        #
        self.filterFlags = filterFlags
        # 加載wiki json
        print('** 加載 wiki json (1/3) **')
        self.__loadJson(self.jsonDataPath)
        print('** 完成 **')
        # 將文章分隔成句子
        print('** 開始分割文章 (2/3) **')
        self.__splitArticleAsSentence(self.jsonData)
        print('** 完成 **')
        # 將句子分割成單詞，並且過濾指定詞性
        print('** 開始分割句子成單詞 (3/3) **')
        self.__splitSentenceAsWords(self.jsonDataWithSplit, self.filterFlags)
        print('** 完成 **')

    def match(self, key=''):
        self.key = key
        # 開始匹配
        print('** 開始關鍵字匹配 **')
        self.__matchKey(self.key, 'seg_lists')
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

            except:
                break
        
        self.jsonDataWithSplit = txtSplitAry
    
    def __splitSentenceAsWords(self, jsonDataWithSplit, filterFlags=[]):
        # 分詞&過濾詞性                
        segLists = []
        lenOfJsonDataWithSplit = len(jsonDataWithSplit)
        for i in range(len(jsonDataWithSplit)):
            print(i,lenOfJsonDataWithSplit)
            # if(i % 10000 == 0):
            #     print(i,lenOfJsonDataWithSplit)
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
            self.jsonDataAsWords = segLists
            # print(seg_list)
            # print(self.jsonDataAsWords)

        # 儲存存檔
        segListsStr = str(segLists).replace('pair(','(')
        with open('seg_lists', 'w', encoding='utf-8') as f:
            f.write(segListsStr)
    
    def __matchKey(self, key, dicPath):     
        with open(dicPath, 'r',encoding="utf-8") as f:
            data = f.read()        

        # 將檔案資料讀入變數
        _jsonDataAsWords = locals()
        exec("jsonDataAsWords="+str(data), globals(), _jsonDataAsWords)
        # print(_jsonDataAsWords['jsonDataAsWords'])        
        jsonDataAsWords = _jsonDataAsWords['jsonDataAsWords']
        
        # 抽離詞性
        dataOnlyAsWordsWithoutFlags = [] # 不含詞性的資料
        for i in jsonDataAsWords:            
            onlyWords = []
            for j in i:                
                w,f = j
                onlyWords.append(w)
            dataOnlyAsWordsWithoutFlags.append(onlyWords)
        # print(dataOnlyAsWordsWithoutFlags)

        # 與關鍵字匹配
        keyMatchRes = []
        for words in dataOnlyAsWordsWithoutFlags:
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
    jsonFile = 'wiki20180805_fullText.json'    
    km = KeyMatch(jsonDataPath = jsonFile)
    km.split(filterFlags = BLACK_LIST_OF_FLAGS)
    km.match(key = key)
    print(km.getTop(20))

    # print(jieba.posseg.lcut('如'))
    # print(jieba.posseg.lcut('亦'))
    # print(jieba.posseg.lcut('有著'))




# print(segLists)

# res = jieba.analyse.extract_tags(string, topK=20, withWeight=True, allowPOS=('n','nr','ns','nsf','nt','nz','nl','ng'))
# print(res)