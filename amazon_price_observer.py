import requests
from bs4 import BeautifulSoup
import smtplib
import time

# Amazon product to observe
URL = 'https://www.amazon.it/gp/product/B01N9VBVN1?pf_rd_p=df2ad00e-5897-4a61-99bf-8e35bfa9a01e&pf_rd_r=NC8X7GGF26JMDVBYAW7Q&th=1'
# https://www.whatismybrowser.com/detect/what-is-my-user-agent
headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}

def checking_price(): 
	page = requests.get(URL, headers=headers)
	soup = BeautifulSoup(page.content, 'html.parser')

	# Finding product name and price
	title = soup.find(id="productTitle").get_text()
	price = soup.find(id="priceblock_ourprice").get_text()
	converted_price = int(price[0:3])
	
	print(title.strip())
	print(converted_price)

	# Chosing threshold value (e.g. 200€)
	if(converted_price < 200): 
		sending_email(converted_price)

def sending_email(price):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()

	# https://support.google.com/accounts/answer/185833?hl=en-GB
	server.login('your_email@gmail.com', 'password')

	subject = 'Price fall down!'
	body = f"Price fall down at {price} !\n\n Check amazon link {URL}"

	msg = f"Subject: {subject}\n\n{body}"

	server.sendmail(
		'from_email@gmail.com',
		'to_email@gmail.com',
		msg
	)
	print('EMAIL SENT!')

	server.quit()

while(True):
	checking_price()
	time.sleep(3600)







