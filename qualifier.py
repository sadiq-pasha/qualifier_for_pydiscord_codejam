"""
Use this file to write your solution for the Summer Code Jam 2020 Qualifier.

Important notes for submission:

- Do not change the names of the two classes included below. The test suite we
  will use to test your submission relies on existence these two classes.

- You can leave the `ArticleField` class as-is if you do not wish to tackle the
  advanced requirements.

- Do not include "debug"-code in your submission. This means that you should
  remove all debug prints and other debug statements before you submit your
  solution.
"""
import datetime
import typing
from collections import Counter, OrderedDict
from functools import total_ordering


class ArticleField:
    """The `ArticleField` class for the Advanced Requirements."""

    def __init__(self, field_type):
        self.field_type = field_type

    def __get__(self, obj, objtype):
        #print('Retrieving', self.name)
        return self.val

    def __set__(self, obj, val):
        #print('Updating', self.name)
        if isinstance(val, self.field_type):
            self.val = val
        else:
            raise TypeError(f"expected\ an\ instance\ of\ type\ '{self.field_type.__name__}'\ for\ attribute\ 'change_this',\ got\ '{type(val).__name__}'\ instead")


@total_ordering
class Article:
    """The `Article` class you need to write for the qualifier."""
    identity = 0
    title = ArticleField(str)
    author = ArticleField(str)
    publication_date = ArticleField(datetime.datetime)

    def __init__(self, title: str, author: str,
                 publication_date: datetime.datetime, content: str):
        self.title = title
        self.author = author
        self.publication_date = publication_date
        self.content = content
        self.id = self.identity
        self.update()

    @property
    def content(self):
        # getter for attribute "content"
        return self._content

    @content.setter
    def content(self, value):
        # setter for attribute "content", creates 
        # creates and updates an attribute "last_edited"
        if 'last_edited' not in self.__dict__:
            self.last_edited = None
        else:
            self.last_edited = datetime.datetime.now()
        self._content = value

    @classmethod
    def update(cls):
        '''increment class variable 'identity' for every new instance'''
        cls.identity += 1
    
    '''comparison checks for total_ordering'''
    def __lt__(self, other):
        return self.publication_date < other.publication_date

    def __eq__(self,other):
        return self.publication_date == other.publication_date

    def __repr__(self):
        return(f"<Article title={repr(self.title)} author={repr(self.author)} publication_date={repr(self.publication_date.isoformat())}>")

    def __len__(self):
        '''Return len of content'''
        if isinstance(self.content, str):
            return len(self.content)

    def short_introduction(self, n_characters):
        '''return a sample string of content, not exceeding 'n' characters'''
        # if text is smaller than requested sample length, return complete text
        if n_characters >= len(self.content):
            return(self.content)
        # if 'nth' cuts a word, decrement 'n' till the closest whitespace
        while self.content[n_characters] not in [' ', '\n']:
            n_characters -= 1
        return(self.content[:n_characters])

    def most_common_words(self, n_words):
        '''return 'n' most common words in content as a dictionary, with frequency.
           1) case insensitive, return dictionary is lowercase
           2) all non alphabetical characters are used to split words
                (they're yield 2 words, 'they' and 're')
           3) if multiple words have same frequency:
                return dictionary has words in the order they appear'''
        lower_string = self.content.lower()
        temp_string = ''
        # Repalce all non alphabetical characters with a whitespace
        for index in range(len(lower_string)):
            if lower_string[index].isalpha():
                temp_string += lower_string[index]
            else:
                temp_string += ' '
        # split temp string and create a counter
        # use counter to create an ordered dictionary:
        # sort by frequency, sort in descending order
        dict_of_words = OrderedDict(sorted(Counter(temp_string.split()).items(), key=lambda occurences: occurences[1], reverse=True))
        # if requested amount of words is greater than number of unique words:
        # return dictionary
        if n_words >= len(dict_of_words):
            return (dict(dict_of_words))
        # trim dictionary of words to the right size and return
        else:
            for _ in range(len(dict_of_words) - n_words):
                dict_of_words.popitem()
            return (dict(dict_of_words))
