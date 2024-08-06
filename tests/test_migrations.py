import pytest

def test_migration(runner, migrate):
    """Example test that might require migrations."""
    result = runner.invoke(args=['db', 'upgrade'])
    assert result.exit_code == 0
