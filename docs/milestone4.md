##What will the directory structure look like?

team27_2023/
|-- .github/workflows/
|--  API_draft/
|--  docs/
|--  src/
|   |-- augment.py
|-- tests/
|   |-- test_augment.py
|-- LICENSE
|-- README.md

##Where will your test suite live?

Our test suite will live in the tests folder under test_augment.py

##How will you distribute your package (e.g. PyPI with PEP517/518 or simply setuptools)?

We can distribute it as a Docker container, which would allow us to package our package into Docker container 

##Other considerations?

We will need to consider the following: 
the preprocessing module: this module (augmentation) depends heavily on the data format outputted by that. Also, we will have src/ and test/ for every module so our package structure will expand.

##Briefly motivate your license choice in the milesone4 document and add a LICENSE file to the root of your project.

We are using the MIT License because it places few restrictions on the reuse of it, so people can use, copy, modify, merge publish, distribute, sublicense and sell copies of what we created.
