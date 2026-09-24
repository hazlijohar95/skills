#!/usr/bin/env python3
"""Deterministic checks for the close skills. Stdlib only, Python 3.9+.

Every figure a check prints comes from Decimal arithmetic on the files given.
Exit 0 means the check passed, 1 means it found problems, 2 means bad input.

Canonical input shapes (normalize any system's export into these first):
  TB  CSV: account,debit,credit
  GL  CSV: date,account,memo,debit,credit[,kind]   kind = opening | activity (default)
  JE  CSV: entry_no,date,account,memo,debit,credit  (see skills/financial-close/journal-entry/reference/je-csv-format.md)
  Log TSV: ts,phase,event,subject,who,evidence       (written by the `log` command)
"""

import argparse
import csv
import hashlib
import json
import re
import sys
import zipfile
from collections import OrderedDict
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path

ZERO = Decimal("0.00")
CENT = Decimal("0.01")
JE_HEADER = ["entry_no", "date", "account", "memo", "debit", "credit"]
LOG_HEADER = ["ts", "phase", "event", "subject", "who", "evidence"]
LOG_EVENTS = {"approve", "decline", "accept", "decision", "question", "answer", "phase-done", "resume", "override"}


class InputError(Exception):
    pass


def money(raw, where, strict=False):
    """Parse an amount. Lenient mode takes 1,234.56 and (12.00); strict mode is the JE CSV contract."""
    text = (raw or "").strip()
    if text == "":
        return ZERO
    if strict and not re.fullmatch(r"\d+\.\d{2}", text):
        raise InputError(f"{where}: amount {raw!r} must be a positive number with two decimals, no symbols")
    negative = text.startswith("(") and text.endswith(")")
    text = text.strip("()").replace(",", "")
    try:
        value = Decimal(text)
    except InvalidOperation:
        raise InputError(f"{where}: {raw!r} is not an amount; normalize the export first") from None
    if value != value.quantize(CENT):
        raise InputError(f"{where}: {raw!r} carries more than two decimals")
    return -value if negative else value


def read_csv(path, required):
    try:
        with open(path, newline="", encoding="utf-8-sig") as fh:
            reader = csv.DictReader(fh)
            header = [h.strip() for h in reader.fieldnames or []]
            rows = list(reader)
    except FileNotFoundError:
        raise InputError(f"{path}: file not found") from None
    missing = [c for c in required if c not in header]
    if missing:
        raise InputError(f"{path}: missing column(s) {', '.join(missing)}; header is {','.join(header)}")
    return [{k.strip(): (v or "").strip() for k, v in r.items() if k} for r in rows]


def load_tb(path):
    """Account -> debit-positive balance, in file order."""
    balances = OrderedDict()
    for i, row in enumerate(read_csv(path, ["account", "debit", "credit"]), start=2):
        name = row["account"]
        if not name:
            raise InputError(f"{path}:{i}: blank account name")
        amount = money(row["debit"], f"{path}:{i}") - money(row["credit"], f"{path}:{i}")
        balances[name] = balances.get(name, ZERO) + amount
    return balances


def fmt(value):
    return f"{value:,.2f}"


def cmd_tb(args):
    rows = read_csv(args.tb, ["account", "debit", "credit"])
    debits = sum((money(r["debit"], f"{args.tb}:{i}") for i, r in enumerate(rows, 2)), ZERO)
    credits = sum((money(r["credit"], f"{args.tb}:{i}") for i, r in enumerate(rows, 2)), ZERO)
    names = [r["account"] for r in rows]
    dupes = sorted({n for n in names if names.count(n) > 1})
    print(f"rows {len(rows)}  total debits {fmt(debits)}  total credits {fmt(credits)}  difference {fmt(debits - credits)}")
    ok = debits == credits
    if not ok:
        print(f"FAIL: trial balance out of balance by {fmt(debits - credits)}")
    if dupes:
        print(f"WARN: account listed more than once: {', '.join(dupes)}")
    if ok:
        print("OK: trial balance balances")
    return 0 if ok else 1


