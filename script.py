from flask import Flask
from flask import render_template
import urllib
import requests
import re

app = Flask(__name__)

airports = [
    "EPWR",
    "KMLJ",
    "K1NM",
    "GQNO",
    "LFLU",
    "CZSM",
    "KFDK",
    "KEKQ",
    "EGAA",
    "CZOL",
    "FXMM",
    "KCEU",
    "LFBM",
    "FJDG",
    "FWKI",
    "YPLM",
    "LFBU",
    "KTVI",
    "KAAO",
    "K06C",
    "YPXM",
    "MHPL",
    "K1LM",
    "KPXE",
    "SBAQ",
    "KLUK",
    "KSGR",
    "KSSC",
    "OPIS",
    "KSPG"
]

#Регулярные выражения для выбора нужных параметров
match_wind = re.compile(r'Wind: .* at (\d*) MPH')
match_humidity = re.compile(r'Relative Humidity: ([\d]*)%')
match_pressure = re.compile(r'Pressure \(altimeter\):.*\(([\d]*) hPa\)')

#Сюда будут записываться предупреждения о погодных условиях
warn = []

#Формирование сообщения с предупреждением по триггерам
def air_warning(a, wind, hum, pres):
    if (wind >= 15):
        warn.append('\n' + a + ': wind speed ' + str(wind) + 'MPH')
    if (hum >= 70):
        warn.append('\n' + a + ': humidity ' + str(hum) + '%')
    if (pres >= 1016):
        warn.append('\n' + a + ': relative pressure' + str(pres) + ' hPa')

#Получение данных
def get_data():
    for a in airports:
        link = 'http://tgftp.nws.noaa.gov/data/observations/metar/decoded/' + a + '.TXT'
        res = requests.get(link).text

        data_wind = match_wind.search(res)
        data_humidity = match_humidity.search(res)
        data_pressure = match_pressure.search(res)

        wind = 0
        if (data_wind != None):
            wind = data_wind.group(1)
        hum = 0
        if (data_humidity != None):
            hum = data_humidity.group(1)
        pres = 0
        if (data_pressure != None):
            pres = data_pressure.group(1)

        air_warning(a, int(wind), int(hum), int(pres))

#Полученный список предупреждений передается в html-шаблон
@app.route('/')
def homepage():
    get_data()
    return render_template('index.html', warn = warn)

app.run('localhost', port=8000)
