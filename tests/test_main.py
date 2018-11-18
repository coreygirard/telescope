from string import ascii_lowercase

from hypothesis import assume, given
from hypothesis.strategies import dictionaries, integers, lists, text

from telescope.main import *


class Flytrap(object):
    def __init__(self):
        self.route = None

    def f(self, route):
        self.route = route


def test__Telescope():
    flytrap = Flytrap()

    t = {"aaa": ("", None)}
    tele = Telescope([], t, "", flytrap.f)
    tele.aaa
    assert flytrap.route == [("aaa", None, None)]

    t = {"aaa": ("()", None)}
    tele = Telescope([], t, "", flytrap.f)
    tele.aaa()
    assert flytrap.route == [("aaa()", (), {})]
    tele.aaa(4)
    assert flytrap.route == [("aaa()", (4,), {})]
    tele.aaa(k=5)
    assert flytrap.route == [("aaa()", (), {"k": 5})]


@given(lists(text(ascii_lowercase)))
def test__Telescope__attribute__property(attrs):
    assume("" not in attrs)
    assume(all("." not in a for a in attrs))
    assume(attrs)  # equivalent to len(attrs) > 0

    flytrap = Flytrap()

    t = None
    for a in reversed(attrs):
        t = {a: ("", t)}

    tele = Telescope([], t, "", flytrap.f)
    assert flytrap.route is None


@given(text(ascii_lowercase), lists(integers()), dictionaries(text(), integers()))
def test__Telescope__method__property(method, args, kwargs):
    assume(method != "")

    flytrap = Flytrap()
    t = {method: ("()", None)}
    tele = Telescope([], t, "", flytrap.f)
    getattr(tele, method)(*args, **kwargs)
    assert flytrap.route == [(method + "()", tuple(args), kwargs)]

    flytrap = Flytrap()
    t = {method: ("()", {})}
    tele = Telescope([], t, "", flytrap.f)
    getattr(tele, method)(*args, **kwargs)
    assert flytrap.route is None