def cmd_tie(args):
    tb = load_tb(args.tb)
    prior = load_tb(args.prior) if args.prior else None
    gl_open, gl_act = {}, {}
    for i, row in enumerate(read_csv(args.gl, ["date", "account", "debit", "credit"]), start=2):
        amount = money(row["debit"], f"{args.gl}:{i}") - money(row["credit"], f"{args.gl}:{i}")
        bucket = gl_open if row.get("kind", "").lower() == "opening" else gl_act
        bucket[row["account"]] = bucket.get(row["account"], ZERO) + amount

    has_gl_opening = bool(gl_open)
    if not has_gl_opening and prior is None:
        print("NOTE: no GL opening rows and no prior TB; balance sheet ties below cover movement only")

    accounts = list(OrderedDict.fromkeys([*tb, *gl_open, *gl_act, *(prior or {})]))
    failures = 0
    print(f"{'account':32} {'opening':>14} {'activity':>14} {'GL closing':>14} {'TB closing':>14} {'difference':>12}  diagnosis")
    for name in accounts:
        opening = gl_open.get(name, ZERO) if has_gl_opening else (prior or {}).get(name, ZERO)
        activity = gl_act.get(name, ZERO)
        gl_close = opening + activity
        tb_close = tb.get(name, ZERO)
        diff = tb_close - gl_close
        diagnosis = "ties"
        if diff:
            failures += 1
            if has_gl_opening and prior is not None:
                opening_diff = prior.get(name, ZERO) - gl_open.get(name, ZERO)
                if opening_diff == diff:
                    diagnosis = "constant difference: records disagree about the opening balance"
                elif opening_diff == ZERO:
                    diagnosis = "difference arose in period activity or cutoff"
                else:
                    diagnosis = f"opening differs by {fmt(opening_diff)} and the gap moved in the period; both"
            else:
                diagnosis = "does not tie; constant-difference test needs GL opening rows and a prior TB"
            if name not in tb:
                diagnosis += "; account absent from TB"
        print(f"{name[:32]:32} {fmt(opening):>14} {fmt(activity):>14} {fmt(gl_close):>14} {fmt(tb_close):>14} {fmt(diff):>12}  {diagnosis}")
    print(f"{'FAIL' if failures else 'OK'}: {failures} of {len(accounts)} accounts do not tie")
    return 1 if failures else 0


def parse_iso(text, where):
    try:
        return date.fromisoformat(text)
    except ValueError:
        raise InputError(f"{where}: date {text!r} is not YYYY-MM-DD") from None


def period_bounds(args):
    """Explicit --start/--end win; otherwise a YYYY-MM or YYYY-Qn label implies them."""
    if args.start and args.end:
        return parse_iso(args.start, "--start"), parse_iso(args.end, "--end")
    m = re.fullmatch(r"(\d{4})-(?:(\d{2})|Q([1-4]))", args.label or "")
    if not m:
        raise InputError("give --start and --end, or a --label like 2026-07 or 2026-Q2 (fiscal-year labels need explicit dates)")
    year = int(m.group(1))
    first = int(m.group(2)) if m.group(2) else 3 * int(m.group(3)) - 2
    last = first if m.group(2) else first + 2
    if not 1 <= first <= 12:
        raise InputError(f"--label {args.label!r} has no month {first}")
    after = date(year + (last == 12), last % 12 + 1, 1)
    return date(year, first, 1), date.fromordinal(after.toordinal() - 1)


def read_log(path):
    if not Path(path).exists():
        return []
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    if rows and list(rows[0].keys()) != LOG_HEADER:
        raise InputError(f"{path}: header must be {' '.join(LOG_HEADER)}")
    return rows


