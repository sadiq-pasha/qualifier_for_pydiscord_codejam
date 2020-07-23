import datetime
import importlib
import unittest
from unittest import mock

import qualifier


class T100BasicTests(unittest.TestCase):
    """Tests for the basic requirements."""

    def setUp(self) -> None:
        """Create a new Article instance before running each test."""
        self.title = "Rapunzel"
        self.author = "The Brothers Grimm"
        self.content = "There were once a man and a woman who had long in vain wished for a child."
        self.publication_date = datetime.datetime(1812, 12, 20, 11, 11, 9)

        self.article = qualifier.Article(
            title=self.title,
            author=self.author,
            content=self.content,
            publication_date=self.publication_date
        )

    def test_101_instantiation(self):
        """The parameters given to __init__ should be assigned to attributes with the same names."""
        for attribute in ("title", "author", "content", "publication_date"):
            with self.subTest(attribute=attribute):
                self.assertTrue(
                    hasattr(self.article, attribute),
                    msg=f"The Article instance has no `{attribute}` attribute"
                )
                self.assertEqual(getattr(self, attribute), getattr(self.article, attribute))

    def test_102_repr(self):
        """The repr should be in a specific format, which includes the title, author, and date."""
        actual_repr = repr(self.article)
        expected_repr = (
            "<Article title='Rapunzel' author='The Brothers Grimm' "
            "publication_date='1812-12-20T11:11:09'>"
        )
        self.assertEqual(expected_repr, actual_repr)

    def test_103_len(self):
        """Using len(article) should return the article's content's length."""
        self.assertTrue(hasattr(self.article, "__len__"), msg="Article has no `__len__` method.")
        self.assertEqual(len(self.article.content), len(self.article))

    def test_104_short_introduction(self):
        """short_introduction should truncate at a space/newline to at most n_characters."""
        contents = (
            (self.content, 'There were once a', 20),
            ("The mother of Hans said: 'Whither away, Hans?'", "The mother of Hans said:", 27),
            ("'What!' said he, ‘is that the way you thank me?", "'What!'", 11),
            ("joined the party.\nSoon afterwards", "joined the party.", 18),
        )

        self.assertTrue(
            hasattr(self.article, "short_introduction"),
            msg="Article has no `short_introduction` method."
        )

        for content, expected, n in contents:
            with self.subTest(content=content, expected=expected, n=n):
                self.article.content = content
                actual = self.article.short_introduction(n_characters=n)
                self.assertEqual(expected, actual)

    def test_105_most_common_words(self):
        """most_common_words should return a dictionary of the n_words most common words."""
        contents = (
            (self.content, {'a': 3, 'there': 1, 'were': 1, 'once': 1, 'man': 1}, 5),
            ("'I know I'm not stupid,'", {"i": 2, "know": 1, "m": 1}, 3),
            ("'Magnificent,' said the two officials", {"magnificent": 1, "said": 1}, 2),
            ("of his.\nHis whole", {"his": 2, "of": 1}, 2),
            ("Am I a fool?", {}, 0),
            ("All the town",  {"all": 1, "the": 1, "town": 1}, 9372)
        )

        self.assertTrue(
            hasattr(self.article, "most_common_words"),
            msg="Article has no `most_common_words` method."
        )

        for content, expected, n in contents:
            with self.subTest(content=content, expected=expected, n=n):
                self.article.content = content
                actual = self.article.most_common_words(n)
                self.assertEqual(expected, actual)


