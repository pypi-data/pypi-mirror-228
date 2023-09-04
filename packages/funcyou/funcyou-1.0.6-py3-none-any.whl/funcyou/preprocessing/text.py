import json
import re
from collections import Counter
from functools import cache
from typing import Callable, Generator, List

__all__ = ['contracations_dict', 'text_cleaning', 'IntegerVectorizer', 'Vocabulary', 'fix_contractions']
# with open('contractions.json') as f:
#    contractions_dict = json.load(f)


contractions_dict = { 
"i ain't": "i am not ", 
"you ain't":"you are not" ,
"he ain't":"he is not", 
"she ain't":"she is not",
"it ain't":"it is not",
"they ain't":"they are not",
"aren't": "are/am not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"didn`t": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he had / he would",
"he'd've": "he would have",
"he'll": "he shall / he will",
"he'll've": "he shall have / he will have",
"he's": "he has / he is",
"how'd": "how did",
"how'd'y": "how do you",
"how'll": "how will",
"how's": "how has / how is / how does",
"I'd": "I had / I would",
"I'd've": "I would have",
"I'll": "I shall / I will",
"I'll've": "I shall have / I will have",
"I'm": "I am",
"I've": "I have",
"isn't": "is not",
"it'd": "it had / it would",
"it'd've": "it would have",
"it'll": "it shall / it will",
"it'll've": "it shall have / it will have",
"it's": "it has / it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"mightn't've": "might not have",
"must've": "must have",
"mustn't": "must not",
"mustn't've": "must not have",
"needn't": "need not",
"needn't've": "need not have",
"o'clock": "of the clock",
"oughtn't": "ought not",
"oughtn't've": "ought not have",
"shan't": "shall not",
"sha'n't": "shall not",
"shan't've": "shall not have",
"she'd": "she had / she would",
"she'd've": "she would have",
"she'll": "she shall / she will",
"she'll've": "she shall have / she will have",
"she's": "she has / she is",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've": "should not have",
"so've": "so have",
"so's": "so as / so is",
"that'd": "that would / that had",
"that'd've": "that would have",
"that's": "that has / that is",
"there'd": "there had / there would",
"there'd've": "there would have",
"there's": "there has / there is",
"they'd": "they had / they would",
"they'd've": "they would have",
"they'll": "they shall / they will",
"they'll've": "they shall have / they will have",
"they're": "they are",
"they've": "they have",
"to've": "to have",
"wasn't": "was not",
"we'd": "we had / we would",
"we'd've": "we would have",
"we'll": "we will",
"we'll've": "we will have",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what shall / what will",
"what'll've": "what shall have / what will have",
"what're": "what are",
"what's": "what has / what is",
"what've": "what have",
"when's": "when has / when is",
"when've": "when have",
"where'd": "where did",
"where's": "where has / where is",
"where've": "where have",
"who'll": "who shall / who will",
"who'll've": "who shall have / who will have",
"who's": "who has / who is",
"who've": "who have",
"why's": "why has / why is",
"why've": "why have",
"will've": "will have",
"won't": "will not",
"won't've": "will not have",
"would've": "would have",
"wouldn't": "would not",
"wouldn't've": "would not have",
"y'all": "you all",
"y'all'd": "you all would",
"y'all'd've": "you all would have",
"y'all're": "you all are",
"y'all've": "you all have",
"you'd": "you had / you would",
"you'd've": "you would have",
"you'll": "you shall / you will",
"you'll've": "you shall have / you will have",
"you're": "you are",
"you've": "you have"
}

# very necessary function you can't tell differece between "’" and "'", I don't even have that symbol in my keyboard
def text_cleaning_apos(text):
    text = str(text)
    text = text.lower()
    text = re.sub("’", "'", text) # removing punctuation
    return text


# FUNCTIONS TO EXPAND CONTRACTIONS
def fix_contractions(x):
    x = str(x).lower()
    xsplited = x.split(' ')
    exp_sentence = []
    for s in x.split():
        if s in contractions_dict.keys():

            s = contractions_dict.get(s)
        exp_sentence.append(s)

    return ' '.join(exp_sentence)

# Compile regex patterns for better performance
PUNCTUATION_REGEX = re.compile(r'[^a-zA-Z]')
SPECIAL_CHARACTERS_REGEX = re.compile(r'[#,@,&]')
DIGIT_REGEX = re.compile(r'\d+')
APOSTROPHE_S_REGEX = re.compile(r"'s")
WWW_REGEX = re.compile(r'w{3}')
URL_REGEX = re.compile(r'http\S+')
MULTIPLE_SPACES_REGEX = re.compile(r'\s+')
SINGLE_CHAR_REGEX = re.compile(r'\s+[a-zA-Z]\s+')

def text_cleaning(text):
    text = str(text)
    text = text.lower()
    text = PUNCTUATION_REGEX.sub(' ', text)  # Remove punctuation
    text = SPECIAL_CHARACTERS_REGEX.sub('', text)
    text = DIGIT_REGEX.sub('', text)
    text = APOSTROPHE_S_REGEX.sub('', text)
    text = WWW_REGEX.sub('', text)
    text = URL_REGEX.sub('', text)
    text = MULTIPLE_SPACES_REGEX.sub(' ', text)
    text = SINGLE_CHAR_REGEX.sub(' ', text)
    
    return text.strip()


class Vocabulary:
    
    """
    Class for storing a vocabulary of words and their corresponding indices.

    Args:
        special_tokens: A list of special tokens to add to the vocabulary .
        Note: special_tokens will not be processed by preprocessing function.

    Attributes:
        word_to_idx: A dictionary mapping words to their indices.
        idx_to_word: A dictionary mapping indices to their words.
        counter: A counter of the number of times each word appears in the data.
        UNK_TOKEN: The token for unknown words.
        UNK: The index of the UNK_TOKEN.
        PAD_TOKEN: The token for padding.
        PAD: The index of the PAD_TOKEN.
        vocab_size: The size of the vocabulary.

    Methods:
        build_vocab: Build the vocabulary from a dataset of text.
        add_word_to_vocab: Add a word to the vocabulary.
        __len__: Get the length of the vocabulary.
    """
    
    def __init__(self, special_tokens: list[str]):
        self.word_to_idx = {}
        self.idx_to_word = {}
        self.counter = Counter()
        
        self.UNK_TOKEN = '<UNK>'
        self.UNK = 1
        self.PAD_TOKEN = '<PAD>'
        self.PAD = 0
        
        self.word_to_idx[self.UNK_TOKEN] = self.UNK
        self.idx_to_word[self.UNK] = self.UNK_TOKEN

        self.word_to_idx[self.PAD_TOKEN] = self.PAD
        self.idx_to_word[self.PAD] = self.PAD_TOKEN

        self.vocab_size = 2
        for idx, token in enumerate(special_tokens, start=2):
            self.word_to_idx[token] = idx
            self.idx_to_word[idx] = token
            self.vocab_size += 1

    def build_vocab(self, tokenized_data, max_tokens, min_freq):
        # sourcery skip: dict-assign-update-to-union
        self.counter = Counter()
        for words in tokenized_data:
            self.counter.update(words)

        if max_tokens is not None:
            sorted_tokens = [word for word, _ in self.counter.most_common()]
            for word in sorted_tokens:
                if word not in self.word_to_idx:
                    self.add_word_to_vocab(word)

                if self.vocab_size == max_tokens:
                    break
        else:
            for word, freq in self.counter.items():
                if freq >= min_freq and word not in self.word_to_idx:
                    self.add_word_to_vocab(word)

    def add_word_to_vocab(self, word):
        self.word_to_idx[word] = self.vocab_size
        self.idx_to_word[self.vocab_size] = word
        self.vocab_size += 1

    def __len__(self):
        return self.vocab_size
    

class IntegerVectorizer:
    """
    Class for converting text data to integer vectors.

    Args:
        - tokenizer: A function that takes a string and returns a list of tokens. (default=None)
        - preprocessing_func: A function that takes a token and returns a processed token. (default=None)
        - max_tokens: The maximum number of tokens to keep in the vocabulary. (default=None)
        - min_freq: The minimum frequency of a token to keep in the vocabulary. (default=1)
        - special_tokens: A list of special tokens to add to the vocabulary. (default=None)
        - max_seq_length: The maximum sequence length for each input. (default=None)
        - pad_to_max: Whether to pad sequences to the maximum length. (default=False)

    Attributes:
        vocab: The vocabulary used to convert text to integers.
        tokenized_data: The tokenized data used to build the vocabulary.

    Methods:
        - adapt: Adapt the vectorizer to a dataset of text.
        - __call__: Convert text data to integer vectors.
        - preprocess_sentence: Preprocess a sentence for tokenization.
        - tokenize_data_generator: Tokenize a dataset of text and yield the tokens.
        - transform: Convert a dataset of text to integer vectors.
        - adjust_sequence_length: Adjust the length of a sequence to the maximum length.
        - reverse_transform: Convert integer vectors to text.
        - transform_generator: Convert a dataset of text to integer vectors in a generator.
        - reverse_transform_generator: Convert integer vectors to text in a generator.
    """
    
    def __init__(self, 
                 tokenizer: Callable[[str], list[str]] = None,
                 preprocessing_func: Callable[[str], str] = None,
                 max_tokens=None,
                 min_freq=1,
                 special_tokens: list[str] = None,
                 max_seq_length=None,
                 pad_to_max=False):
        
        self.min_freq = min_freq
        self.max_tokens = max_tokens
        self.max_seq_length = max_seq_length
        self.tokenizer = tokenizer
        self.preprocessing_func = preprocessing_func
        self.reserved_tokens = ['<UNK>', '<PAD>']
        self.special_tokens = [token for token in special_tokens if token not in self.reserved_tokens] if special_tokens else []
        self.pad_to_max = pad_to_max  # Store the argument

        self.vocab = Vocabulary(self.special_tokens)
        self.tokenized_data = []

    def adapt(self, data):
        self.tokenized_data = self.tokenize_data_generator(data)
        self.vocab.build_vocab(self.tokenized_data, self.max_tokens, self.min_freq)
        print('Vocab size:', len(self.vocab))

    def __call__(self, data, reverse=False, return_generator = True):
        if reverse:
            return self.reverse_transform_generator(data) if return_generator else self.reverse_transform(data)
        else:
            return self.transform_generator(data) if return_generator else self.transform(data)

    def preprocess_sentence(self, sentence):
        if self.preprocessing_func:
            words = sentence.split()
            preprocessed_words = [self.preprocessing_func(word) if word not in self.special_tokens else word for word in words]
            return " ".join(preprocessed_words)
        return sentence

    def tokenize_data_generator(self, data):
        for sentence in data:
            sentence = self.preprocess_sentence(sentence)
            yield self.tokenizer(sentence) if self.tokenizer else str(sentence).split()

    def transform(self, data:List[str]):
        
        if not isinstance(data, list):
            raise TypeError("Input data must be a list")
        
        self.tokenized_data = self.tokenize_data_generator(data)
        vectorized_data = []
        for sentence in self.tokenized_data:
            vectorized_sentence = [self.vocab.word_to_idx.get(word, self.vocab.UNK) for word in sentence]
            vectorized_sentence = self.adjust_sequence_length(vectorized_sentence)
            vectorized_data.append(vectorized_sentence)
        return vectorized_data

    def adjust_sequence_length(self, sequence: Generator[int, None, None]) -> list[int]:
        if self.max_seq_length is not None:
            
            if isinstance(sequence, Generator):                
                sequence = list(sequence)
                
            if len(sequence) < self.max_seq_length:
                if self.pad_to_max:
                    sequence += [self.vocab.PAD] * (self.max_seq_length - len(sequence))
            elif len(sequence) > self.max_seq_length:
                sequence = sequence[:self.max_seq_length]
            return sequence

    def reverse_transform(self, vectorized_data: list[list[int]]) -> list[str]:
        original_data = []
        for vector in vectorized_data:
            sentence = [self.vocab.idx_to_word[idx] for idx in vector if idx != self.vocab.PAD]
            original_data.append(" ".join(sentence).strip())
        return original_data


    def transform_generator(self, data: list[str]) -> Generator[list[int], None, None]:
        
        
        if not isinstance(data, list):
            raise TypeError("Input data must be a list")
        
        self.tokenized_data = self.tokenize_data_generator(data)
        for sentence in self.tokenized_data:
            vectorized_sentence = (self.vocab.word_to_idx.get(word, self.vocab.UNK) for word in sentence)
            vectorized_sentence = self.adjust_sequence_length(vectorized_sentence)
            yield list(vectorized_sentence)  # Convert the generator to a list for yielding

    def reverse_transform_generator(self, vectorized_data: list[list[int]]) -> Generator[str, None, None]:
        for vector in vectorized_data:
            sentence = (self.vocab.idx_to_word[idx] for idx in vector if idx != self.vocab.PAD)
            yield " ".join(sentence).strip()


def main():
	...
	
if __name__ == '__main__':
	main()
