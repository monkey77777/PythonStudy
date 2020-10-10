from janome.tokenizer import Tokenizer
 
#ファイル読み込み
v_data = open(r'C:\Users\81903\OneDrive\デスクトップ\松本_WORK\neko.txt',encoding="utf-8_sig").read()

t = Tokenizer()
tokens = t.tokenize(v_data)

#for token in tokens:
#    print (token)

flg_sur = '0'

#保存する
with open(r'C:\Users\81903\OneDrive\デスクトップ\松本_WORK\neko_Vsur.txt', 'w',encoding="utf-8_sig") as f:
    for token in tokens:
        if flg_sur == '1':
            if token.part_of_speech.split(',')[0] == '名詞' and pre_token.part_of_speech.split(',')[0] == '名詞':
                f.write(str(pre_token.surface))
                f.write('の')
                f.write(str(token.surface))
                f.write('\n')
                flg_sur = '0'
        if token.surface == 'の':
            flg_sur = '1'
        else:
            pre_token = token
