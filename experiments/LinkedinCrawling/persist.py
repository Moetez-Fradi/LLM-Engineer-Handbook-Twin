import re
from typing import List
from bs4 import BeautifulSoup
from DB.models.documents import UserDocument, PostDocument

with open(r"C:\Users\Moetez\Desktop\LLM Twin\llm-twin\experiments\LinkedinCrawling\output.html", "r", encoding="utf-8") as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, "lxml")

user = UserDocument.get_or_create(first_name="Moetez", last_name="Fradi")

post_documents: List[PostDocument] = []

h2_tags = soup.find_all("h2", string=lambda text: text and "Feed post number" in text)

for h2 in h2_tags:
    post_div = h2.find_next_sibling("div")
    if not post_div:
        continue

    # Extract main text: the longest span text
    all_spans = post_div.find_all("span")
    main_text = max((span.text.strip() for span in all_spans if span.text.strip()), key=len, default="")

    post_data = {"text": main_text}

    # Extract images and posters
    images = [img.get("src") for img in post_div.find_all("img") if img.get("src") and "media.licdn.com" in img.get("src")]
    posters = [video.get("poster") for video in post_div.find_all("video") if video.get("poster") and "media.licdn.com" in video.get("poster")]
    all_images = images + posters
    if all_images:
        post_data["images"] = all_images

    # Extract impressions
    strong_tag = post_div.find("strong")
    if strong_tag:
        impressions_str = strong_tag.text.strip().split()[0].replace(",", "")
        if impressions_str.isdigit():
            post_data["impressions"] = int(impressions_str)

    # Extract likes, comments, reposts
    buttons = post_div.find_all("button")
    for button in buttons:
        span = button.find("span")
        if span:
            btn_text = span.text.strip()
            if btn_text.isdigit():
                post_data["likes"] = int(btn_text)
            elif "comments" in btn_text:
                num_str = btn_text.split()[0]
                if num_str.isdigit():
                    post_data["comments"] = int(num_str)
            elif "repost" in btn_text.lower():
                num_str = btn_text.split()[0]
                if num_str.isdigit():
                    post_data["reposts"] = int(num_str)

    # Extract links from text
    link = None
    if main_text:
        urls = re.findall(r"https?://[^\s<>\"']+", main_text)
        if urls:
            post_data["links"] = urls
            link = urls[0]

    # Create PostDocument
    post_doc = PostDocument(
        content=post_data,
        platform="linkedin",
        author_id=user.id,
        author_full_name=user.full_name,
        image=all_images[0] if all_images else None,
        link=link,
    )
    post_documents.append(post_doc)

# Bulk insert
if post_documents:
    success = PostDocument.bulk_insert(post_documents)
    print(f"Bulk insert successful: {success}")
else:
    print("No posts found to insert.")