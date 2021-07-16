import csv
from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
import time
fields=[]
rows=[]
product_name=[]
items = ["Kaaval Kottam","Kutrap Parambarai","The 5 AM club","Eat That Frog","Anna Karenina","The Great Gatsby","A Passage to India","Invisible Man","Things Fall Apart"]

for item in items:
    amazon_url =f"https://www.amazon.in/s?k={item}&crid=1OFM31LB41YBE&sprefix=Eat+that+%2Caps%2C445&ref=nb_sb_ss_ts-doa-p_1_9"
    driver = webdriver.Firefox(executable_path="C:\\Users\\Asus\\Desktop\\geckodriver.exe")
    driver.maximize_window()
    print(f"Searching for {item}.")
    driver1 = driver.get(amazon_url)
    heading=driver.find_element_by_tag_name('h2').text
    print(heading)
    row=[]
    try:
        search_button = driver.find_element_by_link_text(item)
        text=search_button.text
        row.append(text)
        search_button.click()
        print("try")
    except:
        search_button = driver.find_element_by_link_text(heading)
        text=search_button.text
        row.append(text)
        search_button.click()
        print("Except")            
    chwd = driver.window_handles            
    for w in chwd:
        driver.switch_to.window(w)
    time.sleep(1)
    url=driver.current_url
    headers= ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'})
    page=requests.get(url=url,headers=headers)
    soup = BeautifulSoup(page.content,'lxml')
    try:
        d =soup.find("span",class_="author notFaded").text
        l1=(d.split("\n"))
        u=[]
        for i in l1:
            if i != "":
                u.append(i)
        m=[]
        s=0
        for j in u:
            if u[s]=="(Author)":
                m.append(u[s-1])
            s+=1
        Author_name = []
        for i in m:
            if i not in Author_name:
                Author_name.append(i)
        row.append(Author_name[0])
    except:
        row.append("NA")
    try:
        c = soup.find("div",id="detailBulletsWrapper_feature_div").text
        l=(c.split("\n"))
        k=[]
        for i in l:
            if i != "":
                k.append(i)
        k.pop(0)

        z=0
        for i in k:
            
            if i == ":":
                k.pop(z)
                k.pop(z)
                k.pop(z-1)
            z+=1
        heading=['ASIN','Publisher','Language','Hardcover','Item Weight','Paperback','Dimensions','Best Sellers Rank:','Customer Reviews:']
        field=[]
        h=0
        m=len(k)-1
        n="NA"
        for i in heading:
            c=0
            for j in k:
                if k[c]==heading[h]:
                    field.append(j)
                    row.append((k[c+1]))
                    break
                elif m==c:
                    row.append(n)                       
                c+=1
            h+=1
        rows.append(row)
    except:
        print("Attribute Error")
    driver.quit()
heading.insert(0,'Book Name')
heading.insert(1,'Author')
with open('GFG.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(heading) 
    write.writerows(rows)
print("success")

