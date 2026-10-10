# -*- coding: utf-8 -*-
"""Batch fetch user-supplied sources for competitive analysis.

Usage:
  python fetch_sources.py --urls urls.txt --out sources [--timeout 20]

- urls.txt: one URL (or local file path) per line; lines starting with # are ignored.
- Writes fetched content into the output directory and a manifest.csv with status.
- Stdlib only. Does not bypass logins, paywalls, or captchas.
"""
import argparse
import csv
import html
import os
import re
import sys
import urllib.error
import urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
LOGIN_HINTS = ["sign in", "log in", "login", "captcha", "verify you are human", "请登录", "登录后"]


def strip_html(raw):
    raw = re.sub(r"(?is)<script.*?</script>", " ", raw)
    raw = re.sub(r"(?is)<style.*?</style>", " ", raw)
    text = re.sub(r"(?s)<[^>]+>", " ", raw)
    text = html.unescape(text)
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def guess_ext(content_type, url):
    if "pdf" in content_type:
        return ".pdf"
    if "json" in content_type:
        return ".json"
    if "html" in content_type:
        return ".txt"
    ext = os.path.splitext(url.split("?")[0])[1]
    return ext if ext and len(ext) <= 6 else ".txt"


def fetch_one(idx, url, out_dir, timeout):
    status, note, saved, content_type, size = "ok", "", "", "", 0
    try:
        if os.path.exists(url):
            data = open(url, "rb").read()
            content_type = "text/html" if url.lower().endswith((".html", ".htm")) else "application/octet-stream"
        else:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = resp.read()
                content_type = resp.headers.get("Content-Type", "")
        size = len(data)
        ext = guess_ext(content_type, url)
        name = "S%02d%s" % (idx, ext)
        path = os.path.join(out_dir, name)
        if ext == ".txt":
            text = data.decode("utf-8", errors="replace")
            if "html" in content_type or "<html" in text[:2000].lower():
                text = strip_html(text)
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            low = text.lower()
            if any(h in low for h in LOGIN_HINTS):
                status, note = "needs_login_or_blocked", "页面出现登录/验证码提示，需用户手动提供内容"
        else:
            with open(path, "wb") as f:
                f.write(data)
        saved = name
    except urllib.error.HTTPError as e:
        status = "http_error"
        note = "HTTP %s" % e.code
        if e.code in (401, 403, 429):
            status = "needs_login_or_blocked"
    except Exception as e:
        status, note = "fetch_error", str(e)[:200]
    return {"id": "S%02d" % idx, "url": url, "status": status, "content_type": content_type,
            "bytes": size, "saved_file": saved, "note": note}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--urls", required=True, help="text file with one URL per line")
    ap.add_argument("--out", required=True, help="output directory")
    ap.add_argument("--timeout", type=int, default=20)
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    with open(args.urls, encoding="utf-8") as f:
        urls = [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith("#")]

    rows = [fetch_one(i + 1, u, args.out, args.timeout) for i, u in enumerate(urls)]
    manifest = os.path.join(args.out, "manifest.csv")
    with open(manifest, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["id", "url", "status", "content_type", "bytes", "saved_file", "note"])
        w.writeheader()
        w.writerows(rows)

    ok = sum(1 for r in rows if r["status"] == "ok")
    print("fetched %d/%d, manifest: %s" % (ok, len(rows), manifest))
    for r in rows:
        print("%s %-22s %s" % (r["id"], r["status"], r["url"][:90]))


if __name__ == "__main__":
    main()
