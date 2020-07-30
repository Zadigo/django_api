import json

from nltk import NLTKWordTokenizer, TokenSearcher
from nltk import Counter
import ast

class Extractor:
    def __init__(self, data):
        if isinstance(data, str):
            try:
                data = self.read_from_string(data)
            except:
                raise ValueError('The string should contain a list.')
        
        self.data = data

        try:
            self.items = data['items']
        except:
            raise KeyError('The dictionnary should contain "items"')

        self.channel_titles = []
        self.parsed_items = []
        self.cursor = 0

        self._parse()
    
    def __len__(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)

    def __repr__(self):
        return f"{self.__class__.__name__}(channels={','.join(self.channel_titles)})"

    def __next__(self):
        try:
            item = self.parsed_items[self.cursor]
        except IndexError:
            raise StopIteration()
        self.cursor = self.cursor + 1
        return item

    def _parse(self):
        for item in self.data['items']:
            video_id = item['id']['videoId']
            snippet = item['snippet']

            self.parsed_items.append(
                [
                    snippet['channelId'],
                    snippet['channelTitle'],
                    snippet['title'],
                    snippet['description'],
                    [
                        video_id, 
                        self.full_url(video_id)
                    ]
                ]
            )
            
            self.channel_titles.append(
                snippet['channelTitle']
            )

    @property
    def total_results(self):
        return self.data['pageInfo']['totalResults']

    @staticmethod
    def full_url(video_id):
        return f'https://www.youtube.com/watch?v={video_id}'

    @property
    def get_snippets(self):
        return (item['snippet'] for item in self.data['items'])
    
    def get_titles(self, merge=False):
        if merge:
            return self.merge('title')
        return [snippet['title'] for snippet in self.get_snippets]

    def get_descriptions(self, merge=False):
        if merge:
            return self.merge('description')
        return [snippet['description'] for snippet in self.get_snippets]
    
    def get_tokens(self, only_titles=False):
        model = NLTKWordTokenizer()

        tokenized_titles = [model.tokenize(title) for title in self.get_titles()]
        tokenized_descriptions = [model.tokenize(description) for description in self.get_descriptions()]

        if only_titles:
            return tokenized_titles

        return tokenized_titles, tokenized_descriptions

    def merge(self, key, lists: list=None, func=None):
        merged = []
        for snippet in self.get_snippets:
            words = snippet[key].split(' ')
            for word in words:
                merged.append(word)
        return merged

    def merge_lists(self, *lists):
        merged = []
        for item in lists:
            for element in item:
                merged.append(element)
        return merged

    @classmethod
    def count_words(cls, items: list):
        counter = Counter(items)
        return counter.most_common(5)

    @staticmethod
    def read_from_string(s):
        return ast.literal_eval(s)
        

with open('C:\\Users\\Pende\\Documents\\myapps\\django_api\\youtube\\results.json', 'r') as f:
    data = json.load(f)

items = Extractor(data)
e = items.merge_lists(items.get_titles(), items.get_descriptions())
print(items.count_words(e))