def cmd_je(args):
    with open(args.csv, newline="", encoding="utf-8-sig") as fh:
        reader = csv.reader(fh)
        header = next(reader, [])
        lines = list(reader)
    problems = []
    if header != JE_HEADER:
        problems.append(f"header is {','.join(header)!r}, contract is {','.join(JE_HEADER)!r}")
    chart = set(load_tb(args.coa)) if args.coa else None
    start, end = period_bounds(args)

    entries = OrderedDict()
    seen_closed = set()
    last_no = None
    for i, cells in enumerate(lines, start=2):
        where = f"line {i}"
        if len(cells) != len(JE_HEADER):
            problems.append(f"{where}: {len(cells)} columns, expected {len(JE_HEADER)}")
            continue
        row = dict(zip(JE_HEADER, (c.strip() for c in cells)))
        no = row["entry_no"]
        if no != last_no:
            if no in seen_closed or no in entries:
                problems.append(f"{where}: entry {no} lines are not contiguous")
            if last_no is not None:
                seen_closed.add(last_no)
            last_no = no
        try:
            dr = money(row["debit"], where, strict=True) if row["debit"] else ZERO
            cr = money(row["credit"], where, strict=True) if row["credit"] else ZERO
            day = parse_iso(row["date"], where)
        except InputError as err:
            problems.append(str(err))
            continue
        if (dr > 0) == (cr > 0):
            problems.append(f"{where}: exactly one of debit or credit must be filled")
        if not start <= day <= end:
            problems.append(f"{where}: date {day} outside {start} to {end}")
        if chart is not None and row["account"] not in chart:
            problems.append(f"{where}: account {row['account']!r} is not in the chart of accounts")
        if args.label and not row["memo"].startswith(f"{args.label} close: "):
            problems.append(f"{where}: memo must start with '{args.label} close: '")
        entry = entries.setdefault(no, {"dr": ZERO, "cr": ZERO, "memos": set(), "seen_credit": False})
        if dr > 0 and entry["seen_credit"]:
            problems.append(f"{where}: debit line after a credit line in entry {no}")
        entry["seen_credit"] |= cr > 0
        entry["dr"] += dr
        entry["cr"] += cr
        entry["memos"].add(row["memo"])

    total_dr = sum((e["dr"] for e in entries.values()), ZERO)
    total_cr = sum((e["cr"] for e in entries.values()), ZERO)
    for no, e in entries.items():
        if e["dr"] != e["cr"]:
            problems.append(f"entry {no}: debits {fmt(e['dr'])} vs credits {fmt(e['cr'])}")
        if len(e["memos"]) != 1:
            problems.append(f"entry {no}: lines carry different memos")

    if args.log:
        status = {}
        for row in read_log(args.log):
            if row["event"] in ("approve", "decline"):
                status[row["subject"]] = row
        for no, e in entries.items():
            memo = next(iter(e["memos"]))
            last = status.get(memo)
            if last is None:
                problems.append(f"entry {no}: no approval in {args.log} for memo {memo!r}")
            elif last["event"] != "approve":
                problems.append(f"entry {no}: last recorded decision is {last['event']} by {last['who']}")
            elif not last["who"].strip():
                problems.append(f"entry {no}: approval row names no approver")

    print(f"entries {len(entries)}  lines {len(lines)}  total debits {fmt(total_dr)}  total credits {fmt(total_cr)}")
    for p in problems:
        print(f"FAIL: {p}")
    if not problems:
        print("OK: CSV meets the JE contract" + (" and every entry has a logged approval" if args.log else ""))
    return 1 if problems else 0


def fingerprint(path):
    data = Path(path).read_bytes()
    info = {"sha256": hashlib.sha256(data).hexdigest()}
    if path.lower().endswith(".csv"):
        with open(path, newline="", encoding="utf-8-sig") as fh:
            rows = list(csv.DictReader(fh))
        info["rows"] = len(rows)
        for col in ("debit", "credit"):
            if rows and col in rows[0]:
                try:
                    info[f"total_{col}"] = str(sum((money(r[col], path) for r in rows), ZERO))
                except InputError:
                    pass
    return info


def cmd_fingerprint(args):
    current = {str(Path(p)): fingerprint(p) for p in args.files}
    if args.check:
        saved = json.loads(Path(args.check).read_text())
        stale = False
        for name, before in saved.items():
            if not Path(name).exists():
                print(f"STALE: {name} no longer exists")
                stale = True
                continue
            now = current.get(name) or fingerprint(name)
            if now["sha256"] != before["sha256"]:
                changes = [f"{k} {before.get(k)} -> {now.get(k)}" for k in ("rows", "total_debit", "total_credit") if before.get(k) != now.get(k)]
                print(f"STALE: {name} changed" + (f" ({'; '.join(changes)})" if changes else " (content only)"))
                stale = True
        print("FAIL: data changed since the fingerprint was taken" if stale else "OK: every fingerprinted file is unchanged")
        return 1 if stale else 0
    text = json.dumps(current, indent=2)
    if args.out:
        Path(args.out).write_text(text + "\n")
        print(f"wrote {args.out} covering {len(current)} file(s)")
    else:
        print(text)
    return 0


