import twitter

auth = twitter.OAuth(consumer_key="aZHbgnBtyXt1qOV1mdrxNLv0y",
consumer_secret="XmdPZ9IszT9wLvl03uSnxDisPO2V62LudNsHd3WTfhFUuIcOIE",
token="1298769121199321090-XxN8eYIWdTQ5h8usEePZRUfwhRLYun",
token_secret="mfZ2UvyKuU2aMVF5tO1dEGzjhTO0Zu6yjqTlmK73uKJjy")

t = twitter.Twitter(auth=auth)

#ツイートのみ
status="💩" #投稿するツイート
# t.statuses.update(status=status) #Twitterに投稿

#自動でダウンロードする


#画像付きツイート
#画像を投稿するなら画像のパス
pic=r'C:\Users\81903\OneDrive\デスクトップ\OIP.jpg'
with open(pic,"rb") as image_file:
 image_data=image_file.read()
pic_upload = twitter.Twitter(domain='upload.twitter.com',auth=auth)
id_img1 = pic_upload.media.upload(media=image_data)["media_id_string"]
t.statuses.update(status=status,media_ids=",".join([id_img1]))
