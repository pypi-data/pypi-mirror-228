import pathlib
from datetime import date

import pytest
from bs4 import BeautifulSoup

from aew import AEW, Post, _date_or_none

HTML_DIR = (pathlib.Path(__file__).parent / "html").resolve()
SRC_DIR = (pathlib.Path(__file__).parent.parent).resolve()


def soup_from_file(filename: str) -> BeautifulSoup:
    return BeautifulSoup((HTML_DIR / filename).read_bytes(), "html.parser")


def test_date_or_none():
    assert _date_or_none("lolcats") is None
    assert _date_or_none("July 5, 2023") == date(2023, 7, 5)


@pytest.fixture(scope="function")
def local_aew():
    aew = AEW()

    def local_get(url: str) -> BeautifulSoup:
        if url == "https://www.allelitewrestling.com/blog":
            return soup_from_file("blog.html")
        elif "july-5" in url:
            return soup_from_file("preview_7_5_23.html")
        else:
            return soup_from_file("preview_7_1_23.html")

    aew.get = local_get
    yield aew


def test_get_posts(local_aew):
    posts = local_aew.get_posts()
    p1 = Post(
        url="https://www.allelitewrestling.com/post/aew-dynamite-preview-for-july-5-2023",
        title="AEW Dynamite Preview for July 5, 2023",
        image_url="https://static.wixstatic.com/media/815952_edc338480c5744059917f423e7ab0392~mv2.jpg/v1/fill/w_1920,h_1080,fp_0.50_0.50,q_90,enc_auto/815952_edc338480c5744059917f423e7ab0392~mv2.jpg",
        aew=local_aew,
    )
    assert p1 in posts
    p2 = Post(
        url="https://www.allelitewrestling.com/post/aew-collision-preview-for-july-1-2023",
        title="AEW Collision Preview for July 1, 2023",
        image_url="https://static.wixstatic.com/media/815952_6bb8f0d9607b4f1aa70ec9cbcb1e1aea~mv2.jpg/v1/fill/w_1920,h_1080,fp_0.50_0.50,q_90,enc_auto/815952_6bb8f0d9607b4f1aa70ec9cbcb1e1aea~mv2.jpg",
        aew=local_aew,
    )
    assert p2 in posts

    assert p1.date == date(2023, 7, 5)
    assert p2.date == date(2023, 7, 1)


def test_get_strong_text(local_aew):
    p1 = Post(
        url="https://www.allelitewrestling.com/post/aew-dynamite-preview-for-july-5-2023",
        title="AEW Dynamite Preview for July 5, 2023",
        image_url="https://static.wixstatic.com/media/815952_edc338480c5744059917f423e7ab0392~mv2.jpg/v1/fill/w_1920,h_1080,fp_0.50_0.50,q_90,enc_auto/815952_edc338480c5744059917f423e7ab0392~mv2.jpg",
        aew=local_aew,
    )

    assert (
        p1.get_strong_text()
        == """
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
"""
    )


def test_get_title_from_url_fallback(local_aew):
    local_aew.get = lambda url: BeautifulSoup()
    assert (
        local_aew._get_title_from_url(
            "https://www.allelitewrestling.com/post/aew-collision2-preview-for-july-1-2023"
        )
        == "AEW Collision2 Preview For July 1 2023"
    )


def test_post_post_init_sets_date():
    Post(
        url=None,
        title="AEW Dynamite Preview for July 5, 2023",
        image_url=None,
        aew=None,
    ).date == date(2023, 7, 5)
    Post(
        url=None,
        title="AEW Fight For The Fallen Preview 2023",
        image_url=None,
        aew=None,
    ).date is None
    Post(
        url=None, title="AEW Rampage - 09/01/23", image_url=None, aew=None
    ).date == date(2023, 9, 1)
