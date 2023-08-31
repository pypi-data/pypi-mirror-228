![HawkFLow.ai](https://hawkflow.ai/static/images/emails/bars.png)

# HawkFlow.ai apache airflow integration

#### sign up to hawkflow for free: https://hawkflow.ai/

## Monitoring for anyone that writes code

1. Install the pip package `pip install hawkflowairflow`
2. Usage:
```python
from hawkflowairflow.hawkflow_callbacks import *

HF_API_KEY = "YOUR_HAWKFLOW_API_KEY_HERE"
```

# add these two lines to default_args in your DAG:

```
default_args={    
    "on_success_callback": hawkflow_success_callback,
    "on_execute_callback": hawkflow_start_callback
},
"on_success_callback": hawkflow_success_callback,
"on_execute_callback": hawkflow_start_callback
``` 

More examples: [HawkFlow.ai Python examples](https://github.com/hawkflow/hawkflow-examples/tree/master/python)

Read the docs: [HawkFlow.ai documentation](https://docs.hawkflow.ai/)

## What is HawkFlow.ai?

HawkFlow.ai is a new monitoring platform that makes it easier than ever to make monitoring part of your development process. Whether you are an Engineer, a Data Scientist, an Analyst, or anyone else that writes code, HawkFlow.ai helps you and your team take ownership of monitoring.