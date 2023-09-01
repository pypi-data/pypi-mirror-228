"""Helpful validation methods"""
import os
import spacy

class BOVal:
    """Helpful validation methods"""
    def __init__(self):
        """Class constructor"""
        class_dir = os.path.dirname(os.path.realpath(__file__))
        model_path="language_models/en_core_web_sm/en_core_web_sm-3.6.0"
        self.nlp = spacy.load(os.path.join(class_dir, model_path))

    def check_value_not_empty(self, value):
        """Checks that text field was filled.
            Args: string
            Returns:
                True: if string not empty
                False: if string is empty
        """
        if value == '':
            return False

        return True

    def get_first_words(self, word_list):
        """Takes a word list and returns a string that has the first sentence or
        the first five words and three dots if the sentence is longer.

        Args:
            word_list (list)
            
        Returns:
            first_words (str)
        """

        first_words = f'{word_list[0]}'

        for word in word_list[1:5]:
            first_words += f' {word}'
            if any(mark in word for mark in ['.', '?', '!']):
                return first_words.strip('.')

        first_words.strip('.').strip(',')
        if len(word_list) > 5:
            first_words += '...'

        return first_words

    def value_is_min_length(self, value):
        """Checks that text field was filled with at least 8 characters.
            Args: string
            Returns:
                True: if string not empty and contains 8 characters without spaces
                False: if string is empty or to short
        """
        if not self.check_value_not_empty(value):
            return False
        value = value.replace(" ", "")
        if len(value) < 8:
            return False

        return True

    def sentence_is_min_length(self, value):
        """Checks that text field was filled with at least 3 words.
            Args: string
            Returns:
                True: if sentence not empty and contains at least 3 words
                False: if sentence is empty or to short
        """
        if not self.check_value_not_empty(value):
            return False
        words = value.strip()
        words = words.split(' ')
        if len(words) < 3:
            return False

        return True

    def value_not_contains_symbols(self, value):
        """Checks that text field was filled without special symbols.
            Args: string
            Returns:
                True: if string not contains special symbols
                False: if string contains special symbols
        """
        special_characters = ['[','{','@','</','\\','\"','(\'','(\"','()','t(', '<', '>']
        if any(symbol in value for symbol in special_characters):
            return False

        return True

    def value_not_empty_or_contains_symbols(self, value):
        """Checks that text field was filled without special symbols.
            Args: string
            Returns:
                True: if string not contains special symbols or empty
                False: if string is empty or contains special symbols
        """
        if not self.check_value_not_empty(value):
            return False
        special_characters = ['[','{','@','</','\\','\"','(\'','(\"','()','t(', '<', '>']
        if any(symbol in value for symbol in special_characters):
            return False

        return True

    def value_contain_predicate(self, value):
        '''Checks that string contains at least one predicate.
            Args:
                text(str)
            Return:
                true: if sentence contain at least one verb
                false: if value is empty or not contain verb
        '''
        if not self.check_value_not_empty(value):
            return False
        words = self.nlp(value)
        for word in words:
            if word.tag_[0] == 'V':
                return True

        return False

    def value_contain_nlp_object(self, value):
        '''Checks that string contains at least one of the desired sentence elements.

            Args:
                text(str)
            Return:
                true: if sentence contain at least one object
                false: if value is empty or not contain object
        '''
        prep_object = 'pobj'
        direct_object = 'dobj'
        if not self.check_value_not_empty(value):
            return False
        words = self.nlp(value)
        for word in words:
            if word.tag_[0]!='V':
                if word.dep_ in (prep_object, direct_object):
                    return True

        return False

    def value_contain_nlp_subject(self, value):
        '''Checks that string contains at least one of the desired sentence elements.

            Args:
                text(str)
            Return:
                true: if sentence contain at least one subject
                false: if value is empty or not contain subject
        '''
        subject = 'nsubj'
        subject_passive = 'nsubjpass'
        if not self.check_value_not_empty(value):
            return False
        words = self.nlp(value)

        for word in words:
            if word.tag_[0] != 'V':
                if word.dep_ in (subject, subject_passive):
                    return True

        return False

    def lemmatization_of_value(self, value):
        ''' Creates list of lemmas from given text.

            Args:
                text(str)
            Return:
                list: list of lemmas
        '''
        words = self.nlp(value)
        lemmas = []
        for word in words:
            lemmas.append(word.lemma_)

        return lemmas

    def check_text_is_lemmatized(self, value):
        ''' Checks if given value is lemmatized.

            Args:
                value (str)
            Return:
                True: value is lemmatized
                False: value is not lemmatized
        '''
        lemmas = []
        if isinstance(value, str):
            lemmas = self.lemmatization_of_value(value)
            tokens = self.nlp.tokenizer(value)
            tokens = str(tokens).split(' ')
            if tokens == lemmas:
                return True
        if isinstance(value, list):
            for i in value:
                lemmas.append(self.lemmatization_of_value(i)[0])
            if value == lemmas:
                return True
        return False
