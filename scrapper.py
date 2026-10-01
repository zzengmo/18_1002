import requests
from bs4 import BeautifulSoup


def search_incruit(keyword):
    jobs = []

    url = f"https://search.incruit.com/list/search.asp?col=job&kw={keyword}"

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    lis = soup.find_all("li", class_="c_col")

    for li in lis:
        company = li.find("a", class_="cpname").text

        title = li.find(
            "div",
            class_="cell_mid"
        ).find(
            "div",
            class_="cl_top"
        ).find("a").text

        location = li.find(
            "div",
            class_="cl_md"
        ).find_all("span")[0].text

        link = li.find(
            "div",
            class_="cell_mid"
        ).find(
            "div",
            class_="cl_top"
        ).find("a").get("href")

        job_data = {
            "site": "인크루트",
            "company": company,
            "title": title,
            "location": location,
            "link": link
        }

        jobs.append(job_data)

    return jobs


def search_gamejob(keyword):
    jobs = []

    url = f"https://www.gamejob.co.kr/Recruit/joblist?menucode=searchtot&searchtype=all&searchstring={keyword}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table", class_="tblList")

    if table is None:
        return jobs

    tbody = table.find("tbody")

    if tbody is None:
        return jobs

    rows = tbody.find_all("tr")

    for row in rows:
        company_div = row.find("div", class_="company")
        title_div = row.find("div", class_="tit")

        if company_div is None or title_div is None:
            continue

        company_tag = company_div.find("strong")
        title_tag = title_div.find("a")
        info = title_div.find("p", class_="info")

        if company_tag is None or title_tag is None or info is None:
            continue

        company = company_tag.text.strip()
        title = title_tag.text.strip()

        spans = info.find_all("span")

        if len(spans) >= 3:
            location = spans[2].text.strip()
        else:
            location = ""

        link = title_tag.get("href")

        if link is not None:
            link = "https://www.gamejob.co.kr" + link

        job_data = {
            "site": "게임잡",
            "company": company,
            "title": title,
            "location": location,
            "link": link
        }

        jobs.append(job_data)

    return jobs