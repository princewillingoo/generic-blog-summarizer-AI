import streamlit as st
from scrapingbee import ScrapingBeeClient
from openai import OpenAI
import subprocess
import os
from dotenv import load_dotenv, find_dotenv

from summarizer import (
    generate_blog_summary,
    get_blog_html,
    md_bs4,
    num_tokens_in_content,
    remove_tags,
)

load_dotenv(find_dotenv())

bee_client = ScrapingBeeClient(api_key=(st.secrets["BEE_KEY"]))
ai_client = OpenAI(api_key=st.secrets["OPENAI_KEY"])

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

##----------------------- Streamlit App ------------------------##
st.title("Blog Summary Generator")

url_input = st.text_input("Enter the blog post URL:")

if url_input:
    st.text("Processing...")

    URL = url_input
    GPT_MODEL = "gpt-3.5-turbo-instruct"

    _, html_doc = get_blog_html(url=URL, client=bee_client)
    html_body = remove_tags(
        html_content=html_doc, tags_to_remove=tags_to_remove, url=URL
    )
    markdown_content = md_bs4(body=html_body)

    with open(f"./data/blog-post.md", "w") as file:
        file.write(markdown_content)

    subprocess.Popen(f"mdformat ./data/blog-post.md", shell=True)

    with open(
        f"./data/blog-post.md",
        "r",
        encoding="utf-8",
    ) as file:
        lines = file.readlines()
        content = "".join(lines)

    if num_tokens_in_content(content, GPT_MODEL) > 3500:
        total_length = len(content)
        middle_index = total_length // 2
        content_part1 = content[:middle_index]
        content_part2 = content[middle_index:]
        summary_part1 = generate_blog_summary(content_part1, GPT_MODEL, 1500)
        summary_part2 = generate_blog_summary(content_part2, GPT_MODEL, 1500)
        summary = f"{summary_part1}\n{summary_part2}"
    else:
        summary = generate_blog_summary(content, GPT_MODEL, 500)

    # Display the summary
    st.subheader("Generated Summary:")
    st.markdown(summary)