class T110AdditionalBasicTests(unittest.TestCase):
    """Additional tests for the basic requirements."""

    def setUp(self) -> None:
        """Create a new Article instance before running each test."""
        self.title = "Rapunzel"
        self.author = "The Brothers Grimm"
        self.content = "There were once a man and a woman who had long in vain wished for a child."
        self.publication_date = datetime.datetime(1812, 12, 20, 11, 11, 9)

        self.article = qualifier.Article(
            title=self.title,
            author=self.author,
            content=self.content,
            publication_date=self.publication_date
        )

    has_short_introduction = hasattr(qualifier.Article, "short_introduction")

    @unittest.skipUnless(has_short_introduction, reason="short_introduction not implemented")
    def test_111_short_introduction_only_breaks_on_spaces_newlines(self):
        """short_introduction should only break on space/newline characters."""
        contents = (
            ("Hello there,\twho are you?", "Hello", 15),
            ("Why not?\fThat's why!", "Why", 14),
        )

        for content, expected, n in contents:
            with self.subTest(content=content, expected=expected, n=n):
                self.article.content = content
                actual = self.article.short_introduction(n_characters=n)
                self.assertEqual(expected, actual)

    @unittest.skipUnless(has_short_introduction, reason="short_introduction not implemented")
    def test_112_short_introduction_respects_whitespace_characters(self):
        """short_introduction should not 'collapse' or 'fold' whitespace within `n_chararcters`."""
        contents = (
            ("Round about, round about,\nLo and behold!", "Round about, round about,\nLo", 28),
            ("There was   once a queen", "There was   once a", 20),
        )

        for content, expected, n in contents:
            with self.subTest(content=content, expected=expected, n=n):
                self.article.content = content
                actual = self.article.short_introduction(n_characters=n)
                self.assertEqual(expected, actual)

    @unittest.skipUnless(has_short_introduction, reason="short_introduction not implemented")
    def test_113_short_introduction_checks_n_characters_plus_one_for_space_newline_char(self):
        """short_introduction should look for a space/newline in n_characters+1."""
        contents = (
            ("'What!' said he, ‘is that the way you thank me?", "'What!' said", 12),
            ("joined the party.\nSoon afterwards", "joined the party.", 17),
        )

        self.assertTrue(
            hasattr(self.article, "short_introduction"),
            msg="Article has no `short_introduction` method."
        )

        for content, expected, n in contents:
            with self.subTest(content=content, expected=expected, n=n):
                self.article.content = content
                actual = self.article.short_introduction(n_characters=n)
                self.assertEqual(expected, actual)

    has_most_common_words = hasattr(qualifier.Article, "most_common_words")

    @unittest.skipUnless(has_most_common_words, reason="most_common_words not implemented")
    def test_114_most_common_words_should_only_count_alphabetic_words(self):
        """most_common_words should only count alphabetic words."""
        contents = (
            ("It's 8PM!", {"it": 1, "s": 1, "pm": 1}, 3),
            (
                "5 little ducks went out one day and 5 little ducks came back",
                {'little': 2, 'ducks': 2, 'went': 1, 'out': 1, 'one': 1},
                5
            ),
        )

        for content, expected, n in contents:
            with self.subTest(content=content, expected=expected, n=n):
                self.article.content = content
                actual = self.article.most_common_words(n)
                self.assertEqual(expected, actual)

    @unittest.skipUnless(has_most_common_words, reason="most_common_words not implemented")
    def test_115_most_common_words_returns_in_the_correct_order(self):
        """most_common_words should return a dictionary in the right order."""
        contents = (
            (
                "All the ducks are swimming in the water",
                {'the': 2, 'all': 1, 'ducks': 1, 'are': 1, 'swimming': 1},
                5,
            ),
            (
                "Not once, but twice; yes, twice, not once",
                {'not': 2, 'once': 2, 'twice': 2, 'but': 1, 'yes': 1},
                5,
            )

        )

        for content, expected, n in contents:
            with self.subTest(content=content, expected=expected, n=n):
                self.article.content = content
                actual = self.article.most_common_words(n)
                self.assertEqual(list(expected.items()), list(actual.items()))


class T200IntermediateTests(unittest.TestCase):
    """Tests for the intermediate requirements."""

    def test_201_unique_id(self):
        """New Articles should be assigned a unique, sequential ID starting at 0."""
        importlib.reload(qualifier)
        articles = []

        for _ in range(5):
            article = qualifier.Article(
                title="a", author="b", content="c", publication_date=mock.Mock(datetime.datetime)
            )
            articles.append(article)

        # Assert in a separate loop to ensure that new articles didn't affect previous IDs.
        for expected_id, article in enumerate(articles):
            self.assertTrue(hasattr(article, "id"), msg="`Article` object has no `id` attribute")
            self.assertEqual(expected_id, article.id)

    @mock.patch("qualifier.datetime")
    def test_202_last_edited(self, local_datetime):
        """last_edited attribute should update to the current time when the content changes."""
        article = qualifier.Article(
            title="a", author="b", content="c", publication_date=mock.Mock(datetime.datetime)
        )

        self.assertTrue(
            hasattr(article, "last_edited"),
            msg="`Article` object has no `last_edited` attribute"
        )

        self.assertIsNone(article.last_edited, "Initial value of last_edited should be None")

        # Set twice to account for both "import datetime" and "from datetime import datetime"
        side_effects = (
            datetime.datetime(2019, 10, 1, 12, 1, 12),
            datetime.datetime(2019, 11, 3, 3, 2, 5),
        )
        local_datetime.now.side_effect = side_effects
        local_datetime.datetime.now.side_effect = side_effects

        article.content = "'I know I'm not stupid,' the man thought,"
        self.assertEqual(side_effects[0], article.last_edited)

        article.content = "'Magnificent,' said the two officials"
        self.assertEqual(side_effects[1], article.last_edited)

    def test_203_sort(self):
        """Articles should be inherently sortable by their publication date."""
        kwargs = {"title": "a", "author": "b", "content": "c"}
        articles = [
            qualifier.Article(**kwargs, publication_date=datetime.datetime(2001, 7, 5)),
            qualifier.Article(**kwargs, publication_date=datetime.datetime(1837, 4, 7)),
            qualifier.Article(**kwargs, publication_date=datetime.datetime(2015, 8, 20)),
            qualifier.Article(**kwargs, publication_date=datetime.datetime(1837, 4, 7)),
        ]

        expected = [articles[1], articles[3], articles[0], articles[2]]
        try:
            actual = sorted(articles)
        except TypeError:
            self.fail("`Article` does not support sorting.")
        self.assertSequenceEqual(expected, actual)


