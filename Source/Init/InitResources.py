import os
from Source import Globs
from Source.Common.Func import OS, Subprocess

for ever in OS.walk(OS.join(Globs.source_dir),suffix=".ui"):
    text = f"{Globs.uic} {ever} -o {ever.replace('.ui', '.py')}"
    Globs.logger.debug(text)
    os.system(text)



q_res=[]
ever_imgs=[]
ASSETS = "Assets"
for ever in OS.walk(OS.join(Globs.source_dir, ASSETS), relative=True):
    if ever.endswith(".png") or ever.endswith(".svg"):
        q_res.append(f"<file>{ASSETS}{ever}</file>")
        without_under = ever[1:].replace('/', '_')
        for ever in ["/","-","(",")"]:
            without_under=without_under.replace(ever,"_")
        ever_imgs.append(f"{without_under.replace('.','_')} = ':/{ASSETS}/{without_under}'")



q_res_str="\n   ".join(q_res)
with open(OS.join(Globs.source_dir,'icons_rc.qrc'),"w",encoding="utf8") as f:
    f.write(f"""<RCC>
  <qresource prefix="/">
   {q_res_str}
  </qresource>
</RCC>
""")
for ever in OS.walk(OS.join(Globs.main_dir), suffix=".qrc"):
    text = f"{Globs.rcc} {ever} -o {ever.replace('.qrc', '.py')}"
    Globs.logger.debug(text)
    Subprocess.popen(text)

icons_py=OS.join(Globs.custom_dir , "LSIcons.py")
icons_enums='\n\t'.join(ever_imgs)
with open(icons_py,'w',encoding='utf8') as f:
    f.write(f"""class LSIcons:
\t{icons_enums}""")

import Source.icons_rc
Source.icons_rc