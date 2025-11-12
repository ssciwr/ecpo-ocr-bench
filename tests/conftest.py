import pathlib


# Ensure that each subfolder of the data directory is a test case.
# We only have to use the "corpus" fixture and it will run once for
# each corpus.
def pytest_generate_tests(metafunc):
    if "corpus" in metafunc.fixturenames:
        _corpora = [
            p for p in (pathlib.Path(__file__).parent / "data").rglob("*") if p.is_dir()
        ]
        _ids = [c.stem for c in _corpora]
        metafunc.parametrize("corpus", _corpora, ids=_ids)