BANNED = [
    (re.compile("—"), "em dash"),
    (re.compile(r"\s–\s"), "spaced en dash used as a dash"),
    (re.compile(r"\b(delve|delves|delving|robust|seamless(?:ly)?|leverag(?:e|es|ing)|comprehensive|crucial)\b", re.I), "filler word"),
    (re.compile(r"it'?s important to note|in conclusion|i hope this helps|please don'?t hesitate|^overall,", re.I | re.M), "boilerplate"),
    (re.compile(r"\bnot (?:just|only|merely) [^.;\n]{1,80}?,? but\b", re.I), "'not just X, but Y' construction"),
    (re.compile("[\U0001F300-\U0001FAFF☀-➿⭐✅]"), "emoji"),
]


def document_text(path):
    if path.lower().endswith(".docx"):
        with zipfile.ZipFile(path) as z:
            xml = z.read("word/document.xml").decode("utf-8")
        xml = re.sub(r"</w:p>", "\n", xml)
        return re.sub(r"<[^>]+>", "", xml)
    return Path(path).read_text(encoding="utf-8")


def cmd_lint(args):
    hits = 0
    for path in args.files:
        for n, line in enumerate(document_text(path).splitlines(), start=1):
            for pattern, label in BANNED:
                for m in pattern.finditer(line):
                    hits += 1
                    print(f"{path}:{n}: {label}: {line.strip()[:120]}")
    print(f"FAIL: {hits} voice violation(s)" if hits else "OK: no banned tells")
    return 1 if hits else 0


def cell(text):
    text = re.sub(r"[\t\r\n]+", " ", text).strip()
    return "'" + text if text[:1] in ("=", "+", "-", "@") else text


def cmd_log(args):
    if args.event not in LOG_EVENTS:
        raise InputError(f"event must be one of {', '.join(sorted(LOG_EVENTS))}")
    if args.event in ("approve", "decline", "accept", "override") and not args.who.strip():
        raise InputError(f"a {args.event} row must name the person who gave it")
    path = Path(args.logfile)
    fresh = not path.exists() or path.stat().st_size == 0
    path.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    row = [ts, args.phase, args.event, args.subject, args.who, args.evidence]
    with open(path, "a", newline="", encoding="utf-8") as fh:
        if fresh:
            fh.write("\t".join(LOG_HEADER) + "\n")
        fh.write("\t".join(cell(c) for c in row) + "\n")
    print(f"logged {args.event}: {args.subject}")
    return 0


# Revenue: ASC 606 arithmetic. The revenue skill makes every judgment (what the obligations
# are, the transaction price, SSP, which modification method); these functions only do the
# math those judgments imply, from a contract file shaped as in
# skills/technical-accounting/revenue-recognition/reference/contract-file.md.

PATTERNS = {"ratable", "point", "progress", "usage"}
MODIFICATION_METHODS = {"prospective", "cumulative"}


def month_end(d):
    after = date(d.year + (d.month == 12), d.month % 12 + 1, 1)
    return date.fromordinal(after.toordinal() - 1)


def period_end(label, where):
    if not re.fullmatch(r"\d{4}-\d{2}", label or ""):
        raise InputError(f"{where}: period {label!r} must be YYYY-MM")
    return month_end(date(int(label[:4]), int(label[5:]), 1))


def months_between(start, end):
    return (end.year - start.year) * 12 + end.month - start.month + 1


def rounded(value):
    return value.quantize(CENT, rounding="ROUND_HALF_UP")


