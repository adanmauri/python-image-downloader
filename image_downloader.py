#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 2017 Adán Mauri Ungaro <adan.mauri@gmail.com>
#

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import json
import urllib2
import sys
import time

os.environ["PATH"] += os.pathsep + os.getcwd()

class ImageDownloader():
    
    download_path = "image_downloader/"
    save = True
    in_subdirectory = True    
    available_extensions =  ["jpg", "jpeg", "png", "gif"]      
    query_url = "https://www.google.co.in/search?q=__query__&source=lnms&tbm=isch"
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    }
    base_number_of_scrolls = 400
    num_results = 10
    
    dump = False
    
    driver = None
    
    def __init__(self, **kwargs):
        try:
            self.save = kwargs['save']
        except Exception as e:
            pass
        
        try:
            self.download_path = kwargs['download_path']
        except Exception as e:
            pass
        
        try:
            self.in_subdirectory = kwargs['in_subdirectory']
        except Exception as e:
            pass
            
        try:
            self.base_number_of_scrolls = kwargs['base_number_of_scrolls']
        except Exception as e:
            pass
        
        try:
            self.query_url = kwargs['query_url']
        except Exception as e:
            pass
            
        try:
            self.headers.append(kwargs['headers'])
        except Exception as e:
            pass
        
        try:
            self.num_results = kwargs['num_results']
        except Exception as e:
            pass
        
        try:
            self.dump = kwargs['dump']
        except Exception as e:
            pass
        
        #if not os.path.exists(download_path + searchtext.replace(" ", "_")):
        #    os.makedirs(download_path + searchtext.replace(" ", "_"))
    
    def get_png(self, query, **kwargs):
        kwargs.update({'extensions': ['png']})
        self.get_images(query, **kwargs)
    
    def get_gif(self, query, **kwargs):
        kwargs.update({'extensions': ['gif']})
        self.get_images(query, **kwargs)
        
    def get_jpeg(self, query, **kwargs):
        kwargs.update({'extensions': ['jpeg', 'jpg']})
        self.get_images(query, **kwargs)
    
    def get_images(self, query, **kwargs):
        request = {}
        
        try:
            request['num_results'] = kwargs['q']
        except Exception as e:
            pass
        
        try:
            request['save'] = kwargs['save']
        except Exception as e:
            request['save'] = self.save
            
        try:
            request['download_path'] = kwargs['download_path']
        except Exception as e:
            request['download_path'] = self.download_path
        
        try:
            request['in_subdirectory'] = kwargs['in_subdirectory']
        except Exception as e:
            request['in_subdirectory'] = self.in_subdirectory
            
        try:
            request['base_number_of_scrolls'] = kwargs['base_number_of_scrolls']
        except Exception as e:
            request['base_number_of_scrolls'] = self.base_number_of_scrolls
        
        try:
            request['query_url'] = kwargs['query_url']
        except Exception as e:
            request['query_url'] = self.query_url
            
        try:
            request['headers'] = kwargs['headers'].copy()
        except Exception as e:
            request['headers'] = self.headers.copy()

        try:
            if not request['num_results']:
                request['num_results'] = kwargs['num_results']
        except Exception as e:
            if not request['num_results']:
                request['num_results'] = self.num_results
        
        try:
            request['dump'] = kwargs['dump']
        except Exception as e:
            request['dump'] = self.dump
        
        try:
            if set(kwargs['extensions']).issubset(self.available_extensions):
                request['extensions'] = kwargs['extensions']
            else:
                request['extensions'] = self.available_extensions
        except Exception as e:
            request['extensions'] = self.available_extensions
        
        request['query'] = query
        request['query_url'] = request['query_url'].replace('__query__', query) 
        request['number_of_scrolls'] = request['num_results'] / request['base_number_of_scrolls'] + 1
        
        self.execute(**request)        

    def execute(self, **kwargs):
        if kwargs['dump']:
            print '========================================================='
            print 'Getting ('+str(kwargs['num_results'])+') images of: '+kwargs['query']
            print '---------------------------------------------------------'
            print 'URL: '+kwargs['query_url']
            print 'Extensions: '+str(kwargs['extensions'])

        img_count = 0
        downloaded_img_count = 0
        
        self.driver = webdriver.Firefox()
        self.driver.get(kwargs['query_url'])
        
        for _ in xrange(kwargs['number_of_scrolls']):
            for __ in xrange(10):
                self.driver.execute_script("window.scrollBy(0, 1000000)")
                time.sleep(0.2)
            time.sleep(0.5)
            """try:
                driver.find_element_by_xpath("//input[@value='Show more results']").click()
            except Exception as e:
                print "Less images found:", e
                break"""
        
        images = self.driver.find_elements_by_xpath('//div[contains(@class,"rg_meta")]')
        
        if kwargs['dump']:
            print "Total images:", len(images), "\n"
        
        self.save(images, **kwargs)
    
    def save(self, images, **kwargs):
        
        path = None
        
        if kwargs['save']:
            path = kwargs['download_path']
            if kwargs['in_subdirectory']:
                path = path+kwargs['query'].replace(" ", "_")
                if not os.path.exists(path):
                    os.makedirs(path)
        
        img_count = 0
        downloaded_img_count = 0
        for img in images:
            img_count += 1
            img_url = json.loads(img.get_attribute('innerHTML'))["ou"]
            img_type = json.loads(img.get_attribute('innerHTML'))["ity"]
            
            try:
                if img_type not in kwargs['extensions']:
                    img_type = "jpg"
                    
                if img_type in kwargs['extensions']:
                    if kwargs['dump']:
                        print "Downloading image", downloaded_img_count+1, ": ", img_url
                    req = urllib2.Request(img_url, headers=kwargs['headers'])
                    raw_img = urllib2.urlopen(req).read()
                    f = open(path+"/"+str(time.time())+"."+img_type, "wb")
                    f.write(raw_img)
                    f.close
                    downloaded_img_count += 1
            except Exception as e:
                print "Download failed:", e
            finally:
                pass
            if downloaded_img_count >= kwargs['num_results']:
                break
        
        if kwargs['dump']:
            print "Total downloaded: ", downloaded_img_count, "/", img_count
        
        try:
            self.driver.quit()
        except Exception as e:
            try:
                self.driver.close()
            except Exception as e:
                pass

        return {'success': True, 'downloaded_img_count': downloaded_img_count}
