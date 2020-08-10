import requests
import lxml.html

def parser(login, password):
    ses = requests.Session()
    ses.headers.update({'Referer': "https://edu.tatar.ru/logon"})
    ses.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'})
    ses.post('https://edu.tatar.ru/logon', {'main_login': login, 'main_password': password})
    ses.get('https://edu.tatar.ru/start/logon-process')
    text = ses.get('https://edu.tatar.ru/user/diary/week').text
    tree = lxml.html.document_fromstring(text)
    dayy = 0
    days = [[tree.xpath('/html/body/div/div/div[2]/div/table/tbody/tr[1]/td[1]/div/span/text()')[0], []],
                [tree.xpath('/html/body/div/div/div[2]/div/table/tbody/tr[10]/td[1]/div/span/text()')[0], []],
                [tree.xpath('/html/body/div/div/div[2]/div/table/tbody/tr[19]/td[1]/div/span/text()')[0], []]]
    for i in range(2, len(tree.xpath('/html/body/div/div/div[2]/div/table/tbody/tr'))):
        if i % 9 == 0:
            dayy += 1
        if len(tree.xpath(f"/html/body/div/div/div[2]/div/table/tbody/tr[{i}]/td[@class='tt-subj']/div/text()")) > 0:
            days[dayy][1].append(
            {'sub':''.join(tree.xpath(f"/html/body/div/div/div[2]/div/table/tbody/tr[{i}]/td[@class='tt-subj']/div/text()")).replace('\t', ''),
            'task':''.join(tree.xpath(f"/html/body/div/div/div[2]/div/table/tbody/tr[{i}]/td[@class='tt-task']/div/text()")).replace('\t', ''),
            'mark':''.join(tree.xpath(f"/html/body/div/div/div[2]/div/table/tbody/tr[{i}]/td[@class='tt-mark']/div/text()"))})
    return days