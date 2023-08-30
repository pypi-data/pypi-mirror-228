import unittest

from web_utils import (fetch_url, strip_html_markup, InvalidURLException, InsecureURLException)


class TestWebUtils(unittest.IsolatedAsyncioTestCase):

    async def test_invalid_url(self):
        with self.assertRaises(InvalidURLException):
            await fetch_url("not-a-valid-url")

    async def test_insecure_url(self):
        with self.assertRaises(InsecureURLException):
            await fetch_url("http://insecure.com")

    async def test_strip_html_markup(self):
        clean_content = strip_html_markup("<div>Hello</div>")
        self.assertEqual(clean_content, "Hello")

    async def test_fetch_url(self):
        url = 'https://digitalheretic.substack.com/p/claude2-constitutional-hologram'
        core_content = await fetch_url(url)
        clean_content = strip_html_markup(core_content)
        self.assertIsNotNone(clean_content)
        self.assertIn('Constitutional Hallucination', clean_content)

    async def test_fetch_url_search(self):
        url = 'https://digitalheretic.substack.com/p/claude2-constitutional-hologram'
        search_content = await fetch_url(url, div_class='single-post')
        clean_content = strip_html_markup(search_content)
        self.assertIsNotNone(clean_content)


if __name__ == '__main__':
    unittest.main()
