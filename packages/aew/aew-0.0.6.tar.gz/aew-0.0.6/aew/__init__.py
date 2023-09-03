import functools
import logging
import re
from dataclasses import dataclass
from typing import Optional

import requests
from bs4 import BeautifulSoup
from dateutil.parser import ParserError
from dateutil.parser import parse as dateutil_parse

__version__ = "0.0.6"

URL = "https://www.allelitewrestling.com/blog"

logger = logging.getLogger(__name__)


def _date_or_none(date: str) -> Optional[str]:
    """
    Returns a date string or None if it fails to parse
    """
    try:
        return dateutil_parse(date).date()
    except ParserError:
        return None


@dataclass
class Post:
    url: str
    title: str
    image_url: str
    aew: "AEW"

    def __post_init__(self):
        """
        Set the date based off the title having 'for ' in it

        For example: AEW Dynamite Preview for July 5, 2023
        Another case: AEW Rampage - 09/01/23
        """
        self.date = None
        if "for " in self.title:
            self.date = _date_or_none(self.title.split("for ")[1])

        if self.date is None and " - " in self.title:
            self.date = _date_or_none(self.title.split(" - ")[1])

    def get_strong_text(self) -> str:
        """
        Example:
            BLIND ELIMINATOR TAG TEAMTOURNAMENT QUARTER-FINAL...
            AEW International Champion Orange Cassidy & Darby Allin
            vs.
            Keith Lee & Swerve Strickland
            BLIND ELIMINATOR TAG TEAMTOURNAMENT QUARTER-FINAL...
            AEW World Champion MJF & Adam Cole in action!
            OWEN HART FOUNDATION WOMEN'S TOURNAMENT QUARTER-FINAL MATCH...
            Dr. Britt Baker D.M.D vs. The Outcasts' Ruby Soho
            ONE-ON-ONE...
            Kenny Omega vs. The BCC's Wheeler Yuta
            MOXLEY HAS SOMETHING TO SAY...
            JERICHO SPEAKS...

        We assume that ... means we should put an extra newline above it for readability
        """
        soup = self.aew.get(self.url)
        highlights = soup.find_all("strong")
        ret_text = ""
        for highlight in highlights:
            stripped_text = highlight.text.strip()
            if stripped_text.endswith("..."):
                ret_text += "\n"
            ret_text += stripped_text + "\n"
        return ret_text.replace("  ", "")


class AEW:
    """
    Object for working with the allelitewrestling.com website's posts
    """

    def __init__(self, blog_url: str = URL):
        """
        Initializer sets up a reusable session
        """
        self.blog_url = blog_url
        self.session = requests.Session()

    @functools.cache
    def get(self, url: str) -> BeautifulSoup:
        """
        Performs a GET, raises on status code errors and returns a BeautifulSoup object
        """
        result = self.session.get(url)
        result.raise_for_status()
        return BeautifulSoup(result.text, "html.parser")

    def _get_title_from_url(self, url: str) -> str:
        """
        GETs the given URL and returns the post title via the class: blog-post-title-font.
        If that fails, use the end of the URL
        """
        soup = self.get(url)
        for element in soup.find_all("span", {"class": "blog-post-title-font"}):
            return element.text

        logger.warning(f"Could not find title for {url} in content")

        return url.split("/")[-1].replace("-", " ").title().replace("Aew", "AEW")

    def _resize_image_url_to_16x9(self, image_url: str) -> str:
        """
        Example: https://static.wixstatic.com/media/815952_0d4b056ce8504b21baa6d6982641943e~mv2.jpg/v1/fill/w_454,h_341,fp_0.50_0.50,q_90,enc_auto/815952_0d4b056ce8504b21baa6d6982641943e~mv2.jpg

        We change w_X,h_Y to w_1920,h_1080
        """
        return re.sub(r"w_\d+,h_\d+", "w_1920,h_1080", image_url)

    def get_posts(self) -> list[Post]:
        """
        Walks the blog page and returns a list of Post objects via some heuristics
        """
        soup = self.get(self.blog_url)
        all_links = soup.find_all("a", href=True)

        posts = []
        for link in all_links:
            href = link.get("href", "")
            if "/post/" in href:
                url = href
                title = self._get_title_from_url(url)
                image_url = soup.find("img", {"alt": title}).get("src")
                if image_url:
                    image_url = self._resize_image_url_to_16x9(image_url)

                posts.append(Post(url=url, title=title, image_url=image_url, aew=self))

        return posts


if __name__ == "__main__":
    from pprint import pprint

    self = AEW()
    pcs = self.get_posts()
    pprint(pcs)
