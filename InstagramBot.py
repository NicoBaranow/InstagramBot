# Python script to comment on Instagram Posts
#
# requirements:
#    - Python3, pip: https://installpython3.com/
#    - Selenium: pip install -U selenium
#    - Google Chrome
#    - Google Chrome Driver: https://chromedriver.chromium.org/downloads
#      note: check that the Google Chrome Driver and Brave Browser have the same version


# Execution:
#    - Once python3, pip, selenium and Google Chrome Driver are downloaded, copy the Google Chrome Driver to a folder
#      Then, call the script
#
# How to call the script:
#   Execute on a termial:
#   python3 instagramBot.py -t postname -u username -p password -q googleChromeDriverPath+File - browserPath+File
#   python3 instagramBot.py -t CR1panuC2W7 -u YourUsername -p YourPassword -g c:\\temp\\chromedriver.v92.exe -b "C:\\Program Files (x86)\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
#

import time
from datetime import datetime
from datetime import date
import os.path

import os
import sys
import getopt

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

logsFolder = './logs'
statsFolder = './stats'

def getInputParams(argv):
  user = ''
  password = ''
  googledriver = ''
  bravepath = ''
  postname = ''

  try:
    opts, args = getopt.getopt(argv,"ht:u:p:g:b:",["tpostname=", "uusername=","ppassword=", "ggoogledriver", "bbravepath"])
  except getopt.GetoptError:
    print ('Number of arguments: ' + str(len(sys.argv)) +  ' arguments.')
    print ('Argument List: ' + str(sys.argv))
    print ('instagramBot.py -t <postname> -u <username> -p <password> -g <googledriver> -b <bravepath>')
    sys.exit(2)

  for opt, arg in opts:
    if opt == '-h':
      print ('instagramBot.py -u <username> -p <password> -g <googledriver>')
      sys.exit()
    elif opt in ("-t", "--postname"):
      postname = arg
    elif opt in ("-u", "--uusername"):
      user = arg
    elif opt in ("-p", "--ppassword"):
      password = arg
    elif opt in ("-g", "--ggoogledriver"):
      googledriver = arg
    elif opt in ("-b", "--bbravepath"):
      bravepath = arg

  if (len(sys.argv) == 1):
      print ("Error: Tiene que pasar un argumento con postname, usuario, contraseña, ruta+archivo de google chrome driver y de Google Chrome", '\n')
      print ('instagramBot.py -t <postname> -u <username> -p <password> -g <googledriver> - b <ChromePath>', '\n')
      print ('Ejemplo: python3 instagramBot.py -t CR1panuC2W7 -u pepe@gmail.com -p strongP1ssw4rd -g c:\\temp\\chromedriver.v89.exe -b C:\\Program Files (x86)\\BraveSoftware\\Brave-Browser\\Application\\brave.exe')
      print('Descargar google chrome diver (no es el browser) aquí: https://chromedriver.chromium.org/downloads')
      print('\n')
      sys.exit()
  elif (len(postname) == 0):
      print ('Error: parámetro postname no válido')
      sys.exit()
  elif (len(user) == 0):
      print ('Error: parámetro usuario no válido')
      sys.exit()
  elif (len(password) == 0):
      print ('Error: parámetro password no válida')
      sys.exit()
  elif (len(googledriver) == 0 or not os.path.isfile(googledriver)):
      print ('Error: parámetro path y archivo de google chrome driver no válido')
      sys.exit()
  elif (len(bravepath) == 0 or not os.path.isfile(bravepath)):
      print ('Error: parámetro path y archivo de Browser Brave no válido')
      sys.exit()

  return postname, user, password, googledriver, bravepath

def getError(e):
  try:
    # https://stackoverflow.com/questions/33239308/how-to-get-exception-message-in-python-properly
    error = getattr(e, 'message', repr(e))
    return error
  except:
    return ''


def log(msg):
  date = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

  data = date+': '+msg
  filename = logsFolder+'/bot.log'

  print(data)

  with open(filename, "a+") as flog:
    flog.write(data+'\n')
    flog.close()


def getDriver(chromeDriverPath, bravePath):
  d = DesiredCapabilities.CHROME
  d['goog:loggingPrefs'] = { 'browser':'ALL' }

  option = webdriver.ChromeOptions()

  option.add_argument('log-level=3')
  option.add_argument("disable-popup-blocking")
  option.add_argument('start-maximized')
  option.add_argument('disable-infobars')
  option.add_experimental_option('excludeSwitches', ['enable-automation'])
  option.add_experimental_option('excludeSwitches', ['enable-logging'])
  option.add_experimental_option('useAutomationExtension', False)

  option.binary_location = bravePath
  driver = webdriver.Chrome(executable_path=chromeDriverPath, options=option, desired_capabilities=d)
  return driver

def getLastCommentsDayFileName(postName):
  try:
    xdate = date.today()
    year = str(xdate.year)
    month = str(xdate.month).zfill(2)
    day = str(xdate.day).zfill(2)

    return statsFolder+'/'+postName+'/'+year+month+day
  except Exception as e:
    log('Error en getLastCommentsDayFileName: ' + getError(e))


