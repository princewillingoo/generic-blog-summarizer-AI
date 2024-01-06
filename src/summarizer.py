from bs4 import BeautifulSoup
from scrapingbee import ScrapingBeeClient
from markdownify import markdownify as md
from markdownify import MarkdownConverter

from openai import OpenAI
import re
import subprocess
import tiktoken

import os
from urllib.parse import urlparse
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

bee_client = ScrapingBeeClient(api_key=(os.environ.get("BEE_KEY")))
ai_client = OpenAI(
    api_key=os.environ.get("OPENAI_KEY"),
)


tags_to_remove = [
    "footer",
    "style",
    "iframe",
    "script",
    "link",
    "form",
    "header",
    "noscript",
    "section",
    "nav",
    "g",
    "svg",
    "ellipse",
    "defs",
    "clippath",
]

#########################


def get_blog_html(url, client):
    bee_response = client.get(url)
    print("Response HTTP Status Code: ", bee_response.status_code)

    return bee_response.status_code, bee_response.text


def get_base_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


def remove_tags(html_content, tags_to_remove, url):
    def should_remove(tag):
        return (
            tag.name == "a"
            and tag.get("href")
            and re.search(re.escape(get_base_url(url)), tag["href"])
        )

    soup = BeautifulSoup(html_content, "html.parser")

    for tag_name in tags_to_remove:
        while soup.find(tag_name):
            soup.find(tag_name).decompose()

    for tag in soup.find_all(should_remove):
        tag.decompose()

    html_body = BeautifulSoup(str(soup.body), "html.parser")

    return html_body


def md_bs4(body, **options):
    return MarkdownConverter(**options).convert_soup(body)


#################


def num_tokens_in_content(content: str, model_name: str) -> int:
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(content))
    return num_tokens


def generate_blog_summary(content: str, model_name: str, max_tokens: int) -> str:
    prompt = f"Please provide a coherent and complete summary for the following blog content:\n{content}\n"

    # Generate a summary request to the OpenAI client
    response = ai_client.completions.create(
        model=model_name, prompt=prompt, max_tokens=max_tokens
    )

    generated_summary = response.choices[0].text.strip()
    print(generated_summary)
    return generated_summary


if __name__ == "__main__":
    URL = "https://earthly.dev/blog/golang-errors/"
    GPT_MODEL = "gpt-3.5-turbo-instruct"

    _, html_doc = get_blog_html(url=URL, client=bee_client)
    html_body = remove_tags(html_content=html_doc, tags_to_remove=tags_to_remove, url=URL)
    markdown_content = md_bs4(body=html_body)

    with open(f"./data/blog-post.md", "w") as file:
        # Write the Markdown content to the file
        file.write(markdown_content)

    subprocess.Popen(f"mdformat ./data/blog-post.md", shell=True)

    with open(
        f"./data/blog-post.md",
        "r",
        encoding="utf-8",
    ) as file:
        lines = file.readlines()

        content = "".join(lines)
    print(content)

    if num_tokens_in_content(content, "gpt-3.5-turbo-instruct") > 3500:
        total_length = len(content)
        middle_index = total_length // 2

        content_part1 = content[:middle_index]
        content_part2 = content[middle_index:]

        summary_part1 = generate_blog_summary(
            content_part1, "gpt-3.5-turbo-instruct", 1500
        )
        summary_part2 = generate_blog_summary(
            content_part2, "gpt-3.5-turbo-instruct", 1500
        )

        with open("./data/summary.txt", "a", encoding="utf-8") as file:
            file.write(f"{summary_part1}/n{summary_part2}")
    else:
        summary = generate_blog_summary(content, "gpt-3.5-turbo-instruct", 500)
        with open("./data/summary.txt", "w", encoding="utf-8") as file:
            file.write(summary)
