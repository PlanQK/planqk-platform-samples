# PlanQK External Service Example

> An example showing how to prototypically build a PlanQK External Service.
> This example also shows how to meter the usage of the service and reports it back to PlanQK.

## Run the Example

### Python

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Docker

```bash
docker build -t planqk-external-service .    
docker run -it -p 8000:80 planqk-external-service
```

### Render

You can deploy this example to [Render](https://render.com) with just a couple of clicks:

- Go to [Render](https://render.com/deploy)
- Create new "Web Service" from "Public Git repository"
    - Use `https://github.com/PlanQK/planqk-platform-samples` as public repository URL
    - Choose a region close to you
    - Use `master` as branch
    - Use `python/external-service-sample` as root directory
    - Use `Docker` as runtime
    - Choose an instance type, i.e., the "Free" plan is just fine
    - Click "Create Web Service"
