#導入 Discord.py
import discord
import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
chrome_options = Options()

# run chrome without sandbox
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


# 建立client 物件以與 Discord 溝通

client = discord.Client()

# 調用 event 函式庫
@client.event

# 當啟動完畢時
async def on_ready():
    print('The bot is ready!')

@client.event
async def on_message(message):

    # 排除機器人的訊息，避免陷入無限循環
    if message.author == client.user:
          return

    if message.content.startswith('代碼'):
        # 分割訊息成四份並放入訂單資訊中
        orderInfo = message.content.split(" ",4)

        # 如果訂單資訊小於四
    if len(orderInfo) < 4:
          await message.channel.send('正確格式(代碼/商品名稱/電子郵件/金額)')
    else:
          await message.channel.send(f'商品名稱: {orderInfo[1]} \n 郵件: {orderInfo[2]} \n 金額: {orderInfo[3]} ')
          await message.channel.send('處理中...請稍後')
          ITENNAME=orderInfo[1]
          AMT=orderInfo[3]
          EMAIL=orderInfo[2]
          driver = webdriver.Chrome(options=chrome_options)

          # use get func
          driver.get("https://shop.cutespirit.org/newebpay/getinfo.php?ITEMNAME=" 
              +ITENNAME
              +"&AMT="
              +AMT
              +"&EMAIL="+EMAIL)
          # to wait the use click the btn
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
          # get the value by html id
          paycode=driver.find_element(By.NAME, 'CodeNo').get_attribute('value')
          TradeNo=driver.find_element(By.NAME, 'TradeNo').get_attribute('value')
          Amt=driver.find_element(By.NAME, 'Amt').get_attribute('value') 
          ExpireDate=driver.find_element(By.NAME, 'ExpireDate').get_attribute('value')
          MerchantOrderNo=driver.find_element(By.NAME, 'MerchantOrderNo').get_attribute('value')

          # use discord.py embed obj
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

          # send the embed obj the TextChannel
          await message.channel.send(embed=embed)

# run the code
try:
    msg = open('bot.json', mode='r', encoding='utf-8')
    msg = json.load(msg)
    client.run(msg['TOKEN'])
except:
    print('Can not run the bot, you should check if the bot.json is exist or not.')
