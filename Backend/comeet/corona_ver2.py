# time.sleep 으로 시차를 두기 위해
import time
# tqdm : 진행상태를 표시하기 위해
from tqdm import trange

import os
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
import pandas as pd

# 여러 페이지를 가져오기 위한 1단계 - 함수 처리
def get_seoul_covid19_100(page_no):
    """
    page_no : 입력값으로 페이지 번호를 입력하면 해당 페이지 번호의 데이터를 가져옴
    start_no : 입력받은 page_no
    """
    start_no = (page_no - 1) * 100
    url = f"https://news.seoul.go.kr/api/27/getCorona19Status/get_status_ajax.php?draw={page_no}" 
    url = f"{url}&order%5B0%5D%5Bdir%5D=desc&start={start_no}&length=100"
    response = requests.get(url)
    data_json = response.json()
    return data_json

def get_multi_page_list(start_page, end_page = 80):
    # 데이터가 제대로 로드 되는지 앞부분 3페이지 정도만 확인하고 전체페이지를 가져오록 합니다.
    
    page_list = []
    for page_no in trange(start_page, end_page + 1):
        one_page = get_seoul_covid19_100(page_no)
        if len(one_page["data"]) > 0:
            one_page = pd.DataFrame(one_page["data"])
            page_list.append(one_page)
            # 서버에 한번에 너무 많은요청을 보내면 서버에 부담이 됩니다.
            # 서버에 부담을 주지 않기 위애 0.5초씩 쉬었다 가져옵니다.
            time.sleep(0.5)
        else:
            # 수집된 값이 없다면 False를 반환합니다.
            # False 반환 시 수집한 리스트를 반환하도록 합니다.
            return page_list
    return page_list

def save_db(page_list):
    # 모든 컬럼을 db에 저장한다. 
    for page in page_list:
        for line in page:
            print(line)
        break;    


# 첫번째 페이지를 통해 전체 페이지 수를 계산 
data_json = get_seoul_covid19_100(1)

records_total = data_json['recordsTotal']

start_page = 1
end_page = round(records_total / 100) + 1

page_list = get_multi_page_list(start_page, end_page)

# print(page_list[:1])
save_db(page_list)