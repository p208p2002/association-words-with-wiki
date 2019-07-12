# -!- coding: utf-8 -!-
import jieba
import jieba.posseg
# import jieba.analyse
import json


# print(data['0'])

# print(txtSplitAry)

class KeyMatch():
    def __init__(self, key, jsonDataPath, filterFlags=[]):
        self.key = key # match 關鍵字
        self.jsonDataPath = jsonDataPath # json檔案路徑
        self.jsonData = '' # 原始json資料
        self.jsonDataWithSplit = [] # 句子分割
        self.jsonDataAsWords = [] # 拆成單字且過濾後
        self.filterFlags = filterFlags # 詞性過濾黑名單


        # 加載字典
        jieba.initialize('dict/dict.txt.big')
        # jieba.load_userdict('dict/mydict')
            
    def run(self):
        # 加載wiki json
        self.__loadJson(self.jsonDataPath)
        # 將文章分隔成句子
        self.__splitArticleAsSentence(self.jsonData)
        # 將句子分割成單詞，並且過濾指定詞性
        self.__splitSentenceAsWords(self.jsonDataWithSplit, self.filterFlags)
        # 開始匹配
        self.__matchKey(self.key, self.jsonDataAsWords)

                    
    def __loadJson(self, jsonDataPath):
        with open(jsonDataPath, 'r',encoding="utf-8") as f:
            data = json.load(f)
        self.jsonData = data
    
    def __splitArticleAsSentence(self, jsonData):
        # 拆分句子
        data = jsonData        
        tmp = ''
        txtSplitAry = []
        for s in data['0']:
            if(s == '，' or s == '。'):
                txtSplitAry.append(tmp)
                tmp = ''
            else:
                tmp = tmp + s

        if(tmp != ''):
            txtSplitAry.append(tmp)
        
        self.jsonDataWithSplit = txtSplitAry
    
    def __splitSentenceAsWords(self, jsonDataWithSplit, filterFlags=[]):
        # 分詞&過濾詞性                
        segLists = []
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
            self.jsonDataAsWords = segLists
            # print(seg_list)
    
    def __matchKey(self, key, jsonDataAsWords):
        print(key,jsonDataAsWords)

        dataOnlyAsWordsWithoutFlags = []
        for i in jsonDataAsWords:
            onlyWords = []
            for j in i:
                w,f = j
                onlyWords.append(w)
            dataOnlyAsWordsWithoutFlags.append(onlyWords)
        print(dataOnlyAsWordsWithoutFlags)
            
        

        


        



if __name__ == "__main__":
    BLACK_LIST_OF_FLAGS = []
    key = '數學'
    jsonFile = 'little.json'    
    km = KeyMatch(key,jsonFile,filterFlags = BLACK_LIST_OF_FLAGS)
    km.run()




# print(segLists)

# res = jieba.analyse.extract_tags(string, topK=20, withWeight=True, allowPOS=('n','nr','ns','nsf','nt','nz','nl','ng'))
# print(res)