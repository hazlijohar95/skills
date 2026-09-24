#!/usr/bin/env python3
"""Self-check for scripts/closekit.py. Run: python3 tests/test_closekit.py"""

import contextlib
import io
import json
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import closekit  # noqa: E402

FIX = ROOT / "tests" / "fixtures" / "acme-2026-07"
JULY = ["--start", "2026-07-01", "--end", "2026-07-31"]


def run(*argv):
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
        code = closekit.main([str(a) for a in argv])
    return code, out.getvalue()


def write(tmp, name, text):
    path = Path(tmp) / name
    path.write_text(text)
    return path


def rev_checks(tmp):
    seats = write(tmp, "seats.json", json.dumps({
        "id": "C-1", "transaction_price": "12000.00", "convention": "monthly",
        "obligations": [{"id": "saas", "pattern": "ratable", "start": "2026-01-01", "end": "2026-12-31"}],
        "billings": [{"date": "2026-01-01", "amount": "12000.00"}, {"date": "2026-07-01", "amount": "2500.00"}],
        "modifications": [{"date": "2026-07-01", "method": "prospective", "price_change": "2500.00",
                           "obligations": [{"id": "saas", "pattern": "ratable", "start": "2026-07-01", "end": "2026-12-31"}]}]}))
    code, out = run("rev", "schedule", seats, "--through", "2026-12")
    assert code == 0 and "2026-06  revenue        1,000.00" in out and "2026-07  revenue        1,416.67" in out, out
    assert "  14,500.00" in out.splitlines()[-1], out

    bundle = write(tmp, "bundle.json", json.dumps({
        "id": "C-2", "transaction_price": "30000.00",
        "obligations": [{"id": "saas", "pattern": "ratable", "start": "2026-01-15", "end": "2027-01-14", "ssp": "26000"},
                        {"id": "training", "pattern": "point", "date": "2026-02-10", "ssp": "5000"},
                        {"id": "overage", "pattern": "usage", "usage": [{"period": "2026-03", "amount": "412.50"}]}],
        "billings": [{"date": "2026-01-15", "amount": "30000.00"}]}))
    code, out = run("rev", "allocate", bundle)
    assert "25,161.29" in out and "4,838.71" in out, out
    out_csv = Path(tmp) / "sched.csv"
    run("rev", "schedule", bundle, "--through", "2027-01", "--out", out_csv)
    rows = list(closekit.csv.DictReader(open(out_csv)))
    saas = [r for r in rows if r["obligation"] == "saas"]
    assert saas[0]["recognized"] == "1171.90" and saas[-1]["cumulative"] == "25161.29", saas[-1]
    assert sum(closekit.Decimal(r["recognized"]) for r in rows) == closekit.Decimal("30412.50")

    fixed = write(tmp, "fixed.json", json.dumps({
        "id": "C-3", "transaction_price": "50000.00",
        "obligations": [{"id": "build", "pattern": "progress", "progress": [{"period": "2026-01", "complete": "0.2"}, {"period": "2026-02", "complete": "0.4"}]}],
        "billings": [{"date": "2026-02-28", "amount": "25000.00"}],
        "modifications": [{"date": "2026-03-01", "method": "cumulative", "price_change": "10000.00",
                           "obligations": [{"id": "build", "pattern": "progress", "progress": [
                               {"period": "2026-01", "complete": "0.2"}, {"period": "2026-02", "complete": "0.4"}, {"period": "2026-03", "complete": "0.5"}]}]}]}))
    code, out = run("rev", "schedule", fixed, "--through", "2026-03")
    assert "2026-03  revenue       10,000.00" in out, out
    code, out = run("rev", "balances", seats, bundle, fixed, "--asof", "2026-03")
    assert "C-1                    3,000.00      12,000.00       9,000.00  contract liability" in out, out
    assert "total contract asset: 5,000.00" in out, out

    osprey = write(tmp, "osprey.json", json.dumps({
        "id": "OS", "transaction_price": "36000.00", "convention": "monthly",
        "obligations": [{"id": "s", "pattern": "ratable", "start": "2026-05-01", "end": "2027-06-30"}],
        "billings": [{"date": "2026-05-01", "amount": "36000.00"}],
        "booked": [{"period": p, "amount": "3000.00"} for p in ("2026-05", "2026-06", "2026-07")]}))
    code, out = run("rev", "balances", osprey, "--asof", "2026-07")
    assert "correction to booked through 2026-07: -1,285.71 (booked 9,000.00" in out, out

    birch = write(tmp, "birch.json", json.dumps({
        "id": "BR", "transaction_price": "24000.00", "convention": "monthly",
        "obligations": [{"id": "s", "pattern": "ratable", "start": "2026-01-01", "end": "2026-12-31"}],
        "billings": [{"date": "2026-01-01", "amount": "24000.00"}],
        "refund_liability": [{"period": "2026-07", "amount": "6000.00"}]}))
    code, out = run("rev", "balances", birch, "--asof", "2026-07")
    assert "4,000.00  contract liability" in out and "refund liability: 6,000.00" in out, out
    assert "total refund liability: 6,000.00" in out, out

    bad = write(tmp, "bad.json", json.dumps({
        "id": "C-4", "transaction_price": "100.00",
        "obligations": [{"id": "a", "pattern": "point", "date": "2026-01-01", "ssp": "1"},
                        {"id": "b", "pattern": "point", "date": "2026-01-01"}]}))
    code, out = run("rev", "allocate", bad)
    assert code == 2 and "standalone selling price missing" in out, out
    thirds = write(tmp, "thirds.json", json.dumps({
        "id": "C-5", "transaction_price": "100.00",
        "obligations": [{"id": k, "pattern": "point", "date": "2026-01-01", "ssp": "1"} for k in "abc"]}))
    code, out = run("rev", "allocate", thirds)
    assert out.count("33.33") == 2 and out.count("33.34") == 1, out


