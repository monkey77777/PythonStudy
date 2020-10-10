from janome.tokenizer import Tokenizer
 
#ファイル読み込み
v_data = open(r'C:\Users\81903\OneDrive\デスクトップ\松本_WORK\neko.txt',encoding="utf-8_sig").read()

t = Tokenizer()
tokens = t.tokenize(v_data)
 
#for token in tokens:
#    print (token)

#保存する
with open(r'C:\Users\81903\OneDrive\デスクトップ\松本_WORK\neko_Vsur.txt', 'w',encoding="utf-8_sig") as f:
    for token in tokens:
        if token.part_of_speech.split(',')[0] == '動詞':
            f.write(str(token.surface))
            f.write('\n')

#動詞の原形を書き込む
with open(r'C:\Users\81903\OneDrive\デスクトップ\松本_WORK\neko_Vori.txt', 'w',encoding="utf-8_sig") as f1:
#save_file = open(r'C:\Users\81903\OneDrive\デスクトップ\松本_WORK\neko_janome.txt',encoding="utf-8_sig")
    for token in tokens:
        if token.part_of_speech.split(',')[0] == '動詞':
            f1.write(str(token.base_form))
            f1.write('\n')


with open(r'C:\Users\81903\OneDrive\デスクトップ\松本_WORK\neko_Sahen.txt', 'w',encoding="utf-8_sig") as f2:
#save_file = open(r'C:\Users\81903\OneDrive\デスクトップ\松本_WORK\neko_janome.txt',encoding="utf-8_sig")
    for token in tokens:
        if token.part_of_speech.split(',')[1] == 'サ変接続':
            f2.write(str(token.surface))
            f2.write('\n')