#from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time
#import urllib,urllib2
#import urlparse


btn = '1'
while True:
    search_words = "sheet 1" 
    print()
    print("  ==============================================================================  ")
    print("               << The Program of Web Crawler for Naver Band  >>")
    print("                            by shh0456@gmail.com'             ")
    print("  ==============================================================================  ")
    print()
    print("  1. 파일 저장 경로 입력(Enter)    ex) C:/Users/user ")
    print()
    print("  2. 밴드 주소 입력(Enter)    ex) https://band.us/discover/search/50%EB%8C%80 ")
    print()
    print("  3. 멤버수 입력(Enter)      ex) 0, 30, 100 ... ")
    print()
    print("  4. 파일 명 입력(Enter)     ex) 수박, 123, abc ...   ") 
    print()
    print("  ------------------------------------------------------------------------------  ")
     # In[]:   
    if btn is '1' : 
        RESULT_DIRECTORY = input('  - 파일 저장 경로 입력 : ')    

    url = input('  - 밴드 주소 입력 : ')
    crt = input('  - 멤버수 기준 입력 : ')
    file_name = input('  - 파일 명 입력 : ')
    
    ## part that need to modify
#    webpath = 'C:/Users/user/Testingboard/20190122_beautifulsoup/webdriver/chromedriver.exe'
#    wd = webdriver.Chrome(webpath)
    wd = webdriver.Chrome('./webdriver/chromedriver.exe')
    wd.get(url)
    
    
    results = []
    SCROLL_PAUSE_TIME = 0.5
    
    # Get scroll height
    last_height = wd.execute_script("return document.body.scrollHeight")
    
    while True:
        # Scroll down to bottom
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
    
        # Calculate new scroll height and compare with last scroll height
        new_height = wd.execute_script("return document.body.scrollHeight")
        
    
        if new_height == last_height:
            break
        last_height = new_height
        
    html = wd.page_source
    bs = BeautifulSoup(html, 'html.parser')
    
    time.sleep(1)
    tags = bs.find('', attrs={'class': 'cCoverList searchResult _bandListContainer'})
    tags_info =  tags.findAll('a')      
    
    
     # In[]:   
    results = []
    for tag in tags_info:
        
        if tags_info[0].get('class') is None: 
            break 
    
        strings = list(tag.strings)
    
    
        # in thin case, there is a subTxt  
        if len(strings) is 12: 
    
            crts = int(float(strings[-5].replace(",","")))
            crt = int(float(crt))
            if crts > crt :
                name = strings[2]
                subTxt = strings[4]
                member = int(float(strings[-5].replace(",","")))   
                url = 'https://band.us' + tag.get('href')
                results.append((name, member, url, subTxt))
    
    
    table = pd.DataFrame(results, columns=['밴드이름', '멤버수', 'URL', '설명'])
    table = table.sort_values(['멤버수'], ascending = False)
    table = table.reset_index(drop = True)
     # In[]:   
    writer = pd.ExcelWriter(RESULT_DIRECTORY + '/BandInfo_%s.xlsx' %(file_name), engine="xlsxwriter" )
    table.to_excel(writer, sheet_name = search_words)
    
    workbook = writer.book
    worksheet = writer.sheets[search_words]
    worksheet.set_column(1, 1, 110)      
    worksheet.set_column(2, 2, 15)          
    worksheet.set_column(3, 3, 30)        
    worksheet.set_column(4, 4, 200)             
    header_format = workbook.add_format({'bold': True,
                                        'text_wrap': True,
                                        'valign': 'vcenter',
                                        'fg_color': '#FFFF00',
                                        'border': 1})
    
    for col_num, val in enumerate(table.columns.values):
        worksheet.write(0, col_num+1, val, header_format)
    
    
    ## Pandas writer 객체 닫기
    writer.close()
    
    print()            
    print('  완료되었습니다.')  
    print()
    print('  프로그램을 종료 : 0번 (Enter)')
    print('  저장 경로를 변경하고 계속 검색 : 1번 (Enter)')
    print('  계속 검색하기 : 아무키 + (Enter)')
    print("  ==============================================================================  ")
    btn = input()
    if btn is '0':
        break
    