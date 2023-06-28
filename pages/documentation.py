import dash
from dash import html, dcc
import os
from dash.dependencies import Input, Output, State, MATCH, ALL

dash.register_page(__name__, path="/documentation", path_template="/documentation/<part>",
                   title="Alpine Fan F1 Dashboard | Documentation",
                   description="Have a better understanding of this Formula 1 dashboard or about Alpine Fan !",
                   image_url="https://alpinefan.robcorp.net/assets/images/logo.png")


def home():
    page = html.Div(className="doc-main", children=[
        html.A(href="/documentation/patch-notes", children=html.Img(src="/assets/images/banners/patch.svg")),
        html.A(href="/documentation/read-me", children=html.Img(src="/assets/images/banners/read.svg")),
        html.A(href="/documentation/explanations", children=html.Img(src="/assets/images/banners/explanations.svg")),
        html.A(href="/documentation/doc", children=html.Img(src="/assets/images/banners/doc.svg")),
    ])
    return page


def patch():
    patches = []

    def get_version(filename):
        version = filename.lstrip('v').rstrip('.md').replace('.', '')
        return tuple(map(int, version))

    folder_path = 'patchnotes/'

    files = os.listdir(folder_path)

    files = [file for file in files if file.endswith('.md')]

    sorted_files = sorted(files, key=get_version, reverse=True)
    i = 0
    for file in sorted_files:
        with open(os.path.join(folder_path, file), 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        img_name = file.replace(".md", "").replace(".", "-") + ".svg"
        patches.append(html.Div(
            children=[html.Img(src="/assets/images/banners/" + img_name),
                      dcc.Markdown(children=markdown_content)], className="md patchnote"))
        i += 1
    return html.Div(className="content patch", children=patches)

def read():
    with open('README.md', 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    return html.Div(className="content centered", children=dcc.Markdown(children=markdown_content, className="md read"))

def pres():
    with open('docs/process.md', 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    return html.Div(className="content centered", children=dcc.Markdown(children=markdown_content, className="md read"))


def layout(part=None, **other):
    if part is None:
        page = home()
    elif part == "patch-notes":
        page = patch()
    elif part == "read-me":
        page = read()
    elif part == "explanations":
        page = pres()
    else:
        page = home()
    return page

