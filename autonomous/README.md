# 🤖 Autonomous System

The API Yellow Pages autonomous system continuously discovers, validates, and maintains a verified directory of working APIs without human intervention.

## Components

### Discovery Engine (`discovery_engine.py`)
- Searches GitHub, Data.gov, and other sources for new APIs
- Smart categorization by use case and industry
- Automatic tagging (REST, GraphQL, OAuth, etc.)
- Runs every 24 hours

### Registry Manager (`registry_manager.py`)
- Self-healing registry with health tracking
- Promotes/demotes APIs based on performance
- Removes consistently failing APIs
- Maintains health history for all APIs

### Orchestrator (`orchestrator.py`)
- Master controller coordinating all operations
- Configurable scheduling
- Automated GitHub commits
- Health reporting

### Scheduler (`schedule.sh`)
- Bash script for cron integration
- Logs all executions
- Can be run manually or via cron

## Quick Start

```bash
# Run full autonomous cycle
python3 autonomous/orchestrator.py

# Run discovery only
python3 autonomous/discovery_engine.py

# Run validation only
python3 autonomous/registry_manager.py
```

## Configuration

Edit `autonomous/config.json` to customize:

```json
{
  "discovery": {
    "enabled": true,
    "interval_hours": 24
  },
  "validation": {
    "enabled": true,
    "interval_hours": 6
  },
  "auto_commit": {
    "enabled": true
  }
}
```

## Features

- **Auto-Discovery**: Finds new APIs from multiple sources
- **Smart Categorization**: Organizes by industry and use case
- **Truth Engine**: Validates API quality and reliability
- **Self-Healing**: Removes dead APIs, promotes healthy ones
- **Health Tracking**: Maintains history for all APIs
- **Auto-Commit**: Pushes updates to GitHub automatically
- **Live Dashboard**: Real-time monitoring interface

## Timestamp

Created: 01:40 Jan 05 2026
