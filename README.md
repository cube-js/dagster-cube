# Dagster + Cube integration library
This library provides a [resource](https://docs.dagster.io/concepts/resources) to interact with Cube Cloud's REST API from Dagster.

&nbsp;

## Installation

To install the library, use pip alongside your existing Dagster environment.

```bash
pip install dagster_cube
```

## Methods
### make_request
Makes a request to the Cube API.

Parameters:
- method (str): The http method use for this request (e.g. "GET", "POST")
- endpoint (str): The Cube API endpoint to send this request to.
- data (Optional(dict): Query parameters to pass to the API endpoint

Returns:
- Dict[str, Any]: Parsed json data from the response to this request

Example:
```python
my_cube_resource = CubeResource(
    instance_url="https://intancexyz.cubecloudapp.dev/cubejs-api/v1/",
    api_key="token"
)

response = my_cube_resource.make_request(
    method="POST",
    endpoint="pre-aggregations/jobs",
    data={
        'action': 'post',
        'selector': {
            'preAggregations': ['MyCube.myPreAgg'],
            'timezones': ['UTC'],
            'contexts': [{'securityContext': {}}]
        }
    }    
)
```