def allocate(pool, obligations, where):
    """Relative SSP allocation of `pool` to the non-usage obligations, to the cent.
    Largest-remainder rounding makes the allocations sum to the pool exactly. An explicit
    `allocated` on every obligation (residual approach, discount to a subset) is taken as
    given and must sum to the pool."""
    fixed = [o for o in obligations if o["pattern"] != "usage"]
    if not fixed:
        if pool:
            raise InputError(f"{where}: transaction price {fmt(pool)} has no non-usage obligation to go to")
        return {}
    explicit = [o for o in fixed if "allocated" in o]
    if explicit:
        if len(explicit) != len(fixed):
            raise InputError(f"{where}: give `allocated` on every non-usage obligation or on none")
        total = sum((o["allocated"] for o in fixed), ZERO)
        if total != pool:
            raise InputError(f"{where}: allocations sum to {fmt(total)}, transaction price is {fmt(pool)}")
        return {o["id"]: o["allocated"] for o in fixed}
    if len(fixed) == 1:
        return {fixed[0]["id"]: pool}
    missing = [o["id"] for o in fixed if o.get("ssp", ZERO) <= 0]
    if missing:
        raise InputError(f"{where}: standalone selling price missing or zero for {', '.join(missing)}")
    total_ssp = sum((o["ssp"] for o in fixed), ZERO)
    exact = {o["id"]: pool * o["ssp"] / total_ssp for o in fixed}
    shares = {k: v.quantize(CENT, rounding="ROUND_DOWN") for k, v in exact.items()}
    leftover = int((pool - sum(shares.values(), ZERO)) / CENT)
    for k in sorted(exact, key=lambda k: exact[k] - shares[k], reverse=True)[:leftover]:
        shares[k] += CENT
    return shares


def obligation_cumulative(o, amount, as_of, segment_start, convention):
    """Revenue recognized on one obligation from `segment_start` through `as_of`."""
    if o["pattern"] == "usage":
        return sum((a for end, a in o["usage"] if segment_start <= end <= as_of), ZERO)
    if o["pattern"] == "point":
        return amount if o["date"] <= as_of else ZERO
    if o["pattern"] == "progress":
        pct = ZERO
        for end, p in o["progress"]:
            if end <= as_of:
                pct = p
        return rounded(amount * pct)
    if as_of < o["start"]:
        return ZERO
    through = min(as_of, o["end"])
    if convention == "monthly":
        elapsed = months_between(o["start"], through) - (through != month_end(through))
        return rounded(amount * elapsed / months_between(o["start"], o["end"]))
    return rounded(amount * ((through - o["start"]).days + 1) / ((o["end"] - o["start"]).days + 1))


def parse_obligation(raw, where, convention):
    if not isinstance(raw, dict) or not raw.get("id"):
        raise InputError(f"{where}: each obligation needs an id")
    where = f"{where} obligation {raw['id']}"
    pattern = raw.get("pattern")
    if pattern not in PATTERNS:
        raise InputError(f"{where}: pattern must be one of {', '.join(sorted(PATTERNS))}")
    o = {"id": raw["id"], "pattern": pattern}
    if "ssp" in raw:
        o["ssp"] = money(raw["ssp"], f"{where} ssp")
    if "allocated" in raw:
        o["allocated"] = money(raw["allocated"], f"{where} allocated")
    if pattern == "ratable":
        o["start"] = parse_iso(raw.get("start", ""), f"{where} start")
        o["end"] = parse_iso(raw.get("end", ""), f"{where} end")
        if o["end"] < o["start"]:
            raise InputError(f"{where}: end before start")
        if convention == "monthly" and (o["start"].day != 1 or o["end"] != month_end(o["end"])):
            raise InputError(f"{where}: monthly convention needs a service period from a month's first day to a month's last day; use daily")
    elif pattern == "point":
        o["date"] = parse_iso(raw.get("date", ""), f"{where} date")
    elif pattern == "progress":
        o["progress"] = []
        for step in raw.get("progress", []):
            pct = Decimal(str(step.get("complete", "")))
            if not ZERO <= pct <= 1:
                raise InputError(f"{where}: progress {pct} must be between 0 and 1")
            o["progress"].append((period_end(step.get("period"), where), pct))
        o["progress"].sort()
    else:
        o["usage"] = [(period_end(u.get("period"), where), money(u.get("amount"), f"{where} usage")) for u in raw.get("usage", [])]
    return o


