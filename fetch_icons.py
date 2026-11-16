"""skills.json に載っているレジェンド／スキルのアイコンを icons/ に保存する（PCで実行）。

使い方: python fetch_icons.py
アイコンの著作権は EA / Respawn にあります。個人利用の範囲で使い、配布前に利用条件を確認してください。
"""
import json
import pathlib
import time
import urllib.request

root = pathlib.Path(__file__).parent
data = json.loads((root / "skills.json").read_text(encoding="utf-8"))
out = root / "icons"
out.mkdir(exist_ok=True)

urls = []
for legend in data["legends"]:
    urls.append((f"{legend['id']}.svg", legend["icon"]))
    for a in legend["abilities"]:
        fname = f"{legend['id']}_{a['slot']}.svg"
        urls.append((fname, a["icon"]))

failed = []
for fname, url in urls:
    dest = out / fname
    if dest.exists():
        continue
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "apex-tactical-board/0.1 (personal use)"})
        with urllib.request.urlopen(req, timeout=15) as r:
            dest.write_bytes(r.read())
        print("ok  ", fname)
    except Exception as e:  # noqa: BLE001
        failed.append((fname, url, str(e)))
        print("fail", fname, e)
    time.sleep(1)  # サイトに負荷をかけないよう1秒間隔

print(f"\n完了: {len(urls) - len(failed)}/{len(urls)}")
for f in failed:
    print("取得失敗:", *f)