def answer_key_checks():
    keys = ROOT / "tests" / "fixtures" / "revenue" / "answer-keys"
    for row in closekit.csv.DictReader(open(keys / "expected-2026-07.csv")):
        contract = keys / f"{row['key']}.json"
        code, out = run("rev", "schedule", contract, "--from", "2026-07", "--through", "2026-07")
        july = next(l for l in out.splitlines() if l.startswith("2026-07")).split()[-1].replace(",", "")
        assert code == 0 and july == row["july"], (row, out)
        code, out = run("rev", "balances", contract, "--asof", "2026-07")
        cells = out.splitlines()[1].split()
        assert cells[3].replace(",", "") == row["balance"] and " ".join(cells[4:]) == row["classification"], (row, out)
        refund = next((l.split(":")[1].split()[0].replace(",", "") for l in out.splitlines() if "refund liability:" in l and not l.startswith("total")), "0.00")
        assert refund == row["refund_liability"], (row, out)


def main():
    tmp = tempfile.mkdtemp()
    try:
        code, out = run("tb", FIX / "tb.csv")
        assert code == 0 and "32,700.00" in out, out
        code, out = run("tb", write(tmp, "bad.csv", "account,debit,credit\nCash,100.00,\nRevenue,,99.99\n"))
        assert code == 1 and "out of balance by 0.01" in out, out
        code, out = run("tb", write(tmp, "junk.csv", "account,debit,credit\nCash,$100,\n"))
        assert code == 2 and "normalize" in out, out

        code, out = run("tie", "--tb", FIX / "tb.csv", "--gl", FIX / "gl.csv", "--prior", FIX / "prior-tb.csv")
        lines = {l.split("  ")[0].strip(): l for l in out.splitlines()}
        assert code == 1 and "3 of 10" in out, out
        assert "constant difference" in lines["Accounts Receivable"], out
        assert "period activity" in lines["Cash"] and "period activity" in lines["Software"], out
        assert lines["Revenue"].endswith("ties"), out

        base = ["je", FIX / "adjusting-entries.csv", *JULY, "--coa", FIX / "tb.csv", "--label", "2026-07"]
        code, out = run(*base)
        assert code == 0, out
        code, out = run("je", FIX / "adjusting-entries.csv", "--label", "2026-07", "--coa", FIX / "tb.csv")
        assert code == 0, out
        args = closekit.argparse.Namespace(start=None, end=None, label="2024-Q1")
        assert closekit.period_bounds(args) == (closekit.date(2024, 1, 1), closekit.date(2024, 3, 31))
        args.label = "2026-12"
        assert closekit.period_bounds(args) == (closekit.date(2026, 12, 1), closekit.date(2026, 12, 31))
        args.label = "FY2025"
        assert run("je", FIX / "adjusting-entries.csv", "--label", "FY2025")[0] == 2
        code, out = run(*base, "--log", FIX / "close-log.tsv")
        assert code == 1 and "entry 2: no approval" in out and "entry 1" not in out, out

        bad = write(tmp, "bad-je.csv", "\n".join([
            "entry_no,date,account,memo,debit,credit",
            "1,2026-08-01,Cash,2026-07 close: x,10.00,",
            "1,2026-07-31,Made Up,2026-07 close: x,,9.00",
            "2,2026-07-31,Cash,2026-07 close: y,5.00,5.00",
            "3,2026-07-31,Cash,2026-07 close: z,1.005,",
            "1,2026-07-31,Cash,2026-07 close: x,1.00,",
        ]) + "\n")
        code, out = run("je", bad, *JULY, "--coa", FIX / "tb.csv")
        for needle in ("outside 2026-07-01", "not in the chart", "exactly one of debit", "two decimals", "not contiguous", "entry 1: debits"):
            assert needle in out, f"missing {needle!r}:\n{out}"

        log = Path(tmp) / "close-log.tsv"
        assert run("log", log, "adjust", "approve", "=HYPERLINK(\"x\")", "Hazli", "wp#1")[0] == 0
        assert run("log", log, "adjust", "approve", "memo", "   ")[0] == 2
        rows = log.read_text().splitlines()
        assert rows[0] == "\t".join(closekit.LOG_HEADER) and "\t'=HYPERLINK" in rows[1], rows

        data = shutil.copy(FIX / "tb.csv", tmp)
        fp = Path(tmp) / "fp.json"
        assert run("fingerprint", data, "--out", fp)[0] == 0
        assert run("fingerprint", "--check", fp)[0] == 0
        Path(data).write_text(Path(data).read_text().replace("27401.00", "27400.00").replace("2000.00,\nPrepaid", "2001.00,\nPrepaid"))
        code, out = run("fingerprint", "--check", fp)
        assert code == 1 and "changed (content only)" in out, out

        clean = write(tmp, "memo.md", "July lost $2,517, mostly the workstation purchase.\n")
        assert run("lint", clean)[0] == 0
        dirty = write(tmp, "dirty.md", "We delve into cash — it's important to note the trend.\nThis is not just a close, but a story.\n")
        code, out = run("lint", dirty)
        assert code == 1 and all(k in out for k in ("em dash", "filler word", "boilerplate", "not just")), out
        docx = Path(tmp) / "memo.docx"
        with zipfile.ZipFile(docx, "w") as z:
            z.writestr("word/document.xml", "<w:document><w:body><w:p><w:r><w:t>A robust close</w:t></w:r></w:p></w:body></w:document>")
        code, out = run("lint", docx)
        assert code == 1 and "memo.docx:1: filler word" in out, out
        docs = [str(p) for p in ROOT.glob("skills/**/*.md")] + [str(p) for p in ROOT.glob("agents/*.md")]
        code, out = run("lint", *docs)
        assert code == 0, f"agent-facing docs must pass the house style:\n{out}"
        rev_checks(tmp)
        answer_key_checks()
    finally:
        shutil.rmtree(tmp)
    print("closekit self-check passed")


if __name__ == "__main__":
    main()
