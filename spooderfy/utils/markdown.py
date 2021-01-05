from functools import lru_cache


@lru_cache()
def load_md(file) -> str:
    with open(f"./spooderfy/pages/{file}.md") as file:
        return file.read()


@lru_cache()
def get_help(file) -> dict:
    out = {}
    for line in load_md(file).split("### "):
        title, desc = line.split("\n", maxsplit=1)
        out[title] = desc

    return out
