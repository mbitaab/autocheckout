import os
import datetime
import pandas as pd
import time
import re
from tqdm import tqdm
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from collections import defaultdict
import argparse
import requests
import urllib.request
from random import randint
from time import sleep
import random
import numpy as np
import sys
from multiprocessing import Pool
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import undetected_chromedriver as uc
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from datetime import datetime
from merch_extractor import *
from config import *

'''
sudo docker container ls
sudo docker attach <ID>

sudo docker run -d -p 4444:4444 -e SE_NODE_MAX_SESSIONS=3 -e SE_NODE_OVERRIDE_MAX_SESSIONS=true --shm-size="2g" seleniarm/standalone-chromium:latest

or 

sudo docker run --rm -it -p 4444:4444 -p 5900:5900 -p 7900:7900 -e SE_NODE_MAX_SESSIONS=9 -e SE_NODE_OVERRIDE_MAX_SESSIONS=true --shm-size 2g seleniarm/standalone-chromium:latest

'''

info = {
    'email': 'somian123@gmail.com',
    'size': 'M',
    'first': 'Som',
    'name': 'joshua',
    'last' : 'Somian',
    'country': 'US',
    'address': '774 Davis Avenue',
    'apt': '345',
    'city': 'Fortuna',
    'state': 'CA', 
    'zipcode': '95540',
    'phone': '7077261518'
}



def search_elem(driver, xpath_str, text_list):
    if type(xpath_str) is str:
        # get all of the buttons and check their text
        elems = driver.find_elements("xpath", xpath_str)
        for elem in elems:
            elem_text = elem.text
            #print(elem_text)
            for btn_text in text_list:
                if btn_text in elem_text.lower().strip():
                    return elem
    else:
        # get all of the buttons and check their text
        for search_xpath in xpath_str:
            print('>>', xpath_str)
            elems = driver.find_elements("xpath", search_xpath)
            elem_text = []
            for elem in elems:
                if elem.text.lower().strip():
                    elem_text.append(elem.text.lower().strip())
                if not elem_text:
                    inner_elements = elem.find_elements(By.XPATH,".//*")
                    for item in inner_elements:
                        if item.text.lower().strip():    
                            elem_text.append(item.text.lower().strip())
                print(f"list : {elem_text}")
                for btn_text in text_list:
                    if btn_text in elem_text:
                        print("Founded")
                        return elem                
    return None

