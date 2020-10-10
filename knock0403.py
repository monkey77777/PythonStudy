from janome.tokenizer import Tokenizer
 
#ファイル読み込み
v_data = open(r'C:\Users\81903\OneDrive\デスクトップ\松本_WORK\neko.txt',encoding="utf-8_sig").read()

t = Tokenizer()
tokens = t.tokenize(v_data)

#for token in tokens:
#    print (token)

flg_sur = '0'
token_str = ''

#保存する
with open(r'C:\Users\81903\OneDrive\デスクトップ\松本_WORK\neko_NConnect.txt', 'w',encoding="utf-8_sig") as f:
    for token in tokens:
        if token.part_of_speech.split(',')[0] == '名詞':
            token_str = token_str + str(token.surface)
            flg_sur = '1'
        else:
            if flg_sur == '1':
                f.write(token_str)
                f.write('\n')
                flg_sur = '0'
                token_str = ''
            else:
                pass