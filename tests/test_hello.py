import os
import types
import pytest
from unittest.mock import patch, MagicMock

import chat_epam_financials as app

# --- Refactor app for testability ---

# Move main logic into functions (already done for most parts)
# Add injectable dependencies for fetch_report_page and parse_report

def test_fetch_report_page_success(monkeypatch):
    class MockResp:
        text = "<html>test</html>"
        def raise_for_status(self): pass
    monkeypatch.setattr(app.requests, "get", lambda url: MockResp())
    html = app.fetch_report_page("http://test")
    assert html == "<html>test</html>"

def test_fetch_report_page_failure(monkeypatch):
    class MockResp:
        def raise_for_status(self): raise Exception("fail")
    monkeypatch.setattr(app.requests, "get", lambda url: MockResp())
    with pytest.raises(Exception):
        app.fetch_report_page("http://fail")

def test_parse_report_extracts_paragraphs(tmp_path):
    html = "<html><body><p>Para1</p><p>Para2</p></body></html>"
    img_dir = tmp_path / "imgs"
    # Patch extract_images_from_soup to return 0, []
    with patch("chat_epam_financials.extract_images_from_soup", return_value=(0, [])):
        result = app.parse_report(html, img_dir=str(img_dir))
    assert "Para1" in result and "Para2" in result
    assert "[0 images saved to" in result

def test_parse_report_extracts_tables(tmp_path):
    html = """
    <html><body>
    <table>
        <tr><td>A</td><td>B</td></tr>
        <tr><td>1</td><td>2</td></tr>
    </table>
    </body></html>
    """
    img_dir = tmp_path / "imgs"
    # Patch Extractor and extract_images_from_soup
    with patch("chat_epam_financials.Extractor") as MockExtractor, \
         patch("chat_epam_financials.extract_images_from_soup", return_value=(0, [])):
        mock_ex = MagicMock()
        mock_ex.return_list.return_value = [[["A", "B"], ["1", "2"]]]
        MockExtractor.return_value = mock_ex
        result = app.parse_report(html, img_dir=str(img_dir))
    assert "A\tB" in result and "1\t2" in result

def test_build_vector_store(monkeypatch):
    # Patch OpenAIEmbeddings and FAISS
    class DummyEmb:
        pass
    class DummyFAISS:
        @staticmethod
        def from_texts(split, embedding): return ("vdb", split)
    monkeypatch.setattr(app, "OpenAIEmbeddings", lambda openai_api_key: DummyEmb())
    monkeypatch.setattr(app, "FAISS", DummyFAISS)
    text = "chunk1\n\nchunk2"
    vdb, split = app.build_vector_store(text)
    assert vdb == "vdb"
    assert isinstance(split, list)

def test_chat_loop_exit(monkeypatch):
    # Patch input to immediately exit
    vdb = MagicMock()
    texts = ["chunk1"]
    monkeypatch.setattr("builtins.input", lambda _: "exit")
    # Patch llm and other dependencies
    monkeypatch.setattr(app, "ChatOpenAI", lambda **kwargs: MagicMock(invoke=lambda msgs: MagicMock(content="bye")))
    with patch.object(app, "system_prompts", []):
        app.chat_loop(vdb, texts)  # Should exit immediately, no error

# --- End of tests ---