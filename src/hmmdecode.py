import pickle
import sys
import math

from hmmlearn import ReadFiles


class ViterbiDecode:

    def __init__(self):

        # dictionary to store the emission probability for a given word-tag combination
        self.emission_probabilities = {}

        # dictionary to store the transition probability for a given trigram combination
        self.transition_probabilities = {}

        # dictionary where key is the word and value is a set of all its tags
        self.word_tags_set = {}

        # dictionary to store the probabilities in the sequence
        # maximum probability to a given word-tag sequence
        self.word_tag_viterbi_probability = {}

        # saving the index-tag(word-tag) for the last word of the sentence
        # with maximum probability
        self.index_tag_key = None

        # a set of all the unique tags in the training corpus
        self.unique_tags = set()
        self.bigram_counts = None

    def recursive_probability_cal_sequence(self, word_sequence, index, word_tag_i):
        # base case: if the index is the start tag.
        # return the previous probability as 0.
        if index == 1:
            return 0.0

        # if the probability already exists then return that from the dictionary
        if (index, word_tag_i) in self.word_tag_viterbi_probability:
            return self.word_tag_viterbi_probability[index, word_tag_i][0]

        # word-tags from index-1
        if word_sequence[index - 1] in self.word_tags_set:
            word_tags_i_1 = self.word_tags_set[word_sequence[index - 1]]
        else:
            word_tags_i_1 = self.unique_tags

        # word-tags from index-2
        if word_sequence[index - 2] in self.word_tags_set:
            word_tags_i_2 = self.word_tags_set[word_sequence[index - 2]]
        else:
            word_tags_i_2 = self.unique_tags

        max_viterbi_prob = -1000000.0

        back_pointer_tag = "*"

        # iterating through all word-tag combination from previous indexes recursively
        for word_tag_i_1 in word_tags_i_1:
            for word_tag_i_2 in word_tags_i_2:
                viterbi_prob = 0.0

                if (word_tag_i_2, word_tag_i_1, word_tag_i) in self.transition_probabilities:
                    transition_prob = self.transition_probabilities[(
                        word_tag_i_2, word_tag_i_1, word_tag_i)]
                else:
                    if (word_tag_i_2, word_tag_i_1) in self.bigram_counts:
                        transition_prob = math.log(
                            1.0 / float(self.bigram_counts[(word_tag_i_2, word_tag_i_1)] + len(self.unique_tags)))
                    else:
                        transition_prob = math.log(
                            1.0 / float(len(self.unique_tags)))

                if (word_sequence[index], word_tag_i) not in self.emission_probabilities:
                    transition_prob = 0.0
                    viterbi_prob = self.recursive_probability_cal_sequence(word_sequence, index - 1, word_tag_i_1) + \
                        transition_prob
                else:
                    # Viterbi probability for any sequence is
                    # Viterbi Probability from previous words +
                    # Emission probability for given word-tag sequence +
                    # Transition probability for tag(i),tag(i-1),tag(i-2)
                    viterbi_prob = self.recursive_probability_cal_sequence(word_sequence, index - 1, word_tag_i_1) + \
                        self.emission_probabilities[(
                            word_sequence[index], word_tag_i)] + transition_prob

                # Save the maximum probability till now of all the combinations and the back pointer
                # parent pointer(i-1)
                if max_viterbi_prob < viterbi_prob:
                    max_viterbi_prob = viterbi_prob
                    back_pointer_tag = word_tag_i_1

        self.word_tag_viterbi_probability[index, word_tag_i] = (
            max_viterbi_prob, (index - 1, back_pointer_tag))
        return max_viterbi_prob

    def load(self):
        with open("models/hmmmodel.pkl", "rb") as f:
            data = pickle.load(f)
            self.transition_probabilities = data["transition"]
            self.emission_probabilities = data["emission"]
            self.word_tags_set = data["word2tags"]
            self.unique_tags = data["unique_tags"]
            self.bigram_counts = data["bigram"]

    def viterbi_algorithm(self, file_name):
        output = open("models/hmmoutput.txt", "w")
        read_files = ReadFiles(file_name)
        words_sents = read_files.word_raw()
        for words_sent in words_sents:
            max_viterbi_prob = -1000000.0
            self.word_tag_viterbi_probability = {}
            # length of the current sentence
            len_words_sent = len(words_sent)
            if words_sent[len_words_sent - 1] in self.word_tags_set:
                word_tags_i = self.word_tags_set[words_sent[len_words_sent - 1]]
            else:
                word_tags_i = self.unique_tags

            for word_tag_i in word_tags_i:
                viterbi_prob = self.recursive_probability_cal_sequence(
                    words_sent, len_words_sent - 1, word_tag_i
                )
                # Saving the last pointer of the word in the sentence
                if max_viterbi_prob < viterbi_prob:
                    max_viterbi_prob = viterbi_prob
                    self.index_tag_key = (len_words_sent - 1, word_tag_i)

            tagged_sentence = []
            while self.index_tag_key[0] >= 2:
                tagged_sentence.insert(
                    0, words_sent[self.index_tag_key[0]] + "/" + self.index_tag_key[1])
                self.index_tag_key = self.word_tag_viterbi_probability[self.index_tag_key][1]

            output.write(" ".join(tagged_sentence) + "\n")
        output.close()


if __name__ == "__main__":
    file_name = sys.argv[1]
    viterbi = ViterbiDecode()
    viterbi.load()
    viterbi.viterbi_algorithm(file_name)
