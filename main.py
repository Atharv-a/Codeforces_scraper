import time
import os 
import shutil
from xml.etree.ElementPath import xpath_tokenizer
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

def screen_shot(driver,problem_code):
    S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
    driver.set_window_size(S('Width'),S('Height'))
    page=driver.find_element(By.CLASS_NAME,'problemindexholder')
    page.screenshot(f'Problem.png')
    shutil.move(f'Problem.png',problem_code)


def input_output(driver,problem_code):
    sample_io=driver.find_element(By.CLASS_NAME,'sample-test')
    Input_text=sample_io.find_elements(By.CLASS_NAME,'input')
    output_text=sample_io.find_elements(By.CLASS_NAME,'output')
    i=1
    for element in Input_text:
         f=open(f'input{i}.txt','w')
         element=element.find_element(By.TAG_NAME,'pre')
         text=element.text
         f.write(text)
         f.close()
         shutil.move(f'input{i}.txt',problem_code)
         i+=1
    i=1
    for element in output_text:
         f=open(f'output{i}.txt','w')
         element=element.find_element(By.TAG_NAME,'pre')
         text=element.text
         f.write(text)
         f.close()
         shutil.move(f'output{i}.txt',problem_code)
         i+=1


os.chdir(r'C:\Users\Ayush\c++ projects\Codeforces Scraper')
path=ChromeDriverManager().install()
service =Service(path)
options=Options()
options.headless=True
driver = webdriver.Chrome(service=service,options=options)
driver.get("https://codeforces.com/")
contest_page_link=driver.find_element(by=By.XPATH,value='//*[@id="body"]/div[3]/div[5]/ul/li[4]/a')
contest_page_link.send_keys(Keys.RETURN)
print("Enter number of contest to be processed:")
number_of_contest=int(input())
for i in range(2,number_of_contest+2):
    contest=0
    try:
       contest=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,f'//*[@id="pageContent"]/div[1]/div[2]/div[1]/div[6]/table/tbody/tr[{i}]')))
    except:
        print("\nouterLooperror\n")
        driver.quit()
    
    contest_id =contest.get_attribute('data-contestid')
    os.mkdir(f'{contest_id}')
    a =contest.find_element(By.TAG_NAME,'a').click()
    problem_table=driver.find_element(By.CLASS_NAME,'problems')
    table_link=problem_table.find_elements(By.TAG_NAME,'tr')
    number_of_links=len(table_link)-1
    for j in range(2,number_of_links+2):
        try:
            link=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,f'//*[@id="pageContent"]/div[2]/div[6]/table/tbody/tr[{j}]/td[1]/a')))

        except:
            print("\ninnerLooperror\n")
            driver.quit()

        problem_code=link.text
        os.mkdir(f'{problem_code}')
        link.click()
        screen_shot(driver,problem_code)
        input_output(driver,problem_code)
        shutil.move(problem_code,contest_id)
        driver.back()    

    driver.back()


print("successfull execution")
time.sleep(5000)
driver.quit()
