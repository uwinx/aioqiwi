from ..core.tooling.htstrings import HeadTailString


class TerminalsURL(HeadTailString):
    __head__ = "https://edge.qiwi.com/"


class urls:
    base = TerminalsURL("locator/v3/nearest/clusters")
    ttp_groups = TerminalsURL("locator/v3/ttp-groups")
