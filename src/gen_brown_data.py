def main():
    with open("../data/en_brown_tagged.txt", "w") as f1, \
            open('../data/brown-universal.txt', 'r') as f2:
        words = []
        for line in f2:
            word_tag = line.strip().split()
            if not word_tag:
                sentence = ' '.join(words)
                f1.write(sentence + "\n")
                words = []
            if len(word_tag) == 2:
                words.append(word_tag[0] + '/' + word_tag[1])


if __name__ == '__main__':
    main()
