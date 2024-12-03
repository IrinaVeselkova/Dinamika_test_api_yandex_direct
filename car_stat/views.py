import time
import urllib
from datetime import datetime

import requests
import json
from django.shortcuts import render
from .models import *
from openpyxl import Workbook
from django.http import HttpResponse

YANDEX_API_URL = "https://api-sandbox.direct.yandex.ru/v4/json/"
HEADERS = {
    "Content-Type": "application/json; charset=utf-8",

}


def collect_data(request):
    brands = CarBrand.objects.all()
    regions = Region.objects.all()
    phrases = QueryType.objects.all()
    query_text = [phrase.query_template.replace("[марка]", brand.name) for brand in brands for phrase in phrases]
    geo_id = [int(region.name) for region in regions]
    data = {
        "token": "y0_AgAAAABGQP9eAAzZHAAAAAEaDXZEAACS3VdzyyFKaJF6g9HxtE_-jk86yg",
        "method": "CreateNewWordstatReport",
        "param": {
            "Phrases": query_text,
            "GeoID": geo_id
        }
    }
    response = requests.post(YANDEX_API_URL, headers=HEADERS, data=json.dumps(data, ensure_ascii=False).encode("utf8"))
    print(f"Body: {json.dumps(data, ensure_ascii=False)}")
    print(f"Статус-код: {response.status_code}")
    print(f"Статус-текст: {response.content}")
    if response.status_code == 200:
        report_id = response.json().get("data", {})
        print(report_id)
        if not report_id:
            print("Нет данных в отчете.")
            return

        #status_response = requests.post(
            #YANDEX_API_URL,
            #headers=HEADERS,
            #data=json.dumps({"token": "y0_AgAAAABGQP9eAAzZHAAAAAEaDXZEAACS3VdzyyFKaJF6g9HxtE_-jk86yg",
                             #"method": "GetWordstatReportList", "param": {}})
        #)
        
        #print(status_response)
        data = {
                    "token": "y0_AgAAAABGQP9eAAzZHAAAAAEaDXZEAACS3VdzyyFKaJF6g9HxtE_-jk86yg",
                    "method": "GetWordstatReport",
                    "param": report_id,
                }
        #print(data)
        #Ждем, когда будет готов отчет
        time.sleep(20)
        report_response = requests.post(YANDEX_API_URL, data=json.dumps(data, ensure_ascii=False).encode("utf8"))
        print(report_response.json())
        # Сохранение данных в базу
        for item in report_response.json().get("data", {}):
            #print(item)
            phrase = item['Phrase']
            geo = (int(i) for i in item['GeoID'])
            QueryResult.objects.create(
                    region=item['GeoID'],
                    car_brand=CarBrand.objects.get(name = phrase[:phrase.find(" ")]),
                    query_text=phrase,
                    count=item['SearchedWith'][0]["Shows"]
                )
    else:
        print(f"Ошибка создания отчёта: {response.status_code}, {response.text}")
def export_to_excel():
    results = QueryResult.objects.all()
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Статистика запросов"
    sheet.append(["Регион", "Бренд", "Запрос", "Количество запросов"])

    for result in results:
        sheet.append([result.region, result.car_brand.name, result.query_text, result.count])
    file_name = f"wordstat_results_{str(datetime.now())}.xlsx"
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={file_name}'
    workbook.save(response)
    return response


def index_view(request):
    if request.method == "POST":
        if "collect" in request.POST:
            collect_data(request)
        if "export" in request.POST:
            return export_to_excel()

    return render(request, "car_stat/index.html")
