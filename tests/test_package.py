import chordian


def test_version_is_exposed():
    assert isinstance(chordian.__version__, str)
    assert chordian.__version__.count(".") >= 2


def test_resources_are_exported():
    for name in (
        "AgenticCrawler",
        "ChordianDeepSearch",
        "CompanySearch",
        "PeopleSearch",
        "Research",
        "WebAndResearch",
        "EnterpriseSearch",
        "Memory",
    ):
        assert hasattr(chordian, name)


def test_default_base_urls():
    assert chordian.core_base_url == "https://chordian-core.chordian.ai"
    assert chordian.memory_base_url == "https://graph-kb.chordian.ai"
