"""Shared closed grammars and format rules (T05 #7 d1/d5; T09/T22 formats).

Reject, never normalize: nothing here lowercases, trims, case-folds, or
repairs (T05 #7 d5).
"""

import re

# The stable key / alias grammar (T05 #7 d1; T15 #10 d5).
KEY_RE = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")

PERMISSION_SET_KEY_BOUNDS = (2, 24)
GROUP_KEY_BOUNDS = (2, 64)

# The documented AWS PermissionSet.Description character pattern
# (T05 #7 d3; pin-reverified per T15): printable ASCII plus Latin-1
# supplement, with tab/LF/CR.
DESCRIPTION_RE = re.compile("^[\t\n\r\x20-\x7e\xa1-\xff]*$")

# The AWS permission-set Name pattern (T05 #7 d3).
DEPLOYED_NAME_RE = re.compile(r"^[\w+=,.@-]+$")

# ISO-8601 duration (session_duration; T21 #20 d3).
DURATION_RE = re.compile(r"^P(([0-9]+[YMWD])+|([0-9]+[YMWD])*T([0-9]+[HMS])+)$")

# The complete RFC 3339 UTC representation T09 permits for discovered_at,
# fractional seconds accepted when present (T22 #21 d1; T09 #12 d4).
RFC3339_UTC_RE = re.compile(
    r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]+)?Z$"
)

SNAPSHOT_ID_RE = re.compile(r"^[0-9a-f]{64}$")

PREFIX_BUDGET = 8          # including the delimiter (T05 #7 d1)
COMPOSED_NAME_MAX = 32     # AWS Name limit (T05 #7 d1/d3)

_DAYS = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)


def key_valid(value, bounds):
    lo, hi = bounds
    return (
        isinstance(value, str)
        and bool(KEY_RE.match(value))
        and lo <= len(value) <= hi
    )


def alias_valid(value):
    return isinstance(value, str) and bool(KEY_RE.match(value))


def idstore_name_defects(value):
    """T05 #7 d2/d5: exact code-point rules; no normalization ever."""
    if not isinstance(value, str) or value == "":
        return ["missing or empty"]
    defects = []
    if value[0].isspace() or value[-1].isspace():
        defects.append("leading or trailing Unicode whitespace")
    if any(ch.isspace() and ch != " " for ch in value) or any(
        ord(ch) < 0x20 or ord(ch) == 0x7F for ch in value
    ):
        defects.append("Unicode control or non-space whitespace character")
    return defects


def rfc3339_utc_calendar_valid(value):
    """Clock-free calendar validity (declaration-vocabulary amendment 4):
    the shape is checked by RFC3339_UTC_RE; this rejects impossible dates
    and times without consulting any clock."""
    if not isinstance(value, str) or not RFC3339_UTC_RE.match(value):
        return False
    year = int(value[0:4])
    month = int(value[5:7])
    day = int(value[8:10])
    hour = int(value[11:13])
    minute = int(value[14:16])
    second = int(value[17:19])
    if not 1 <= month <= 12:
        return False
    days = _DAYS[month - 1]
    if month == 2 and (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)):
        days = 29
    if not 1 <= day <= days:
        return False
    # 23:59:60 leap seconds are not accepted: T09 timestamps are producer
    # clock strings and AWS emits none.
    return hour <= 23 and minute <= 59 and second <= 59
