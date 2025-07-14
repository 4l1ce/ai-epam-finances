# 💬 Chat with EPAM Financial Report (2024)

A console-based AI assistant that lets you chat with EPAM Systems' Q4 and full-year 2024 financial data — including text, tables, and infographic images — using GPT and Retrieval-Augmented Generation (RAG).

---

## 📌 Features

- ✅ Extracts and chunks financial report data from a live webpage (PR Newswire)
- ✅ Downloads **tables, HTML content, and infographic images**
- ✅ Runs **OCR** on images using Tesseract to capture embedded numbers or insights
- ✅ Uses **FAISS** for in-memory vector similarity search
- ✅ Supports multi-turn, console-based conversation
- ✅ Uses **OpenAI GPT-4** to generate contextual answers
- ✅ Optionally displays source chunks when relevant

---

## 🧱 Architectural Overview

```txt
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
