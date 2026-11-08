"""Fail-closed production release checker. Human and in-app checks require evidence, not AI assertions."""
import argparse, json, struct, sys
from pathlib import Path
COLORS={"#0A0F14","#101821","#1EC7C6","#A8FF00","#D4A43A","#FFFFFF"}
REQUIRED=("editorial_independent_review","arabic_language_review","english_language_review",
"source_and_numerical_review","no_people_visual_review","dubai_font_integrity",
"mobile_360_review","platform_in_app_preview","final_export_review","owner_release_approval")
def png_dimensions(path):
    with open(path,"rb") as f: h=f.read(24)
    if len(h)!=24 or h[:8]!=b"\x89PNG\r\n\x1a\n" or h[12:16]!=b"IHDR": raise ValueError("invalid PNG header")
    return struct.unpack(">II",h[16:24])
def validate(m,root):
    err=[]
    fields=("content_id","platform","brand_colors","assets","checks","publication_authorised")
    for k in fields:
        if k not in m: err.append("Missing field: "+k)
    if err: return err
    if m["platform"] not in ("instagram_carousel","instagram_story","tiktok"): err.append("Unknown platform")
    if set(m["brand_colors"])!=COLORS: err.append("Brand palette mismatch")
    size=(1080,1350) if m["platform"]=="instagram_carousel" else (1080,1920)
    if not isinstance(m["assets"],list) or not m["assets"]: err.append("No exported assets")
    else:
        for a in m["assets"]:
            p=(root/a).resolve()
            if not p.is_relative_to(root.resolve()): err.append("Path escape: "+a); continue
            try:
                if png_dimensions(p)!=size: err.append("Wrong dimensions: "+a)
            except (OSError,ValueError): err.append("Missing/invalid PNG: "+a)
    checks=m["checks"]
    if not isinstance(checks,dict): err.append("Invalid checks")
    else:
        for k in REQUIRED:
            c=checks.get(k)
            if not isinstance(c,dict) or c.get("status")!="PASS" or not str(c.get("evidence","")).strip():
                err.append("Missing independent evidence or PASS: "+k)
    if m["publication_authorised"] is not True: err.append("Publication not authorised")
    if m.get("unresolved_defects"): err.append("Unresolved defects")
    if m.get("recurring_production_enabled") is True and err: err.append("Unsafe recurrence enabled")
    return err
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("manifest",type=Path);p.add_argument("--root",type=Path,default=Path("."))
    a=p.parse_args()
    e=validate(json.loads(a.manifest.read_text(encoding="utf-8")),a.root)
    print(json.dumps({"decision":"HOLD" if e else "READY_FOR_MANUAL_RELEASE","errors":e},indent=2))
    sys.exit(bool(e))
