import requests
import time
from bs4 import BeautifulSoup


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def get_data_from_bookmeter(aurl):
    site = requests.get(aurl, headers=headers)
    data = BeautifulSoup(site.content, 'html.parser')

    bookList = data.findAll(class_="detail__title")
    pageTagList = data.findAll(class_="detail__page")
    pageList = [tag.text for tag in pageTagList]    
    print(pageList)
    dateTagList = data.findAll(class_="detail__date")
    datelist = [tag.text for tag in dateTagList]
    # 結果を出力
    print(datelist)
    return (pageList, datelist)

# これを{無印、&page=2, &page=3, }と繰り返せばすべて取得できる
urlBase = "https://bookmeter.com/users/780800/books/read?display_type=list"
allPageList = []
allDateList = []
i = 0
while(1):
    i += 1
    if (i == 1):
        print(urlBase)
        (datelist, pagelist) = get_data_from_bookmeter(urlBase)
    else:
        url = urlBase + "&page=" + str(i)
        print(url)
        (datelist, pagelist) = get_data_from_bookmeter(url)
        print(datelist)
    allPageList += datelist
    allDateList += pagelist
    if (len(datelist) == 0 or len(pagelist) == 0):
        break

print(allPageList)
print(allDateList)
allPageList.reverse()
allDateList.reverse()

page_numbers = allPageList
dates = allDateList

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime


# 不明な日付のインデックスを特定
unknown_date_indices = [i for i, date in enumerate(dates) if date == '日付不明']

# ページ数のリストを整数に変換して累積ページ数を計算
page_numbers = list(map(int, page_numbers))
cumulative_page_numbers = [sum(page_numbers[:i + 1]) for i in range(len(page_numbers))]

# 不明な日付のデータを除外
dates = [date for i, date in enumerate(dates) if i not in unknown_date_indices]
cumulative_page_numbers = [num for i, num in enumerate(cumulative_page_numbers) if i not in unknown_date_indices]

# 累積の本の冊数を計算 (要素数はcumulative_page_numbersと同じ)
unknown_num = len(unknown_date_indices)
cumulative_book_counts = list(range(unknown_num + 1, len(cumulative_page_numbers) + unknown_num + 1))

# 日付のリストをdatetimeオブジェクトに変換
dates = [datetime.strptime(date, '%Y/%m/%d') for date in dates]

# グラフをプロット
fig, ax1 = plt.subplots(figsize=(12, 6))  # グラフのサイズを指定

# 累積ページ数の散布図をプロット
ax1.scatter(dates, cumulative_page_numbers, label='Cumulative Pages', color='b', alpha=0.5)
ax1.fill_between(dates, 0, cumulative_page_numbers, alpha=0.5, color='b')
ax1.set_xlabel("Date")
ax1.set_ylabel("Cumulative Pages", color='b')

# 累積本の冊数の散布図をプロット (右側の目盛りに表示)
ax2 = ax1.twinx()
ax2.scatter(dates, cumulative_book_counts, label='Cumulative Books', marker='x', color='r', alpha=0.5)
ax2.fill_between(dates, 0, cumulative_book_counts, alpha=0.5, color='r')
ax2.set_ylabel("Cumulative Books", color='r')

# X軸の日付フォーマットをカスタマイズ
date_format = "%Y/%m/%d"  # 表示フォーマットを指定
date_formatter = mdates.DateFormatter(date_format)
months = mdates.MonthLocator()  # 月ごとの目盛りを設定
days = mdates.DayLocator()  # 日ごとの目盛りを設定

# X軸の目盛りを設定
ax1.xaxis.set_major_locator(months)
ax1.xaxis.set_minor_locator(days)
ax1.xaxis.set_major_formatter(date_formatter)

# X軸のラベルを90度回転して表示
plt.xticks(rotation=90)

# グラフのタイトルと凡例を設定
plt.title("Cumulative Pages and Books by Date")
plt.legend()

# グラフを表示
plt.tight_layout()
plt.show()
