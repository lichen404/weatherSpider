#返回到19年3月的郑州天气URL
def get_url_list(city):
	url_temp='http://www.tianqihoubao.com/lishi/{0}/month/{1}.html'
	month_list=['01','02','03','04','05','06','07','08','09','10','11','12']

	url_list=[]
	for x in month_list:
		for y in range(8):
			url_list.append(url_temp.format(city,str(2011+y)+x))
	for x in month_list[0:3]:
		url_list.append(url_temp.format(city,'2019'+x))
	return url_list
