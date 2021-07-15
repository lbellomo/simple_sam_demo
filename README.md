# simple_sam_demo

This is a simple project that tries to illustrate how to use python and AWS SAM.

![arquitecture](https://github.com/lbellomo/simple_sam_demo/blob/development/diagram/arquitecture.png?raw=true)


## Creating the environment

Clone this repo:
``` bash
git clone https://github.com/lbellomo/simple_sam_demo.git
cd simple_sam_demo
```

Install conda if you don't have it (recommended to do it from [miniforge](https://github.com/conda-forge/miniforge#miniforge3)), and create and active the virtual env from the file `environment.yml`. This downlaod a python3.8 (the last one supported by aws lambda) and the things we are going to use like aws-sam-cli and linters.

``` bash
conda env create -f environment.yml
conda activate simple_sam_demo
```

Some optional dependencies 
- Docker: It can be used to make local builds (for example if you have problems in the other way) and to test the api locally with lambdas. See [instructions](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install-linux.html#serverless-sam-cli-install-linux-docker).
- HTTPie: To test the api. See [instructions](https://github.com/httpie/httpie#installation).

## Linters

To run the linters (standing at the home of the project, At the same level as the `template.yaml`)

``` bash
# python linters
black src internal_layer
flake8 src/ internal_layer

# template linters
yamllint template.yaml
cfn-lint template.yaml
```

There is a github action that runs them in the repo.

## Build and Deploy with SAM



## Notes



## Build diagram

The diagram is made with [diagrams](https://github.com/mingrammer/diagrams). To create it: 

``` bash
pip install diagrams
cd diagram
python diagram.py
```