def getLastCommentsDayCounter(postName):
  try:
    fileName = getLastCommentsDayFileName(postName)
    fileExists = os.path.exists(fileName)
    lastCommentsDayounter = 0

    if (fileExists):
      with open(fileName, 'r') as flast:
        Lines = flast.readlines()
        for line in Lines:
            lastCommentsDayounter = int(line.strip())
      flast.close()

    return lastCommentsDayounter

  except Exception as e:
    log('Error en getLastCommentsDayCounter: ' + getError(e))


def saveLastCommentsDayCounter(postName):
  try:
    fileName = getLastCommentsDayFileName(postName)
    lastCommentsDayCounter = getLastCommentsDayCounter(postName)

    with open(fileName, 'w') as flast:
      flast.write(str(lastCommentsDayCounter+1))

  except Exception as e:
    log('Error en saveLastCommentsDayCounter: ' + getError(e))


def getLastCommentsHourFileName(postName):
  try:
    xdate = date.today()
    year = str(xdate.year)
    month = str(xdate.month).zfill(2)
    day = str(xdate.day).zfill(2)
    hour = str(datetime.now().hour).zfill(2)

    return statsFolder+'/'+postName+'/'+year+month+day+hour
  except Exception as e:
    log('Error en getLastCommentsHourFileName: ' + getError(e))


def getLastCommentsHourCounter(postName):
  try:
    fileName = getLastCommentsHourFileName(postName)
    fileExists = os.path.exists(fileName)
    lastCommentsHourCounter = 0

    if (fileExists):
      with open(fileName, 'r') as flast:
        Lines = flast.readlines()
        for line in Lines:
            lastCommentsHourCounter = int(line.strip())
      flast.close()

    return lastCommentsHourCounter

  except Exception as e:
    log('Error en getLastCommentsHourCounter: ' + getError(e))


def saveLastCommentsHourCounter(postName):
  try:
    fileName = getLastCommentsHourFileName(postName)
    lastCommentsHourCounter = getLastCommentsHourCounter(postName)

    with open(fileName, 'w') as flast:
      flast.write(str(lastCommentsHourCounter+1))

  except Exception as e:
    log('Error en saveLastCommentsHourCounter: ' + getError(e))


def getPostFileName(postName):
  try:
    folderName = statsFolder+'/'+postName
    fileName = folderName+'/'+postName
    return fileName

  except Exception as e:
    log('Error en getPostFileName: ' + getError(e))


def saveWhoComment(postName, user):
  try:
    fileName = getPostFileName(postName)
    with open(fileName, 'a') as flast:
        flast.write(str(user)+'\n')

  except Exception as e:
    log('Error en saveLastCommentsCounter: ' + getError(e))


def userAlreadyCommentInPost(postName, user):
  try:
    fileName = getPostFileName(postName)
    fileExists = os.path.exists(fileName)

    if (fileExists):
      with open(fileName) as myfile:
        return user in myfile.read()

  except Exception as e:
    log('Error en userAlreadyCommentInPost: ' + getError(e))

  return False


def exceedsLimits(postName):
  hourLimits = 45
  dayLimits = 960
  currentHourCounter = getLastCommentsHourCounter(postName)
  currentDayCounter = getLastCommentsHourCounter(postName)
  return (currentHourCounter+1 > hourLimits or currentDayCounter+1 > dayLimits)


def makeComment(driver, user):
  try:
    # comment
    textBox = driver.find_elements_by_xpath("//textarea[contains(@class, 'Ypffh')]")
    time.sleep(15) # to avoid error element is not interactable
    textBox[0].click()
    time.sleep(3)
    textBox[0].clear()
    time.sleep(3)
    textBox[0].send_keys(user)
    time.sleep(2)
    textBox[0].send_keys(Keys.ENTER)
    time.sleep(2)
    textBox[0].send_keys(Keys.RETURN)
    time.sleep(2)
    textBox[0].send_keys('\n')
    time.sleep(40) # wait to comment

    try:
      driver.refresh() # por error al comentar, habilitación del campo
      time.sleep(10)
    except:
      pass
    #publicar = driver.find_elements_by_xpath("//button[contains(@class, 'sqdOP yWX7d    y3zKF     ')]")
    #time.sleep(3)
    #publicar[0].click()
    return True
  except Exception as e:
    log('Error makeComment with user ' + user + ': ' + getError(e))
  return False


