# Data.gov API

![Truth Score](https://img.shields.io/badge/Truth%20Score-100%2F100-brightgreen)
![Status](https://img.shields.io/badge/Status-Verified-success)
![Auth](https://img.shields.io/badge/Auth-None-blue)

## Overview

Data.gov is the home of the U.S. Government's open data. The API provides access to over 200,000 datasets from federal, state, and local governments.

## API Details

- **Base URL:** `https://catalog.data.gov/api/3`
- **Authentication:** None required
- **Rate Limit:** 60 requests/minute
- **Response Format:** JSON
- **Documentation:** https://www.data.gov/developers/apis

## Truth Engine Results

| Metric | Score | Details |
|--------|-------|---------|
| **Connectivity** | 100/100 | ✅ HTTP 200, 735ms response time |
| **Data Quality** | 100/100 | ✅ Valid JSON, structured results |
| **Reliability** | 100/100 | ✅ No auth required, documented rate limits |
| **Truth Score** | **100/100** | **🟢 VERIFIED** |

**Last Tested:** January 5, 2026

## Quick Start

### Search for Datasets

```bash
curl "https://catalog.data.gov/api/3/action/package_search?q=CBRN"
```

### Python Example

```python
import requests

# Search for datasets
response = requests.get(
    "https://catalog.data.gov/api/3/action/package_search",
    params={"q": "CBRN training"}
)

data = response.json()
results = data['result']['results']

for dataset in results[:5]:
    print(f"Title: {dataset['title']}")
    print(f"URL: https://catalog.data.gov/dataset/{dataset['name']}")
    print()
```

### JavaScript Example

```javascript
fetch('https://catalog.data.gov/api/3/action/package_search?q=CBRN')
  .then(response => response.json())
  .then(data => {
    data.result.results.forEach(dataset => {
      console.log(`Title: ${dataset.title}`);
      console.log(`URL: https://catalog.data.gov/dataset/${dataset.name}`);
    });
  });
```

## Available Endpoints

### 1. Search Datasets
- **Endpoint:** `/action/package_search`
- **Method:** GET
- **Parameters:**
  - `q` (string): Search query
  - `rows` (int): Number of results (default: 10)
  - `start` (int): Offset for pagination

### 2. Get Dataset Details
- **Endpoint:** `/action/package_show`
- **Method:** GET
- **Parameters:**
  - `id` (string): Dataset ID or name

## Response Format

```json
{
  "success": true,
  "result": {
    "count": 1234,
    "results": [
      {
        "id": "dataset-id",
        "name": "dataset-name",
        "title": "Dataset Title",
        "notes": "Dataset description",
        "organization": {
          "name": "Organization Name"
        },
        "resources": [
          {
            "url": "https://example.com/data.csv",
            "format": "CSV"
          }
        ]
      }
    ]
  }
}
```

## Use Cases

- **Government Research:** Find official government datasets
- **Policy Analysis:** Access regulatory and compliance data
- **Data Science:** Download datasets for analysis
- **Transparency:** Track government spending and operations

## Rate Limits

- **Limit:** 60 requests per minute
- **No API key required**
- **No daily cap**

## Best Practices

1. **Cache Results:** Store frequently accessed datasets locally
2. **Use Pagination:** Don't request all results at once
3. **Specific Queries:** Use targeted search terms for better results
4. **Check Updates:** Datasets are regularly updated

## Known Issues

None currently.

## Related APIs

- [USAspending.gov](https://api.usaspending.gov) - Government spending data
- [Federal Register](./federal_register.md) - Regulations and notices

## Support

- **Documentation:** https://www.data.gov/developers/apis
- **Issues:** Report via GitHub Issues
- **Community:** https://www.data.gov/contact

---

**Verified by Truth Engine** | Last Updated: January 5, 2026