def checkout_wordpress(domain, driver,f_log):
    try_again, flag = True, False

    # check for popups
    f_log.write("[*]Search for popup - 1"+"\n")
    for i in ["//button[contains(@aria-label, 'Close')]", "//button[contains(@aria-label, 'close')]"]:
        close_btn = driver.find_elements('xpath', i)
        if close_btn != []:
            try:
                close_btn[0].click()
            except:
                pass
    f_log.write("[*]start finding links"+"\n")
    # get prod links
    #print(driver.page_source, file=open('/home/ubuntu/new_drive/bp_pp/code/test.html', 'w'))
    links = []
    links.extend([i.get_attribute('href') for i in driver.find_elements("xpath", "//a[contains(@href, \"%s\")]" % ('/product'))])

    links.extend([i.get_attribute('href') for i in driver.find_elements("xpath", "//link[contains(@href, \"%s\")]" % ('/product'))])

    print('links first attempt ======== ', links)
  
    links.extend([i.get_attribute('href') for i in driver.find_elements("xpath", "//a[contains(@href, \"%s\")]" % ('?product'))])

    print('links second attempts ======== ', links)

    if links == []:
        links = []
        shallow_filter = ['/about', '/cart', '/track', '/contact', '/privacy', '/policy', '/terms', '/refund']
        for e in driver.find_elements("xpath", "//a"):
            link = e.get_attribute('href')
            avoid = False

            if link is None:
                continue

            for s in shallow_filter:
                if s in link:
                    avoid = True
                    break
            if not avoid:
                links.append(e.get_attribute('href'))

    print('another attempt to find links ========', links)
    f_log.write("[*]Start checking links"+"\n")
    all_links = list(set(links))
    links = [link for link in all_links if not link.endswith('.css') and not link.endswith('.xml')]
    for i in range(3):
        try: 
            time.sleep(randint(1, 5))
            # prod_elems = driver.find_elements("xpath", "//a[contains(@href, \"%s\")]" % ('/product'))
            # prod_link = prod_elems[randint(0, len(prod_elems) - 1)].get_attribute('href')
            prod_link = links[randint(0, len(links) - 1)]
            print('===========product:', prod_link)
            f_log.write(f"[*]product : {prod_link}"+"\n")
            driver.get(prod_link)
            time.sleep(randint(2, 4))

            
            try:
                f_log.write("[*]Close seconf popup"+"\n")
                time.sleep(10)
                window_size = driver.get_window_size()
                width = window_size['width']
                height = window_size['height']
                print(f"w: {width} , h: {height}")
                random_x = random.randint(0, width)
                random_y = random.randint(0, height)
                actions = ActionChains(driver)
                actions.move_by_offset(100, 100).click().perform()
                print("A dialog closed")
                f_log.write("[*]Popup is closed"+"\n")
            except Exception as e:
                print("Error clicking the button:", e)
                f_log.write(f"[*]There is a problem : {e}"+"\n")
            

            # find cart button
            cart_elem = search_elem(driver, '//button', ['add to cart', 'buy now', 'buy product', 'Añadir al carrito', 'Ajouter au panier', ' Aggiungi al carrello '])
            if cart_elem:
                print("add to cart")
                cart_elem.click()
                time.sleep(5)
                f_log.write("[*]add to card ..."+"\n")
                break

            if 'amazon' in driver.current_url:
                continue

        except Exception as e:
            print(e)
            f_log.write(f"[*]An error occurce {e}"+"\n")
            pass

    # proceed to checkout
    try:
        f_log.write("[*]Looking for checkout"+"\n")
        time.sleep(randint(3,5))
        print("checkout")
        #print(driver.page_source, )
        checkout_elem = search_elem(driver, ['//button', '//a'], ['checkout', 'check out', 'view cart', 'proceed to checkout','Finalizar compra', 'Voir mon panier', 'mon panier', 'Finaliser ma commande', 'Procedi all\'acquisto', 'Vai al carrello'])
        if checkout_elem:
            checkout_elem.click()
        time.sleep(randint(3,5))
    except Exception as e:
        f_log.write(f"[*]An error occure in checkout {e}"+"\n")
        print('CHECKOUT:', e)

    # fill out the form
    keys = {
        'id': 'name',
        'name': 'name',
        'first': 'first',
        'last': 'last',
        'address': 'address',
        'city': 'city',
        'cty': 'city',
        'town': 'city',
        'zip': 'zipcode',
        'postcode': 'zipcode',
        'postalCode': 'zipcode',
        'postalcode': 'zipcode',
        'phone': 'phone',
        'email': 'email',
        'state': 'state',
        'zone': 'state',
        'country': 'country',
        'addr': 'address',
    }
    f_log.write("[*]Start looking paypal -1 "+"\n")
    for paypal_filter in ['//img[contains(@alt, "PayPal")]', '//div[contains(@role, "link")]', '//div[contains(@class, "paypal-button-number-0")]', '//a[contains(@href, "paypal")]', '//div[contains(@class, "paypal")]']:
            try:
                paypal_buttons = driver.find_elements("xpath", paypal_filter)
                print('PPLBTN STAGE...')
                for btn in paypal_buttons:
                    try:
                        if '//a' in paypal_filter:
                            driver.get(btn.get_attribute('href'))
                            print('PYPL(1) LINK')
                            f_log.write("[*]paypal link"+"\n")
                            flag = True
                        else:
                            print('PYPL(1) BTN')
                            f_log.write("[*]paypal btn"+"\n")
                            #driver.save_screenshot('../../tesssssstP3.png')
                            time.sleep(5)
                            btn.click()
                            flag = True
                        # break
                    except Exception as e:
                        print(e)
                        f_log.write(f"[*]an error {e}"+"\n")
                        pass
                    if flag:
                        break
                if flag:
                    break
            except Exception as e:
                print('Filter Issue:', paypal_filter, e)
                f_log.write(f"[*]an error (1) : {e}"+"\n")
                pass
    
    time.sleep(5)

    if flag is False:
        print("Not found paypal yet , try another method ... ")
        f_log.write(f"[*]Not found paypal yet , try another method ... "+"\n")
        f_log.write(f"[*]Filling Form "+"\n")
        for i in range(1):
            try:
                all_inputs = driver.find_elements("xpath", '//input')
                for inp in all_inputs:
                    try:
                        for k, v in keys.items():
                            if k in inp.get_attribute('id').lower() or k in inp.get_attribute('name').lower():
                                inp.clear()
                                inp.send_keys(info[v])
                    except Exception as e:
                        f_log.write(f"[*]internal error in filling form : {e} "+"\n")
                        break
    
                all_selects = driver.find_elements(By.XPATH, "//select")
                print(f"selector : {all_selects}")
                for select in all_selects:
                    print(f"try -> {select.get_attribute('name')}")
                    #select.click()
                    select_ok = Select(select)
                    if 'state' in select.get_attribute('name').lower() or 'zone' in select.get_attribute('name').lower():
                        print(f"found 1")
                        select_ok.select_by_value(info['state'])
                    elif 'country' in select.get_attribute('name').lower():
                        print("found 2")
                        select_ok.select_by_value(info['country'])
                    #driver.save_screenshot('../../tesssssstP.png')
            except Exception as ex:
                print(f"ERROR in filling form: {ex}")
                f_log.write(f"[*]Error : {ex} "+"\n")
                #driver.save_screenshot('../../tesssssstERROR.png')
                

        time.sleep(5)

        # with open('../../test.html', 'w') as f:
        #     f.write(driver.page_source)
        #     f.flush()
        
        # try to find and click paypal button
        # click on paypal text!
        # Define the pattern for PayPal text with small and capital P

        # special form of PayPal 
        f_log.write(f"[*] Find paypal span"+"\n")
        possible_paypal_chks = ["//span[contains(text(), 'PayPal')]", "//span[contains(text(), 'paypal')]"]
        for chk in possible_paypal_chks:
            elems = driver.find_elements("xpath", chk)
            if elems:
                for e in elems:
                    print(f"Elements : {e.text}")
                    print(e.get_attribute('outerHTML'))
                    e.click()
        
        #driver.save_screenshot('../../tesssssstP2.png')
        f_log.write(f"[*]click paypal span btn "+"\n")
        for paypal_filter in ['//img[contains(@alt, "PayPal")]', '//div[contains(@role, "link")]', '//div[contains(@class, "paypal-button-number-0")]', '//a[contains(@href, "paypal")]', '//div[contains(@class, "paypal")]']:
                try:
                    paypal_buttons = driver.find_elements("xpath", paypal_filter)
                    for btn in paypal_buttons:
                        try:
                            if '//a' in paypal_filter:
                                driver.get(btn.get_attribute('href'))
                                print('PYPL LINK')
                                f_log.write(f"[*]paypal link "+"\n")
                                flag = True
                            else:
                                print('PYPL BTN')
                                f_log.write(f"[*]paypal btn "+"\n")
                                #driver.save_screenshot('../../tesssssstP3.png')
                                time.sleep(10)
                                btn.click()
                                flag = True
                            # break
                        except Exception as e:
                            print(e)
                            f_log.write(f"[*]error : {e} "+"\n")
                            pass
                        if flag:
                            break
                    if flag:
                        break
                except Exception as e:
                    print('Filter Issue:', paypal_filter, e)
                    pass
    
    
    driver.switch_to.default_content()
    if not flag and driver.find_elements("xpath", "//iframe"):
        print("looking for iframe")
        for iframe in driver.find_elements("xpath", "//iframe"):
            try:
                #print(iframe)

                # focus on the iframe -> required for selenium search to work
                driver.switch_to.frame(iframe)
                jq = 'document.querySelectorAll(\'[role="link"]\').forEach(function (el){el.click();});'
                driver.execute_script(jq)
            except:
                pass
    
    
    print('Click Chekout', flag)
    time.sleep(5)
    f_log.write(f"[*]flag : {flag}"+"\n")
    #have no idea about this part , please check later!!
    if not flag:
        # perform general checkout
        for chk in ["//form[contains(@id, 'checkout')]", "//form[contains(@type, 'submit')]"]:
            elems = driver.find_elements("xpath", chk)
            print(elems)
            if elems:
                e[0].submit()
                flag = True
                break
    print('Force Chkout', flag)
    if flag:
        time.sleep(3)
    else:
        s = """var form = document.querySelector("form[id*=checkout]");
        if (form) { form.submit(); }"""
        driver.execute_script(s)
        time.sleep(3)
    # -------------------------------------------------
    log_entries = []
    for index, handle in enumerate(driver.window_handles):
        # save checkout page source
        driver.switch_to.window(handle)
        with open(args.html_file_address + domain.replace('/', '_').replace(':', '_') + str(index) + '.html', "w", encoding='utf-8') as f:
            f.write(driver.page_source)
        log_entries.append(driver.get_log('performance'))
        log_entries.append(driver.current_url)

    return log_entries


