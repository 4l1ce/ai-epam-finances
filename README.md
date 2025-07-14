
# Chat with EPAM Financial Report (2024)

A console-based AI assistant that lets you chat with EPAM Systems' Q4 and full-year 2024 financial data — including text, tables, and infographic images — using GPT and Retrieval-Augmented Generation (RAG).

---

## Features

- ✅ Extracts and chunks financial report data from a live webpage (PR Newswire)
- ✅ Downloads **tables, HTML content, and infographic images**
- ✅ Runs **OCR** on images using Tesseract to capture embedded numbers or insights
- ✅ Uses **FAISS** for in-memory vector similarity search
- ✅ Supports multi-turn, console-based conversation
- ✅ Uses **OpenAI GPT-4** to generate contextual answers
- ✅ Optionally displays source chunks when relevant

---

## Architectural Overview

```
                ┌────────────────────────────┐
                │   PR Newswire Webpage      │
                └────────────┬───────────────┘
                             │
                ┌────────────▼───────────────┐
                │     HTML Scraper           │
                │ (text + tables + images)   │
                └────────────┬───────────────┘
                             │
                ┌────────────▼───────────────┐
                │     OCR on Infographics    │
                │     (via Tesseract)        │
                └────────────┬───────────────┘
                             │
                ┌────────────▼───────────────┐
                │     Text Chunking          │
                └────────────┬───────────────┘
                             │
                ┌────────────▼───────────────┐
                │   FAISS Vector Store       │
                └────────────┬───────────────┘
                             │
                ┌────────────▼───────────────┐
                │     OpenAI GPT-4           │
                └────────────┬───────────────┘
                             │
                ┌────────────▼───────────────┐
                │  Interactive CLI Chat Loop │
                └────────────────────────────┘
```

---

## How to run

### 1. Clone this repository

```bash
git clone https://github.com/your-username/ai-epam-finances.git
cd ai-epam-finances
```

### 2. Install dependencies

Install system tools:

```bash
# macOS
brew install tesseract

# Debian/Ubuntu
sudo apt install tesseract-ocr
```

Install Python packages:

```bash
pip install -r requirements.txt
```

> Ensure you're using **Python 3.9+**

---

### 3. Set your OpenAI API key

You can use an environment variable:

```bash
export OPENAI_API_KEY=sk-...
```

Or add to `.env` and load it using `dotenv` (optional extension).

---

### 4. Run the chat app

```bash
python chat_epam_web.py
```

---

## Example Usage

```bash
You: What was EPAM’s revenue in Q4 2024?

Assistant: According to the context, EPAM reported revenue of $1.175 billion in Q4 2024. This figure was originally listed as "1,175,000" in a table marked "in thousands".

You: What does the infographic say about revenue growth?

Assistant: The image text indicates a year-over-year revenue decrease of 4.4% for Q4 2024.
```

---

## Key Components

- `chat_epam_web.py`: Main entry point for the CLI
- `extract_images_from_soup()`: Downloads and OCRs all infographic images
- `extract_text_from_image()`: Runs Tesseract OCR on images
- `parse_report()`: Combines text, tables, and OCR'd image text into a single context document
- `FAISS`: In-memory vector database for fast similarity search
- `langchain + OpenAI GPT-4`: Handles multi-turn reasoning

---
