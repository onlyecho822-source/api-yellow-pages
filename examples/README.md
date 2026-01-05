# 🐙 Octopus Mode Examples

This directory contains examples of how to use the API Yellow Pages with Octopus Mode for parallel API queries.

## Quick Start

### 1. Query Multiple APIs Simultaneously

```python
import asyncio
from octopus_engine import OctopusEngine

async def main():
    # Initialize engine
    engine = OctopusEngine('../verified_apis/registry.json')
    
    # Query all working APIs
    results = await engine.query_all("CBRN training safety")
    
    # Print report
    engine.print_report(results)
    
    print(f"\nFound {results['total_results']} results across {results['successful_queries']} APIs")

if __name__ == '__main__':
    asyncio.run(main())
```

### 2. Query Specific APIs

```python
# Query only government APIs
results = await engine.query_all(
    "military training", 
    api_ids=['data_gov', 'federal_register']
)
```

### 3. Access Individual Results

```python
for api_result in results['api_results']:
    if api_result['status'] == 'success':
        print(f"\n{api_result['api_name']}:")
        for item in api_result['results']:
            print(f"  - {item['title']}")
            print(f"    {item.get('url', 'No URL')}")
```

## Example: CBRN Research Query

```python
import asyncio
from octopus_engine import OctopusEngine

async def cbrn_research():
    engine = OctopusEngine('../verified_apis/registry.json')
    
    # Query for CBRN training data
    results = await engine.query_all("CBRN training mishap safety")
    
    # Filter results by source
    pubmed_results = [
        r for r in results['api_results'] 
        if r['api_id'] == 'pubmed' and r['status'] == 'success'
    ]
    
    print(f"Found {len(pubmed_results[0]['results'])} PubMed articles")
    
    return results

asyncio.run(cbrn_research())
```

## Running the Examples

```bash
# Install dependencies
pip install -r ../requirements.txt

# Run octopus engine
python octopus_engine.py "your search query"
```

## Output Format

The engine returns a structured report:

```json
{
  "query": "CBRN training",
  "timestamp": "2026-01-05T01:20:00",
  "apis_queried": 7,
  "successful_queries": 6,
  "total_results": 42,
  "api_results": [
    {
      "api_id": "data_gov",
      "api_name": "Data.gov",
      "status": "success",
      "results_count": 10,
      "results": [...]
    }
  ]
}
```

## Advanced Usage

### Custom Timeout

```python
engine = OctopusEngine('../verified_apis/registry.json')
engine.config['timeout_seconds'] = 30  # Increase timeout
```

### Filter by Category

```python
# Get only research APIs
research_apis = [
    api['id'] for api in engine.registry['apis'] 
    if api['category'] == 'research'
]

results = await engine.query_all("training", api_ids=research_apis)
```

### Save Results

```python
import json

results = await engine.query_all("CBRN")

# Save to file
with open('cbrn_results.json', 'w') as f:
    json.dump(results, f, indent=2)
```

## Performance Tips

1. **Use Specific Queries**: More specific queries return better results
2. **Limit API Count**: Query only relevant APIs for faster results
3. **Cache Results**: Save results locally to avoid repeated queries
4. **Handle Failures**: Always check `status` field before accessing results

## Need Help?

- Check the [main README](../README.md)
- Review [API documentation](../verified_apis/)
- Open an [issue](https://github.com/onlyecho822-source/api-yellow-pages/issues)
