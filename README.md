# Instagram Bot

## Requerimientos:

    - Python3, pip: https://installpython3.com/
    - Selenium: pip install -U selenium
    - Google Chrome
    - Brave Browser
    - Google Chrome Driver (necesario para Selenium): https://chromedriver.chromium.org/downloads
      Nota: depende de la versión de chrome que tengas, actual v89 (ver en las settings de google chrome, puede ser 87, 88, 89, 90...)
    - Estar registrado con la misma cuenta (mail+password) en cada uno de los sitios debajo (validSites)
    - (recomendado) una VPN com oAVG VPN, que permite cambiar la IP de la máquina

## Ejecución:

    - Una vez instalado  python3, pip, selenium y descargado Chrome Driver, copiar este último a
      una carpeta. Ejemplo:/tmp/chromedriver.v89.exe (será sin extensión en linux, dar permisos +x)
      Luego llamar al script

## Comando para llamar al script

    python3 instagramBot.py -u username -p password -q googleDriverPath+File - browserPathANdFile
    python3 instagramBot.py -u zaraza -p zaraza -g c:\\temp\\chromedriver.v92.exe -b "C:\\Program Files (x86)\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
    python3 instagramBot.py -u zaraza -p zaraza -g c:\\temp\\chromedriver.v92.exe -b "C:\Program Files (x86)\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"

---

## Referencias

- js executor: https://stackoverflow.com/questions/7263824/get-html-source-of-webelement-in-selenium-webdriver-using-python
