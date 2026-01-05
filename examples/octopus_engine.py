#!/usr/bin/env python3
"""
Octopus Mode - Query Engine
Executes parallel queries across multiple APIs and aggregates results
"""

import json
import asyncio
import aiohttp
import time
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
from urllib.parse import quote

class OctopusEngine:
    def __init__(self, registry_path: str):
        self.registry_path = Path(registry_path)
        self.registry = self._load_registry()
        self.working_apis = self._load_working_apis()
        
    def _load_registry(self) -> Dict:
        """Load API registry from JSON file"""
        with open(self.registry_path, 'r') as f:
            return json.load(f)
    
    def _load_working_apis(self) -> List[Dict]:
        """Load list of working APIs from latest test results"""
        cache_dir = Path(self.registry_path).parent.parent / 'cache'
        test_files = sorted(cache_dir.glob('test_results_*.json'), reverse=True)
        
        if test_files:
            with open(test_files[0], 'r') as f:
                results = json.load(f)
                return results.get('working_apis', [])
        
        # Fallback: return all active APIs
        return [api for api in self.registry['apis'] if api.get('active', False)]
    
    def _get_api_config(self, api_id: str) -> Optional[Dict]:
        """Get full API configuration by ID"""
        for api in self.registry['apis']:
            if api['id'] == api_id:
                return api
        return None
    
    async def query_api(self, api_id: str, query: str, session: aiohttp.ClientSession) -> Dict:
        """Query a single API"""
        api_config = self._get_api_config(api_id)
        if not api_config:
            return {
                'api_id': api_id,
                'status': 'error',
                'error': 'API not found in registry'
            }
        
        api_name = api_config['name']
        print(f"  🐙 Querying {api_name}...")
        
        result = {
            'api_id': api_id,
            'api_name': api_name,
            'category': api_config['category'],
            'query': query,
            'queried_at': datetime.now().isoformat(),
            'status': 'unknown',
            'response_time_ms': None,
            'results_count': 0,
            'results': [],
            'error': None
        }
        
        # Build query URL
        base_url = api_config['base_url']
        endpoints = api_config.get('endpoints', {})
        
        if not endpoints:
            result['status'] = 'no_endpoint'
            result['error'] = 'No endpoints defined'
            return result
        
        # Use search endpoint
        endpoint_key = 'search' if 'search' in endpoints else list(endpoints.keys())[0]
        endpoint_path = endpoints[endpoint_key]
        
        # Replace query placeholder
        encoded_query = quote(query)
        query_url = base_url + endpoint_path.replace('{query}', encoded_query)
        
        # Make request
        start_time = time.time()
        try:
            headers = {
                'User-Agent': 'OctopusMode/1.0 (Research Tool)',
                'Accept': 'application/json'
            }
            
            async with session.get(query_url, headers=headers, timeout=15) as response:
                response_time = (time.time() - start_time) * 1000
                result['response_time_ms'] = round(response_time, 2)
                
                if response.status == 200:
                    try:
                        data = await response.json()
                        result['status'] = 'success'
                        result['raw_data'] = data
                        
                        # Parse results based on API type
                        parsed = self._parse_results(api_id, data)
                        result['results'] = parsed
                        result['results_count'] = len(parsed)
                        
                        print(f"    ✅ {api_name}: {result['results_count']} results ({result['response_time_ms']}ms)")
                    except Exception as e:
                        result['status'] = 'parse_error'
                        result['error'] = f"Failed to parse JSON: {str(e)}"
                        print(f"    ⚠️  {api_name}: Parse error")
                else:
                    result['status'] = 'http_error'
                    result['error'] = f"HTTP {response.status}"
                    print(f"    ❌ {api_name}: HTTP {response.status}")
                    
        except asyncio.TimeoutError:
            result['status'] = 'timeout'
            result['error'] = 'Request timeout (>15s)'
            print(f"    ⏱️  {api_name}: Timeout")
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
            print(f"    ❌ {api_name}: {str(e)[:50]}")
        
        return result
    
    def _parse_results(self, api_id: str, data: Dict) -> List[Dict]:
        """Parse API-specific response formats into standardized results"""
        results = []
        
        try:
            if api_id == 'data_gov':
                for item in data.get('result', {}).get('results', [])[:10]:
                    results.append({
                        'title': item.get('title', 'No title'),
                        'description': item.get('notes', '')[:200],
                        'url': f"https://catalog.data.gov/dataset/{item.get('name', '')}",
                        'source': 'Data.gov'
                    })
            
            elif api_id == 'federal_register':
                for item in data.get('results', [])[:10]:
                    results.append({
                        'title': item.get('title', 'No title'),
                        'description': item.get('abstract', '')[:200],
                        'url': item.get('html_url', ''),
                        'date': item.get('publication_date', ''),
                        'source': 'Federal Register'
                    })
            
            elif api_id == 'pubmed':
                id_list = data.get('esearchresult', {}).get('idlist', [])[:10]
                for pmid in id_list:
                    results.append({
                        'title': f"PubMed Article {pmid}",
                        'url': f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                        'pmid': pmid,
                        'source': 'PubMed'
                    })
            
            elif api_id == 'arxiv':
                # arXiv returns XML, but we got it as text
                # For now, just note the count
                results.append({
                    'title': 'arXiv results available',
                    'description': 'XML parsing required for full details',
                    'source': 'arXiv'
                })
            
            elif api_id == 'crossref':
                for item in data.get('message', {}).get('items', [])[:10]:
                    results.append({
                        'title': item.get('title', ['No title'])[0] if item.get('title') else 'No title',
                        'authors': ', '.join([f"{a.get('given', '')} {a.get('family', '')}" 
                                            for a in item.get('author', [])[:3]]),
                        'url': item.get('URL', ''),
                        'published': item.get('published', {}).get('date-parts', [['']])[0],
                        'source': 'CrossRef'
                    })
            
            elif api_id == 'world_bank':
                # World Bank has complex structure
                if isinstance(data, list) and len(data) > 1:
                    for item in data[1][:10]:
                        results.append({
                            'title': item.get('country', {}).get('value', 'No title'),
                            'value': item.get('value', ''),
                            'date': item.get('date', ''),
                            'source': 'World Bank'
                        })
            
            elif api_id == 'github':
                for item in data.get('items', [])[:10]:
                    results.append({
                        'title': item.get('full_name', 'No title'),
                        'description': item.get('description', '')[:200],
                        'url': item.get('html_url', ''),
                        'stars': item.get('stargazers_count', 0),
                        'language': item.get('language', 'Unknown'),
                        'source': 'GitHub'
                    })
            
            else:
                # Generic parser
                if isinstance(data, dict):
                    results.append({
                        'title': 'Raw data available',
                        'description': str(data)[:200],
                        'source': api_id
                    })
        
        except Exception as e:
            results.append({
                'title': 'Parse error',
                'error': str(e),
                'source': api_id
            })
        
        return results
    
    async def query_all(self, query: str, api_ids: Optional[List[str]] = None) -> Dict:
        """Query multiple APIs in parallel"""
        print(f"\n🐙 OCTOPUS MODE - Parallel Query")
        print("=" * 60)
        print(f"Query: \"{query}\"")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Determine which APIs to query
        if api_ids:
            target_apis = [api_id for api_id in api_ids if self._get_api_config(api_id)]
        else:
            # Use all working APIs
            target_apis = [api['id'] for api in self.working_apis]
        
        print(f"Activating {len(target_apis)} tentacles...\n")
        
        # Execute queries in parallel
        async with aiohttp.ClientSession() as session:
            tasks = [self.query_api(api_id, query, session) for api_id in target_apis]
            results = await asyncio.gather(*tasks)
        
        # Compile report
        report = {
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'apis_queried': len(target_apis),
            'successful_queries': len([r for r in results if r['status'] == 'success']),
            'total_results': sum(r['results_count'] for r in results),
            'api_results': results
        }
        
        return report
    
    def print_report(self, report: Dict):
        """Print formatted query report"""
        print("\n" + "=" * 60)
        print("🐙 OCTOPUS MODE - Query Results")
        print("=" * 60)
        
        print(f"\n📊 Summary:")
        print(f"  Query: {report['query']}")
        print(f"  APIs Queried: {report['apis_queried']}")
        print(f"  Successful: {report['successful_queries']}")
        print(f"  Total Results: {report['total_results']}")
        
        print(f"\n📚 Results by Source:\n")
        
        for api_result in report['api_results']:
            if api_result['status'] == 'success' and api_result['results_count'] > 0:
                print(f"  {api_result['api_name']} ({api_result['category']}):")
                print(f"    Found: {api_result['results_count']} results")
                
                for i, result in enumerate(api_result['results'][:3], 1):
                    print(f"    {i}. {result.get('title', 'No title')[:60]}")
                    if result.get('url'):
                        print(f"       🔗 {result['url']}")
                print()
        
        print("=" * 60)

async def main():
    """Main execution function"""
    import sys
    
    registry_path = Path(__file__).parent.parent / 'config' / 'api_registry.json'
    engine = OctopusEngine(registry_path)
    
    # Get query from command line or use default
    query = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else "CBRN training safety"
    
    # Execute parallel query
    report = engine.query_all(query)
    results = await report
    
    # Print report
    engine.print_report(results)
    
    # Save results
    timestamp = int(time.time())
    results_path = Path(__file__).parent.parent / 'cache' / f'query_results_{timestamp}.json'
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Full results saved to: {results_path}")

if __name__ == '__main__':
    asyncio.run(main())
