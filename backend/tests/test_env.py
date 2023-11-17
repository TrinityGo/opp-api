import env

def test_alembic_configuration():
    assert env.config is not None
    assert 'sqlalchemy.url' in env.config.get_main_option()
