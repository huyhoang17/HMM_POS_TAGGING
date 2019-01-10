from math import log
import sys
import pickle

from read_data_from_file import ReadFiles


class CalProbabilities:
    def __init__(self):
        # dictionary to store the number of occurrences for a given word-tag combination
        # EX: ('Al', 'NNP'), 78), (('-', 'HYPH'), 643), (('Zaman', 'NNP'), 3)
        self.word_tag_count = {}

        # dictionary to store the number of occurrences for a tag.
        self.tag_count = {}

        # dictionary to store the number of occurrences of triplet or trigram of tags
        self.trigram_tags_count = {}

        # dictionary to store the number of occurrences of bigram tags
        self.bigram_tags_count = {}

        # dictionary to store the emission probability for a given word-tag combination
        self.emission_probabilities = {}

        # dictionary to store the transition probability for a given trigram combination
        self.transition_probabilities = {}

        # a dictionary containing all the tags for every word.
        # So key is a word and value is a set/list of tags
        self.word_tags_set = {}

        # a set of all unique tags in the training corpus
        self.unique_tags = set()

    # calculate the word-tag counts and word counts and populate the respective dictionaries
    def populate_count_dicts(self, filename):
        read_files = ReadFiles(filename)
        all_tuples = read_files.word_tag_tuples()
        self.word_tags_set = read_files.word_tags
        self.unique_tags = read_files.unique_tags
        for sentence in all_tuples:
            for i in range(2, len(sentence)):
                # populate word-tag dictionary
                if sentence[i] in self.word_tag_count:
                    self.word_tag_count[sentence[i]] += 1
                else:
                    self.word_tag_count[sentence[i]] = 1

                # populate tag count dictionary
                # index 0: word, 1: tag
                tag = sentence[i][1]
                self.tag_count[tag] = self.tag_count.get(tag, 0) + 1

                # make trigram by tag
                # EX: ('*', '*', 'NNP'), ('HYPH', 'NNP', ':'), ..
                words_trigram = (
                    sentence[i - 2][1],
                    sentence[i - 1][1],
                    sentence[i][1]
                )
                if words_trigram in self.trigram_tags_count:
                    self.trigram_tags_count[words_trigram] += 1
                else:
                    self.trigram_tags_count[words_trigram] = 1

                # make bigram by tag
                # EX: ('*', '*'), ('*', 'NNP'), ('NNP', 'HYPH')
                words_bigram = (
                    sentence[i - 2][1],
                    sentence[i - 1][1]
                )
                if words_bigram in self.bigram_tags_count:
                    self.bigram_tags_count[words_bigram] += 1
                else:
                    self.bigram_tags_count[words_bigram] = 1

    def _save(self):
        data = {
            "transition": self.transition_probabilities,
            "emission": self.emission_probabilities,
            "word2tags": self.word_tags_set,
            "unique_tags": self.unique_tags,
            "trigram": self.trigram_tags_count,
            "bigram": self.bigram_tags_count
        }

        with open("models/hmmmodel.pkl", "wb") as f:
            pickle.dump(data, f)

    def run(self, filename):
        self.populate_count_dicts(filename)
        self.calculate_emission_probabilities()
        self.calculate_transition_probabilities()
        self._save()

    # calculate emission probabilities
    # p(word/tag)
    def calculate_emission_probabilities(self):
        # getting (key, value) pair from dictionary word_tag_count
        for word_tag, word_tag_count in self.word_tag_count.items():
            # emission probability for a word-tag pair.
            # no. of occurrences of a given word-tag divided by no. of occurrences of the tag.
            self.emission_probabilities[word_tag] = log(
                float(word_tag_count) / float(self.tag_count[word_tag[1]]))

    # calculate transition probabilities - trigram probabilities - tag given previous two tags.
    def calculate_transition_probabilities(self):
        # getting trigram tuple(key) and  count (value) pair from dictionary
        for trigram_tuple, trigram_tuple_count in self.trigram_tags_count.items():
            # getting bigram count for denominator of probability
            bigram_count = self.bigram_tags_count[(
                trigram_tuple[0], trigram_tuple[1])]
            unique_tags_count = len(self.unique_tags)
            # transition probability
            # taking log probabilities
            # computations are less costly
            # adding one to numerator and unique tag counts to denominator for smoothing
            self.transition_probabilities[trigram_tuple] = log(
                float(trigram_tuple_count + 1) / float(bigram_count + unique_tags_count))


if __name__ == "__main__":
    filename = sys.argv[1]
    prob = CalProbabilities()
    prob.run(filename)
