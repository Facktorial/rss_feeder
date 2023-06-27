from my_types import PostRecord, FeedRecord, Sandbox
from typing import Callable, Dict, List, Set
import rich.progress
from rich.markdown import Markdown
from rich.panel import Panel
from rich.tree import Tree
from rich.table import Table
from rich import box
from rich.prompt import Prompt

import asyncio

import curses

import os


def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

def render(data: List[FeedRecord], sandbox):
    render_topics(sandbox)
    render_data(data, sandbox)

def render_topics(sandbox):
    clearConsole()

    left : str = '<' if (sandbox.cursor_pos != 0) else ''
    right : str = '>' if (len(sandbox.topics) - 1 != sandbox.cursor_pos) else ''

    sandbox.console.print(Markdown(f"# {[x for x in sandbox.topics]}"))
    sandbox.console.print(Markdown(
        f"# {left} " \
        f"{''.join(['-' for _ in range(sandbox.cursor_pos)])}" \
        f" ```{sandbox.topics[sandbox.cursor_pos]}``` " \
        f"{''.join(['-' for _ in range(len(sandbox.topics) -1 - sandbox.cursor_pos)])}"
        f" {right}"))

def render_data(data: List[FeedRecord], sandbox):
    tree = Tree("New posts")
    colors : Tuple[str, str] = ("cyan", "green")
    for x in data:
        if x.group == sandbox.topics[sandbox.cursor_pos]:
            table = Table(show_header=False)
            for i, post in enumerate(x.posts):
                table.add_row(f'[{colors[i % 2]}]{post.title}', post.link, post.published[:-6])
            tree.add(f'[gold1]{x.name} - {x.feed_link}').add(table)
    sandbox.console.print(tree) 


async def wrap(links_count: Dict[str, int], links_progress: Dict[str, int], key: str, func: Callable, sandbox):
    x = await func

    # clearConsole()

    links_progress[key] = links_progress.get(key, 0) + 1
    with rich.progress.Progress(
        "[progress.description]{task.description}",
        "[progress.percentage]{task.percentage:>3.0f}%",
        rich.progress.BarColumn(bar_width=None),
        rich.progress.TextColumn("{task.completed}/[green]{task.total}  "),
    ) as progress:
        download_tasks = [progress.add_task(f"[cyan]{k}", total=links_count[k]) for k, v in links_count.items()]
        _ = [progress.update(download_tasks[i], completed=v) for i, (_, v) in enumerate(links_progress.items())]

    return x

