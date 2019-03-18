## weatherSpider
爬取天气后报网站（www.tianqihoubao.com/weather/city.aspx）上的历史天气数据，并使用MongoDB进行数据存储，pyecharts进行数据分析和展示.
## usage
python spider.py -c 城市拼音名
## example
python spider.py  -c  "zhengzhou"

爬取并存储郑州市2011年至2019年3月的天气数据，在项目目录生成数据展示页面。


![郑州2011年至今气温变化](https://www.stayw1thme.xyz/usr/uploads/2019/03/1201606047.png)

![郑州历史天气占比](https://www.stayw1thme.xyz/usr/uploads/2019/03/226720097.png)

![郑州历年晴雨天总数](https://www.stayw1thme.xyz/usr/uploads/2019/03/3354371723.png)
