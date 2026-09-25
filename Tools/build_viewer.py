from pathlib import Path
import json,base64
from build_studio import build,nodes,MATS

root=Path(__file__).resolve().parents[1]
build()
data=[]
for n in nodes:
    color,emit=MATS[n['mat']]
    data.append(dict(layer=n['layer'],v=n['v'].round(5).tolist(),f=n['f'].tolist(),
                     color=[int(color[i:i+2],16)/255 for i in (1,3,5)]+[emit/100]))
template=(root/'Tools/viewer_template.html').read_text()
poster='data:image/png;base64,'+base64.b64encode((root/'Preview/01_Studio_Overview.png').read_bytes()).decode('ascii')
(root/'NOVA_Mac_Viewer.html').write_text(template.replace('__MODEL_DATA__',json.dumps(data,separators=(',',':'))).replace('__POSTER_DATA__',poster),encoding='utf8')
print('Created offline viewer: '+str(root/'NOVA_Mac_Viewer.html'))
