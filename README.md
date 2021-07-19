# simple_sam_demo

This is a simple project that tries to illustrate how to use python and AWS SAM.

This creates an endpoint in an api, two lambdas, and a dynamo table. One lambda adds the item to the table and the other adds a field to the table item asynchronously.

![arquitecture](https://github.com/lbellomo/simple_sam_demo/blob/master/diagram/arquitecture.png?raw=true)


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

To do the build:

``` bash
sam build -cp
```

The option `c` is to use the cache and `p` is to do it in parallel. If you run into a problem and you have docker installed, you can use `u` to make the build inside a container (this always works but is slower).

To do the deploy:

``` bash
sam deploy
```

This reads the `samconfig.toml` and does the deploy.

The first time you need to run it with `sam deploy --guided`, this creates the `samconfig.toml` and creates the bucket where you upload the artifacts.


## Notes

- For this workflow I thought that the data of the table will be wanted even if they do not have the prediction of the class. If this is not the case it is better not to save them in the table from the write lambda, but to put them in a stream queue directly. In this way, the first writing to the table is not necessary.

- The model is totally dummy. For anything more serious it will be better to save the model in S3 and read it from the lambda.

- Lambdas are very easy to scale and cheap, but they have limitations such as the maximum amount of ram and the maximum amount of time they can run. Nor can you choose to choose the hardware to run on. If you need more power (have faster responses or run more complex models) you can use AWS Fragata, something similar to lambda but with containers. To understand how lambdas work at a low level, look at this article: [Behind the scenes, AWS Lambda](https://www.bschaatsbergen.com/behind-the-scenes-lambda).

## Build diagram

The diagram is made with [diagrams](https://github.com/mingrammer/diagrams). To create it: 

``` bash
pip install diagrams
cd diagram
python diagram.py
```