def run_fc(data_pack):
    urls = data_pack
    my_id = 0
    results = []
    print('Hi, I\'m process number %d' %my_id)
    c_date = datetime.today().strftime('%Y_%m_%d')
    #f_log = open(f"/app/data/log/logs_{c_date}_{my_id}.log" , "w")
    f_log = open(args.log_file_address,"w")
    iterator = tqdm(urls) if my_id == 0 else urls

    for domain in iterator:

        d = DesiredCapabilities.CHROME
        d['goog:loggingPrefs'] = { 'performance':'ALL', 'browser':'ALL' }
        options = uc.ChromeOptions()
        options.add_argument("--incognito")
        options.add_argument("--enable-javascript")
        options.add_argument("--ignore-certificate-errors")
        prefs = {
            "translate_whitelists": {"fr":"en", "es":"en"},
            "translate":{"enabled":"true"}
        }
        options.add_experimental_option("prefs", prefs)

        try:
            print(f"SEL : {selenium_addr}")
            driver = webdriver.Remote(selenium_addr, d, options=options)
            # Changing the property of the navigator value for webdriver to undefined
            #driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            # driver = webdriver.Chrome(options=options)
        except Exception as e:
            print('Remote Error:', e)
            continue

        if domain:
            try:
                if 'https://' not in domain:
                    domain = 'https://' + domain
                f_log.write(f"[+]{domain}"+"\n")
                print(domain)
                driver.get(domain)
                try:
                    action = ActionChains(driver)
                    action.move_by_offset(10, 20).perform()
                    print("A dialog closed")
                except Exception as e:
                    print("Error clicking the button:", e)

                time.sleep(4)
                f_log.write("[*]Get Domain Done"+"\n")
                driver.save_screenshot(args.screen_file_address + domain.replace('/', '_').replace(':', '_') + '.png')
                log = checkout_wordpress(domain, driver,f_log)
                f_log.write("[*]Checkout Done"+"\n")
                f_log.flush()
                results.append(
                    json.dumps({'refs': get_redirections_all({'domain': domain, 'log': log}), 'domain': domain})
                )

            except Exception as e:
                print('ERRORRRR:', e)
                pass
        
        try:
            driver.close()
        except:
            pass

        try:
            driver.quit()
        except:
            pass
    return results

