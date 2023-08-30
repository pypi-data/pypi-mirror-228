import unittest

from fictus.folder import Folder


class MyTestCase(unittest.TestCase):
    def test_parent(self):
        a = Folder("a")
        b = Folder("b")
        a.folder(b)
        self.assertEqual(
            a,
            b.parent,
        )
        self.assertEqual(None, a.parent)


if __name__ == "__main__":
    unittest.main()
