import ecpo_ocr_bench


def test_ecpo_ocr_bench(corpus):
    def _tool(p):
        return "Some text."

    result = ecpo_ocr_bench.evaluate_ocr_tool(_tool, data_dir=corpus)

    for _id in ["001", "002", "003"]:
        assert _id in result

    assert result["001"]["distance"] == 0
    assert result["002"]["distance"] == 1
    assert result["003"]["distance"] == 1
