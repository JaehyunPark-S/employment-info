import requests
from bs4 import BeautifulSoup
from recruits import models
from users import models as user_models

user = user_models.User.objects.get(username="jaehyun@jj.hh")
URL = f"https://www.stackoverflow.com/jobs?q=python&sort=i"


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)


def extract_job(html):
    try:
        image = html.find("img", {"class": "bar-sm"})["src"]
    except Exception:
        image = "/static/img/company.png"
    title = html.find("h2", {"class": "mb4"}).find("a")["title"]
    company, location = html.find("h3", {"class": "mb4"}).find_all(
        "span", recursive=False
    )
    company = company.get_text(strip=True).strip("\n")
    location = location.get_text(strip=True).strip("-").strip(" \r").strip("\n")
    job_id = html["data-jobid"]
    return {
        "title": title,
        "company": company,
        "location": location,
        "apply_link": f"https://stackoverflow.com/jobs/{job_id}",
        "image": image,
    }


def extract_jobs(last_page):
    for page in range(last_page):
        print(f"Scrapping SO: Page: {page}")
        result = requests.get(f"{URL}&pg={page + 1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        for result in results:
            job = extract_job(result)
            try:
                models.Recruit.objects.get(
                    title=job["title"],
                    company=job["company"],
                    link=job["apply_link"],
                )
            except models.Recruit.DoesNotExist:
                print("Does Not Exist", job["title"], job["apply_link"])
                models.Recruit.objects.create(
                    title=job["title"],
                    company=job["company"],
                    location=job["location"],
                    link=job["apply_link"],
                    image=job["image"],
                    host=user,
                )
    return print("Success")
