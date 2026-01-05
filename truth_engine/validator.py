#!/usr/bin/env python3
"""
Truth Engine - API Validator
Verifies API connectivity, response quality, and data integrity
"""

import json
import asyncio
import aiohttp
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum

class VerificationLevel(Enum):
    """API verification status levels"""
    VERIFIED = "verified"      # ✅ Working perfectly
    CAUTION = "caution"        # ⚠️  Working with issues
    FAILED = "failed"          # ❌ Not working
    UNTESTED = "untested"      # ⏸️  Not yet tested

@dataclass
class ValidationResult:
    """Result of API validation"""
    api_id: str
    api_name: str
    category: str
    tested_at: str
    verification_level: str
    
    # Connectivity
    connectivity_score: int  # 0-100
    response_time_ms: Optional[float]
    http_status: Optional[int]
    
    # Data Quality
    data_quality_score: int  # 0-100
    returns_json: bool
    data_structure_valid: bool
    results_count: int
    
    # Reliability
    reliability_score: int  # 0-100
    rate_limit_info: Optional[Dict]
    auth_required: bool
    auth_type: Optional[str]
    
    # Overall
    truth_score: int  # 0-100 (weighted average)
    passed: bool
    errors: List[str]
    warnings: List[str]
    
    def to_dict(self):
        return asdict(self)

