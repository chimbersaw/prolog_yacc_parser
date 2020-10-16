#!/usr/bin/env python3
import prolog_parser
import re


# Correct


def test_integrate_correct_trivial(tmp_path, monkeypatch, capsys):
    (tmp_path / 'input.mod').write_text('f.')
    monkeypatch.chdir(tmp_path)
    prolog_parser.main(['input.mod', 'test'])
    out, err = capsys.readouterr()
    assert err == '' or err == 'Generating LALR tables\n'
    assert out == 'relation\n	head\n		identifier = f\n'


def test_integrate_correct_spaces(tmp_path, monkeypatch, capsys):
    (tmp_path / 'input.mod').write_text('f.       \n\n\n\n  f :- g.      \n '
                                        '         f \n    :-   g, \n\n\nh   ; t  . '
                                        '   \n\n\n')
    monkeypatch.chdir(tmp_path)
    prolog_parser.main(['input.mod', 'test'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'relation\n	head\n		identifier = f\nrelation\n	head\n		identifier = f\n	body\n		' \
                  'identifier = g\nrelation\n	head\n		identifier = f\n	body\n		disjunction\n			' \
                  'conjunction\n				identifier = g\n				identifier = h\n			identifier ' \
                  '= t\n'


def test_integrate_correct_brackets(tmp_path, monkeypatch, capsys):
    (tmp_path / 'input.mod').write_text('f ((f)) :- g ; h.')
    monkeypatch.chdir(tmp_path)
    prolog_parser.main(['input.mod', 'test'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'relation\n	head\n		atom\n			identifier = f\n			atom\n				atom\n	' \
                  '				identifier = f\n	body\n		disjunction\n			identifier = g\n			' \
                  'identifier = h\n'


def test_integrate_correct_atom(tmp_path, monkeypatch, capsys):
    (tmp_path / 'input.mod').write_text('f :- g, (h; t).')
    monkeypatch.chdir(tmp_path)
    prolog_parser.main(['input.mod', 'test'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'relation\n	head\n		identifier = f\n	body\n		conjunction\n			identifier = ' \
                  'g\n			disjunction\n				identifier = h\n				identifier = t\n'


def test_integrate_correct_atom_args(tmp_path, monkeypatch, capsys):
    (tmp_path / 'input.mod').write_text('a b c.\na (b c).')
    monkeypatch.chdir(tmp_path)
    prolog_parser.main(['input.mod', 'test'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'relation\n	head\n		atom\n			identifier = a\n			identifier = b\n			' \
                  'identifier = c\nrelation\n	head\n		atom\n			identifier = a\n			atom\n		' \
                  '		identifier = b\n				identifier = c\n'


def test_integrate_correct_shtopor(tmp_path, monkeypatch, capsys):
    (tmp_path / 'input.mod').write_text('f :- g.')
    monkeypatch.chdir(tmp_path)
    prolog_parser.main(['input.mod', 'test'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'relation\n	head\n		identifier = f\n	body\n		identifier = g\n'


def test_integrate_correct_big(tmp_path, monkeypatch, capsys):
    (tmp_path / 'input.mod').write_text('f :- g.\nf :- (a, b).\nf :- (a; b), h.\nf :- (a, b); h.\nf :- h, (a; b).\nf '
                                        ':- h; (a, b).\nf :- a , b , c ; d , e , f ; g , h , ((a) , (a , a ; a , '
                                        '((a ; (b)) ; a))) ; u ; a , a , a ; a ; a, a, (a) , (a ; h) , g.\n')
    monkeypatch.chdir(tmp_path)
    prolog_parser.main(['input.mod', 'test'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'relation\n	head\n		identifier = f\n	body\n		identifier = g\nrelation\n	head\n		' \
                  'identifier = f\n	body\n		conjunction\n			identifier = a\n			identifier = ' \
                  'b\nrelation\n	head\n		identifier = f\n	body\n		conjunction\n			' \
                  'disjunction\n				identifier = a\n				identifier = b\n			identifier ' \
                  '= h\nrelation\n	head\n		identifier = f\n	body\n		disjunction\n			' \
                  'conjunction\n				identifier = a\n				identifier = b\n			identifier ' \
                  '= h\nrelation\n	head\n		identifier = f\n	body\n		conjunction\n			identifier = ' \
                  'h\n			disjunction\n				identifier = a\n				identifier = ' \
                  'b\nrelation\n	head\n		identifier = f\n	body\n		disjunction\n			identifier = ' \
                  'h\n			conjunction\n				identifier = a\n				identifier = ' \
                  'b\nrelation\n	head\n		identifier = f\n	body\n		disjunction\n			' \
                  'conjunction\n				identifier = a\n				conjunction\n					' \
                  'identifier = b\n					identifier = c\n			disjunction\n				' \
                  'conjunction\n					identifier = d\n					conjunction\n				' \
                  '		identifier = e\n						identifier = f\n				disjunction\n		' \
                  '			conjunction\n						identifier = g\n						' \
                  'conjunction\n							identifier = h\n							' \
                  'conjunction\n								identifier = a\n								' \
                  'disjunction\n									conjunction\n									' \
                  '	identifier = a\n										identifier = a\n						' \
                  '			conjunction\n										identifier = a\n					' \
                  '					disjunction\n											disjunction\n			' \
                  '									identifier = a\n												' \
                  'identifier = b\n											identifier = a\n					' \
                  'disjunction\n						identifier = u\n						disjunction\n		' \
                  '					conjunction\n								identifier = a\n					' \
                  '			conjunction\n									identifier = a\n						' \
                  '			identifier = a\n							disjunction\n								' \
                  'identifier = a\n								conjunction\n									' \
                  'identifier = a\n									conjunction\n									' \
                  '	identifier = a\n										conjunction\n							' \
                  '				identifier = a\n											conjunction\n			' \
                  '									disjunction\n													' \
                  'identifier = a\n													identifier = h\n				' \
                  '								identifier = g\n'


# Incorrect

def test_integrate_incorrect_empty(tmp_path, monkeypatch, capsys):
    (tmp_path / 'input.mod').write_text('')
    monkeypatch.chdir(tmp_path)
    prolog_parser.main(['input.mod'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'Syntax error: unexpected end of file.\n'


def test_integrate_incorrect_eof1(tmp_path, monkeypatch, capsys):
    (tmp_path / 'input.mod').write_text('')
    monkeypatch.chdir(tmp_path)
    prolog_parser.main(['input.mod'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'Syntax error: unexpected end of file.\n'


def test_integrate_incorrect_eof2(tmp_path, monkeypatch, capsys):
    (tmp_path / 'input.mod').write_text('f :- g')
    monkeypatch.chdir(tmp_path)
    prolog_parser.main(['input.mod'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'Syntax error: unexpected end of file.\n'


def test_integrate_incorrect_eof3(tmp_path, monkeypatch, capsys):
    (tmp_path / 'input.mod').write_text('f :-')
    monkeypatch.chdir(tmp_path)
    prolog_parser.main(['input.mod'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'Syntax error: unexpected end of file.\n'


def test_integrate_incorrect_illegal_character(tmp_path, monkeypatch, capsys):
    (tmp_path / 'input.mod').write_text('f : - f.')
    monkeypatch.chdir(tmp_path)
    prolog_parser.main(['input.mod'])
    out, err = capsys.readouterr()
    assert err == ''
    assert re.match(r'Illegal character', out)


def test_integrate_incorrect_no_right_operand(tmp_path, monkeypatch, capsys):
    (tmp_path / 'input.mod').write_text('f :- a , .')
    monkeypatch.chdir(tmp_path)
    prolog_parser.main(['input.mod'])
    out, err = capsys.readouterr()
    assert err == ''
    assert re.fullmatch(r'Syntax error: line \d+, col \d+.\n', out)


def test_integrate_incorrect_no_left_operand(tmp_path, monkeypatch, capsys):
    (tmp_path / 'input.mod').write_text('f :- , b.')
    monkeypatch.chdir(tmp_path)
    prolog_parser.main(['input.mod'])
    out, err = capsys.readouterr()
    assert err == ''
    assert re.fullmatch(r'Syntax error: line \d+, col \d+.\n', out)


def test_integrate_incorrect_no_head(tmp_path, monkeypatch, capsys):
    (tmp_path / 'input.mod').write_text(':- f.')
    monkeypatch.chdir(tmp_path)
    prolog_parser.main(['input.mod'])
    out, err = capsys.readouterr()
    assert err == ''
    assert re.fullmatch(r'Syntax error: line \d+, col \d+.\n', out)


def test_integrate_incorrect_no_body(tmp_path, monkeypatch, capsys):
    (tmp_path / 'input.mod').write_text('f :- .')
    monkeypatch.chdir(tmp_path)
    prolog_parser.main(['input.mod'])
    out, err = capsys.readouterr()
    assert err == ''
    assert re.fullmatch(r'Syntax error: line \d+, col \d+.\n', out)


def test_integrate_incorrect_bad_brackets(tmp_path, monkeypatch, capsys):
    (tmp_path / 'input.mod').write_text('f :- (g ; (f).')
    monkeypatch.chdir(tmp_path)
    prolog_parser.main(['input.mod'])
    out, err = capsys.readouterr()
    assert err == ''
    assert re.fullmatch(r'Syntax error: line \d+, col \d+.\n', out)


def test_integrate_incorrect_multiple_lines(tmp_path, monkeypatch, capsys):
    (tmp_path / 'input.mod').write_text('f :- g.\nf :- f ; f . f ; (f).\n f.     \nf :- a , b ; .')
    monkeypatch.chdir(tmp_path)
    prolog_parser.main(['input.mod'])
    out, err = capsys.readouterr()
    assert err == ''
    assert re.match(r'Syntax error: line \d+, col \d+.\n', out)
