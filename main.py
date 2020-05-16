#!/usr/bin/python
# coding=utf-8
'''
@Author: Recar
@Date: 2020-05-02 19:11:42
@LastEditors: Recar
@LastEditTime: 2020-05-02 19:21:49
'''
# banner 信息高速获取
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
from selenium.webdriver.chrome.options import Options
from jinja2 import Environment, FileSystemLoader
from selenium import webdriver
from lib.parser import get_options
from dateutil.parser import parse
from lib.log import logger
from lib.utils import Utils
import HackRequests
import threading
import shutil
import time
import os
import sys


class Banner(object):
    def __init__(self, domains, is_html=True):
        self.domains = domains
        self.used_domains = list()
        self.is_html = is_html
        self.all_test_count = len(domains)
        self.thread_count = 50
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.logger = logger
        self.result_list = list()
        self.lock = threading.Lock()
        self.start_time_str = time.strftime('%Y%m%d%H%M', time.localtime())
        self.start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.out_put = os.path.join(self.base_path, "output", self.start_time_str)
        if not os.path.exists(self.out_put):
            os.makedirs(self.out_put)

    def generate_html(self, body, all_test_count, start_time, end_time, use_time):
        template_path = os.path.join(self.base_path, "config")
        env = Environment(loader=FileSystemLoader(template_path))
        template = env.get_template('template.html')
        html_path = os.path.join(self.out_put, "report.html")
        len_domain_get = len(body)
        with open(html_path, 'w', encoding="utf-8") as fout:
            html_content = template.render(start_time=start_time,
                                           stop_time=end_time,
                                           use_time=use_time,
                                           all_test_count=all_test_count,
                                           len_domain_get=len_domain_get,
                                           body=body)
            fout.write(html_content)

    def _run_get_png(self, domain):
        url = "http://" + domain
        try:
            if Utils.is_windows():
                chromedriver_path = os.path.join(self.base_path, "config", "chromedriver.exe")
            else:
                chromedriver_path = os.path.join(self.base_path, "config", "chromedriver")
                os.system(f"chmod +x {chromedriver_path}")
            opt = Options()
            opt.add_argument('headless')
            opt.add_experimental_option('excludeSwitches', ['enable-logging'])
            driver = webdriver.Chrome(chromedriver_path, options=opt)
            driver.get(url)
            width = driver.execute_script("return document.documentElement.scrollWidth")
            height = driver.execute_script("return document.documentElement.scrollHeight")
            driver.set_window_size(width, height)
            output_png_dir_path = os.path.join(self.base_path, "output", self.start_time_str, "images")
            if not os.path.exists(output_png_dir_path):
                os.makedirs(output_png_dir_path)
            output_png_path = os.path.join(output_png_dir_path, domain+".png")
            driver.get_screenshot_as_file(output_png_path)
            title = driver.title
            return output_png_path, title
        except Exception as e:
            self.logger.error(e)
            return None, None
        finally:
            driver.close()

    def _run_get_headers(self, domain):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
        url = "http://"+domain
        self.logger.info(url)
        try:
            hack = HackRequests.hackRequests()
            response = hack.http(url, headers=headers, timeout=5)
            response_headers = response.log.get("response")
            if not self.is_html:
                return response_headers
            else:
                return response_headers.replace("\n", "<br/>")
        except Exception as e:
            self.logger.error(e)
            return None

    def run_banner(self, domain):
        headers_str = self._run_get_headers(domain)
        if not headers_str:
            return
        png_path, title = self._run_get_png(domain)
        if png_path and title and headers_str:
            self.result_list.append({
                "domain": domain,
                "title": title,
                "png_path": png_path,
                "headers_str": headers_str
            })
            self.lock.acquire()
            self.logger.info(f"[+] find :{title}")
            # 用于做进度条
            self.used_domains.append(domain)
            len_all_domains = len(self.domains)
            len_used_domains = len(self.used_domains)
            self.logger.info(f"[*] all: {len_all_domains}  testd: {len_used_domains}")
            self.lock.release()

    def run(self):
        self.logger.info("[*] statrt ")
        self.pool = ThreadPoolExecutor(self.thread_count) # 定义线程池
        all_task = list()
        for domain in domains:
            all_task.append(self.pool.submit(self.run_banner, domain))
        for task in all_task:
            task.result()
        # wait(all_task, return_when=ALL_COMPLETED)
        self.logger.info(f"[end] find count: {len(self.result_list)}")
        end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.logger.info("start create result html")
        use_time = (parse(end_time)-parse(self.start_time)).total_seconds()
        self.logger.info(f"use time: {use_time}")
        self.generate_html(self.result_list, self.all_test_count, self.start_time, end_time, use_time)
        self.logger.info("end")


if __name__ == "__main__":
    options = get_options()
    domains = options.domains
    domain_file = options.domain_file
    rm_output = options.rm_output
    if rm_output:
        base_path = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(base_path, "output")
        if os.path.exists(output_path):
            shutil.rmtree(output_path)
        print("删除成功")
        sys.exit(0)

    if domain_file:
        domains = list()
        with open(domain_file, "r") as f:
            for line in f:
                domain = line.strip()
                if "http" or "https" in domain:
                    domain = domain.replace("http://", "").replace("https://", "")
                    domains.append(domain)
    banner = Banner(domains)
    banner.run()
