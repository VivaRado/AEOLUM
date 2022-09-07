#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import os
import sys
import glob
import re
import time
#from bs4 import BeautifulSoup
from shutil import copyfile
from Lib.weasyprint import HTML
from Lib.weasyprint.document import Document, Page  # noqa

import pprint
import datetime
import operator
import collections
#from collections import Iterable
from Lib.pdf_common import make_bookmark_tree_b
from Lib.pdf_common import *
from Lib.md_common import *
from Lib.generic_tools import *
#
from argparse import ArgumentParser
#
rasterize = False
#
from bs4 import BeautifulSoup as bs
#
#if rasterize == True:
	
from selenium import webdriver
from pyvirtualdisplay import Display

#
dir_path = os.path.dirname(os.path.realpath(__file__))
up_dir = os.path.abspath(os.path.join(dir_path, '..'))
#
css_file = os.path.join(dir_path, 'assets/css/'+'pdf'+'.css')
css_file_cover = os.path.join(dir_path, 'assets/css/'+'pdf_cover'+'.css')
css_file_contents = os.path.join(dir_path, 'assets/css/'+'pdf_contents'+'.css')
#
project_name = up_dir.rsplit('/', 1)[1]
gen_date = datetime.datetime.today().strftime('%Y/%m/%d')
version = open(os.path.join(dir_path,'version'),'r').read()
#

#
bookmark_override = make_bookmark_tree_b
Document.make_bookmark_tree = bookmark_override
make_bookmark_tree = bookmark_override

#
dir_path = os.path.dirname(os.path.realpath(__file__))
#
#
parser = ArgumentParser()
parser.add_argument("-f", "--format", dest="format",
                    help="Export Format: comma separated")
parser.add_argument("-v", "--volume", dest="volume",
                    help="Export Volume: V0 or V1")
#
args = parser.parse_args()
#
langs = ["en"]
#
def rasterize_html(html_path, lang):
	#
	#
	#
	#dir_path = os.path.dirname(os.path.realpath(__file__))
	#
	_addon_location = dir_path+'/addons'
	_gecko = _addon_location+'/geckodriver-v0.26.0-linux64/geckodriver'
	#
	temp_html = open(html_path, "r")
	html_data = temp_html.read()
	#
	book_path_rasterizeable = os.path.join(dir_path,"README_rasterizeable_"+lang+".html")
	#
	new_data = combine_header(html_data, '', True)
	newfile = open(book_path_rasterizeable, "w")
	newfile.write(new_data)
	#
	newfile.close()
	#
	data_final_results = []
	#


	profile = webdriver.FirefoxProfile()
	#
	#display = Display(visible=0, size=[1200, 600])
	#display.start()
	#
	driver = webdriver.Firefox(firefox_profile=profile, executable_path=_gecko)
	#
	css_file = os.path.join(dir_path, 'assets/css/'+'style'+'.css')
	css_file_pdf = os.path.join(dir_path, 'assets/css/'+'pdf'+'.css')
	#
	print("STARTED Rasterize")
	#
	local_url = 'file://'+book_path_rasterizeable#os.path.join(dir_path,'README_raster.html')
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
	#soup = bs(html_pretty, "html.parser")
	#

	#
	div = soup.find('article', id='body')
	contents = ''.join(map(str, div.contents))
	#body_content = str(body.findChildren())
	#
	doc = HTML(string=contents, base_url=dir_path ).render(stylesheets=[css_file_pdf, css_file])
	#
	#print(doc)
	output = os.path.join(dir_path,'README_rasterized_'+lang+'.html')
	rasfile = open(output, "w")
	rasfile.write(contents)
	
	#doc.write_pdf(output)
	#
	#os.remove(os.path.join(dir_path,'README_raster.html'))
	#os.remove(os.path.join(dir_path,lang,'md_temp.html'))
	#
	driver.quit()
	#
	#
	return contents
	#
#
def make_multilingual_html(langs, title):
	#
	lang_contents = []
	lang_comb_path = os.path.join(dir_path,"README.html")
	#
	for z in langs:
		#
		lang_path = os.path.join(dir_path,"README_"+z+".html")
		#
		local_url = 'file://'+lang_path#os.path.join(dir_path,'README_raster.html')
		#
		soup = bs(open(lang_path), "html.parser")
		#
		#html = driver.page_source
		#
		#html = str(html)
		#
		#soup = bs(html, "html.parser")
		#
		#prettyHTML = soup.prettify()
		div = soup.find('article', id='body')
		contents = ''.join(map(str, div.contents))
		#body_content = str(body.findChildren())
		#
		lang_contents.append('<div data-language="'+z+'">'+contents+'</div>')
		#
	#
	lang_str = ''
	#
	for x in lang_contents:
		#
		lang_str = lang_str + x
		#
	#
	new_data_ml = combine_header(lang_str, str(title), False)
	newfile_ml = open(lang_comb_path, "w")
	newfile_ml.write(new_data_ml)
	#
	newfile_ml.close()
	#
	#