def get_redirections_all(log):
    domain = log['domain'].replace('https://', '').replace('http://', '').replace('/', '')
    ref_res = []

    for l in log['log'][0]:
        if 'paypal.com' in l['message']:
            try:

                ref = json.loads(l['message'])['message']['params']['request']['headers']['Referer']
                if domain not in ref and 'paypal' not in ref and ref != '':
                    headers = json.loads(l['message'])['message']['params']['request']
                    ref_res.append({
                        'domain': log['domain'],
                        'referer': headers['headers']['Referer'],
                        'paypal_link': headers['url']
                    })

            except:
                pass
    return ref_res

def perform_checkout(urls, out_file):

    results = run_fc(urls)
    # results = [ [r1, r2, ...], [r1, r2, ...] ... ]
    with open(out_file, 'a+') as fout:
        for result in results:
            print(result)
            fout.write(result + '\n')
        fout.close()


def clean_url(url):
    # Regular expression pattern to match and remove the desired prefixes
    pattern = re.compile(r'^(http:\/\/|https:\/\/|www\.)+')
    # Replace the matched prefixes with an empty string
    cleaned_url = re.sub(pattern, '', url)
    return cleaned_url

def main(args):

    urls= []

    if args.input_bp and args.input_ec:
        df_scam = pd.read_csv(args.input_bp)
        df_scam['URL'] = df_scam['URL'].apply(clean_url)

        df_shop = pd.read_csv(args.input_ec)
        df_shop['URL'] = df_shop['URL'].apply(clean_url)

        df_filtered = df_scam[df_scam['Label'] == 'scam'].merge(df_shop[df_shop['label'] == 'shop'], on='URL')
   
        print('df filtered length: %s' %len(df_filtered))
            


        # call force checkout on it
        outpath = args.p_log_file_address
        print(outpath)


        # check output file for existing domains
        visited_domains = []
        if os.path.exists(outpath):
            with open(outpath, 'r') as fin:
                for line in fin.readlines():
                    visited_domains.append(json.loads(line.strip())['domain'] )

        for row in df_filtered.iterrows():
            if row[1]['URL'] not in visited_domains:
                urls.append(row[1]['URL'])

    elif args.url:
        urls.append(args.url)
       

    perform_checkout(urls, outpath)

    # extract merchant IDs
    final_outpath = outpath.replace('log', 'merch-info').replace('.jsonl', '.json')
    parse_data(outpath, final_outpath)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Optional app description')

    parser.add_argument('--input_bp', type=str, help='input containing bp results', required=False)
    parser.add_argument('--input_ec', type=str, help='input containing shopping classifier result', required=False)
    parser.add_argument('--url', type=str, help='url to checkout', required=False)
    parser.add_argument('--log_file_address', type=str, help='log file address', required=True)
    parser.add_argument('--p_log_file_address', type=str, help='log file address', required=True)
    parser.add_argument('--screen_file_address', type=str, help='screenshot dir', required=True)
    parser.add_argument('--html_file_address', type=str, help='screenshot dir', required=True)
    args = parser.parse_args()
    main(args)