class T210AdditionalIntermediateTests(unittest.TestCase):
    """Additional tests for the intermediate requirements."""

    def test_211_id_should_set_on_creation_not_access(self):
        """IDs should be assigned when the Article is instantiated."""
        importlib.reload(qualifier)
        articles = []

        for _ in range(5):
            article = qualifier.Article(
                title="a", author="b", content="c", publication_date=mock.Mock(datetime.datetime)
            )
            articles.append(article)

        # Check articles in reverse creation order
        for expected_id, article in reversed(tuple(enumerate(articles))):
            self.assertTrue(hasattr(article, "id"), msg="`Article` object has no `id` attribute")
            self.assertEqual(expected_id, article.id)

    def test_212_last_edited_should_stay_none_after_updating_other_attributes(self):
        """last_edited attribute should still be `None` after changing non-content attributes."""
        article = qualifier.Article(
            title="b", author="c", content="d", publication_date=mock.Mock(datetime.datetime)
        )

        self.assertTrue(
            hasattr(article, "last_edited"),
            msg="`Article` object has no `last_edited` attribute"
        )

        self.assertIsNone(article.last_edited, "Initial value of last_edited should be None")

        # We need to make sure to set correct types to account for solutions
        # that use the ArticleField descriptor.
        new_values = (
            ("title", "one"),
            ("author", "two"),
            ("publication_date", mock.Mock(datetime.datetime))
        )

        for attribute, new_value in new_values:
            try:
                setattr(article, attribute, new_value)
            except AttributeError:
                # We did not explicitly state that the attributes have to be
                # mutable, so I guess making them immutable is another way to
                # make sure that `last_edited` only changes when `content` is
                # changed.
                continue
            else:
                self.assertIsNone(article.last_edited, "Value of last_edited should still be None")

    @mock.patch("qualifier.datetime")
    def test_213_last_edited_should_not_change_when_updating_other_attributes(self, local_datetime):
        """last_edited attribute should not change after another attribute gets updated."""
        article = qualifier.Article(
            title="x", author="y", content="z", publication_date=mock.Mock(datetime.datetime)
        )

        self.assertTrue(
            hasattr(article, "last_edited"),
            msg="`Article` object has no `last_edited` attribute"
        )

        self.assertIsNone(article.last_edited, "Initial value of last_edited should be None")

        # Set twice to account for both "import datetime" and "from datetime import datetime"
        side_effects = (
            datetime.datetime(2019, 1, 1, 12, 1, 12),
            datetime.datetime(2019, 1, 2, 3, 2, 5),
            datetime.datetime(2019, 1, 3, 3, 2, 5),
            datetime.datetime(2019, 1, 4, 3, 2, 5),
        )
        local_datetime.now.side_effect = side_effects
        local_datetime.datetime.now.side_effect = side_effects

        article.content = "You know what's odd? A flying elephant, that's odd!"
        self.assertEqual(side_effects[0], article.last_edited)

        # We need to make sure to set correct types to account for solutions
        # that use the ArticleField descriptor.
        new_values = (
            ("title", "Dumbo"),
            ("author", "The White Elephant"),
            ("publication_date", mock.Mock(datetime.datetime))
        )

        for attribute, new_value in new_values:
            try:
                setattr(article, attribute, new_value)
            except AttributeError:
                # We did not explicitly state that the attributes have to be
                # mutable, so I guess making them immutable is another way to
                # make sure that `last_edited` only changes when `content` is
                # changed.
                continue
            else:
                self.assertEqual(side_effects[0], article.last_edited)

    @mock.patch("qualifier.datetime")
    def test_214_last_edited_should_be_unique_for_each_article(self, local_datetime):
        """Each Article instance should have its own `last_edited` field."""
        article_one = qualifier.Article(
            title="one", author="een", content="en", publication_date=mock.Mock(datetime.datetime)
        )
        article_two = qualifier.Article(
            title="two", author="twee", content="to", publication_date=mock.Mock(datetime.datetime)
        )
        self.assertTrue(
            hasattr(article_one, "last_edited"),
            msg="`Article` object has no `last_edited` attribute"
        )
        self.assertIsNone(article_one.last_edited, "Initial value of last_edited should be None")
        self.assertIsNone(article_two.last_edited, "Initial value of last_edited should be None")

        # Set twice to account for both "import datetime" and "from datetime import datetime"
        side_effects = (
            datetime.datetime(2019, 2, 1, 12, 1, 12),
            datetime.datetime(2019, 2, 2, 3, 2, 5),
        )
        local_datetime.now.side_effect = side_effects
        local_datetime.datetime.now.side_effect = side_effects

        article_one.content = "one one"
        self.assertEqual(article_one.last_edited, side_effects[0])
        self.assertIsNone(
            article_two.last_edited,
            "last_edited for article_two should still be None"
        )

        article_two.content = "two two"
        self.assertEqual(article_one.last_edited, side_effects[0])
        self.assertEqual(article_two.last_edited, side_effects[1])


