brown:
	python3 src/gen_brown_data.py

learn:
	python3 src/hmmlearn.py data/en_brown_tagged.txt

predict:
	python3 src/hmmdecode.py data/en_test_tag.txt