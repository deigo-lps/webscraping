from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#https://www.google.com/search?q=previsao+rio+preto
def get_weather_data(url):
  chrome_options = Options()
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-gpu')
  chrome_options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome('/home/diego/virtualenvs/previsao/chromedriver/chromedriver',options=chrome_options)
  driver.get(url)
  soup = BeautifulSoup(driver.page_source, 'html.parser')
  result={}
  result['loc'] = soup.find("div", attrs={"id": "wob_loc"}).text
  result['time'] = soup.find("div", attrs={"id": "wob_dts"}).text
  result['temp'] = soup.find("span", attrs={"id": "wob_tm"}).text+'ºC'
  result['cond'] = soup.find("span", attrs={"id": "wob_dc"}).text
  result['prec'] = soup.find("span", attrs={"id": "wob_pp"}).text
  result['humi'] = soup.find("span", attrs={"id": "wob_hm"}).text
  result['wind'] = soup.find("span", attrs={"id": "wob_ws"}).text
  i=0
  for day in soup.find("div",attrs={"id": "wob_dp"}):
    if i==0:
      result['max']=day.findAll("span",attrs={"class": "wob_t"})[0].text+'ºC'
      result['min']=day.findAll("span",attrs={"class": "wob_t"})[2].text+'ºC'
    else:
      result['weekday'+str(i)]=day.find("div").attrs["aria-label"]
      result['cond'+str(i)]=day.find("img").attrs["alt"]
      result['max'+str(i)]=day.findAll("span",attrs={"class": "wob_t"})[0].text+'ºC'
      result['min'+str(i)]=day.findAll("span",attrs={"class": "wob_t"})[2].text+'ºC'
    i+=1
  return result

if __name__ == '__main__':
  import os
  city=input('Digite a cidade:')
  pre=get_weather_data('https://www.google.com/search?q=previsao+{}'.format(city.replace(' ','+')))
  os.system("clear")
  print('{}\n{}\nMáxima: {}\nMínima: {}\nAtual: {}\nCondição: {}\nPrecipitação: {}\nUmidade: {}\nVento: {}'
  .format(pre['loc'],pre['time'],pre['max'],pre['min'],pre['temp'],pre['cond'],pre['prec'],pre['humi'],pre['wind']))
  for i in range(1,8):
    print('/--------{}--------/'.format(pre['weekday'+str(i)]))
    print('Condição: {}'.format(pre['cond'+str(i)]))
    print('Máxima: {}'.format(pre['max'+str(i)]))
    print('Mínima: {}'.format(pre['min'+str(i)]))
"""
beautifulsoup4==4.9.3
bs4==0.0.1
certifi==2020.12.5
chardet==4.0.0
idna==2.10
selenium==3.141.0
soupsieve==2.2
urllib3==1.26.4
"""
