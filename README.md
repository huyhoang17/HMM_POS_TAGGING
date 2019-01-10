# Hidden Markov Model

- POS-Tagging model for English based on Hidden Markov Model algorithm
- Dataset: Brown Dataset (English)

### Command

- First, export environment variable so that program can read the correct path!

```
export PYTHONPATH=path-to-root-folder
```

- To generate brown data to right format

```
make brown
```

- To train and save model. After that, model file stored in `models` folder

```
make learn
```

- To load pretrain file and predict for new data. After that, see result in `models/hmmoutput.txt`

```
make predict
```

### TODO

- Add basic document
- Add model evaluated with metric (acc).
- POS Tagging for Vietnamese data.