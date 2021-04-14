import csv
import json
import requests


def fetch_raw_data(page_num):
    url = 'https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry?gameNo=35&provinceId=0&pageSize=100&isVerify=1&pageNo=%s' % str(page_num)
    response = requests.get(url)
    raw_data = json.loads(response.text)
    print('第%s页信息获取中。。。' % page_num)
    return raw_data


def clean_raw_data(raw_data, info_list):
    results = raw_data['value']
    for result in results['list']:
        stage_count = result['lotteryDrawNum']
        stage_res = result['lotteryDrawResult']
        stage_time = result['lotteryDrawTime']
        info_list.append([stage_count, stage_res, stage_time])


def save_clean_data(info_list):
    with open('3nums_rev.csv', 'a') as file:
        writer = csv.writer(file)
        for info in info_list:
            writer.writerow(info)
        print('任务结束！')


if __name__ == '__main__':
    info_list = []
    for page_num in range(1, 60):
        data = fetch_raw_data(page_num)
        clean_raw_data(data, info_list)
    save_clean_data(info_list)
