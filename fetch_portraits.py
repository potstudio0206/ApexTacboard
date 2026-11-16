"""各レジェンドのキャラクター画像（全身／上半身）を portraits/ に保存する（PCで実行）。

使い方: python fetch_portraits.py
保存後、Claude が顔部分を切り抜いて icons/faces/<id>.png を作ります。
画像の著作権は EA / Respawn にあります。個人利用の範囲で使ってください。
"""
import json
import pathlib
import time
import urllib.parse
import urllib.request

root = pathlib.Path(__file__).parent
data = json.loads((root / "skills.json").read_text(encoding="utf-8"))
out = root / "portraits"
out.mkdir(exist_ok=True)

ok, failed = 0, []
for legend in data["legends"]:
    name = legend["name"].replace(" ", "_")
    if any((out / f"{legend['id']}{ext}").exists() for ext in (".png", ".jpg")):
        ok += 1
        continue
    got = False
    for ext in (".png", ".jpg"):
        url = f"https://apexlegends.wiki.gg/images/{urllib.parse.quote(name)}{ext}?format=original"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "apex-tactical-board/0.1 (personal use)"})
            with urllib.request.urlopen(req, timeout=20) as r:
                body = r.read()
            if len(body) < 2000:  # エラーページなど
                raise ValueError("too small")
            (out / f"{legend['id']}{ext}").write_bytes(body)
            print("ok  ", legend["name"], ext, f"{len(body)//1024} KB")
            got = True
            break
        except Exception as e:  # noqa: BLE001
            last = e
        finally:
            time.sleep(1)  # サイトに負荷をかけないよう1秒間隔
    if got:
        ok += 1
    else:
        failed.append(legend["name"])
        print("fail", legend["name"], last)

print(f"\n完了: {ok}/{len(data['legends'])}")
if failed:
    print("取得できなかったレジェンド:", ", ".join(failed))
