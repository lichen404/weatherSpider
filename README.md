## weatherSpider
爬取天气后报网站（www.tianqihoubao.com/weather/city.aspx） 上从2011年至今的历史天气数据，并使用MongoDB进行数据存储，pyecharts进行数据分析和展示.
## usage
python spider.py -c 城市拼音名   #爬取数据到MonogoDB数据库

python create_htm.py   #在代码文件夹目录生成相关图表，可以自己调整

python get_url_list #获取所有城市对应的url以及城市名称，爬取的内容我以dict的形式放在了config.py,避免反复爬取.





## example
python spider.py  -c  "zhengzhou"  #爬取并存储郑州市2011年至2019年3月的天气数据

![爬虫运行](https://www.stayw1thme.xyz/usr/uploads/2019/04/3484431250.png)

郑州2011年至今气温变化

![气温变化](https://www.stayw1thme.xyz/usr/uploads/2019/04/2697402371.png
)

郑州历史天气占比

![郑州历史天气占比](https://www.stayw1thme.xyz/usr/uploads/2019/04/2345370710.png)

郑州历年晴雨天总数

![郑州历年晴雨天总数](https://www.stayw1thme.xyz/usr/uploads/2019/04/1015283070.png)

郑州六月天气词云
![六月天气词云](https://www.stayw1thme.xyz/usr/uploads/2019/04/1615476831.png)