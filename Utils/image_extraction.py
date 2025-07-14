import os
import requests
from bs4 import BeautifulSoup

from Utils.ocr_helper import extract_text_from_image

def extract_images_from_soup(soup, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    downloaded = 0
    seen = set()
    image_chunks = []

    def download_image(src):
        nonlocal downloaded
        if src in seen:
            return
        seen.add(src)
        if src.startswith("//"):
            src = "https:" + src
        if src.startswith("http"):
            try:
                r = requests.get(src)
                r.raise_for_status()
                ext = os.path.splitext(src.split("?")[0])[-1] or ".jpg"
                img_path = os.path.join(output_dir, f"img_{downloaded+1}{ext}")
                with open(img_path, "wb") as f:
                    f.write(r.content)
                downloaded += 1

                # OCR
                ocr_text = extract_text_from_image(img_path)
                if ocr_text:
                    chunk = f"[OCR from image {img_path}]\n{ocr_text}"
                    image_chunks.append(chunk)

            except Exception as e:
                print(f"⚠️ Failed to download {src}: {e}")

    # From <img> tags
    for img in soup.select("img"):
        src = img.get("src")
        if src:
            download_image(src)

    # From <noscript> fallback tags
    for ns in soup.select("noscript"):
        inner_html = ns.decode_contents()
        inner_soup = BeautifulSoup(inner_html, "html.parser")
        for img in inner_soup.find_all("img"):
            src = img.get("src")
            if src:
                download_image(src)

    # From og:image or meta tags
    og_img = soup.find("meta", property="og:image")
    if og_img and og_img.get("content"):
        download_image(og_img["content"])

    # From data-getimg or lazy-load attributes
    lazy_attrs = ["data-src", "data-getimg", "data-lazy", "data-image"]
    for tag in soup.find_all():
        for attr in lazy_attrs:
            src = tag.get(attr)
            if src:
                download_image(src)

    return downloaded, image_chunks