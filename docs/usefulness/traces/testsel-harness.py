"""Test-selection experiment harness. Usage: python3 -I harness.py CASE_ID [CASE_ID...]"""
import json, os, re, subprocess, sys, time, xml.etree.ElementTree as ET

D = os.path.dirname(os.path.abspath(__file__))
CASES = {c["id"]: c for c in json.load(open(os.path.join(D, "cases.json")))}
TRACE = open(os.path.join(D, "trace.txt"), "a")


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    TRACE.write(s + "\n")
    TRACE.flush()


def sh(cmd, cwd, env=None, quiet=False):
    log(f"$ (cd {os.path.basename(cwd)}) {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
    p = subprocess.run(cmd, cwd=cwd, shell=isinstance(cmd, str), capture_output=True, text=True,
                       env={**os.environ, **(env or {})})
    out = (p.stdout + p.stderr).strip()
    if not quiet and out:
        log(out[-1500:])
    return p.returncode, out


def run_pytest(case, label, args, extra_env=None, cov=False):
    repo = os.path.join(D, case["repo"])
    xml = os.path.join(D, "out", f"{case['id']}_{label}.xml")
    cmd = [".venv/bin/pytest", "-q", "-p", "no:cacheprovider", "-p", "no:randomly",
           f"--junitxml={xml}", "-o", "junit_family=xunit1"]
    if cov:
        cmd += [f"--cov={case['pkg']}", "--cov-context=test", "--cov-report="]
    cmd += args
    t0 = time.time()
    rc, out = sh(cmd, repo, env=extra_env, quiet=True)
    dt = time.time() - t0
    tail = "\n".join(out.splitlines()[-4:])
    log(tail)
    failed, total = set(), 0
    if os.path.exists(xml):
        root = ET.parse(xml).getroot()
        for tc in root.iter("testcase"):
            total += 1
            if tc.find("failure") is not None or tc.find("error") is not None:
                failed.add(f"{tc.get('classname')}::{tc.get('name')}")
            elif tc.find("skipped") is not None:
                total -= 1
    return {"failed": sorted(failed), "ran": total, "secs": round(dt, 1), "rc": rc}


def changed_lines(case):
    repo = os.path.join(D, case["repo"])
    _, diff = sh(["git", "diff", "-U0", f"{case['commit']}^", case["commit"], "--", "src/"], repo, quiet=True)
    res, cur = {}, None
    for line in diff.splitlines():
        m = re.match(r"\+\+\+ b/(.*)", line)
        if m:
            cur = m.group(1); res.setdefault(cur, set()); continue
        m = re.match(r"@@ -\S+ \+(\d+)(?:,(\d+))? @@", line)
        if m and cur:
            start, n = int(m.group(1)), int(m.group(2) or 1)
            if n == 0:  # pure deletion: take neighbouring lines
                res[cur].update({start, start + 1})
            else:
                res[cur].update(range(start, start + n))
    return res


def covering_tests(case, covfile):
    py = os.path.join(D, case["repo"], ".venv/bin/python")
    lines = {os.path.join(D, case["repo"], f): sorted(v) for f, v in changed_lines(case).items()}
    code = ("import json,sys\nfrom coverage import CoverageData\n"
            "d=CoverageData(basename=sys.argv[1]);d.read()\nlines=json.loads(sys.argv[2])\n"
            "out=set();hit={}\n"
            "for f,ls in lines.items():\n"
            "  by=d.contexts_by_lineno(f)\n"
            "  for l in ls:\n"
            "    cs=[c for c in by.get(l,[]) if c]\n"
            "    if cs: hit[f+':'+str(l)]=len(cs)\n"
            "    out.update(c.rsplit('|',1)[0] for c in cs)\n"
            "print(json.dumps({'tests':sorted(out),'hit':hit}))")
    p = subprocess.run([py, "-I", "-c", code, covfile, json.dumps(lines)], capture_output=True, text=True)
    r = json.loads(p.stdout)
    log(f"changed lines: { {os.path.relpath(k, D): v for k, v in lines.items()} }")
    log(f"changed lines with covering test contexts (line: n_tests): { {os.path.basename(k): v for k, v in r['hit'].items()} }")
    return r["tests"]


def main(cid):
    c = CASES[cid]
    repo = os.path.join(D, c["repo"])
    log(f"\n==================== CASE {cid} {c['repo']} {c['commit']} ====================")
    sh(["git", "checkout", "-q", "-f", c["commit"]], repo)
    sh(["git", "show", "--stat", "--format=%H %ad %s", "--date=short", c["commit"]], repo)
    res = {"id": cid, "repo": c["repo"], "commit": c["commit"], "bug": c["bug"]}
    covfile = os.path.join(D, "out", f"{cid}.coverage")
    if os.path.exists(covfile):
        os.remove(covfile)
    log("--- clean full suite with coverage contexts")
    res["clean"] = run_pytest(c, "clean", [], {"COVERAGE_FILE": covfile}, cov=True)
    base = set(res["clean"]["failed"])
    log(f"baseline failures on clean commit: {sorted(base)}")
    tests = covering_tests(c, covfile)
    res["cov_tests"] = tests
    # inject bug
    path = os.path.join(repo, c["file"])
    src = open(path).read()
    assert src.count(c["old"]) == 1, f"pattern count {src.count(c['old'])}"
    open(path, "w").write(src.replace(c["old"], c["new"]))
    _, d = sh(["git", "diff"], repo)
    res["diff"] = d
    for label, args in [("full", []), ("default", c["default"])]:
        log(f"--- buggy {label}: {args}")
        r = run_pytest(c, label, args)
        r["new_failures"] = sorted(set(r["failed"]) - base)
        r["caught"] = bool(r["new_failures"])
        log(f"{label}: caught={r['caught']} ran={r['ran']} secs={r['secs']} new_failures={r['new_failures'][:5]}")
        res[label] = r
    log(f"--- buggy coverage subset: {len(tests)} tests")
    if tests:
        argf = os.path.join(D, "out", f"{cid}_covtests.txt")
        open(argf, "w").write("\n".join(tests) + "\n")
        r = run_pytest(c, "cov", ["@" + argf])
        r["new_failures"] = sorted(set(r["failed"]) - base)
        r["caught"] = bool(r["new_failures"])
    else:
        r = {"caught": False, "ran": 0, "secs": 0.0, "new_failures": []}
    log(f"cov: caught={r['caught']} ran={r['ran']} secs={r['secs']} new_failures={r['new_failures'][:5]}")
    res["cov"] = r
    sh(["git", "checkout", "-q", "-f", c["commit"]], repo)
    json.dump(res, open(os.path.join(D, "out", f"{cid}.json"), "w"), indent=1)


if __name__ == "__main__":
    os.makedirs(os.path.join(D, "out"), exist_ok=True)
    for cid in sys.argv[1:]:
        main(cid)
