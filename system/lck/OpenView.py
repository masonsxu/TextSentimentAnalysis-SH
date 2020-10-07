from selenium import webdriver

class OpenView:
    driver = None
    def __init__(self):
        driver = webdriver.Chrome()
        #可视化页面的地址
        url = 'E:/Pycharm_xjf/ShangHai_Porject/View/head.html'
        driver.get(url)
        driver.maximize_window()
        # time.sleep(60 * 60)

# view = OpenView()