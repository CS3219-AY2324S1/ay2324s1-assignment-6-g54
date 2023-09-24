from selenium import webdriver
from tempfile import mkdtemp
from selenium.webdriver.common.by import By

import requests
from bs4 import BeautifulSoup
import json
import time
import markdownify

def html_to_md(someHtml):
    change_dict = {
        "\n\n"  : "\n",
        "\n \n": "\n",
        "```"   : "",
        "\u00a0": ""
    }

    md_str = markdownify.markdownify(someHtml)
    for key in change_dict:
        md_str = md_str.replace(key, change_dict[key])
    return md_str.replace(":**\n\n\n", ":**\n").replace(":**\n\n", ":**\n").replace("\n\n\n\n**", "\n\n**")

def get_question_content(URL):
    page = requests.get(URL).content
    soup = BeautifulSoup(page, "html.parser")
    question_json = json.loads(soup.find(id="__NEXT_DATA__").text.strip())["props"]["pageProps"]["dehydratedState"]["queries"]

    title = []
    complexity = []
    description = []
    tags = []
    request = {}

    for info_list in question_json:
        main = info_list["state"]["data"]
        if "question" in main:
            info_item = main["question"]
            if "title" in info_item:
                title.append(info_item["title"])

            if "difficulty" in info_item:
                complexity.append(info_item["difficulty"])

            if "content" in info_item:
                description.append(info_item["content"])

            if "topicTags" in info_item:
                tagsList = info_item["topicTags"]
                for tag in tagsList:
                    tags.append(tag["name"])

    request["title"] = title[0]
    request["complexity"] = complexity[0].lower()
    request["categories"] = tags
    request["link"] = URL
    request["description"] = html_to_md(description[0])

    return request

def get_problem_links(ALGORITHMS_ENDPOINT_URL):
    page = requests.get(ALGORITHMS_ENDPOINT_URL).content
    problems_json = json.loads(page)

    links = []
    for child in problems_json["stat_status_pairs"]:
        # Only process free problems
        if not child["paid_only"]:
            question__title_slug = child["stat"]["question__title_slug"]
            question__article__slug = child["stat"]["question__article__slug"]
            question__title = child["stat"]["question__title"]
            frontend_question_id = child["stat"]["frontend_question_id"]
            difficulty = child["difficulty"]["level"]
            links.append(
                (question__title_slug, difficulty, frontend_question_id, question__title, question__article__slug))

    # Sort by problem id
    links = sorted(links, key=lambda x: (x[2])) #key=lambda x: (x[1], x[2]))
    return links

def setup():
    options = webdriver.ChromeOptions()
    service = webdriver.ChromeService("/opt/chromedriver")

    options.binary_location = '/opt/chrome/chrome'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    options.add_argument("--remote-debugging-port=9222")

    driver = webdriver.Chrome(options=options, service=service)
    return driver


def handler(event=None, context=None):
    driver = setup()

    LEETCODE_ALGORITHMS_URL = "https://leetcode.com/api/problems/algorithms/"
    ALGORITHMS_BASE_URL = "https://leetcode.com/problems/"

    links = get_problem_links(LEETCODE_ALGORITHMS_URL)
    question_data_list = []

    completed_upto = -1
    num_questions = 5
    if (event != None and isinstance(event, dict)):
        if 'completed_upto' in event:
            completed_upto = int(event['completed_upto'])
        if 'num_questions' in event:
            num_questions = int(event['num_questions'])

    try:
        for i in range(completed_upto + 1, min(len(links), completed_upto + 1 + num_questions)  ):
            question__title_slug, _, frontend_question_id, question__title, question__article__slug = links[i]
            url = ALGORITHMS_BASE_URL + question__title_slug
            questionInfo = get_question_content(url)
            questionInfo["frontend_question_id"] = frontend_question_id
            question_data_list.append(questionInfo)
            
            time.sleep(1) # Sleep for 1 secs between each problem
    except Exception as error:
        return {
            "response": 404,
            "error": error
        }
    
    driver.quit()
    # json.dumps(question_data_list)
    return {
        "response": 200,
        "questions": question_data_list
    }

