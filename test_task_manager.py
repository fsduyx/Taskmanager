import os
import tempfile
import unittest

from StorageManager import StorageManager
from Task import Task
from TaskManager import TaskManager


class FakeInterface:
    def __init__(self):
        self.input = {"title": "", "description": "", "author": ""}
        self.selected = None
        self.confirm = True
        self.warnings = []
        self.messages = []
        self.shown = []

    def set_callbacks(self, **kwargs): pass
    def build(self): pass
    def run(self): pass
    def get_input(self): return dict(self.input)
    def clear_input(self): self.input = {"title": "", "description": "", "author": ""}
    def show_tasks(self, tasks, select=None): self.shown = list(tasks)
    def show_message(self, title, text): self.messages.append(text)
    def show_warning(self, title, text): self.warnings.append(text)
    def ask_confirm(self, title, text): return self.confirm
    def get_selected_index(self): return self.selected


class TestTask(unittest.TestCase):
    def test_dict_roundtrip(self):
        task = Task("A", "B", True, "C", id=3)
        self.assertEqual(Task.from_dict(task.to_dict()), task)

    def test_defaults(self):
        task = Task("A")
        self.assertFalse(task.status)
        self.assertEqual(task.author, "—")
        self.assertIsNone(task.id)


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.folder.name, "t.json")
        self.storage = StorageManager(self.path)

    def tearDown(self):
        self.folder.cleanup()

    def test_file_created(self):
        self.assertTrue(os.path.exists(self.path))
        self.assertEqual(self.storage.load(), [])

    def test_broken_file(self):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write("{не json")
        self.assertEqual(self.storage.load(), [])

    def test_crud(self):
        a, b = Task("A"), Task("B")
        self.storage.add(a)
        self.storage.add(b)
        self.assertEqual((a.id, b.id), (1, 2))
        self.storage.update(2, Task("B2", status=True))
        loaded = self.storage.load()
        self.assertEqual([t.title for t in loaded], ["A", "B2"])
        self.assertTrue(loaded[1].status)
        self.storage.delete(1)
        self.assertEqual([t.id for t in self.storage.load()], [2])

    def test_persist_between_instances(self):
        self.storage.add(Task("Дело"))
        self.assertEqual(StorageManager(self.path).load()[0].title, "Дело")


class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.ui = FakeInterface()
        storage = StorageManager(os.path.join(self.folder.name, "t.json"))
        self.tm = TaskManager(None, storage, self.ui)

    def tearDown(self):
        self.folder.cleanup()

    def test_create(self):
        self.ui.input = {"title": "Дело", "description": "d", "author": ""}
        self.tm.create_task()
        self.assertEqual(len(self.ui.shown), 1)
        self.assertEqual(self.ui.shown[0].author, "—")

    def test_create_empty_title(self):
        self.tm.create_task()
        self.assertEqual(len(self.ui.warnings), 1)
        self.assertEqual(self.tm.storage.load(), [])

    def test_edit_toggle_delete(self):
        self.ui.input = {"title": "A", "description": "", "author": "я"}
        self.tm.create_task()
        self.ui.selected = 0
        self.ui.input = {"title": "A2", "description": "x", "author": "я"}
        self.tm.edit_task()
        self.assertEqual(self.tm.storage.load()[0].title, "A2")
        self.tm.toggle_status()
        self.assertTrue(self.tm.storage.load()[0].status)
        self.ui.confirm = False
        self.tm.delete_task()
        self.assertEqual(len(self.tm.storage.load()), 1)
        self.ui.confirm = True
        self.tm.delete_task()
        self.assertEqual(self.tm.storage.load(), [])

    def test_no_selection(self):
        self.tm.edit_task()
        self.tm.delete_task()
        self.tm.toggle_status()
        self.assertEqual(len(self.ui.warnings), 3)


if __name__ == "__main__":
    unittest.main()
