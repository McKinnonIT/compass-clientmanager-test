# Compass Client Manager Test

This repository contains test files for scenarios unavailable in the Compass API, which includes just about anything important.
Includes:

- Offline CompassLink clients, from Compass' Client Manager page (https://yourschool.compass.education/Configure/ConnectedClients.aspx).
- Any Import Jobs with a failed or error status (https://yourschool.compass.education/Configure/ImportJobs.aspx). Limited to the first page (first 25 results).

## Getting Started

### Prerequisites

Ensure you have the following installed:
- Python 3.7+
- `pytest` for running tests
- Any required environment variables configured in an `.env` file.

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/McKinnonIT/compass-clientmanager-test.git
   cd compass-clientmanager-test
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Environment Configuration

Copy the sample environment file and update the values:

```bash
cp .env.sample .env
```

Edit `.env` to include your environment-specific settings.

### Running Tests

To execute the test suite:

```bash
pytest
```

Debugging/Headed
```bash
pytest --headed -s
```

If any CompassLink clients are offline, this test will fail. This occurs based on the existence of the class `.client-error` on the Client Manager page.

### File Structure

- **`.auth/`**: Stores the ASP.NET_SessionId cookie to facilitate subsequent tests following the initial login.
- **`.env.sample`**: Sample environment configuration file.
- **`conftest.py`**: Configuration for `pytest`.
- **`test_compass.py`**: Unit tests for the Compass Client Manager.

