import requests
import re
import json
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from tqdm import tqdm
import warnings
import sys

def get_problem(url: str) -> str:
    def elems2data(cur_url: str, elems: list, markdown = True) -> list[dict]:
        graphs = []
        texts = ''
        for elem in elems:
            if markdown:        # if use markdown format
                if bs := elem.find_all('b'):    # bold
                    for ele in bs:
                        ele.replace_with(f'**{ele.string}**')
                if links := elem.find_all('a'): # hyperref
                    for ele in links:
                        if ele.string and 'href' in ele.attrs:
                            ele.replace_with(f'[{ele.string}]({ele["href"]})')
                for hx in 3, 4:
                    if elem.name == f'h{hx}': # head
                        elem.string = (f'{"#" * hx} {elem.get_text()}\n')
            if imgs := elem.find_all('img', class_=['latex', 'latexcenter']):   # latex equatoin
                for img in imgs:
                    img.replace_with(img['alt'])
            elif imgs := elem.find_all('img'):  # graphs
                graphs += [urljoin(cur_url, img['src']) for img in imgs]
            if text := elem.get_text():
                texts += text
        return {'graphs': graphs, 'text': texts}

    def valid_subtitle(subtitle: str) -> bool:
        return (re.search(r'solution', subtitle, re.I) \
            or re.search(r'problem', subtitle, re.I)) \
        and not re.search(r'video', subtitle, re.I)

    problem_html = requests.get(url).content.decode('utf-8')
    soup = BeautifulSoup(problem_html, 'html.parser')
    inner_div = soup.find('div', class_='mw-parser-output')
    if toc := inner_div.find('div', id='toc'):
        toc.extract()   # remove toc

    data = {'Problem': None, 'Solutions': []}
    for h2 in inner_div.find_all('h2'):         # find all h2
        subtitle = h2.get_text().strip()        # get subtitle text
        if not valid_subtitle(subtitle):
            continue
        content = []    # list of contents led by this subtitle
        for sibling in h2.find_next_siblings():
            if sibling.name == "h2":
                break   # stop at next subtitle
            content.append(sibling)

        ret = elems2data(url, content)
        if re.search(r'solution', subtitle, re.I):    # is this section a solution?
            data['Solutions'].append(ret)
        elif re.search(r'problem', subtitle, re.I):
            data['Problem'] = ret
        else:
            data[subtitle] = ret
            warnings.warn('Unknown Subtitle Type!', UserWarning)
    return data

if __name__ == "__main__":
    main_page_url = r'https://artofproblemsolving.com/wiki/index.php/IMO_Problems_and_Solutions'
    output_filename = 'data.json'
    if len(sys.argv) > 2:
        warnings.warn('Too Many Arguments', UserWarning)
        exit(0)
    elif len(sys.argv) == 2:
        output_filename = sys.argv[1]

    main_page_html = requests.get(main_page_url).content.decode('utf-8')
    problem_reg = re.compile(r'(/wiki/index.php/(\d{4})_IMO_Problems/Problem_(\d+))', re.M)
    problem_urls = problem_reg.findall(main_page_html)

    print(f'{len(problem_urls)} Problems')
    print(f'Write to: {output_filename}')

    data = dict()
    for url, year, no in tqdm(problem_urls):
        absolute_url = urljoin(main_page_url, url)
        if not year in data:
            data[year] = dict()
        if not no in data[year]:
            data[year][no] = dict()
        data[year][no] = get_problem(absolute_url)
        # break
    with open(output_filename, 'w', encoding='utf-8') as fd:
        fd.write(json.dumps(data))
