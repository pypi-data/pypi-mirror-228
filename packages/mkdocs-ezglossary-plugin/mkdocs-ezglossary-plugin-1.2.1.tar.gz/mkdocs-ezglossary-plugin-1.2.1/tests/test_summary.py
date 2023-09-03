import logging

from lxml import etree
from yaxp import xpath as xp

import mock

log = logging.getLogger(__name__)


def test_summary(simple, summary, config):
    config['inline_refs'] = "short"
    pages = mock.render([simple, summary], config)
    summary = pages["summary.md"]
    log.debug(summary)
    tree = etree.fromstring(summary)

    dd = xp.dd().ul().li().a(href="../simple.md#test_first_defs_0",
                             text="Hello")
    dl = xp.dl(_class="mkdocs-ezglossary-summary", _id="test")
    dl = dl.has(xp.dt(text="first"))
    dl = dl.has(dd)
    assert len(tree.xpath(str(dl))) == 1

    dd = xp.dd().ul().li().a(href="../simple.md#test_first_refs_0",
                             text="Hello")
    dl = xp.dl(_class="mkdocs-ezglossary-summary", _id="test")
    dl = dl.has(xp.dt(text="first"))
    dl = dl.has(dd)
    assert len(tree.xpath(str(dl))) == 0

    dd = xp.dd().ul().li().a(href="../simple.md#test_third_defs_0",
                             text="Hello")
    dl = xp.dl(_class="mkdocs-ezglossary-summary", _id="test")
    dl = dl.has(xp.dt(text="third"))
    dl = dl.has(dd)
    assert len(tree.xpath(str(dl))) == 1

    dd = xp.dd().ul().li().a(href="../simple.md#demo_first_defs_0",
                             text="Hello")
    dl = xp.dl(_class="mkdocs-ezglossary-summary", _id="demo")
    dl = dl.has(xp.dt(text="first"))
    dl = dl.has(dd)
    assert len(tree.xpath(str(dl))) == 1

    dd = xp.dd().ul().li().a(href="../simple.md#test_third_refs_0",
                             text="Hello")
    dl = xp.dl(_class="mkdocs-ezglossary-summary", _id="test")
    dl = dl.has(xp.dt(text="third"))
    dl = dl.has(dd)
    assert len(tree.xpath(str(dl))) == 1

    dd = xp.dd().ul().li().a(href="../simple.md#demo_third_refs_0",
                             text="Hello")
    dl = xp.dl(_class="mkdocs-ezglossary-summary", _id="demo")
    dl = dl.has(xp.dt(text="third"))
    dl = dl.has(dd)
    assert len(tree.xpath(str(dl))) == 0


def test_summary_noref(simple, summary, config):
    config['list_references'] = False
    pages = mock.render([simple, summary], config)
    summary = pages["summary.md"]
    tree = etree.fromstring(summary)

    dd = xp.dd().ul().li().a(href="../simple.md#test_first_defs_0",
                             text="Hello")
    dl = xp.dl(_class="mkdocs-ezglossary-summary", _id="test")
    dl = dl.has(xp.dt(text="first"))
    dl = dl.has(dd)
    assert len(tree.xpath(str(dl))) == 1

    dd = xp.dd().ul().li().a(href="../simple.md#test_third_refs_0",
                             text="Hello")
    dl = xp.dl(_class="mkdocs-ezglossary-summary", _id="test")
    dl = dl.has(xp.dt(text="third"))
    dl = dl.has(dd)
    assert len(tree.xpath(str(dl))) == 0


def test_summary_nodef(simple, summary, config):
    config['list_definitions'] = False
    pages = mock.render([simple, summary], config)
    summary = pages["summary.md"]
    tree = etree.fromstring(summary)

    dd = xp.dd().ul().li().a(href="../simple.md#test_first_defs_0",
                             text="Hello")
    dl = xp.dl(_class="mkdocs-ezglossary-summary", _id="test")
    dl = dl.has(xp.dt(text="first"))
    dl = dl.has(dd)
    assert len(tree.xpath(str(dl))) == 0

    dd = xp.dd().ul().li().a(href="../simple.md#test_third_refs_0",
                             text="Hello")
    dl = xp.dl(_class="mkdocs-ezglossary-summary", _id="test")
    dl = dl.has(xp.dt(text="third"))
    dl = dl.has(dd)
    assert len(tree.xpath(str(dl))) == 1


def test_custom_summaryf(simple, summary, config):
    config['templates'] = "tests/custom"
    pages = mock.render([simple, summary], config)
    summary = pages["summary.md"]
    tree = etree.fromstring(summary)

    dd = xp.dd().ul().li().a(href="../simple.md#test_third_refs_0",
                             text="Hello")
    dl = xp.dl(_class="custom-summary", _id="test")
    dl = dl.has(xp.dt(text="third"))
    dl = dl.has(dd)
    assert len(tree.xpath(str(dl))) == 1
