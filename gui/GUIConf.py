from tkinter.font import BOLD, ITALIC, Font
from functools import partial


TEST: str = "RSS_feeds_test.json"
SOURCE: str = "RSS_feeds.json"
BACKUP_DATA: str = "backup_data.data"

TREE_IMG_SIZE = 20
STAR = "starred"
NOT_STAR = "not-starred"
IMAGES: dict[str, str] = {
	STAR: "imgs/star.png",
	NOT_STAR: "imgs/notstar.png"
}

CONF_FILE = "conf.yaml"

RESULTS_WIDTH = 60
RESULTS_HEIGHT = 60

FONT_SIZE_BIG = 35
FONT_SIZE_MID = 25
FONT_SIZE = 14

FONT_HEADLINE = ("Verdana", FONT_SIZE_BIG)
FONT_MID = ("Verdana", FONT_SIZE_MID)
FONT_MID_BOLD = ("Verdana", FONT_SIZE_MID, BOLD)
FONT_MID_ITALIC = ("Verdana", FONT_SIZE_MID, ITALIC)
FONT_PARAGRAPH = ("Courier", FONT_SIZE)
FONT = ("Verdana", FONT_SIZE)
FONT_BOLD = ("Verdana", FONT_SIZE, BOLD)

def font_link_init():
    return Font(family="Verdana", size=FONT_SIZE, slant=ITALIC, underline=True)

RELIEF_TREE = 2
RELIEF_DETAIL = 2

MAX_TREE_LINE_WIDTH = 24
TREE_LINE_WIDTH = 22
SOME_FACTOR = 9
