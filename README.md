# Hidden Markov Model

- POS-Tagging model for English based on Hidden Markov Model algorithm
- Dataset: Brown Dataset (English)

### Command

- Create `models` folder

```
mkdir models
```

- First, export environment variable so that program can read the correct path!

```
export PYTHONPATH=path-to-root-folder
```

- To train and save model. After that, model file stored in `models` folder

```
make learn
```

- To load pretrain file and predict for testing data. After that, see result in `models/hmmoutput.txt`

```
make predict
```

- To evaluate model

```
make eval
```

### TODO

- POS Tagging for Vietnamese data.

### Reference

- https://medium.freecodecamp.org/a-deep-dive-into-part-of-speech-tagging-using-viterbi-algorithm-17c8de32e8bc
- https://github.com/oucler/HMM-Tagger
- https://github.com/stathwang/POS-Taggers