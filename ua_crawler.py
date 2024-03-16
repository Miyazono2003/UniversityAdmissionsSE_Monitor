import os
import random
import platform
import argparse
from time import sleep

import requests
from plyer import notification
import logging
import colorlog
from bs4 import BeautifulSoup

USER_AGENT_LIST = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
]
USER_AGENT = random.choice(USER_AGENT_LIST)
headers = {"user-agent": USER_AGENT}
s = requests.Session()
s.trust_env = False

log_colors_config = {
    "DEBUG": "white",  # cyan white
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "bold_red",
}

logger = logging.getLogger("logger_name")

console_handler = logging.StreamHandler()
file_handler = logging.FileHandler(
    filename="UniversityAdmissions.txt", mode="a", encoding="utf8"
)

logger.setLevel(logging.DEBUG)
console_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.DEBUG)

file_formatter = logging.Formatter(
    fmt="[%(asctime)s] : %(message)s", datefmt="%b-%d %H:%M"
)
console_formatter = colorlog.ColoredFormatter(
    fmt="%(log_color)s[%(asctime)s] : %(message)s",
    datefmt="%b-%d %H:%M",
    log_colors=log_colors_config,
)
console_handler.setFormatter(console_formatter)
file_handler.setFormatter(file_formatter)
if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

parser = argparse.ArgumentParser(description="University Admissions Crawler")
parser.add_argument(
    "-u",
    "--username",
    type=str,
    help="Username for universityadmissions.se",
    required=True,
)
parser.add_argument(
    "-p",
    "--password",
    type=str,
    help="Password for universityadmissions.se",
    required=True,
)
parser.add_argument(
    "-i",
    "--interval",
    type=int,
    help="Refresh interval in seconds",
    default=300,
    required=False,
)


def clear():
    sys = platform.system()
    if sys == "Windows":
        os.system("cls")
    elif sys == "Linux" or sys == "Darwin":
        os.system("clear")


if __name__ == "__main__":
    # clear()
    args = parser.parse_args()
    params = {
        "username": args.username,
        "password": args.password,
        "url": "/intl/mypages",
    }

    application_status = ["", "", "", ""]
    while 42:
        response = s.post(
            "https://www.universityadmissions.se/intl/loginajax",
            headers=headers,
            params=params,
            verify=False,
        )
        if response.text != "/intl/mypages":
            logger.error(response.text)
            input("Press Any Key to Exit...")
            exit(0)
        else:
            logger.info("Login Success!")
        response = s.get(
            "https://www.universityadmissions.se/intl/mypages",
            headers=headers,
            verify=False,
        )
        soup = BeautifulSoup(response.text, "html.parser")
        if soup.head is None:
            continue
        if soup.head.title is None:
            continue
        if soup.head.title.text != "My applications - Universityadmissions.se":
            continue
        courses = soup.find_all("div", class_="course")
        for i, course in enumerate(courses):
            course_name = course.find(
                "h3", class_="coursehead_desktop heading4 coursename moreinfolink"
            ).text.strip()
            course_uni = (
                course.find("span", class_="appl_fontsmall").text.split(",")[1].strip()
            )
            course_status = course.find("div", class_="statusblock").text.strip()
            if application_status[i] != course_status:
                if application_status[i] != "":
                    logger.warning("STATUS CHANGED!!!")
                logger.info(course_name)
                logger.info("\t" + course_uni)
                for course_status_lines in course_status.split("\n"):
                    logger.info("\t" + course_status_lines)
                print()
                if notification.notify is None:
                    continue
                notification.notify(
                    title="STATUS CHANGED!!!",
                    message=course_status + ", " + course_name + " | " + course_uni,
                    app_icon=None,
                    timeout=300,
                )
                application_status[i] = course_status
        sleep(args.interval)
