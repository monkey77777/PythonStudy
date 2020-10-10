from janome.tokenizer import Tokenizer
 
#ファイル読み込み
v_data = open(r'C:\Users\81903\OneDrive\デスクトップ\松本_WORK\neko.txt',encoding="utf-8_sig").read()

t = Tokenizer()
tokens = t.tokenize(v_data)
 
#for token in tokens:
#    print (token)

#保存する
with open(r'C:\Users\81903\OneDrive\デスクトップ\松本_WORK\neko_janome.txt', 'w',encoding="utf-8_sig") as f:
#save_file = open(r'C:\Users\81903\OneDrive\デスクトップ\松本_WORK\neko_janome.txt',encoding="utf-8_sig")
    for token in tokens:
#    save_file.write(str(token))
#    save_file.write("\n")

        f.write(str(token))
        f.write('\n')