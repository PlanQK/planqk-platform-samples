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
