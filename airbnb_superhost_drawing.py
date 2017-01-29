# -*- coding: utf-8 -*-

import json
import os
import pandas
import matplotlib.pyplot as plt


def read_profile():
    file_in = open('./Data/Superhost/Profile_Super.txt')
    superhost_list_tmp = file_in.read().split('\n')
    superhost_list = []
    for superhost in superhost_list_tmp:
        if superhost != '':
            superhost_list.append(superhost.split('\t'))
    return superhost_list


def draw_map():
    superhost_list = read_profile()
    city = dict()
    country = dict()
    for superhost in superhost_list:
        user_id = superhost[0]
        if not os.path.exists('./Data/Superhost/Location/' + user_id + '.json'):
            continue
        with open('./Data/Superhost/Location/' + user_id + '.json', 'r') as f:
            geo = json.load(f)
        if geo.has_key('country'):
            country[geo['country']] = country.get(geo['country'], 0) + 1
            if geo.has_key('city'):
                city[geo['city'] + '(' + geo['country'] + ')'] = city.get(geo['city'] + '(' + geo['country'] + ')', 0) + 1
    city_list = [['City', 'Super hosts']]
    for k, v in city.items():
        city_list.append([k, v])
    country_list = [['Country', 'Super hosts']]
    for k, v in country.items():
        country_list.append([str(k), v])
    print(len(city_list))
    html_city = '''<html>
  <head>
    <script type='text/javascript' src='https://www.gstatic.com/charts/loader.js'></script>
    <script type='text/javascript'>
     google.charts.load('upcoming', {'packages': ['geochart']});
     google.charts.setOnLoadCallback(drawMarkersMap);

      function drawMarkersMap() {
      var data = google.visualization.arrayToDataTable(''' + str(city_list) + ''');

      var options = {
        displayMode: 'markers',
        colorAxis: {colors: ['#FFCED0', '#fd5c63']}
      };

      var chart = new google.visualization.GeoChart(document.getElementById('chart_div'));
      chart.draw(data, options);
    };
      download(chart.getImageURI(), 'city.png', "image/png");
    </script>
  </head>
  <body>
    <div id="chart_div" style="width: 1300px; height: 600px;"></div>
  </body>
</html>'''
    html_city = html_city.replace("u'", "'").replace('u"', '"')
    with open('./Result/superhost_city_map.html', 'w') as f:
        f.write(html_city)
    city_data = pandas.DataFrame(city.items(), columns=['city', 'quantity'])
    country_data = pandas.DataFrame(country.items(), columns=['country', 'quantity'])
    city_data = city_data.sort(columns='quantity', ascending=False)
    country_data = country_data.sort(columns='quantity', ascending=False)
    ax = city_data[0:9].plot(x='city', y='quantity', kind='barh', color='black')
    ax.set_xlabel('Superhost quantity')
    ax.set_ylabel('Cities')
    ax.set_title('Top 10 Superhost cities')
    ax.legend().set_visible(False)
    plt.tight_layout()
    plt.savefig('./Result/top_10_superhost_cities.eps')
    plt.close()
    ax = country_data[0:9].plot(x='country', y='quantity', kind='bar', color='black')
    ax.set_xlabel('Countries')
    ax.set_ylabel('Superhost quantity')
    ax.set_title('Top 10 Superhost countries')
    ax.legend().set_visible(False)
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig('./Result/top_10_superhost_countries.eps')
    plt.close()


if __name__ == '__main__':
    if not os.path.exists('./Result'):
        os.mkdir('./Result')
    draw_map()
