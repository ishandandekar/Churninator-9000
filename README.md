# Churnobyl

> **Warning**: This is a work in progress. Until specified, please do not directly use the code. There will be addtition as well as improvements over the time. Use the code only to get inspiration and not for actual production usage.

## Contributions

Any help is always welcomed. The project is open-source. The key features that are needed to be updated are marked as TODO in readme as well as in code. If you think there can be any other improvement, please make a PR or an issue, and I'll go over it as soon as possible.

### TODO:

- [x] Setup project
- [x] Integrate python environment
- [x] Learn pre-commit and linters
- [x] Make base notebooks without thinking of optimization
- [x] Create a `pipeline.py` script
- [x] Explore and update the files in `./data_schema`
- [x] Only keep `.yaml` file for schema
- [ ] Figure out preprocessing code present in [`./temp/temp.py`](./temp/temp.py)
- [ ] Add code to save preprocessor and all models into the specified directory
- [ ] Fill the [`./churnobyl/data.py`](./churnobyl/data.py)
- [ ] Fill the [`./churnobyl/model.py`](./churnobyl/model.py)
- [ ] Fill the [`./churnobyl/pipeline.py`](./churnobyl/pipeline.py), to reflect the actual workflow
- [ ] Run model experiments notebook
- [ ] Update config file
- [ ] Modulize the notebook code into python scripts
- [ ] Integrate prefect for workflow orchestration
- [ ] Create `Dockerfile`
- [ ] Add workflow files using Github Actions
- [ ] Explore AWS services to think for deployment options
- [ ] Try EvidentlyAI model monitoring service
- [ ] Integrate Streamlit to display graphs

### Refs:

- https://stackoverflow.com/questions/52570869/load-yaml-as-nested-objects-instead-of-dictionary-in-python
- https://www.youtube.com/watch?v=-tU7fuUiq7w&ab_channel=ArjanCodes
- https://github.com/ishandandekar/misc
- https://pandera.readthedocs.io/en/stable/checks.html
- https://gist.github.com/ishandandekar/d9a60b1d7d5b8af9fd1c640e63c8ceb2
- https://gist.github.com/ishandandekar/fa7dbf05b41e30b8dc492cf18968f12a
- https://octopus.com/blog/githubactions-docker-ecr
- https://aws.amazon.com/blogs/compute/using-aws-lambda-extensions-to-send-logs-to-custom-destinations/
- https://neptune.ai/blog/ml-model-testing-teams-share-how-they-test-models
