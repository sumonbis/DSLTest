## P Model Benchmark

1. Examples from tutorials: https://github.com/p-org/P/
2. Drona ([paper](https://arxiv.org/pdf/2008.09707.pdf)): https://github.com/Drona-Org/Drona
3. SOTERonROS ([paper](https://people.eecs.berkeley.edu/~sseshia/pubdir/iccps17-drona.pdf)): https://github.com/Drona-Org/SOTERonROS/


## Installation

Follow these steps to create a virtual environment.

1. Clone this repository. 

2. Run this on command line to create a virtual environment:

```
python3 -m venv llmenv
source llmenv/bin/activate
```
Run the following command to update pip on Python: `python3 -m pip install --upgrade pip`.

3. Navigate to the repository and install required packages:
```
pip install -r requirements.txt
```

4. Run the `python testgen.py <p_model_directory>` to generate the tests for the given models. The generated tests are stored in the corresponding directory.

Before running the command, place the openai key (`api_key.txt`) in the root directory of the repository.