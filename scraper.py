import threading
import time
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.chrome.options import Options
import subprocess
import urllib3
import importlib
import domains
import wget
import tkinter as tk

chrome_driver = "/Users/jessec18/Downloads/chromedriver"
gecko_driver = "/Users/jessec18/Downloads/geckodriver"

options = Options()
options.add_experimental_option("prefs", {
    #"plugins.always_open_pdf_externally": True,
    "download.default_directory": r"~/Documents/scraper/pdfs/",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    #"safebrowsing.enabled": True
})

#browser = webdriver.Chrome(executable_path = chrome_driver, chrome_options=options)
browser = webdriver.Firefox(executable_path=gecko_driver)#, chrome_options=options)
browser.get("google.com")

def search_scholar(title):

    url = "https://scholar.google.com"
    browser.get(url)

    # textbox
    txt = browser.find_element_by_xpath("//*[@id=\"gs_hdr_tsi\"]")
    txt.send_keys(title)

    # search button
    search = browser.find_element_by_xpath("//*[@id=\"gs_hdr_tsb\"]/span/span[1]")
    search.click()

    # results
    # if link to pdf is inlined in results
    #try:
    #    link = browser.find_elements_by_css_selector(
    #        "#gs_res_ccl_mid > div:nth-child(1) > div.gs_ggs.gs_fl > div > div > a"
    #    )
    #    print("found link inline")
    #    download_pdf(link.get_attribute("href"))
    #    return

    #except:
    #    pass

    results = browser.find_elements_by_css_selector("h3 a")

    # top result
    results[0].click()

    # domain specific behavior
    importlib.reload(domains)

    # if behavior for domain has been encoded
    domain = urllib3.util.parse_url(browser.current_url).netloc
    domain = domain.split(".")[1]
    print(domain)

    try:
        getattr(domains, domain)(browser)
        print("found instructions")
        download_pdf(browser)
        while DOWNLOAD == False:
            pass
    
    except:
        result = False

        function = ["def {}(browser):".format(domain)]

        while(result != True):

            print("Which link?")
            clip = get_input_from_clipboard()
            print(clip)

            if clip == "Download":
                result = True
                continue

            try:
                print("clicking xpath")
                link = browser.find_element_by_xpath(clip)
                link.click()

                function.append("\tlink = browser.find_element_by_xpath('{}')".format(clip))
                function.append("\tlink.click()\n")

            # if text in clipboard is url
            except:
                print("error")
                print(clip)
                result = download_pdf(clip)

        with open("domains.py", "a") as d:
            d.write("\n".join(function) + "\n")


DOWNLOAD = False
def get_input_from_clipboard():
    global DOWNLOAD

    p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
    retcode = p.wait()
    clip = p.stdout.read()

    while True:
        p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
        retcode = p.wait()
        new_clip = p.stdout.read()

        if new_clip != clip:
            return str(new_clip, 'utf-8')

        elif DOWNLOAD == True:
            DOWNLOAD = False
            return "Download"

def download_button():

    def download(event):
        global DOWNLOAD
        DOWNLOAD = True

    root = tk.Tk()
    frame = tk.Frame(root, width=100, height=100)
    frame.bind("<Button-1>", download)
    frame.pack()
    
    root.mainloop()

def download_pdf(browser):

    # download pdf
    print("downloading pdf")
    time.sleep(5)
    print(browser.page_source)

    with open("pdfs/out.pdf", 'w') as pdf:
        pdf.write(browser.get_page_source())

        #browser.find_element_by_id("download").click()
        #return True

    #except:
    #    print("Error while downloading pdf from \n{}".format(url))
    #    return None


def search_papers():
    print("parsing input")
    with open("papers.txt", 'r') as f:
        for i, line in enumerate(f):
            if i == 0:
                continue
            print(line)
            search_scholar(line.strip())

t1 = threading.Thread(target=search_papers)
t1.start()
download_button()
t1.join()