def earliest(o):
    return {"ratable": lambda: o["start"], "point": lambda: o["date"],
            "progress": lambda: o["progress"][0][0] if o["progress"] else date.max,
            "usage": lambda: min((e for e, _ in o["usage"]), default=date.max)}[o["pattern"]]()


class Segment:
    """One stretch of a contract between modifications: its obligations, the consideration
    allocated to them, and the date it starts recognizing from."""

    def __init__(self, start, pool, obligations, convention, where):
        self.start, self.pool, self.obligations, self.convention = start, pool, obligations, convention
        ids = [o["id"] for o in obligations]
        if len(set(ids)) != len(ids):
            raise InputError(f"{where}: obligation ids repeat")
        self.allocation = allocate(pool, obligations, where)

    def cumulative(self, as_of):
        return {o["id"]: obligation_cumulative(o, self.allocation.get(o["id"], ZERO), as_of, self.start, self.convention)
                for o in self.obligations}


def add(a, b):
    out = dict(a)
    for k, v in b.items():
        out[k] = out.get(k, ZERO) + v
    return out


def load_contract(path):
    try:
        raw = json.loads(Path(path).read_text())
    except (OSError, json.JSONDecodeError) as err:
        raise InputError(f"{path}: {err}") from None
    where = str(path)
    convention = raw.get("convention", "daily")
    if convention not in ("daily", "monthly"):
        raise InputError(f"{where}: convention must be daily or monthly")
    kind = raw.get("kind", "revenue")
    if kind not in ("revenue", "cost"):
        raise InputError(f"{where}: kind must be revenue or cost")
    unbilled = raw.get("unbilled", "contract_asset")
    if unbilled not in ("contract_asset", "receivable"):
        raise InputError(f"{where}: unbilled must be contract_asset or receivable")
    obligations = [parse_obligation(o, where, convention) for o in raw.get("obligations", [])]
    if not obligations:
        raise InputError(f"{where}: no obligations")
    start = min(earliest(o) for o in obligations)
    pool = money(raw.get("transaction_price", "0"), f"{where} transaction_price")
    # Each entry: (method, date it takes effect, segment, note). The first is the inception.
    timeline = [("base", date.min, Segment(date.min, pool, obligations, convention, where), "")]
    for n, ev in enumerate(sorted(raw.get("modifications", []), key=lambda e: e.get("date", "")), start=1):
        ew = f"{where} modification {n}"
        method = ev.get("method")
        if method not in MODIFICATION_METHODS:
            raise InputError(f"{ew}: method must be prospective or cumulative")
        on = parse_iso(ev.get("date", ""), f"{ew} date")
        change = money(ev.get("price_change", "0"), f"{ew} price_change")
        new_obligations = [parse_obligation(o, ew, convention) for o in ev.get("obligations", [])]
        if not new_obligations:
            raise InputError(f"{ew}: list the obligations as they stand after the modification")
        active = timeline[-1][2]
        if method == "prospective":
            early = [o["id"] for o in new_obligations if o["pattern"] != "usage" and earliest(o) < on]
            if early:
                raise InputError(f"{ew}: prospective treatment covers only what remains; {', '.join(early)} starts before {on}")
            done = active.cumulative(date.fromordinal(on.toordinal() - 1))
            unrecognized = sum((v - done[k] for k, v in active.allocation.items()), ZERO)
            seg = Segment(on, unrecognized + change, new_obligations, convention, ew)
        else:
            seg = Segment(active.start, active.pool + change, new_obligations, convention, ew)
        timeline.append((method, on, seg, ev.get("note", "")))
    return {"id": raw.get("id") or Path(path).stem, "customer": raw.get("customer", ""), "kind": kind,
            "unbilled": unbilled, "start": start, "timeline": timeline,
            "billings": [(parse_iso(b.get("date", ""), f"{where} billing"), money(b.get("amount"), f"{where} billing")) for b in raw.get("billings", [])],
            "booked": [(period_end(b.get("period"), f"{where} booked"), money(b.get("amount"), f"{where} booked")) for b in raw.get("booked", [])],
            "refunds": [(period_end(b.get("period"), f"{where} refund_liability"), money(b.get("amount"), f"{where} refund_liability")) for b in raw.get("refund_liability", [])]}


