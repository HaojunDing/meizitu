from lxml import etree
import os, re
import requests
# s = Session()


headers ={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}


def index():
    url = 'http://www.mzitu.com'
    try:
        html = requests.get(url, headers=headers, timeout=2).text
        # print(html)
        html_ele = etree.HTML(html)

        li_list = html_ele.xpath('//ul[@id="menu-nav"]/li')
        # 通过 url 匹配 所有分类
        for li_ele in li_list[1:]:
            page_url = li_ele.xpath('./a/@href')[0]
            fname = li_ele.xpath('./a')[0].text
            print(fname, page_url)
            #  创建分类文件夹名
            if not os.path.exists(fname):
                os.mkdir(fname)
            #  调用分类下的 函数
            classify(url, fname)
            # break
    except:
        print('连接超时')
        index()


def classify(url, fname):
    try:
        html = requests.get(url, headers=headers, timeout=2).text
        html_ele = etree.HTML(html)
        li_list = html_ele.xpath('//ul[@id="pins"]/li')
        for li_ele in li_list:
            li_url = li_ele.xpath('./a/@href')[0]
            fnames = li_ele.xpath('./span[1]/a')[0].text
            list_name = './'+fname + '/' + fnames + '/'
            list_name = list_name.replace(' ', '')
            if not os.path.exists(list_name):
                os.mkdir(list_name)
            ref = list_name.split('/')[-1]
            print(ref)
            hea = {
                'Referer': 'http://www.mzitu.com/' + ref,
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
            }
            info(li_url, list_name, hea)
    except:
        classify(url, fname)
        # break


def info(url, fname, head):
    try:
        html = requests.get(url, headers=headers, timeout=2).text
        req = re.compile(r'.*>(\d+)</span></a><a')
        max_page = req.search(html).group(1)
        for i in range(1, int(max_page)+1):
            info_url = url + '/'+str(i)
            info_html = requests.get(info_url, headers=headers, timeout=2).text
            html_ele = etree.HTML(info_html)
            img_url = html_ele.xpath('//div[@class="main-image"]/p/a/img/@src')[0]
            a = img_url.split('/')[-1]
            print(fname+a)
            if not os.path.exists(fname + str(a)):
                download(img_url, fname, head)
            else:
                print('文件存在跳过')
        # break
    except:
        info(url, fname, head)


def download(url, fname, head):
    a = url.split('/')[-1]
    try:
        data = requests.get(url, headers=head, timeout=2).content
        with open(fname + str(a), 'wb') as f:
            f.write(data)
            f.close()
            print('%s下载完成' % a)

    except Exception as e:
        print(str(e))
    except:
        print('超时,重试中...')
        download(url, fname, head)


if __name__ == '__main__':
    index()
