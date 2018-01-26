import urllib3

def get_pdf(browser):


    #if "sciencedirect" in browser.current_url:
    #    return sciencedirect(browser)

    if False:
        return None

    else:
        return None

def sciencedirect(browser):
	link = browser.find_element_by_xpath('//*[@id="pdfLink"]')
	link.click()

	link = browser.find_element_by_xpath('//*[@id="app"]/div/div/div/section/div/div[1]/div/div/div/div[2]/div[1]/div/ul/li[1]/a')
	link.click()
