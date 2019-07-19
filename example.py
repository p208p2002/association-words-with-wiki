from KeyMatch import KeyMatch
import pickle

if __name__ == "__main__":
    # 自訂詞性黑名單
    with open('blacklists/flags.txt','r',encoding='utf-8') as f:
        data = f.read()
    blackFlags = data.split()

    # 自訂單詞黑名單
    with open('blacklists/words.txt','r',encoding='utf-8') as f:
        data = f.read()
    blackWords = data.split()

    # 單詞黑名單字典
    with open('blacklists/words.pkl', 'rb') as f:
        data = list(pickle.load(f))
    blackWords = blackWords + data

    # 配對關鍵字
    key = '周杰倫'

    # 維基資料
    jsonFile = 'wikidata/wiki20180805_fullText.json'

    # 
    km = KeyMatch() # 初始化
    # km.split(jsonDataPath = jsonFile, blackFlags = blackFlags) # wiki file 切割，可下載已切割完成檔案
    km.match(key = key, blackWords = blackWords) # 開始配對
    print(km.getTop(40)) # 取得最高結果