run_advanced = hasattr(qualifier, "ArticleField") and hasattr(qualifier.ArticleField, "__set__")


@unittest.skipUnless(run_advanced, reason="No valid ArticleField class found.")
class T300AdvancedTests(unittest.TestCase):
    """Tests for the advanced requirements."""

    def setUp(self) -> None:
        """Before running each test, instantiate some classes which use an ArticleField."""
        class TestArticle:
            """Test class which uses an ArticleField."""
            attribute = qualifier.ArticleField(field_type=int)

        self.article = TestArticle()
        self.article_2 = TestArticle()

    def test_301_descriptor_properly_validates_values(self):
        """The ArticleField descriptor successfully get and set a value of a valid type."""
        class CustomInt(int):
            """int subclass used to test that the descriptor considers subclasses valid."""

        values = (10, CustomInt(20))
        for value in values:
            with self.subTest(value=value):
                self.article.attribute = value
                self.assertEqual(
                    value,
                    self.article.attribute,
                    msg="The attribute value is not equal to the value that was assigned to it."
                )

    def test_302_descriptor_raises_type_error(self):
        """Setting a value with an invalid type should raise a TypeError."""
        with self.assertRaises(TypeError, msg="Setting an incorrect type should raise a TypeError"):
            self.article.attribute = "some string"

    def test_303_descriptor_values_are_separate(self):
        """Should store a separate value for each instance of a class using the descriptor."""
        self.article.attribute = 10
        self.article_2.attribute = 20

        self.assertEqual(10, self.article.attribute)
        self.assertEqual(20, self.article_2.attribute)

    def test_304_descriptor_type_error_message(self):
        """Should include the attribute's name, the expected type, and the received type."""
        with self.assertRaises(TypeError) as assertion_context:
            self.article.attribute = "some string"

        exception_message = str(assertion_context.exception)
        self.assertIn(
            "int",
            exception_message,
            msg="The exception message should include the expected type",
        )
        self.assertIn(
            "attribute",
            exception_message,
            msg="The exception message should include the name of the attribute",
        )
        self.assertIn(
            "str",
            exception_message,
            msg="The exception message should include the received type",
        )


@unittest.skipUnless(run_advanced, reason="No valid ArticleField class found.")
class T310AdditionalAdvancedTests(unittest.TestCase):
    """Additional tests for the advanced requirements."""

    def setUp(self) -> None:
        """Before running each test, instantiate some classes which use an ArticleField."""
        class MyClass:
            """Test class which uses an ArticleField."""
            name = qualifier.ArticleField(field_type=str)

        self.instance = MyClass()

    def test_311_descriptor_raises_attribute_error_for_unset_attribute(self):
        """Descriptor should raise an AttributeError if an attribute was not set yet."""
        with self.assertRaises(AttributeError):
            getattr(self.instance, "name")
