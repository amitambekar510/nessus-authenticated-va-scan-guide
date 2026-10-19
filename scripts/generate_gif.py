#!/usr/bin/env python3
"""Build a six-step animated diagram showing the authorized VA planning process."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
out=Path(__file__).resolve().parents[1]/"assets"/"va-planning.gif"
out.parent.mkdir(parents=True,exist_ok=True)
def font(n,b=False):
 p=Path("/usr/share/fonts/truetype/dejavu")/("DejaVuSans-Bold.ttf" if b else "DejaVuSans.ttf")
 return ImageFont.truetype(str(p),n) if p.exists() else ImageFont.load_default()
steps=[
 ("01 / SCOPE","Select Windows, Linux or mixed infrastructure","List asset categories, critical services and exclusions."),
 ("02 / PERMISSION","Confirm authorization and change window","No operational scans without written approval."),
 ("03 / AUTHENTICATION","Choose secure credential approach","Vault-managed SSH or delegated Windows access."),
 ("04 / POLICY","Review safe scan settings and pilot","Confirm plugin feed, safe checks and rate limits."),
 ("05 / FINDINGS","Review and validate reported vulnerabilities","Triage risk, assign owners and document exceptions."),
 ("06 / AUDIT","Retest and retain redacted evidence","Record approvals, remediation, results and sign-off.")]
frames=[]
for i,(title,subtitle,detail) in enumerate(steps):
 im=Image.new("RGB",(1100,430),"#081727");d=ImageDraw.Draw(im)
 d.rounded_rectangle((20,20,1080,410),radius=22,fill="#133149",outline="#3acfac",width=3)
 d.text((53,48),"NESSUS AUTHENTICATED VA GUIDE 2.0",font=font(27,True),fill="#70e4cb")
 d.text((53,115),title,font=font(37,True),fill="#fff")
 d.text((53,171),subtitle,font=font(22),fill="#d4edf5")
 d.text((53,211),detail,font=font(19),fill="#a8c7d8")
 for j,t in enumerate(("SCOPE","APPROVE","AUTH","POLICY","TRIAGE","AUDIT")):
  x=52+j*174
  d.rounded_rectangle((x,288,x+158,336),radius=10,fill="#40d0ac" if j<=i else "#35556e")
  d.text((x+17,304),t,font=font(15,True),fill="#082331" if j<=i else "#eaf5fc")
 d.text((53,378),"SYNTHETIC EXAMPLE • PLANNING ONLY • NO SCANS EXECUTED",font=font(15),fill="#bad0dd")
 frames.append(im)
frames[0].save(out,save_all=True,append_images=frames[1:],duration=1000,loop=0,optimize=True)
assert Image.open(out).n_frames==6
