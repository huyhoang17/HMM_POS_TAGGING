class ReadFiles:

    def __init__(self, file_name):
        self.file_name = file_name
        # list of list of tuples of sentences.
        self.all_tuples = []

        # dictionary where key is the word and value is a set of all its tags
        self.word_tags = {}

        # set to hold the unique tags in the training corpus
        self.unique_tags = set()

    def word_tag_tuples(self):
        # Reading the data corpus
        with open(self.file_name, "r") as f:
            for line in f:
                # list of tuples for a sentence
                list_tuples_sentence = []
                tuple_words = line.split()

                # for word
                for tup in tuple_words:
                    split_word = tup.split('/')
                    split_word_word = "/".join(split_word[:-1])
                    split_word_tag = split_word[-1]

                    # saving the unique tags in the training data in the corpus
                    if split_word_tag not in self.unique_tags:
                        self.unique_tags.add(split_word_tag)

                    # tuple for word-tag pair
                    tuples_for_sentence = (split_word_word, split_word_tag)
                    # add the tuple to the list
                    list_tuples_sentence.append(tuples_for_sentence)

                    # adding the all the corresponding tags of a word to a dictionary
                    if split_word_word in self.word_tags:
                        tags_set = self.word_tags[split_word_word]
                        tags_set.add(split_word_tag)
                    else:
                        tags_set = set([split_word_tag])
                        self.word_tags[split_word_word] = tags_set

                # adding (*,*) tuple at the start of a sentence
                # for trigram transition probability computation
                # word-tag
                list_tuples_sentence.insert(0, ('*', '*'))
                list_tuples_sentence.insert(0, ('*', '*'))
                self.all_tuples.append(list_tuples_sentence)
        self.word_tags["*"] = "*"
        return self.all_tuples

    def word_raw(self):

        words_sents = []

        # Reading the raw text file
        with open(self.file_name, "r", encoding='utf-8') as f:
            for line in f:
                # list of tuples for a sentence
                words_sent = []

                words = line.split()
                for word in words:
                    words_sent.append(word)

                # adding (*,*) tuple at the start of a sentence
                # for trigram transition probability computation
                # word-tag
                words_sent.insert(0, ('*'))
                words_sent.insert(0, ('*'))

                words_sents.append(words_sent)

        return words_sents