def contract_cumulative(timeline, as_of):
    """Cumulative revenue by obligation id through `as_of`, applying each modification.
    Prospective: what the old segment recognized up to the day before stays; the new
    segment adds from its date. Cumulative: the new segment replaces the old one from its
    date, so the catch-up lands in the modification's period."""
    frozen = {}
    active = timeline[0][2]
    for method, on, seg, _ in timeline[1:]:
        if as_of < on:
            break
        if method == "prospective":
            frozen = add(frozen, active.cumulative(date.fromordinal(on.toordinal() - 1)))
        active = seg
    return add(frozen, active.cumulative(as_of))


def month_labels(first, last):
    y, m = first.year, first.month
    while (y, m) <= (last.year, last.month):
        yield f"{y:04d}-{m:02d}"
        y, m = y + (m == 12), m % 12 + 1


def cmd_rev_allocate(args):
    for path in args.contracts:
        c = load_contract(path)
        print(f"{c['id']} {c['customer']}".strip())
        for method, on, seg, note in c["timeline"]:
            head = "inception" if method == "base" else f"{method} modification {on}"
            print(f"  {head}: consideration {fmt(seg.pool)}" + (f"  ({note})" if note else ""))
            for o in seg.obligations:
                amount = "variable, recognized as incurred" if o["pattern"] == "usage" else fmt(seg.allocation[o["id"]])
                ssp = f"  ssp {fmt(o['ssp'])}" if "ssp" in o else ""
                print(f"    {o['id']:24} {o['pattern']:9} {amount:>16}{ssp}")
    return 0


def cmd_rev_schedule(args):
    through = period_end(args.through, "--through")
    rows = []
    for path in args.contracts:
        c = load_contract(path)
        first = period_end(args.start, "--from") if args.start else month_end(c["start"])
        previous = contract_cumulative(c["timeline"], date.fromordinal(date(first.year, first.month, 1).toordinal() - 1))
        for label in month_labels(first, through):
            now = contract_cumulative(c["timeline"], period_end(label, "period"))
            for ob in sorted(set(now) | set(previous)):
                amount = now.get(ob, ZERO) - previous.get(ob, ZERO)
                if amount:
                    rows.append([c["id"], c["kind"], ob, label, amount, now.get(ob, ZERO)])
            previous = now
    if args.out:
        with open(args.out, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["contract", "kind", "obligation", "period", "recognized", "cumulative"])
            w.writerows([r[:4] + [f"{r[4]:.2f}", f"{r[5]:.2f}"] for r in rows])
        print(f"wrote {args.out}: {len(rows)} rows")
    by_period = OrderedDict()
    for r in rows:
        by_period.setdefault((r[3], r[1]), ZERO)
        by_period[(r[3], r[1])] += r[4]
    for (label, kind), total in by_period.items():
        print(f"{label}  {kind:8} {fmt(total):>14}")
    if not args.out:
        for r in rows:
            print(f"  {r[0]:16} {r[2]:24} {r[3]}  {fmt(r[4]):>14} {fmt(r[5]):>14}")
    return 0


