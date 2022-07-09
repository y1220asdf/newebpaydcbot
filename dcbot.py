#導入 Discord.py
import discord

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


#client 是我們與 Discord 連結的橋樑

client = discord.Client()

#調用 event 函式庫
@client.event
#當機器人完成啟動時
async def on_ready():
    print('目前登入身份：', client.user)

@client.event
#當有訊息時
async def on_message(message):
    #排除自己的訊息，避免陷入無限循環
    if message.author == client.user:
        return
    #如果包含 ping，機器人回傳 pong
      
    if message.content.startswith('代碼'):
      #分割訊息成兩份
      orderdate = message.content.split(" ",4)
      #如果分割後串列長度只有1
      if len(orderdate) < 4:
        await message.channel.send("正確格式(代碼/商品名稱/電子郵件/金額)")
      else:
        await message.channel.send("商品名稱:"+orderdate[1]+"|"+"郵件:"+orderdate[2]+"|"+"金額:"+orderdate[3])
        await message.channel.send("處理中...請稍後")
        ITENNAME=orderdate[1]
        AMT=orderdate[3]
        EMAIL=orderdate[2]
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://shop.cutespirit.org/newebpay/getinfo.php?ITEMNAME=" 
+ITENNAME
+"&AMT="
+AMT
+"&EMAIL="+EMAIL)
        driver.implicitly_wait(6)
        driver.find_element("xpath", "/html/body/div[1]/div[2]/div[2]/form/div[7]/button").click()
        driver.implicitly_wait(6)
        driver.find_element("xpath", '//*[@id="mpg_info"]/div[1]/div[2]/label[3]').click()
        driver.implicitly_wait(6)
        driver.find_element("xpath", '//*[@id="show_pay_footer_m"]/div/div[1]/label/input').click()
        driver.implicitly_wait(6)
        driver.find_element("xpath", '//*  [@id="confirm_send_order"]').click()
        driver.implicitly_wait(6)
        WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "CodeNo"))
    )
        paycode=driver.find_element(By.NAME, 'CodeNo').get_attribute('value')
        TradeNo=driver.find_element(By.NAME, 'TradeNo').get_attribute('value')
        Amt=driver.find_element(By.NAME, 'Amt').get_attribute('value') 
        ExpireDate=driver.find_element(By.NAME, 'ExpireDate').get_attribute('value')
        MerchantOrderNo=driver.find_element(By.NAME, 'MerchantOrderNo').get_attribute('value')
        embed=discord.Embed(title="繳費系統", url="https://shop.cutespirit.org/newebpay/", color=0x00ffd5)
        embed.set_author(name="繳費系統", url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRp1SULUXCTTabtHoKVuIF7PrAhHT2Yz6CqgA&usqp=CAU", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRp1SULUXCTTabtHoKVuIF7PrAhHT2Yz6CqgA&usqp=CAU")
        embed.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRp1SULUXCTTabtHoKVuIF7PrAhHT2Yz6CqgA&usqp=CAU")
        embed.add_field(name='商品名稱', value=ITENNAME, inline=True)
        embed.add_field(name='金額', value=Amt, inline=True)
        embed.add_field(name='超商代碼', value=paycode, inline=True)
        embed.add_field(name='電子郵件', value=EMAIL, inline=True)
        embed.add_field(name='繳費期限', value=ExpireDate, inline=True)
        embed.add_field(name='訂單編號', value=MerchantOrderNo, inline=True)
        embed.add_field(name='交易序號', value=TradeNo, inline=True)
        embed.set_footer(text='創作心得: ' + "爽")
        await message.channel.send(embed=embed)

client.run('OTk0ODg3OTMwMjYwNzUwNDE2.GA_AYz.7hl4O3TaVtAD0iUFMi8-ezV3WdX5Mo-1wMr5AE') 