class TruthEngine:
    """
    The Truth Engine validates APIs through comprehensive testing
    """
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._default_config_path()
        self.config = self._load_config()
        
    def _default_config_path(self) -> Path:
        """Get default config path"""
        return Path(__file__).parent / 'config.json'
    
    def _load_config(self) -> Dict:
        """Load truth engine configuration"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return self._default_config()
    
    def _default_config(self) -> Dict:
        """Default configuration"""
        return {
            'thresholds': {
                'connectivity_min': 70,
                'data_quality_min': 60,
                'reliability_min': 50,
                'truth_score_min': 65
            },
            'weights': {
                'connectivity': 0.4,
                'data_quality': 0.4,
                'reliability': 0.2
            },
            'timeout_seconds': 15,
            'max_retries': 2
        }
    
    async def validate_api(self, api_config: Dict, session: aiohttp.ClientSession) -> ValidationResult:
        """
        Validate a single API through comprehensive testing
        """
        api_id = api_config['id']
        api_name = api_config['name']
        
        print(f"🔍 Validating {api_name}...")
        
        errors = []
        warnings = []
        
        # Initialize scores
        connectivity_score = 0
        data_quality_score = 0
        reliability_score = 0
        
        response_time_ms = None
        http_status = None
        returns_json = False
        data_structure_valid = False
        results_count = 0
        
        # Test 1: Connectivity
        print(f"  ├─ Testing connectivity...")
        connectivity_result = await self._test_connectivity(api_config, session)
        connectivity_score = connectivity_result['score']
        response_time_ms = connectivity_result.get('response_time_ms')
        http_status = connectivity_result.get('http_status')
        
        if connectivity_result.get('error'):
            errors.append(connectivity_result['error'])
        if connectivity_result.get('warning'):
            warnings.append(connectivity_result['warning'])
        
        # Test 2: Data Quality (only if connected)
        if connectivity_score >= 50:
            print(f"  ├─ Testing data quality...")
            data_result = await self._test_data_quality(api_config, session)
            data_quality_score = data_result['score']
            returns_json = data_result.get('returns_json', False)
            data_structure_valid = data_result.get('structure_valid', False)
            results_count = data_result.get('results_count', 0)
            
            if data_result.get('error'):
                errors.append(data_result['error'])
            if data_result.get('warning'):
                warnings.append(data_result['warning'])
        else:
            warnings.append("Skipped data quality test due to connectivity failure")
        
        # Test 3: Reliability
        print(f"  ├─ Testing reliability...")
        reliability_result = await self._test_reliability(api_config, session)
        reliability_score = reliability_result['score']
        
        if reliability_result.get('warning'):
            warnings.append(reliability_result['warning'])
        
        # Calculate truth score (weighted average)
        weights = self.config['weights']
        truth_score = int(
            connectivity_score * weights['connectivity'] +
            data_quality_score * weights['data_quality'] +
            reliability_score * weights['reliability']
        )
        
        # Determine verification level
        thresholds = self.config['thresholds']
        passed = truth_score >= thresholds['truth_score_min']
        
        if passed and truth_score >= 80:
            verification_level = VerificationLevel.VERIFIED.value
        elif passed:
            verification_level = VerificationLevel.CAUTION.value
        else:
            verification_level = VerificationLevel.FAILED.value
        
        # Build result
        result = ValidationResult(
            api_id=api_id,
            api_name=api_name,
            category=api_config.get('category', 'unknown'),
            tested_at=datetime.now().isoformat(),
            verification_level=verification_level,
            connectivity_score=connectivity_score,
            response_time_ms=response_time_ms,
            http_status=http_status,
            data_quality_score=data_quality_score,
            returns_json=returns_json,
            data_structure_valid=data_structure_valid,
            results_count=results_count,
            reliability_score=reliability_score,
            rate_limit_info=api_config.get('rate_limits'),
            auth_required=api_config.get('requires_key', False),
            auth_type=api_config.get('auth_type'),
            truth_score=truth_score,
            passed=passed,
            errors=errors,
            warnings=warnings
        )
        
        # Print result
        status_emoji = "✅" if passed else "❌"
        print(f"  └─ {status_emoji} Truth Score: {truth_score}/100 ({verification_level})\n")
        
        return result
    
    async def _test_connectivity(self, api_config: Dict, session: aiohttp.ClientSession) -> Dict:
        """Test API connectivity and response time"""
        score = 0
        result = {'score': score}
        
        base_url = api_config['base_url']
        endpoints = api_config.get('endpoints', {})
        
        if not endpoints:
            result['error'] = "No endpoints defined"
            return result
        
        # Build test URL
        endpoint_key = list(endpoints.keys())[0]
        endpoint_path = endpoints[endpoint_key]
        test_url = base_url + endpoint_path.replace('{query}', 'test')
        
        try:
            start_time = time.time()
            headers = {
                'User-Agent': 'TruthEngine/1.0 (API Validator)',
                'Accept': 'application/json'
            }
            
            async with session.get(test_url, headers=headers, timeout=self.config['timeout_seconds']) as response:
                response_time = (time.time() - start_time) * 1000
                result['response_time_ms'] = round(response_time, 2)
                result['http_status'] = response.status
                
                # Score based on HTTP status
                if response.status == 200:
                    score = 100
                elif response.status in [201, 202, 204]:
                    score = 90
                elif response.status == 429:  # Rate limited but working
                    score = 70
                    result['warning'] = "Rate limited"
                elif response.status in [400, 404]:
                    score = 40
                    result['error'] = f"HTTP {response.status}"
                elif response.status in [401, 403]:
                    score = 30
                    result['error'] = f"Authentication required (HTTP {response.status})"
                else:
                    score = 20
                    result['error'] = f"HTTP {response.status}"
                
                # Penalize slow responses
                if response_time > 2000:
                    score = max(score - 20, 0)
                    result['warning'] = "Slow response (>2s)"
                elif response_time > 5000:
                    score = max(score - 40, 0)
                    result['warning'] = "Very slow response (>5s)"
                
        except asyncio.TimeoutError:
            result['error'] = "Timeout"
            score = 0
        except Exception as e:
            result['error'] = str(e)[:100]
            score = 0
        
        result['score'] = score
        return result
    
    async def _test_data_quality(self, api_config: Dict, session: aiohttp.ClientSession) -> Dict:
        """Test quality and structure of returned data"""
        score = 0
        result = {'score': score}
        
        base_url = api_config['base_url']
        endpoints = api_config.get('endpoints', {})
        endpoint_key = list(endpoints.keys())[0]
        endpoint_path = endpoints[endpoint_key]
        test_url = base_url + endpoint_path.replace('{query}', 'test')
        
        try:
            headers = {
                'User-Agent': 'TruthEngine/1.0 (API Validator)',
                'Accept': 'application/json'
            }
            
            async with session.get(test_url, headers=headers, timeout=self.config['timeout_seconds']) as response:
                if response.status != 200:
                    result['error'] = f"HTTP {response.status}"
                    return result
                
                # Try to parse as JSON
                try:
                    data = await response.json()
                    result['returns_json'] = True
                    score += 40
                    
                    # Check if data has expected structure
                    if isinstance(data, dict):
                        score += 20
                        
                        # Look for common result patterns
                        result_keys = ['results', 'items', 'data', 'entries', 'records']
                        has_results = any(key in data for key in result_keys)
                        
                        if has_results:
                            score += 20
                            result['structure_valid'] = True
                            
                            # Try to count results
                            for key in result_keys:
                                if key in data and isinstance(data[key], list):
                                    result['results_count'] = len(data[key])
                                    if result['results_count'] > 0:
                                        score += 20
                                    break
                    elif isinstance(data, list):
                        score += 20
                        result['results_count'] = len(data)
                        if result['results_count'] > 0:
                            score += 20
                            result['structure_valid'] = True
                    
                except Exception as e:
                    # Not JSON, try text
                    text = await response.text()
                    if len(text) > 0:
                        score = 30
                        result['warning'] = "Returns non-JSON data"
                    else:
                        result['error'] = "Empty response"
        
        except Exception as e:
            result['error'] = str(e)[:100]
        
        result['score'] = min(score, 100)
        return result
    
    async def _test_reliability(self, api_config: Dict, session: aiohttp.ClientSession) -> Dict:
        """Test API reliability and rate limits"""
        score = 70  # Default score
        result = {'score': score}
        
        # Check if rate limits are documented
        if api_config.get('rate_limits'):
            score += 15
        else:
            result['warning'] = "Rate limits not documented"
        
        # Check authentication requirements
        if not api_config.get('requires_key', False):
            score += 15  # No auth required is good for accessibility
        
        result['score'] = min(score, 100)
        return result
    
    async def validate_all(self, apis: List[Dict]) -> List[ValidationResult]:
        """Validate multiple APIs in parallel"""
        print("🔍 TRUTH ENGINE - API Validation")
        print("=" * 60)
        print(f"Validating {len(apis)} APIs...\n")
        
        async with aiohttp.ClientSession() as session:
            tasks = [self.validate_api(api, session) for api in apis]
            results = await asyncio.gather(*tasks)
        
        return results
    
    def generate_report(self, results: List[ValidationResult]) -> Dict:
        """Generate validation report"""
        total = len(results)
        verified = len([r for r in results if r.verification_level == VerificationLevel.VERIFIED.value])
        caution = len([r for r in results if r.verification_level == VerificationLevel.CAUTION.value])
        failed = len([r for r in results if r.verification_level == VerificationLevel.FAILED.value])
        
        avg_truth_score = sum(r.truth_score for r in results) / total if total > 0 else 0
        
        return {
            'summary': {
                'total_apis': total,
                'verified': verified,
                'caution': caution,
                'failed': failed,
                'pass_rate': round((verified + caution) / total * 100, 1) if total > 0 else 0,
                'avg_truth_score': round(avg_truth_score, 1)
            },
            'verified_apis': [r.to_dict() for r in results if r.verification_level == VerificationLevel.VERIFIED.value],
            'caution_apis': [r.to_dict() for r in results if r.verification_level == VerificationLevel.CAUTION.value],
            'failed_apis': [r.to_dict() for r in results if r.verification_level == VerificationLevel.FAILED.value],
            'full_results': [r.to_dict() for r in results]
        }
    
    def print_report(self, report: Dict):
        """Print formatted validation report"""
        print("\n" + "=" * 60)
        print("🔍 TRUTH ENGINE - Validation Report")
        print("=" * 60)
        
        summary = report['summary']
        print(f"\n📊 Summary:")
        print(f"  Total APIs:       {summary['total_apis']}")
        print(f"  ✅ Verified:      {summary['verified']}")
        print(f"  ⚠️  Caution:       {summary['caution']}")
        print(f"  ❌ Failed:        {summary['failed']}")
        print(f"  📈 Pass Rate:     {summary['pass_rate']}%")
        print(f"  🎯 Avg Truth Score: {summary['avg_truth_score']}/100")
        
        if report['verified_apis']:
            print(f"\n✅ Verified APIs ({len(report['verified_apis'])}):")
            for api in report['verified_apis']:
                print(f"  • {api['api_name']} - Truth Score: {api['truth_score']}/100")
        
        if report['caution_apis']:
            print(f"\n⚠️  Caution APIs ({len(report['caution_apis'])}):")
            for api in report['caution_apis']:
                print(f"  • {api['api_name']} - Truth Score: {api['truth_score']}/100")
                if api['warnings']:
                    for warning in api['warnings']:
                        print(f"    ⚠️  {warning}")
        
        if report['failed_apis']:
            print(f"\n❌ Failed APIs ({len(report['failed_apis'])}):")
            for api in report['failed_apis']:
                print(f"  • {api['api_name']} - Truth Score: {api['truth_score']}/100")
                if api['errors']:
                    for error in api['errors']:
                        print(f"    ❌ {error}")
        
        print("\n" + "=" * 60)

async def main():
    """Main execution"""
    # Load API registry
    registry_path = Path(__file__).parent.parent / 'verified_apis' / 'registry.json'
    
    if not registry_path.exists():
        print("❌ API registry not found. Please create registry.json first.")
        return
    
    with open(registry_path, 'r') as f:
        registry = json.load(f)
    
    # Initialize truth engine
    engine = TruthEngine()
    
    # Validate all APIs
    results = await engine.validate_all(registry['apis'])
    
    # Generate and print report
    report = engine.generate_report(results)
    engine.print_report(report)
    
    # Save results
    output_path = Path(__file__).parent / f'validation_results_{int(time.time())}.json'
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n💾 Full results saved to: {output_path}")

if __name__ == '__main__':
    asyncio.run(main())
