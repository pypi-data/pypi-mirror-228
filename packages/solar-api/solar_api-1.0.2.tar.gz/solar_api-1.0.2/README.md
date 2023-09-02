# Overview
This library contains useful wrappers around the Solar API

## Usage

Instantiate the API wrapper using the following code:

```
from solar_api.api import SolarApi

# Do not include trailing backslash in TONIC_URL
api = SolarApi(SOLAR_URL, API_KEY)
```

Once instantiated, the following endpoints are available for consumption. Note that available endpoints and response types are limited. Available fields may be severely limited compared to the current Tonic API.