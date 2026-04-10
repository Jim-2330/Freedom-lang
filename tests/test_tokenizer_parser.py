from freedon_lang.tokenizer import tokenize
from freedon_lang.parser import parse, Symbol


def test_tokenizer_skips_semicolon_comment_to_eol() -> None:
    tokens = tokenize('(print "a") ; comment here\n(print "b")')
    assert tokens == ["(", "print", '"a"', ")", "(", "print", '"b"', ")"]


def test_parser_symbols_are_distinct_type() -> None:
    program = parse(tokenize("(print 1)"))
    form = program.forms[0]
    assert isinstance(form, list)
    assert isinstance(form[0], Symbol)

