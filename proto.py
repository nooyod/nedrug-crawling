import os
import requests
import bs4
import pandas as pd
from urllib.request import urlretrieve
import base64
from datetime import datetime

URL_H = "https://nedrug.mfds.go.kr/pbp/CCBBB01/getItemDetailCache?cacheSeq="
URL_T = "aupdateTs2024-10-13%2024:02:23.0b"

df = pd.read_csv('updated_data.csv', encoding='UTF-8')
# df = pd.read_csv('test.csv', encoding='UTF-8')
df['PATH'] = df['PATH'].astype('object')
# print(df.columns)
# subset = df.iloc[:, 20:30]

# for value in df['ID']:
start_index = 5789  # 시작 행 (index 30002->30000)
end_index = 12000   # 끝 행 (포함되지 않음)13900

# 진행 상황을 표시하면서 이미지 다운로드 및 PATH 열 업데이트
subset = df.iloc[start_index:end_index]  # 특정 행 범위만 선택
total = len(subset)
# total = len(df['ID'])
# for index, value in enumerate(df['ID']):    
for i, (index, row) in enumerate(subset.iterrows(), start=1):
    value = row['ID']
    url = URL_H + str(value) + URL_T
    # print(url)

    response = requests.get(url)
    html = response.text

    soup = bs4.BeautifulSoup(html, features="html.parser")
    # print(soup)

    articles = soup.find_all('div', class_='pc-img')
    # print(articles)

    src_list = [img['src'] for article in articles for img in article.find_all('img')]
    # print(src_list)

    # progress = f"{index + 1}/{total}"  # n/n 형식
    # percentage = f"{((index + 1) / total) * 100:.2f}%"  # 퍼센트 형식
    progress = f"{i}/{total}"  # n/n 형식
    percentage = f"{(i / total) * 100:.2f}%"  # 퍼센트 형식

    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    src = src_list[0] if src_list else None
    if src:
        if src.startswith("data:image"):  # 데이터 URL인 경우
            # Base64 인코딩된 데이터만 추출
            base64_data = src.split(",")[1]
            
            # 디코딩 및 저장
            try:
                image_data = base64.b64decode(base64_data)
                name = str(value) + ".jpg"
                with open("images2/"+ name, "wb") as f:
                    f.write(image_data)
                df.at[index, 'PATH'] = name
                print(f"[{current_time}][{progress} - {percentage}] 다운로드 성공 - {name}")
            except Exception as e:
                print(f"[{current_time}][{progress} - {percentage}] 다운로드 실패")
                df.at[index, 'PATH'] = "ERROR"

        else:  # 일반 URL인 경우
            save_path = "downloaded_image.jpg"
            urlretrieve(src, save_path)
            print(f"Image downloaded and saved as {save_path}")

    else:
        df.at[index, 'PATH'] = "not exists"
        print(f"[{current_time}][{progress} - {percentage}] ID가 비어 있습니다. Index {index}")
    
    df.to_csv('updated_data.csv', index=False, encoding='utf-8')
