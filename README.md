# 🟡 The API Yellow Pages

**A verified directory of working APIs, tested and validated by the Truth Engine**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![APIs Verified](https://img.shields.io/badge/APIs%20Verified-7-brightgreen)](./verified_apis/)
[![Truth Engine](https://img.shields.io/badge/Truth%20Engine-Active-blue)](./truth_engine/)

---

## 📖 What is this?

The **API Yellow Pages** is a community-maintained directory of publicly accessible APIs that have been **live-tested** and **verified** to work. Unlike other API directories that simply list endpoints, every API in this directory has passed through our **Truth Engine** - a validation system that:

✅ Tests live connectivity  
✅ Verifies response formats  
✅ Measures response times  
✅ Validates data quality  
✅ Checks rate limits  
✅ Documents authentication requirements  

Think of it as a **phone book for APIs**, but one where every number has been called and verified to work.

---

## 🎯 Why This Exists

**The Problem:** Most API directories are outdated, incomplete, or list APIs that no longer work. Developers waste hours testing APIs only to find they're broken, require expensive keys, or have been deprecated.

**The Solution:** A living, verified directory where every API is continuously tested. If an API is listed here, **it works right now**.

---

## 🐙 Octopus Mode

This project is powered by **Octopus Mode** - a parallel API query system that can reach out to multiple APIs simultaneously, like an octopus with many arms. This enables:

- **Parallel Testing**: Test 20+ APIs in seconds
- **Multi-Source Queries**: Query multiple APIs at once for comprehensive results
- **Intelligent Aggregation**: Combine and deduplicate results from different sources
- **Failure Resilience**: Continue working even if individual APIs fail

---

## 📊 Current Status

| Category | Verified APIs | Status |
|----------|---------------|--------|
| Government | 2 | ✅ Active |
| Research | 3 | ✅ Active |
| Data | 1 | ✅ Active |
| Code | 1 | ✅ Active |
| **Total** | **7** | **✅ Verified** |

*Last updated: January 5, 2026*

---

## 🗂️ Directory Structure

```
api-yellow-pages/
├── verified_apis/          # Verified API configurations
│   ├── government/         # Government & public sector APIs
│   ├── research/           # Academic & research APIs
│   ├── data/              # Data & statistics APIs
│   ├── code/              # Code repository APIs
│   └── README.md          # Directory guide
├── truth_engine/          # Validation & testing system
│   ├── validator.py       # Core validation engine
│   ├── tests.py          # Test suite
│   └── README.md         # How the truth engine works
├── examples/             # Usage examples
├── docs/                 # Documentation
└── tests/                # Automated tests
```

---

## 🚀 Quick Start

### 1. Browse Verified APIs

Check out the [`verified_apis/`](./verified_apis/) directory to see all working APIs organized by category.

### 2. Run Your Own Tests

```bash
# Clone the repository
git clone https://github.com/onlyecho822-source/api-yellow-pages.git
cd api-yellow-pages

# Install dependencies
pip install -r requirements.txt

# Run the truth engine
python truth_engine/validator.py
```

### 3. Query Multiple APIs at Once

```python
from octopus_mode import OctopusEngine

engine = OctopusEngine()
results = await engine.query_all("CBRN training safety")
print(f"Found {results['total_results']} results across {results['successful_queries']} APIs")
```

---

## 🔍 Featured APIs

### Government & Public Sector

- **[Data.gov](./verified_apis/government/data_gov.md)** - 200,000+ US government datasets
- **[Federal Register](./verified_apis/government/federal_register.md)** - Official US regulations and notices

### Research & Academic

- **[PubMed](./verified_apis/research/pubmed.md)** - 35+ million biomedical citations
- **[arXiv](./verified_apis/research/arxiv.md)** - 2+ million preprint research papers
- **[CrossRef](./verified_apis/research/crossref.md)** - 140+ million scholarly works

### Data & Statistics

- **[World Bank](./verified_apis/data/world_bank.md)** - Global development indicators

### Code Repositories

- **[GitHub](./verified_apis/code/github.md)** - 100+ million repositories

---

## 🛡️ The Truth Engine

Every API in this directory has passed through our **Truth Engine** validation system:

### Validation Criteria

1. **Connectivity Test** - Can we reach the API?
2. **Response Validation** - Does it return valid data?
3. **Performance Check** - Is response time acceptable (<2s)?
4. **Data Quality** - Is the returned data useful and structured?
5. **Rate Limit Check** - What are the usage limits?
6. **Authentication Test** - What auth is required?

### Verification Levels

- 🟢 **Verified** - Tested within last 24 hours, working perfectly
- 🟡 **Caution** - Tested within last week, may have intermittent issues
- 🔴 **Failed** - Not working, removed from directory

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Add a New API

1. Test the API using our truth engine
2. Document it following our template
3. Submit a pull request with verification results

### Report Issues

Found an API that's not working? [Open an issue](https://github.com/onlyecho822-source/api-yellow-pages/issues) with:
- API name
- Error message
- Timestamp of test

### Improve Documentation

Help make this resource better by improving docs, adding examples, or translating content.

---

## 📜 License

MIT License - feel free to use this directory for any purpose.

---

## 🌟 Star This Repo

If you find this useful, please star the repository to help others discover it!

---

## 📞 Contact

- **Issues**: [GitHub Issues](https://github.com/onlyecho822-source/api-yellow-pages/issues)
- **Discussions**: [GitHub Discussions](https://github.com/onlyecho822-source/api-yellow-pages/discussions)

---

**Built with 🐙 Octopus Mode**  
*Extending our reach across the API universe, one tentacle at a time.*

## 🤖 Autonomous System

The API Yellow Pages now includes a fully autonomous system that continuously discovers, validates, and maintains the directory without human intervention.

### Key Features

- **Auto-Discovery**: Searches GitHub, Data.gov, and other sources every 24 hours
- **Smart Categorization**: Automatically organizes APIs by industry and use case
- **Truth Engine Validation**: Tests all APIs every 6 hours
- **Self-Healing Registry**: Removes dead APIs, promotes healthy ones
- **Health Tracking**: Maintains performance history for all APIs
- **Auto-Commit**: Pushes updates to GitHub automatically
- **Live Dashboard**: Real-time monitoring interface

### Components

- `autonomous/` - Discovery engine, registry manager, orchestrator
- `dashboard/` - Live monitoring interface
- `docs/` - Architecture and system documentation

### Quick Start

```bash
# Run autonomous cycle
python3 autonomous/orchestrator.py

# View live dashboard
cd dashboard && python3 -m http.server 8000
```

### Configuration

All autonomous behavior is configurable via `autonomous/config.json`:

- Discovery interval (default: 24h)
- Validation interval (default: 6h)
- Reporting interval (default: 7d)
- Auto-commit enabled/disabled

---

**Timestamp:** 01:42 Jan 05 2026
