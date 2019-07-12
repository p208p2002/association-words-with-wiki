# -!- coding: utf-8 -!-
import jieba
import jieba.posseg
# import jieba.analyse
import json


# print(data['0'])

# print(txtSplitAry)

class KeyMatch():
    def __init__(self, key, jsonDataPath, filterFlags=[]):
        self.key = key
        self.jsonData = ''
        self.jsonDataWithSplit = []
        self.jsonDataPath = jsonDataPath
        self.filterFlags = filterFlags


        # 加載字典
        jieba.initialize('dict/dict.txt.big')
        # jieba.load_userdict('dict/mydict')
         
        self.__loadJson(self.jsonDataPath)
        self.__splitArticleAsSentence(self.jsonData)
        self.__splitSentenceAsWords(self.jsonDataWithSplit, self.filterFlags)
                
    
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
            segLists.append(seg_list)
            # print(seg_list)        

        



if __name__ == "__main__":
    BLACK_LIST_OF_FLAGS = ['c','e']
    key = '數學'
    jsonFile = 'little.json'    
    km = KeyMatch(key,jsonFile,filterFlags = BLACK_LIST_OF_FLAGS)




# print(segLists)

# res = jieba.analyse.extract_tags(string, topK=20, withWeight=True, allowPOS=('n','nr','ns','nsf','nt','nz','nl','ng'))
# print(res)