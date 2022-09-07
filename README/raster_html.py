import os
import sys
#
from bs4 import BeautifulSoup
from selenium import webdriver
from Lib.weasyprint import HTML
from pyvirtualdisplay import Display
import time
#
def raster_readme():
	#
	#
	bs = BeautifulSoup
	#
	dir_path = os.path.dirname(os.path.realpath(__file__))
	#
	_addon_location = dir_path+'/addons'
	_gecko = _addon_location+'/geckodriver-v0.15.0-linux64/geckodriver'
	#
	data_final_results = []
	#
	profile = webdriver.FirefoxProfile()
	#
	display = Display(visible=0, size=[1600, 600])
	display.start()
	#
	driver = webdriver.Firefox(firefox_profile=profile, executable_path=_gecko)
	#
	css_file = os.path.join(dir_path, 'assets/css/'+'style'+'.css')
	css_file_pdf = os.path.join(dir_path, 'assets/css/'+'pdf'+'.css')
	#
	print("STARTED Schedule Rasterize")
	#
	local_url = 'file://'+os.path.join(dir_path,'README_raster.html')
	#
	driver.get(local_url)
	#
	time.sleep(2)
	#
	html = driver.page_source
	#
	html = str(html)
	#print(html)
	#
	soup = bs(html, "html.parser")
	#
	html_pretty = str(soup.prettify())
	#
	doc = HTML(string=html_pretty, base_url=dir_path ).render(stylesheets=[css_file_pdf, css_file])
	#
	output = os.path.join(dir_path,'README_raster.pdf')
	doc.write_pdf(output)
	#
	os.remove(os.path.join(dir_path,'README_raster.html'))
	#
	driver.quit()
	#
#
raster_readme()
#