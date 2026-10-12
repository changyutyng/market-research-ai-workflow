#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批次驗證研究筆記裡的網址。

用法：
    python3 verify_urls.py 筆記.md                # 全部驗
    python3 verify_urls.py 筆記.md --sample 10    # 隨機抽 10 條
    python3 verify_urls.py 筆記.md --json out.json

判讀：
    OK        連得上，而且沒有被導回首頁
    REDIRECT  連得上，但被導到不同路徑（常見於「網址是編的、站方導回首頁」）
    DEAD      404、410、連不上
    BLOCKED   403、429 等，需要人工開瀏覽器確認
"""
import argparse, json, random, re, subprocess, sys
from collections import Counter
from urllib.parse import urlparse

URL_RE = re.compile(r'https?://[^\s<>()\[\]"\'，。、；：]+')
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0 Safari/537.36")


def extract(path):
    text = open(path, encoding="utf-8", errors="ignore").read()
    seen, out = set(), []
    for m in URL_RE.finditer(text):
        u = m.group(0).rstrip(".,;)")
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def check(url, timeout=20):
    """回傳 (狀態, HTTP 碼, 最終網址)。"""
    cmd = ["curl", "-sIL", "-o", "/dev/null", "-A", UA,
           "--max-time", str(timeout),
           "-w", "%{http_code}\t%{url_effective}", url]
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = (r.stdout or "").strip()
    if not out or "\t" not in out:
        # 有些站擋 HEAD，改用 GET 只取前幾 KB
        cmd = ["curl", "-sL", "-o", "/dev/null", "-A", UA, "-r", "0-2047",
               "--max-time", str(timeout),
               "-w", "%{http_code}\t%{url_effective}", url]
        r = subprocess.run(cmd, capture_output=True, text=True)
        out = (r.stdout or "").strip()
    if not out or "\t" not in out:
        return "DEAD", 0, url
    code_s, final = out.split("\t", 1)
    try:
        code = int(code_s)
    except ValueError:
        return "DEAD", 0, url
    if code in (403, 429):
        return "BLOCKED", code, final
    if code >= 400 or code == 0:
        return "DEAD", code, final
    a, b = urlparse(url), urlparse(final)
    deep = a.path.strip("/").count("/") >= 1 or len(a.path.strip("/")) > 12
    landed_home = b.path.strip("/") in ("", "index.html", "home")
    if deep and landed_home:
        return "REDIRECT", code, final
    if a.netloc.replace("www.", "") != b.netloc.replace("www.", ""):
        return "REDIRECT", code, final
    return "OK", code, final


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--sample", type=int, default=0, help="隨機抽樣幾條，0 表示全驗")
    ap.add_argument("--json", help="另存 JSON 結果")
    a = ap.parse_args()

    urls = extract(a.file)
    if not urls:
        print("檔案裡找不到任何網址。"); return 1
    if a.sample and a.sample < len(urls):
        urls = random.sample(urls, a.sample)

    print(f"共 {len(urls)} 個網址，開始驗證⋯⋯\n")
    rows, tally = [], Counter()
    for i, u in enumerate(urls, 1):
        st, code, final = check(u)
        tally[st] += 1
        rows.append({"url": u, "status": st, "code": code, "final": final})
        mark = {"OK": "✓", "REDIRECT": "→", "DEAD": "✗", "BLOCKED": "?"}[st]
        print(f"{mark} [{code or '--'}] {u[:92]}")
        if st == "REDIRECT":
            print(f"    導向 {final[:92]}")

    total = len(rows)
    bad = tally["DEAD"] + tally["REDIRECT"]
    print("\n" + "─" * 60)
    print(f"可用 {tally['OK']}　導回首頁或換站 {tally['REDIRECT']}　"
          f"失效 {tally['DEAD']}　需人工確認 {tally['BLOCKED']}")
    rate = bad / total * 100 if total else 0
    print(f"問題比例　{bad}/{total} = {rate:.0f}%")
    if rate > 20:
        print("\n⚠️  超過兩成有問題。這一批的查證結果不可信，建議整批重做，")
        print("    並在下一批指令開頭寫明：上一批有 N 個網址無法驗證，")
        print("    請降低產出量、提高可驗證性。")
    elif bad:
        print("\n有問題的項目必須逐條人工確認，確認不了就改寫成「查無」。")
    else:
        print("\n全部可用。仍建議隨機開 2 到 3 個，確認頁面內容真的講那件事。")
    if a.json:
        json.dump(rows, open(a.json, "w"), ensure_ascii=False, indent=1)
        print(f"\n明細已存：{a.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
