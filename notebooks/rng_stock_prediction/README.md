# Random Walk for stock price prediction using true Random Numbers

## Prerequisites
- Uploading and deploying services on the PlanQK platform, see tutorial [here](https://docs.platform.planqk.de/en/latest/platform_instructions/service_platform.html#deploy-services-on-the-planqk-platform)
- Setting up a Python environment using Conda, see tutorial [here](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html)
- Setting up Jupyter Lab, see tutorial [here](https://jupyterlab.readthedocs.io/en/stable/getting_started/installation.html)

## Content & How To
Provided are two Jupyter notebooks demonstrating how to generate random numbers and how to further process them, as well as the underlying source code wrapped by the PlanQK user code template within `src`.  
`rng_local.ipynb` is a self consistent notebook which includes the main logic of `src/program.py` in order to understand the general idea of the toy use case.  
`rng_platform.ipynb` is basically a copy of the the former notebook except that it replaces the locally running service with the necessary commands to communicate with a service on the platform and retrieve results from it.
It was created with an already existing service and application, which is to be replaced by your own.  
In order to do this, follow the steps you need to provide the implementation as a service by zipping the `src` repo.  
If you successfully deployed the service, you should publish it internally and subscribe to it from within a (new or existing) application. By doing so, you should be able to follow the steps within `rng_platform.ipynb` and be able to execute the service from within the notebook.