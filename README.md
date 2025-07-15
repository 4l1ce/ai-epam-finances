
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

### 0. Clone this repository

```bash
git clone https://github.com/your-username/ai-epam-finances.git
cd ai-epam-finances
```

### 1. Create a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

Install system tools:

```bash
# macOS
brew install tesseract
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
python chat_epam_financials.py
```

---

## Example Usage

### Example 1:
***You:***  
`Can you compare EPAM revenue in 2023 and 2024?`

***Assistant:***  
```
In 2023, EPAM's revenue was $4.690 billion. In 2024, the revenue increased slightly to $4.728 billion.
```

### Example 2:
***You:***  
`What does the infographic say about revenue growth?`

***Assistant:***  
```
The infographic indicates that the Q4 revenues for EPAM in 2024 were $1.248 billion, 
representing a 7.9% year-over-year growth. The organic year-over-year growth was 1.0%. 
For Q1 2025, the projected revenues are in the range of $1.275 billion to $1.290 billion, 
indicating a 10% year-over-year growth at the midpoint of the range.
```

### Example 3:
***You:***  
`What is an outlook for 2025? provide sources`

***Assistant:***  
```
The outlook for EPAM in 2025 is as follows: 
For the first quarter, the expected revenue growth is 10.0%. 
For the full year, the expected revenue growth ranges between 10.0% and 14.0%. 
However, when adjusted for the impact of foreign exchange rates (1.4% for Q1 and 0.9% for the full year) 
and inorganic revenue growth (-11.4% for Q1 and -9.9% for the full year), 
the revenue growth on an organic constant currency basis is expected to be 0% for the first quarter 
and between 1.0% and 5.0% for the full year. 

The company also mentions a focus on investing in talent, advanced technological and consulting capabilities, 
and the integration of recent acquisitions to capture market share once demand returns to more normalized levels. 

These estimates are based on the company's current expectations and estimates of future events and trends,
as presented in the company's forward-looking statements and the reconciliation table provided.

📚 Sources (shown because model referenced them):

[Chunk 1 | Score: 0.4431]
EPAM Systems, Inc. Press Release, Feb. 20, 2025; Infographic: EPAM Systems, Inc. 2025 Outlook
----------------------------------------
[Chunk 2 | Score: 0.4498]
Reconciliation of expected revenue growth on a GAAP basis to expected revenue growth
on an organic constant currency basis is presented in the table below:

First Quarter 2025

Full Year 2025

(at midpoint of  range)

Revenue growth

10.0 %

10.0% to 14.0%

Foreign exchange rates impact

1.4 %

0.9 ...
----------------------------------------
[Chunk 3 | Score: 0.4697]
as clients balance their cost focus with the need to accelerate their transformational and GenAI journeys.
We see a strong need to continue to invest in our talent, advanced technological and consulting capabilities,
and the integration of recent acquisitions to best position ourselves to capture ma...
----------------------------------------
```
---

## Key Components

- `chat_epam_financials.py`: Main entry point for the CLI
- `extract_images_from_soup()`: Downloads and OCRs all infographic images
- `extract_text_from_image()`: Runs Tesseract OCR on images
- `parse_report()`: Combines text, tables, and OCR'd image text into a single context document
- `FAISS`: In-memory vector database for fast similarity search
- `langchain + OpenAI GPT-4`: Handles multi-turn reasoning

---
