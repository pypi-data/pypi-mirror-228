# """
# threadsafe_generators.py

# This file contains a collection of classes aimed at providing thread-safe operations over generators 
# and iterables. 

# The utility of this module can be mainly seen in multi-threaded environments where generators or iterables 
# need to be consumed across threads without race conditions. Additionally, functionalities like character-based 
# iteration and accumulation are provided for enhanced flexibility.
# """


import threading
from collections import deque
from typing import Union, Iterator

class CharIterator:
    def __init__(self):
        self.items = []
        self._index = 0
        self._char_index = None
        self._current_iterator = None
        self.immediate_stop = threading.Event()
        self.iterated_text = ""

    def add(self, item: Union[str, Iterator[str]]) -> None:
        self.items.append(item)

    def stop(self):
        self.immediate_stop.set()        

    def __iter__(self) -> "CharIterator":
        return self

    def __next__(self) -> str:
        if self.immediate_stop.is_set():
            raise StopIteration
        
        while self._index < len(self.items):
            item = self.items[self._index]

            if isinstance(item, str):
                if self._char_index is None:
                    # we are just starting with this string
                    self._char_index = 0

                if self._char_index < len(item):
                    char = item[self._char_index]
                    self._char_index += 1
                    self.iterated_text += char
                    return char
                else:
                    self._char_index = None
                    self._index += 1
            else:
                # item is an iterator
                if self._current_iterator is None:
                    self._current_iterator = iter(item)
                
                try:
                    char = next(self._current_iterator)
                    self.iterated_text += char
                    return char
                except StopIteration:
                    self._current_iterator = None
                    self._index += 1

        raise StopIteration

# class TextSource:
#     """
#     Represents a source of text that can be either a string or an iterator.
#     """

#     def __init__(self, source: Union[str, Iterator[str]]):
#         """
#         Initialize the TextSource instance with the provided text source.

#         Args:
#             source (Union[str, Iterator[str]]): Source of the text, can be either a string or an iterator.
#         """
#         self.source = source
#         self.index = 0 if isinstance(source, str) else None

#     def next_char(self) -> Union[str, None]:
#         """
#         Retrieves the next character from the source.

#         Returns:
#             Union[str, None]: The next character from the source or None if no more characters are available.
#         """
#         if isinstance(self.source, str):
#             if self.index < len(self.source):
#                 char = self.source[self.index]
#                 self.index += 1
#                 return char
#         else:
#             try:
#                 return next(self.source)
#             except StopIteration:
#                 pass
#         return None

# class CharIterator:
#     """
#     Provides an iterator over characters from multiple text sources.
#     """

#     def __init__(self):
#         """
#         Initialize the CharIterator instance.
#         """
#         self.text_sources = deque()
#         self.current_text_source = None
#         self.stop_event = threading.Event()
#         self.iterated_chars = ""

#     def add(self, source: Union[str, Iterator[str]]) -> None:
#         """
#         Add a new text source to the iterator.

#         Args:
#             source (Union[str, Iterator[str]]): The text source to be added, can be either a string or an iterator.
#         """
#         self.text_sources.append(TextSource(source))

#     def stop(self) -> None:
#         """
#         Stops the character iterator, raising StopIteration for any future calls to __next__().
#         """
#         self.stop_event.set()

#     def _get_next_char(self) -> str:
#         """
#         Fetch the next character from the current text source or move to the next source if needed.

#         Returns:
#             str: The next character from the source.

#         Raises:
#             StopIteration: If there are no more characters left and the iterator is stopped.
#         """
#         print (f"_get_next_char")
#         while self.text_sources or self.current_text_source:
#             if self.stop_event.is_set():
#                 raise StopIteration

#             if self.current_text_source is None:
#                 print (f"pop source")
#                 self.current_text_source = self.text_sources.popleft()

#             print (f"source next_char")
#             char = self.current_text_source.next_char()
#             if char:
#                 self.iterated_chars += char
#                 return char
#             else:
#                 self.current_text_source = None

#         if self.stop_event.is_set():
#             raise StopIteration

#         raise StopIteration

#     def __iter__(self) -> "CharIterator":
#         """
#         Returns the iterator object itself.

#         Returns:
#             CharIterator: The instance of CharIterator.
#         """
#         return self

#     def __next__(self) -> str:
#         """
#         Fetch the next character from the iterator.

#         Returns:
#             str: The next character from the iterator.

#         Raises:
#             StopIteration: If the iterator is stopped or there are no more characters left.
#         """
#         if self.stop_event.is_set():
#             raise StopIteration

#         return self._get_next_char()

class AccumulatingThreadSafeGenerator:
    """
    A thread-safe generator that accumulates the iterated tokens into a text.
    """

    def __init__(self, gen_func):
        """
        Initialize the AccumulatingThreadSafeGenerator instance.

        Args:
            gen_func: The generator function to be used.
        """
        self.lock = threading.Lock()
        self.generator = gen_func
        self.exhausted = False
        self.iterated_text = ""

    def __iter__(self):
        """
        Returns the iterator object itself.

        Returns:
            AccumulatingThreadSafeGenerator: The instance of AccumulatingThreadSafeGenerator.
        """
        return self

    def __next__(self):
        """
        Fetch the next token from the generator in a thread-safe manner.

        Returns:
            The next item from the generator.

        Raises:
            StopIteration: If there are no more items left in the generator.
        """
        with self.lock:
            try:
                token = next(self.generator) 
                self.iterated_text += str(token)
                return token
            except StopIteration:
                self.exhausted = True
                raise

    def is_exhausted(self):
        """
        Check if the generator has been exhausted.

        Returns:
            bool: True if the generator is exhausted, False otherwise.
        """
        with self.lock:
            return self.exhausted

    def accumulated_text(self):
        """
        Retrieve the accumulated text from the iterated tokens.

        Returns:
            str: The accumulated text.
        """
        with self.lock:
            return self.iterated_text