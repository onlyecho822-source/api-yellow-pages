# 🟢 Verified APIs Directory

This directory contains APIs that have passed through the **Truth Engine** validation system and are confirmed to be working.

## Verification Levels

- 🟢 **VERIFIED** (Truth Score ≥ 80) - Working perfectly, tested within last 24 hours
- 🟡 **CAUTION** (Truth Score 65-79) - Working with minor issues or warnings
- 🔴 **FAILED** (Truth Score < 65) - Not working or unreliable

## Current Status

**Last Validation:** January 5, 2026  
**APIs Tested:** 20  
**Verified:** 6  
**Caution:** 1  
**Failed:** 13  
**Pass Rate:** 35.0%  
**Average Truth Score:** 51.7/100

## Verified APIs (6)

### Government

1. **[Data.gov](./government/data_gov.md)** - Truth Score: 100/100 ✅
   - 200,000+ US government datasets
   - No authentication required
   - Response time: ~735ms

2. **[Federal Register](./government/federal_register.md)** - Truth Score: 84/100 ✅
   - Official US regulations and notices
   - No authentication required
   - Response time: ~876ms

### Research

3. **[PubMed](./research/pubmed.md)** - Truth Score: 84/100 ✅
   - 35+ million biomedical citations
   - No authentication required (API key recommended for higher limits)
   - Response time: ~846ms

4. **[arXiv](./research/arxiv.md)** - Truth Score: 84/100 ✅
   - 2+ million preprint research papers
   - No authentication required
   - Response time: ~694ms

5. **[CrossRef](./research/crossref.md)** - Truth Score: 92/100 ✅
   - 140+ million scholarly works
   - No authentication required
   - Response time: ~1242ms

### Data

6. **[World Bank](./data/world_bank.md)** - Truth Score: 100/100 ✅
   - Global development indicators
   - No authentication required
   - Response time: ~433ms

## Caution APIs (1)

### Code

1. **[GitHub](./code/github.md)** - Truth Score: 72/100 ⚠️
   - 100+ million repositories
   - Authentication recommended for higher rate limits
   - Response time: ~1776ms
   - ⚠️ Slow response time

## Failed APIs (13)

The following APIs failed validation and are not included in the directory:

- USAspending.gov (HTTP 405)
- Semantic Scholar (Rate limited - HTTP 429)
- NewsAPI (Requires API key)
- The Guardian (Requires API key)
- US Census Bureau (Requires API key)
- Bureau of Labor Statistics (Requires API key)
- FRED Economic Data (Requires API key)
- Wikipedia (HTTP 403)
- OpenAlex (Encoding error)
- CORE (Requires API key)
- Defense Technical Information Center (Encoding error)
- SEC EDGAR (HTTP 403)
- Library of Congress (HTTP 403)

## How to Use

1. Browse by category (government, research, data, code)
2. Check the API's documentation page
3. Review authentication requirements
4. Test the API using provided examples
5. Report any issues via GitHub Issues

## Contributing

Found a working API? Submit it for validation:

1. Add API details to `registry.json`
2. Run the truth engine: `python3 truth_engine/validator.py`
3. If truth score ≥ 65, create documentation
4. Submit pull request with validation results

---

**Truth Engine Validation Criteria:**

- **Connectivity** (40%): Response time, HTTP status, uptime
- **Data Quality** (40%): JSON format, structure, result count
- **Reliability** (20%): Rate limits, documentation, auth requirements

**Minimum passing score:** 65/100
