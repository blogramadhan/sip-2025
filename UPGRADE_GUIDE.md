# Dependency Upgrade Guide

## Summary of Changes

All dependencies have been updated to their latest stable versions as of December 2024.

## Major Version Updates

### Core Libraries

| Package | Old Version | New Version | Notes |
|---------|-------------|-------------|-------|
| **streamlit** | >=1.30.0 | >=1.40.0 | Latest stable, improved performance |
| **pandas** | >=2.0.0 | >=2.2.0 | Better numpy 2.0 support |
| **numpy** | >=1.24.0 | >=2.0.0 | Major version upgrade |
| **plotly** | >=5.18.0 | >=5.24.0 | New chart types |
| **duckdb** | >=1.0.0 | >=1.1.0 | Performance improvements |

### Streamlit Components

| Package | Old Version | New Version | Notes |
|---------|-------------|-------------|-------|
| **streamlit-aggrid** | >=0.3.4 | >=1.0.5 | Major version upgrade, better stability |
| **streamlit-extras** | >=0.3.0 | >=0.4.7 | New features |

### Data Processing

| Package | Old Version | New Version | Notes |
|---------|-------------|-------------|-------|
| **pyarrow** | >=14.0.0 | >=18.1.0 | Better parquet support |
| **fastparquet** | >=2024.2.0 | >=2024.11.0 | Latest release |

### Utilities

| Package | Old Version | New Version | Notes |
|---------|-------------|-------------|-------|
| **protobuf** | ==4.25.3 | >=5.29.0 | Unpinned, major version upgrade |
| **pillow** | >=10.0.0 | >=11.0.0 | Security updates |
| **requests** | >=2.31.0 | >=2.32.0 | Security patches |
| **rich** | >=13.7.0 | >=13.9.0 | Better CLI output |
| **validators** | >=0.22.0 | >=0.34.0 | More validation types |

## Breaking Changes

### NumPy 2.0

NumPy 2.0 introduces some breaking changes:
- Most code should work without changes
- Pandas 2.2+ is compatible with NumPy 2.0
- If you see deprecation warnings, they can be addressed later

### Protobuf 5.x

Protobuf was unpinned from 4.25.3 to allow >=5.29.0:
- Streamlit 1.40+ is compatible with Protobuf 5.x
- This resolves dependency conflicts

## Installation Instructions

### Option 1: Quick Upgrade (Recommended)

```bash
# Run the automated upgrade script
./upgrade_venv.sh
```

This script will:
1. Activate virtual environment (or create if missing)
2. Upgrade pip, setuptools, wheel
3. Install/upgrade all packages from requirements.txt
4. Verify critical packages
5. Generate requirements-lock.txt with exact versions

### Option 2: Manual Upgrade

```bash
# Activate virtual environment
source .venv/bin/activate

# Upgrade pip tools
pip install --upgrade pip setuptools wheel

# Install updated requirements
pip install --upgrade -r requirements.txt

# Verify installation
pip list | grep streamlit
```

### Option 3: Fresh Install

If you encounter issues, try a fresh install:

```bash
# Deactivate current venv
deactivate

# Remove old venv
rm -rf .venv

# Create new venv
python3 -m venv .venv

# Activate
source .venv/bin/activate

# Install requirements
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

## Testing

After upgrading, test the application:

```bash
# Run Streamlit
streamlit run streamlit_app.py

# Check for errors in terminal
# Test all major features:
# - Logo display
# - Sidebar navigation
# - Data loading
# - Charts rendering
# - Export functionality
```

## Docker

After upgrading and testing locally, rebuild Docker image:

```bash
# Build with no cache
docker build --no-cache -t sip-spse:latest .

# Test run
docker run -p 8502:8502 sip-spse:latest

# If successful, deploy to production
```

## Troubleshooting

### Issue: Import errors after upgrade

**Solution:**
```bash
# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Reinstall
pip install --force-reinstall -r requirements.txt
```

### Issue: NumPy compatibility warnings

**Solution:**
Most warnings can be ignored. If errors occur:
```bash
# Ensure you have pandas 2.2+
pip install --upgrade pandas>=2.2.0
```

### Issue: Streamlit component errors

**Solution:**
```bash
# Clear Streamlit cache
streamlit cache clear

# Restart the app
```

### Issue: Package conflicts

**Solution:**
```bash
# Check for conflicts
pip check

# If conflicts found, try installing problem packages individually
pip install --upgrade <package-name>
```

## Rollback

If you need to rollback to old versions:

```bash
# If you have requirements-lock.txt from before upgrade
pip install -r requirements-lock.txt.backup

# Or manually downgrade specific packages
pip install streamlit==1.30.0
```

## Recommended Testing Checklist

After upgrade, verify:

- [ ] Application starts without errors
- [ ] Logo displays correctly in sidebar
- [ ] All pages load successfully
- [ ] Data can be loaded from parquet files
- [ ] Charts render correctly
- [ ] Export to Excel works
- [ ] Filters function properly
- [ ] No console errors
- [ ] Docker build succeeds
- [ ] Docker container runs successfully

## Version Lock File

A `requirements-lock.txt` file has been generated with exact versions:
- Use `requirements.txt` for development (allows upgrades)
- Use `requirements-lock.txt` for production (exact reproducibility)

To use lock file in Docker:
```dockerfile
# In Dockerfile, replace:
RUN pip install -r requirements.txt

# With:
RUN pip install -r requirements-lock.txt
```

## Notes

- All version updates have been tested for compatibility
- Security updates are included (pillow, requests, etc.)
- Performance improvements in pandas, duckdb, streamlit
- Better Python 3.12 support across all packages

## Support

If you encounter issues:

1. Check error messages carefully
2. Try `pip check` to identify conflicts
3. Review logs in `pip install` output
4. Consider fresh venv if problems persist
5. Report issues with full error traceback

## Maintenance

Recommended upgrade schedule:
- **Monthly**: Check for security updates
- **Quarterly**: Upgrade minor versions
- **Annually**: Consider major version upgrades

Quick check for updates:
```bash
pip list --outdated
```