#
def formats(_f, _err):
	#
	gen_formats = []
	#
	supported_f = ["pdf","md","html"]
	#
	if ',' in _f:
		#
		gen_formats = _f.split(',')
		#
	else:
		#
		gen_formats = [_f]
		#
	#
	for x in gen_formats:
		#
		if x not in supported_f:
			#
			_err = True
			#
			print('=\n=> Please Provide Supported Formats: '+x+' is not Supported. Supported Formats: '+','.join(supported_f)+'\n=')	
			#
		#
	#
	return [gen_formats, _err]
	#
#
def volumes(_f, _err):
	#
	gen_volumes = []
	#
	supported_v = ["M0","M1", "L0"]
	#
	if ',' in _f:
		#
		_err = True
		#
		print('=\n=> Please Provide Supported Volumes: '+x+' is not Supported. Supported Volumes: '+','.join(supported_v)+'\n=')	
		#
	else:
		#
		if _f not in supported_v:
			#
			_err = True
			#
			print('=\n=> Please Provide Supported Volumes: '+_f+' is not Supported. Supported Volumes: '+','.join(supported_v)+'\n=')	
			#
		else:
			#
			gen_volumes = [_f]
			#
		#
	#
	#
	return [gen_volumes, _err]
	#
#

faults = False
#
if  args.format is None:
	#
	faults = True
	#
	print('=\n=> Please Provide Export Format: -f "pdf,md,html"\n=')	
	#
#
if  args.volume is None:
	#
	faults = True
	#
	print('=\n=> Please Provide Export Volume: -v "V0" or "V1"\n=')	
	#
#
if faults == False:
	#
	check_formats = formats(args.format, faults)
	check_volumes = volumes(args.volume, faults)
	#
	gen_formats = check_formats[0]
	format_faults = check_formats[1]
	gen_volumes = check_volumes[0]
	volume_faults = check_volumes[1]
	#
	print(gen_volumes)
	#
	bookpaths = []
	#
	if format_faults:
		#
		print('=\n=> Please Provide Valid Export Format: -f "pdf,md,html"\n=')	
		#
	elif volume_faults:
		#
		print('=\n=> Please Provide Valid Export Volume: -v "V0" or "V1"\n=')	
		#
	else:
		#
		for x in gen_formats:
			#
			for _y in langs:
				#
				if x == 'pdf' or x == 'html':
					#
					md_name = "README_collected_"+_y+".md"
					md_path = os.path.join(dir_path,"lang",_y)
					md_path_b = os.path.join(dir_path,"lang",_y)
					up_dir = os.path.abspath(os.path.join(md_path, '../../..'))
					#
				elif x == 'md':
					#
					print("JUST MD")
					#
					md_name = "README_"+_y+".md"
					md_path = os.path.join(dir_path,"lang",_y)
					up_dir = os.path.abspath(os.path.join(md_path, '../../..'))
					md_path_b = os.path.join(dir_path,"lang",_y)
					#md_path_b = up_dir
					#
					#
				#
				collect_mds(md_path, md_path_b, md_name, gen_volumes)
				make_default_github_md(md_path, md_path_b, md_name, gen_volumes)
				#
				if x == 'pdf' or x == 'html':
					#
					md_to_html(os.path.join(dir_path,"lang",_y), md_name)
					#
					book_path = os.path.join(dir_path,"lang",_y,"md_temp.html")
					book_path_new = os.path.join(dir_path,"README_"+_y+".html")
					#
					temp_html = open(book_path, "r")
					html_data = temp_html.read()
					#
					#
					temp_html.close()
					#
					title_full = "VRD | "+project_name+' | '+version+' | '+gen_date
					#
					if x == 'pdf':
						#
						title = "VRD | "+project_name
						#
					elif x == 'html':
						#
						title = title_full#"VRD | "+project_name+' | '+version+' | '+gen_date
						#
					#
					#
					if x == 'pdf': # only rasterize pdfs
						#
						raster_content = rasterize_html(book_path,_y)
						new_data = combine_header(raster_content, str(title_full))
						newfile = open(book_path, "w")
						newfile.write(new_data)
						#
						newfile.close()
						#
					#
					if x == 'html':
						#
						new_data_nr = combine_header(html_data, str(title_full), False)
						newfile_nr = open(book_path_new, "w")
						newfile_nr.write(new_data_nr)
						#
						newfile_nr.close()
						#
						
					#os.remove(book_path)
					#os.remove(os.path.join(os.path.join(dir_path,"lang",_y), "README_collected_"+_y+".md"))
					#
					try:

						os.remove(book_path)
						

					except Exception as e:

						pass
					#
					if x == 'pdf':
						#
						make_pdf(new_data, new_list, css_file, css_file_contents, css_file_cover, version, up_dir, title, gen_date, _y)
						#
					#
			#
			title_full = "VRD | "+project_name+' | '+version+' | '+gen_date
			#
			for _y in langs:
				#
				if x == 'html':
					#
					if len(langs) > 0:
						#
						make_multilingual_html(langs, title_full)
						#
					#
				try:

					
					os.remove(os.path.join(os.path.join(dir_path,"lang",_y), "README_"+_y+".md"))
					os.remove(os.path.join(dir_path, "README_rasterizeable_"+_y+".html"))
					os.remove(os.path.join(dir_path, "README_rasterized_"+_y+".html"))
					

				except Exception as e:

					pass
				#
			#
			#
		#
	#
#
