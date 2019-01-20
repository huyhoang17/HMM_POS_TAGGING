learn:
	python3 src/hmmlearn.py data/en_brown_tagged.txt

predict:
	python3 src/hmmdecode.py data/en_test_tag.txt

eval:
	python3 src/eval.py data/en_brown_tagged.txt models/sample_output.txt