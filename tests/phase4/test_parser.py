import pytest

from phase4.parser import ParseError, parse_llm_response


def test_parse_llm_response_from_json_object():
  raw = """
  {
    "recommendations": [
      {"rank": 2, "name": "Truffles", "explanation": "Great Italian options."},
      {"rank": 1, "name": "Onesta", "explanation": "Strong pizza choice."}
    ]
  }
  """
  parsed = parse_llm_response(raw)
  assert [item["name"] for item in parsed] == ["Onesta", "Truffles"]


def test_parse_llm_response_extracts_embedded_json():
  raw = 'Here you go:\n{"recommendations":[{"name":"Cafe","explanation":"Nice"}]}'
  parsed = parse_llm_response(raw)
  assert parsed[0]["name"] == "Cafe"


def test_parse_llm_response_rejects_invalid_payload():
  with pytest.raises(ParseError):
    parse_llm_response('{"summary":"no list here"}')
