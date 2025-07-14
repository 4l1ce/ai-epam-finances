import os
import requests
from bs4 import BeautifulSoup
from html_table_extractor.extractor import Extractor
from PIL import Image
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.schema import HumanMessage, AIMessage

from langchain.text_splitter import RecursiveCharacterTextSplitter

from Utils.image_extraction import extract_images_from_soup

# Config
PAGE_URL = "https://www.prnewswire.com/news-releases/epam-reports-results-for-fourth-quarter-and-full-year-2024-302381106.html"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

from langchain.schema import SystemMessage

system_prompts = [
    SystemMessage(
        content=(
        "You are a helpful financial assistant. "
        "Always pay attention to context around tables — especially notes like '(in thousands)' or '(in millions)'. "
        "If a table or note says values are in thousands, convert them correctly in your answer "
        "(e.g., 1,200,000 = $1.2 billion). "
        "Use the context to be accurate and clear in financial terms."
        "Don't add explanation about this logic in the answear"
            )
        ),
    SystemMessage(
        content = (
            "Answer the question below based on the context. "
            f"Only mention sources or reference chunks if the answer requires justification.\n\n"
            )
        )
]   

# Step 1: Fetch HTML
def fetch_report_page(url):
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text

# Step 2: Parse text, tables, images
def parse_report(html, img_dir="web_images"):
    os.makedirs(img_dir, exist_ok=True)
    soup = BeautifulSoup(html, "html.parser")
    chunks = []

    # Extract paragraphs
    for p in soup.select("p"):
        txt = p.get_text().strip()
        if txt:
            chunks.append(txt)

    # Extract tables
    for table in soup.find_all("table"):
        ex = Extractor(table)
        ex.parse()
        df = ex.return_list()[0]
        table_txt = "\n".join(["\t".join(row) for row in df])
        chunks.append(table_txt)

    # Images + OCR
    num_images, image_chunks = extract_images_from_soup(soup, img_dir)
    chunks.extend(image_chunks)
    chunks.append(f"[{num_images} images saved to {img_dir}]")

    return "\n\n".join(chunks)

# Step 3: Build vector store
def build_vector_store(text_chunks):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    split = splitter.split_text(text_chunks)
    emb = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    return FAISS.from_texts(split, embedding=emb), split

# Step 4: Chat loop
def chat_loop(vdb, texts):
    llm = ChatOpenAI(model="gpt-4", openai_api_key=OPENAI_API_KEY, temperature=0.2)
    history = []
    while True:
        q = input("You: ")
        if q.lower() in ("exit", "quit"):
            break
        docs = vdb.similarity_search_with_score(q, k=4)
        ctx = "\n\n---\n\n".join([d.page_content for d, _ in docs])
        prompt = f"Use context to answer:\n\n{ctx}\n\nQuestion: {q}"

        messages = system_prompts + history + [HumanMessage(content=prompt)]

        resp = llm.invoke(messages)
        print("\nAssistant:", resp.content, "\n")
        if any(word in resp.content.lower() for word in ["source", "according to", "based on the context", "as stated"]):
            print("📚 Sources (shown because model referenced them):\n")
            for i, (doc, score) in enumerate(docs):
                print(f"[Chunk {i+1} | Score: {score:.4f}]\n{doc.page_content[:300]}...\n{'-'*40}")

        history += [HumanMessage(content=q), AIMessage(content=resp.content)]

if __name__ == "__main__":
    html = fetch_report_page(PAGE_URL)
    text = parse_report(html)
    vdb, texts = build_vector_store(text)
    print("✅ Ready to chat with EPAM web report!\n(Type ‘exit’ to stop.)\n")
    chat_loop(vdb, texts)
