import sys


def evaluate(fn_1, fn_2):
    total_words = 0
    total_correct_words = 0
    with open(fn_1) as f1, open(fn_2) as f2:
        for user_sent, correct_sent in zip(f1, f2):
            user_tok = user_sent.split()
            correct_tok = correct_sent.split()

            total_words += len(user_tok)
            if len(user_tok) != len(correct_tok):
                continue

            for u, c in zip(user_tok, correct_tok):
                if u == c:
                    total_correct_words += 1

    score = float(total_correct_words) / total_words * 100
    print("Percent correct tags:", score)


if __name__ == '__main__':
    fn_1 = sys.argv[1]
    fn_2 = sys.argv[2]
    evaluate(fn_1, fn_2)
