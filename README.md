## P Model

A few hand-crafted P models: https://github.com/Drona-Org/SOTERonROS/tree/master
Papers: https://drona-org.github.io/Drona/

The case studies: https://p-org.github.io/P/casestudies/

## UML Model

1. Dataset of UML-English:

https://github.com/songyang-dev/uml-classes-and-specs
Paper: https://arxiv.org/pdf/2210.14441.pdf

Only UML (mined):
https://ieeexplore.ieee.org/abstract/document/7962411

Modelset: https://github.com/modelset/modelset-dataset
https://models-lab.github.io/blog/2021/modelset/


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