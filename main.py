import os
import requests
import bs4
import pandas as pd
from urllib.request import urlretrieve
import base64
from datetime import datetime

URL_H = "https://nedrug.mfds.go.kr/pbp/CCBBB01/getItemDetailCache?cacheSeq="
URL_T = "aupdateTs2024-10-13%2024:02:23.0b"
CSV_INPUT = 'test.csv' # 입력 csv
CSV_OUTPUT = 'updated_data.csv' # 출력csv
INDEX_START = 0 # 시작 행 (index 30002->30000)
INDEX_END = 3 # 끝 행 (포함되지 않음)
IMAGE_FOLDER = 'images' # 이미지가 저장될 폴더

os.makedirs(IMAGE_FOLDER, exist_ok=True)

df = pd.read_csv(CSV_INPUT, encoding='UTF-8')
df['PATH'] = df['PATH'].astype('object')

subset = df.iloc[INDEX_START:INDEX_END]
total = len(subset)
  
for i, (index, row) in enumerate(subset.iterrows(), start=1):
    value = row['ID']
    url = URL_H + str(value) + URL_T

    response = requests.get(url)
    html = response.text
    soup = bs4.BeautifulSoup(html, features="html.parser")

    articles = soup.find_all('div', class_='pc-img')
    src_list = [img['src'] for article in articles for img in article.find_all('img')]

    progress = f"{i}/{total}"
    percentage = f"{(i / total) * 100:.2f}%"

    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    src = src_list[0] if src_list else None
    if src and src.startswith("data:image"):
        base64_data = src.split(",")[1]
        try:
            image_data = base64.b64decode(base64_data)
            name = str(value) + ".jpg"
            with open(IMAGE_FOLDER + "/" + name, "wb") as f:
                f.write(image_data)
            df.at[index, 'PATH'] = name
            print(f"[{current_time}][{progress} - {percentage}] 다운로드 성공 - {name}")
        except Exception as e:
            print(f"[{current_time}][{progress} - {percentage}] 다운로드 실패")
            df.at[index, 'PATH'] = "ERROR"
    else:
        df.at[index, 'PATH'] = "not exists"
        print(f"[{current_time}][{progress} - {percentage}] ID가 비어 있습니다. Index {index}")
    
    df.to_csv(CSV_OUTPUT, index=False, encoding='utf-8')