def cmd_rev_balances(args):
    as_of = period_end(args.asof, "--asof")
    totals = {"contract liability": ZERO, "contract asset": ZERO, "unbilled receivable": ZERO, "capitalized cost": ZERO, "refund liability": ZERO}
    print(f"{'contract':16} {'recognized':>14} {'billed':>14} {'balance':>14}  classification")
    for path in args.contracts:
        c = load_contract(path)
        recognized = sum(contract_cumulative(c["timeline"], as_of).values(), ZERO)
        billed = sum((a for d, a in c["billings"] if d <= as_of), ZERO)
        # Refund liability is the balance owed back at the period end, stated by the contract
        # file for the latest period on or before as_of. It is carved out, never netted.
        refund = next((a for d, a in sorted(c["refunds"], reverse=True) if d <= as_of), ZERO)
        net = billed - recognized - refund
        if c["kind"] == "cost":
            label = "capitalized cost"
        elif net > 0:
            label = "contract liability"
        elif net < 0:
            label = "contract asset" if c["unbilled"] == "contract_asset" else "unbilled receivable"
        else:
            label = None
        if label:
            totals[label] += abs(net)
        print(f"{c['id']:16} {fmt(recognized):>14} {fmt(billed):>14} {fmt(abs(net)):>14}  {label or 'none'}")
        if refund:
            totals["refund liability"] += refund
            print(f"  refund liability: {fmt(refund)} (presented separately, not netted)")
        if c["booked"]:
            booked = sum((a for d, a in c["booked"] if d <= as_of), ZERO)
            print(f"  correction to booked through {args.asof}: {fmt(recognized - booked)} (booked {fmt(booked)}, recognized {fmt(recognized)})")
    for label, value in totals.items():
        if value:
            print(f"total {label}: {fmt(value)}")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(prog="closekit", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("tb", help="trial balance foots: debits equal credits")
    p.add_argument("tb")
    p.set_defaults(func=cmd_tb)

    p = sub.add_parser("tie", help="GL opening plus activity equals TB closing, per account, with the constant-difference test")
    p.add_argument("--tb", required=True)
    p.add_argument("--gl", required=True)
    p.add_argument("--prior", help="prior-period TB; supplies openings and arbitrates the constant-difference test")
    p.set_defaults(func=cmd_tie)

    p = sub.add_parser("je", help="JE import CSV meets the contract; with --log, every entry has a recorded approval")
    p.add_argument("csv")
    p.add_argument("--start", help="period start, YYYY-MM-DD; implied by a month or quarter --label")
    p.add_argument("--end", help="period end, YYYY-MM-DD; implied by a month or quarter --label")
    p.add_argument("--coa", help="TB or chart CSV (account column) that every account must appear in")
    p.add_argument("--label", help="period label every memo must open with, e.g. 2026-07 or 2026-Q2")
    p.add_argument("--log", help="close-log.tsv holding approve/decline rows keyed by memo")
    p.set_defaults(func=cmd_je)

    p = sub.add_parser("fingerprint", help="record or check control totals so later phases detect changed data")
    p.add_argument("files", nargs="*")
    p.add_argument("--out", help="write the fingerprint JSON here")
    p.add_argument("--check", help="compare the files a saved fingerprint names against their current content")
    p.set_defaults(func=cmd_fingerprint)

    p = sub.add_parser("lint", help="banned voice tells in .md, .txt, .csv, or .docx deliverables")
    p.add_argument("files", nargs="+")
    p.set_defaults(func=cmd_lint)

    p = sub.add_parser("log", help="append one row to the close log")
    p.add_argument("logfile")
    p.add_argument("phase")
    p.add_argument("event", help=", ".join(sorted(LOG_EVENTS)))
    p.add_argument("subject", help="what the row is about; for approve/decline, the entry memo exactly")
    p.add_argument("who")
    p.add_argument("evidence", nargs="?", default="", help="path, workpaper, or message that proves it")
    p.set_defaults(func=cmd_log)

    rev = sub.add_parser("rev", help="ASC 606 arithmetic over contract files (skills/technical-accounting/revenue-recognition/reference/contract-file.md)")
    rsub = rev.add_subparsers(dest="rev_command", required=True)
    p = rsub.add_parser("allocate", help="transaction price allocated to each obligation, at inception and after each modification")
    p.add_argument("contracts", nargs="+")
    p.set_defaults(func=cmd_rev_allocate)
    p = rsub.add_parser("schedule", help="revenue by obligation by month, cumulative-exact")
    p.add_argument("contracts", nargs="+")
    p.add_argument("--through", required=True, help="last period, YYYY-MM")
    p.add_argument("--from", dest="start", help="first period, YYYY-MM; default is each contract's first month")
    p.add_argument("--out", help="write the schedule CSV here")
    p.set_defaults(func=cmd_rev_schedule)
    p = rsub.add_parser("balances", help="contract liability, contract asset, or unbilled receivable per contract at period end")
    p.add_argument("contracts", nargs="+")
    p.add_argument("--asof", required=True, help="period, YYYY-MM")
    p.set_defaults(func=cmd_rev_balances)

    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except InputError as err:
        print(f"INPUT ERROR: {err}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
