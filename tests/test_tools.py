from app.tools import describe_provider, list_model_benchmarks


def test_describe_provider_known():
    result = describe_provider("anthropic")
    assert "content" in result
    assert "Claude" in result["content"]


def test_describe_provider_unknown():
    result = describe_provider("does-not-exist")
    assert "error" in result


def test_list_model_benchmarks_without_key(monkeypatch):
    monkeypatch.delenv("ARTIFICIALANALYSIS_API_KEY", raising=False)
    result = list_model_benchmarks()
    assert "error" in result
