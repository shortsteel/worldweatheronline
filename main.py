import datetime
import json

import requests
from dateutil.relativedelta import relativedelta

# make csv using json result using command:
# cat weather.json | jsoncsv -A | mkexcel > weather.csv

if __name__ == '__main__':
    start_date = datetime.datetime(2021, 1, 1)
    today = datetime.datetime.today()
    out_file_name = 'weather.json'

    current_date = start_date
    result = []
    while current_date + relativedelta(day=31) <= today:
        first_day_of_month = current_date.replace(day=1)
        last_day_of_month = current_date + relativedelta(day=31)
        res = requests.get(
            'https://api.worldweatheronline.com/premium/v1/past-weather.ashx',
            params={
                'key': 'bb2fd95f9c0d4a1cb86143432220105',
                'format': 'json',
                'q': 'Lushan',
                'date': first_day_of_month.strftime('%Y-%m-%d'),
                'enddate': last_day_of_month.strftime('%Y-%m-%d')
            })
        weather_month_data = res.json()['data']['weather']
        for weather_day_data in weather_month_data:
            date_str = weather_day_data['date']
            for weather_hour_data in weather_day_data['hourly']:
                weather_hour_data['date'] = date_str
                result.append(weather_hour_data)

        current_date = current_date + relativedelta(months=1)

    with open(out_file_name, 'w') as outfile:
        outfile.write(json.dumps(result))

# print(start_date)
# start_year = 2021
# start_month = 8
# end_year = 2022
# end_month = 4
#
# response = requests.get(
#     'https://api.worldweatheronline.com/premium/v1/past-weather.ashx',
#     params={'key': 'bb2fd95f9c0d4a1cb86143432220105', 'format': 'json', 'q': 'Lushan', 'date': '2020-01-01',
#             'enddate': '2022-04-30'})
# print(response.json()['data']['weather'])
# ?key=bb2fd95f9c0d4a1cb86143432220105&q=Lushan&format=json&date=2020-01-01&enddate=2022-04-30'

#
# class WeatherRow(scrapy.Item):
#     date = scrapy.Field()
#     time = scrapy.Field()
#     temperature = scrapy.Field()
#     forecast = scrapy.Field()
#     rain = scrapy.Field()
#     rain_percent = scrapy.Field()
#     cloud = scrapy.Field()
#     pressure = scrapy.Field()
#     wind = scrapy.Field()
#     gust = scrapy.Field()
#     direction = scrapy.Field()

#
# class WeatherSpider(scrapy.Spider):
#     name = 'world weather online'
#     start_urls = ['https://www.worldweatheronline.com/lushan-weather-history/henan/cn.aspx']
#
#     def parse(self, response, **kwargs):
#         for row in response.css('.city-hourly-weather')[0].css('.days-details-row'):
#
#             row_items = row.css('.days-details-row-item')
#             if len(row_items) > 0:
#                 weather_row = WeatherRow()
#                 weather_row['date'] = ''
#                 weather_row['time'] = row_items[0].css('.days-comment::text').get()
#                 weather_row['temperature'] = row_items[0].css('.days-temp::text').get()
#                 weather_row['forecast'] = row_items[2].css('.days-table-forecast-p::text').get()
#                 weather_row['rain'] = row_items[3].css('.days-rain-number::text').get()
#                 weather_row['rain_percent'] = row_items[4].css('::text').get()
#                 weather_row['cloud'] = row_items[5].css('::text').get()
#                 weather_row['pressure'] = row_items[6].css('::text').get()
#                 weather_row['wind'] = row_items[7].css('.days-wind-number::text').get()
#                 weather_row['gust'] = row_items[8].css('.days-wind-number::text').get()
#                 weather_row['direction'] = row_items[9].css('.days-arrow').xpath('@style').extract()
#                 yield weather_row
