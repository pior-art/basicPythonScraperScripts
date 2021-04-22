import os
import requests
from lxml import etree
import concurrent.futures

headers = {'User-Agent': 'CERN-LineMode/2.15 libwww/2.17b3'}


def get_html(url):
    response = requests.get(url, headers=headers)
    return response if response.status_code == 200 else None


def get_img_urls(res_obj, paper_urls):
    page_nodes = etree.HTML(res_obj.text)
    img_urls = page_nodes.xpath('//*[@class="grid-column teaser"]/a/@href')
    base_url = 'https://images.static-thomann.de/pics/bdb/wallpapers/'
    for link in img_urls:
        name = link.split('wallpapers_')[1].split('.html')[0]
        paper_urls.append(base_url + name + '/im/1920x1080.jpg')


def download_img(link):
    name = link.split('/im/1920x1080.jpg')[0].split('wallpapers/')[1] + '.jpg'
    print('下载%s中。。。' % name)
    img_response = get_html(link)
    with open('thomann_wallpapers/%s' % name, 'wb') as file:
        file.write(img_response.content)


def main():
    img_urls = []
    url = 'https://www.thomann.de/gb/browse_wallpapers.html'
    res_obj = get_html(url)
    get_img_urls(res_obj, img_urls)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download_img, img_urls)


if __name__ == '__main__':
    if not os.path.exists('thomann_wallpapers'):
        print('creating folder...')
        os.makedirs('thomann_wallpapers')
    main()