def commentSpam(postName, driver, allowRepeated):
  try:
    log ('commentSpam ...')

    usersSent = [""]
    counter = 0

    with open('randomAccounts.txt', newline='\n') as f:
      Lines = f.readlines()
      accountsList = list(Lines)

    log('getting link ...')
    link = 'https://www.instagram.com/p/'+postName+'/'
    driver.get(link)
    time.sleep(5)
    
    while (not exceedsLimits(postName) and counter < len(accountsList)):
      try:
        user = accountsList[counter].strip().replace('\n', '')
        log('starting to comment with user : ' + user)

        # [1:]: Elimino el '@' del usuario dato que en followers y followings está sin ese caracter
        
        blockedToComment = (not allowRepeated and userAlreadyCommentInPost(postName, user))



        if (blockedToComment):
          log('El usuario : ' + user + " ya comentó en éste post")

        if (not blockedToComment):
          if (makeComment (driver, user)):
            usersSent.append(user)
            log ('user ' + user + ' comentó en el post !!')
            saveLastCommentsHourCounter(postName)
            saveLastCommentsDayCounter(postName)
            saveWhoComment(postName, user)
            time.sleep(5)

      except Exception as e:
        log('Se omite usuario ' + user + ' por error ' + getError(e))
        time.sleep(2)
        pass

      counter += 1

  except Exception as e:
    log('CommentSpam error ' + getError(e))
    pass

# def getFollowers(driver, username):
#   try:
#     log('Getting followers ...')

#     driver.get("https://www.instagram.com/"+username)
#     driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').click() #clicks followers
#     time.sleep(1)

#     scroll_div = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]') #caja donde scrolleo
#     previous_height = 0
#     current_height = 1

#     while previous_height != current_height:
#       previous_height = current_height
#       current_height = driver.execute_script('arguments[0].scrollTo(0, arguments[0].scrollHeight); return arguments[0].scrollHeight;', scroll_div)
#       time.sleep(1)

#     links = scroll_div.find_elements_by_tag_name('a')
#     names = [name.text for name in links if name.text != '']

#     driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/div[2]/button').click() #close button
#     log('followers: ' + ','.join(names))
#     return names

#   except Exception as e:
#     log('getFollowers error ' + getError(e))
#     pass
#     return []


# def getFollowings(driver, username):
#   try:
#     log('Getting followings ...')

#     driver.get("https://www.instagram.com/"+username)

#     driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a').click() #clicks following
#     time.sleep(1)

#     scroll_div = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]') #caja donde scrolleo
#     previous_height = 0
#     current_height = 1

#     while previous_height != current_height:
#       previous_height = current_height
#       current_height = driver.execute_script('arguments[0].scrollTo(0, arguments[0].scrollHeight); return arguments[0].scrollHeight;', scroll_div)
#       time.sleep(1)

#     links = scroll_div.find_elements_by_tag_name('a')
#     names = [name.text for name in links if name.text != '']

#     driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/div[2]/button').click() #close button
#     log('followings: ' + ','.join(names))
#     return names

#   except Exception as e:
#     log('getFollowings error ' + getError(e))
#     pass
#     return []


def disableAlerts(driver):
  try:
    element = driver.find_elements_by_xpath("//button[contains(@class, 'aOOlW   HoLwm ')]")
    if (element):
      time.sleep(2)
      element[0].click()

  except Exception as e:
    log('disableAlerts error ' + getError(e))
    pass


def login(username, password, driver):
  try:

    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(5) # esperar a que la página se muestre

    username_element = driver.find_element_by_xpath("//input[@name=\"username\"]")
    username_element.send_keys(username)

    password_element = driver.find_element_by_xpath("//input[@name=\"password\"]")
    password_element.send_keys(password)
    
    login_button = driver.find_element_by_xpath('//button[@type="submit"]')
    login_button.click()
    
    time.sleep(10) # Esperar fin login

    return True

  except Exception as e:
    log('login error ' + getError(e))
    return False


def process (user, password, postName, chromeDriverPath, bravePath):
  while True:
    log('Starting to process with post ' + postName + ' ...')
    driver = getDriver(chromeDriverPath, bravePath)

    try:
      if (login(user, password, driver)):
        if (not exceedsLimits(postName)):
          disableAlerts(driver) # eliminar alertas de notificación
          # followings = getFollowings(driver, user)
          # followers = getFollowers(driver, user)
          commentSpam(postName, driver, False)
        else:
          log('Se excede límite de comentarios, esperando 1 hora ...')
          time.sleep(1800)
    except Exception as e:
      log('Se omite repetición de proceso por error ' + getError(e))
      pass
      
    # https://www.zyxware.com/articles/5552/what-is-close-and-quit-commands-in-selenium-webdriver
    driver.quit()
    log('Esperando 1 minuto ...')
    time.sleep(60) 


def getPosts():
  try:
    with open('posts.txt', newline='\n') as fPosts:
      Lines = fPosts.readlines()
      return list(Lines)
  except Exception as e:
    log('Error getPosts: ' + getError(e))

  return []

def main(argv): # Start here!
  if not os.path.exists(logsFolder):
    os.makedirs(logsFolder)
  if not os.path.exists(statsFolder):
    os.makedirs(statsFolder)

  postName, username, password, chromeDriverPath, bravePath = getInputParams(argv)

  if not os.path.exists(statsFolder+'/'+postName):
    os.makedirs(statsFolder+'/'+postName)

  process(username, password, postName, chromeDriverPath, bravePath)


if __name__ == "__main__":
  main(sys.argv[1:])