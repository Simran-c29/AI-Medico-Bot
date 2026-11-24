import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from utils.vectorstore import VectorStore


class FakeRAG:
    def doctor_questions(self):
        return "What does this result mean?"


class AppControlsTests(unittest.TestCase):
    def create_app(self):
        app = AppTest.from_file("app.py").run(timeout=60)
        self.assertEqual(len(app.exception), 0)
        return app

    def test_clear_chat_removes_messages_and_retrieved_context(self):
        app = self.create_app()
        app.session_state["messages"] = [
            {"role": "user", "content": "Question"}
        ]
        app.session_state["retrieved_docs"] = [object()]

        next(
            button
            for button in app.sidebar.button
            if button.key == "clear_chat"
        ).click()
        app.run(timeout=60)

        self.assertEqual(app.session_state["messages"], [])
        self.assertEqual(app.session_state["retrieved_docs"], [])

    def test_delete_database_clears_session_and_deletes_selected_store(self):
        app = self.create_app()
        app.session_state["database_ready"] = True
        app.session_state["vector_db"] = "ChromaDB"
        app.session_state["pdf_name"] = "report.pdf"
        app.session_state["messages"] = [
            {"role": "user", "content": "Question"}
        ]

        with patch("utils.vectorstore.VectorStore.delete") as delete:
            next(
                button
                for button in app.sidebar.button
                if button.key == "delete_database"
            ).click()
            app.run(timeout=60)

        delete.assert_called_once_with(db_type="ChromaDB")
        self.assertFalse(app.session_state["database_ready"])
        self.assertEqual(app.session_state["vector_db"], "")
        self.assertEqual(app.session_state["pdf_name"], "")
        self.assertEqual(app.session_state["messages"], [])

    def test_doctor_questions_are_generated_from_ready_report(self):
        app = self.create_app()
        app.session_state["database_ready"] = True
        app.session_state["rag"] = FakeRAG()

        next(
            button
            for button in app.button
            if button.key == "generate_doctor_questions"
        ).click()
        app.run(timeout=60)

        self.assertEqual(
            app.session_state["doctor_questions"],
            "What does this result mean?",
        )

    def test_vector_store_delete_removes_only_selected_directory(self):
        with TemporaryDirectory() as directory:
            target = Path(directory) / "faiss_db"
            target.mkdir()
            (target / "index.bin").write_text("test", encoding="utf-8")

            store = VectorStore(embedding_model=None)
            store.faiss_path = str(target)
            store.delete("FAISS")

            self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main()
