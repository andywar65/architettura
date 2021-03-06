def get_material_blob():
    material = """id=:camera-ent=;position=:-1.4231 0.0 -0.0011=;rotation=:0 324.9208 0=;layer=:0=;tag=:a-entity=;closing=:0
id=:camera=;position=:0 1.6 0=;look-controls=:pointerLockEnabled: true=;layer=:0=;tag=:a-camera=;closing=:0
id=:camera-light=;type=:point=;distance=:10=;intensity=:1=;layer=:0=;tag=:a-light=;closing=:1
id=:cursor=;layer=:0=;tag=:a-cursor=;closing=:3
id=:40-sphere-2=;position=:-0.5943 0.25 -2.5021=;rotation=:0 0 0=;scale=:0.25 0.25 0.25=;repeat=:0.25 0.25=;layer=:0=;material=:=;component=:0=;tag=:a-sphere=;closing=:1
id=:40-light-3=;position=:-1.2111 6.0832 -1.5403=;rotation=:30.4719 -44.2111 0.0=;light=:type: directional; intensity: 1.0; shadowCameraBottom: -3.0; shadowCameraLeft: -2.5; shadowCameraTop: 3.0; shadowCameraRight: 2.5; target: #40-light-3-target; =;tag=:a-entity=;color=:=;layer=:0=;closing=:0
id=:40-light-3-target=;position=:0 -1 0=;tag=:a-entity=;layer=:0=;closing=:2
id=:40-BIM-block-4=;position=:0.6559 -0.15 -3.5021=;rotation=:0 0 0=;layer=:0=;tag=:a-entity=;closing=:0
id=:40-slab-4-floor=;position=:0 0.145 0=;geometry=:width: 3.0; height: 0.01; depth: 3.0;=;material=:=;component=:2=;layer=:0=;tag=:a-box=;closing=:1=;partition=:=;repeat=:3.0 3.0
id=:40-slab-4-ceiling=;position=:0 -0.005 0=;geometry=:width: 3.0; height: 0.29; depth: 3.0;=;material=:=;component=:0=;layer=:0=;tag=:a-box=;closing=:2=;partition=:=;repeat=:3.0 3.0
id=:40-BIM-block-5=;position=:0.6559 1.05 -5.1521=;rotation=:0 0 0=;layer=:0=;tag=:a-entity=;closing=:0
id=:40-door-5-left-frame=;position=:-0.449 0.0495 0=;rotation=:0 0 90=;geometry=:width: 2.199; height: 0.1; depth: 0.32;=;material=:=;component=:2=;layer=:0=;tag=:a-box=;closing=:1=;partition=:=;repeat=:1 1
id=:40-door-5-right-frame=;position=:0.449 0.0495 0=;rotation=:0 0 90=;geometry=:width: 2.199; height: 0.1; depth: 0.32;=;material=:=;component=:2=;layer=:0=;tag=:a-box=;closing=:1=;partition=:=;repeat=:1 1
id=:40-door-5-top-frame=;position=:0 1.099 0=;rotation=:0 0 0=;geometry=:width: 0.798; height: 0.1; depth: 0.32;=;material=:=;component=:2=;layer=:0=;tag=:a-box=;closing=:1=;partition=:=;repeat=:1 1
id=:40-door-5-hinge=;position=:-0.4 -1.05 0.15=;animation=:property: rotation; easing: easeInOutQuad; from:0 0 0; to:0 -90.0 0; startEvents: click; loop: 1; dir: alternate;=;layer=:0=;tag=:a-entity=;closing=:0
id=:40-door-5-moving-part=;position=:0.4 1.0495 -0.025=;geometry=:width: 0.798; height: 2.099; depth: 0.05;=;material=:=;component=:0=;partition=:=;repeat=:0.798 2.099=;layer=:0=;tag=:a-box=;closing=:3
id=:40-BIM-block-6=;position=:0.6559 1.5 -5.1521=;rotation=:0 0 0=;layer=:0=;tag=:a-entity=;closing=:0
id=:40-openwall-left-6-ent=;position=:-0.95 0 0=;layer=:0=;tag=:a-entity=;closing=:0
id=:40-openwall-left-6-int-skirt=;position=:0 -1.45 0.005=;geometry=:width: 1.09996214415371; height: 0.1; depth: 0.29; =;layer=:0=;tag=:a-box=;closing=:1=;material=:=;component=:2=;partition=:
id=:40-openwall-left-6-int-tile=;position=:0 -0.65 0.005=;geometry=:width: 1.09996214415371; height: 1.5; depth: 0.29; =;layer=:0=;tag=:a-box=;closing=:1=;material=:=;component=:1=;partition=:
id=:40-openwall-left-6-int-plaster=;position=:0 0.8 0.005=;geometry=:width: 1.09996214415371; height: 1.4; depth: 0.29; =;layer=:0=;tag=:a-box=;closing=:1=;material=:=;component=:0=;partition=:
id=:40-openwall-left-6-ext-skirt=;position=:0 -1.45 -0.145=;geometry=:width: 1.09996214415371; height: 0.1; depth: 0.01; =;layer=:0=;tag=:a-box=;closing=:1=;material=:=;component=:2=;partition=:
id=:40-openwall-left-6-ext-tile=;position=:0 -0.65 -0.145=;geometry=:width: 1.09996214415371; height: 1.5; depth: 0.01; =;layer=:0=;tag=:a-box=;closing=:1=;material=:=;component=:1=;partition=:
id=:40-openwall-left-6-ext-plaster=;position=:0 0.8 -0.145=;geometry=:width: 1.09996214415371; height: 1.4; depth: 0.01; =;layer=:0=;tag=:a-box=;closing=:2=;material=:=;component=:0=;partition=:
id=:40-openwall-above-6-ent=;position=:-0.0 2.1 0=;layer=:0=;tag=:a-entity=;closing=:0
id=:40-openwall-above-6-int-plaster=;position=:0 -1.05 0.005=;geometry=:width: 0.8000000000000003; height: 0.8999999999999999; depth: 0.29; =;layer=:0=;tag=:a-box=;closing=:1=;material=:=;component=:0=;partition=:
id=:40-openwall-above-6-ext-plaster=;position=:0 -1.05 -0.145=;geometry=:width: 0.8000000000000003; height: 0.8999999999999999; depth: 0.01; =;layer=:0=;tag=:a-box=;closing=:2=;material=:=;component=:0=;partition=:
id=:40-openwall-right-6-ent=;position=:0.95 0 0=;layer=:0=;tag=:a-entity=;closing=:0
id=:40-openwall-right-6-int-skirt=;position=:0 -1.45 0.005=;geometry=:width: 1.1000378558462898; height: 0.1; depth: 0.29; =;layer=:0=;tag=:a-box=;closing=:1=;material=:=;component=:2=;partition=:
id=:40-openwall-right-6-int-tile=;position=:0 -0.65 0.005=;geometry=:width: 1.1000378558462898; height: 1.5; depth: 0.29; =;layer=:0=;tag=:a-box=;closing=:1=;material=:=;component=:1=;partition=:
id=:40-openwall-right-6-int-plaster=;position=:0 0.8 0.005=;geometry=:width: 1.1000378558462898; height: 1.4; depth: 0.29; =;layer=:0=;tag=:a-box=;closing=:1=;material=:=;component=:0=;partition=:
id=:40-openwall-right-6-ext-skirt=;position=:0 -1.45 -0.145=;geometry=:width: 1.1000378558462898; height: 0.1; depth: 0.01; =;layer=:0=;tag=:a-box=;closing=:1=;material=:=;component=:2=;partition=:
id=:40-openwall-right-6-ext-tile=;position=:0 -0.65 -0.145=;geometry=:width: 1.1000378558462898; height: 1.5; depth: 0.01; =;layer=:0=;tag=:a-box=;closing=:1=;material=:=;component=:1=;partition=:
id=:40-openwall-right-6-ext-plaster=;position=:0 0.8 -0.145=;geometry=:width: 1.1000378558462898; height: 1.4; depth: 0.01; =;layer=:0=;tag=:a-box=;closing=:3=;material=:=;component=:0=;partition=:
id=:40-block-7=;position=:0.9914 0.375 -3.2604=;rotation=:0 316.8896 0=;layer=:0=;tag=:a-entity=;closing=:0
id=:40-table01-7-top=;position=:0 0.35 0=;geometry=:width: 1.2; height: 0.05; depth: 0.6;=;layer=:0=;tag=:a-box=;closing=:1=;material=:=;component=:2
id=:40-table01-7-leg-1=;position=:0.55 -0.012500000000000011 0.25=;geometry=:radius: 0.025; height: 0.725; =;layer=:0=;tag=:a-cylinder=;closing=:1=;material=:=;component=:1
id=:40-table01-7-leg-2=;position=:0.55 -0.012500000000000011 -0.25=;geometry=:radius: 0.025; height: 0.725; =;layer=:0=;tag=:a-cylinder=;closing=:1=;material=:=;component=:1
id=:40-table01-7-leg-3=;position=:-0.55 -0.012500000000000011 0.25=;geometry=:radius: 0.025; height: 0.725; =;layer=:0=;tag=:a-cylinder=;closing=:1=;material=:=;component=:1
id=:40-table01-7-leg-4=;position=:-0.55 -0.012500000000000011 -0.25=;geometry=:radius: 0.025; height: 0.725; =;layer=:0=;tag=:a-cylinder=;closing=:2=;material=:=;component=:1
id=:40-BIM-block-8=;position=:2.3559 1.2 -3.5021=;rotation=:0 270.0 0=;layer=:0=;tag=:a-entity=;closing=:0
id=:40-window-under-8-ent=;position=:0 -0.75 0=;layer=:0=;tag=:a-entity=;closing=:0
id=:40-window-under-8-int-skirt=;position=:0 -0.4 0.005=;geometry=:width: 0.8; height: 0.1; depth: 0.19; =;layer=:0=;tag=:a-box=;closing=:1=;material=:=;component=:2=;partition=:
id=:40-window-under-8-int-tile=;position=:0 0.05 0.005=;geometry=:width: 0.8; height: 0.8; depth: 0.19; =;layer=:0=;tag=:a-box=;closing=:1=;material=:=;component=:1=;partition=:
id=:40-window-under-8-ext-skirt=;position=:0 -0.4 -0.095=;geometry=:width: 0.8; height: 0.1; depth: 0.01; =;layer=:0=;tag=:a-box=;closing=:1=;material=:=;component=:2=;partition=:
id=:40-window-under-8-ext-tile=;position=:0 0.05 -0.095=;geometry=:width: 0.8; height: 0.8; depth: 0.01; =;layer=:0=;tag=:a-box=;closing=:2=;material=:=;component=:1=;partition=:
id=:40-window-8-sill=;position=:0 -0.314 0=;scale=:0.84 0.03 0.24=;layer=:0=;tag=:a-box=;closing=:1
id=:40-window-8-frame-right=;position=:0.375 0.45 0=;rotation=:0 0 0=;layer=:0=;tag=:a-box=;closing=:1=;material=:=;component=:2=;partition=:=;scale=:0.05 1.5 0.06
id=:40-window-8-frame-left=;position=:-0.375 0.45 0=;rotation=:0 0 0=;layer=:0=;tag=:a-box=;closing=:1=;material=:=;component=:2=;partition=:=;scale=:0.05 1.5 0.06
id=:40-window-8-frame-bottom=;position=:0 -0.275 0=;rotation=:0 0 90=;layer=:0=;tag=:a-box=;closing=:1=;material=:=;component=:2=;partition=:=;scale=:0.05 0.7 0.06
id=:40-window-8-frame-top=;position=:0 1.175 0=;rotation=:0 0 90=;layer=:0=;tag=:a-box=;closing=:1=;material=:=;component=:2=;partition=:=;scale=:0.05 0.7 0.06
id=:40-window-8-hinge-1=;position=:-0.35 0 0.025=;animation=:property: rotation; easing: easeInOutQuad; from:0 0 0; to:0 -90.0 0; startEvents: click; loop: 1; dir: alternate; =;layer=:0=;tag=:a-entity=;closing=:0
id=:40-window-8-moving-1-right=;position=:0.675 0.45 -0.01=;rotation=:0 0 0=;layer=:0=;tag=:a-box=;closing=:1=;material=:=;component=:2=;partition=:=;scale=:0.05 1.4 0.07
id=:40-window-8-moving-1-left=;position=:0.025 0.45 -0.01=;rotation=:0 0 0=;layer=:0=;tag=:a-box=;closing=:1=;material=:=;component=:2=;partition=:=;scale=:0.05 1.4 0.07
id=:40-window-8-moving-1-bottom=;position=:0.35 -0.225 -0.01=;rotation=:0 0 90=;layer=:0=;tag=:a-box=;closing=:1=;material=:=;component=:2=;partition=:=;scale=:0.05 0.6 0.07
id=:40-window-8-moving-1-top=;position=:0.35 1.125 -0.01=;rotation=:0 0 90=;layer=:0=;tag=:a-box=;closing=:3=;material=:=;component=:2=;partition=:=;scale=:0.05 0.6 0.07
id=:40-BIM-block-9=;position=:0.6559 3.15 -3.5021=;rotation=:0 0 0=;layer=:0=;tag=:a-entity=;closing=:0
id=:40-slab-9-floor=;position=:0 0.145 0=;geometry=:width: 3.0; height: 0.01; depth: 3.0;=;material=:=;component=:2=;layer=:0=;tag=:a-box=;closing=:1=;partition=:=;repeat=:3.0 3.0
id=:40-slab-9-ceiling=;position=:0 -0.005 0=;geometry=:width: 3.0; height: 0.29; depth: 3.0;=;material=:=;component=:0=;layer=:0=;tag=:a-box=;closing=:2=;partition=:=;repeat=:3.0 3.0
id=:40-BIM-block-10=;position=:2.3059 1.5 -3.5021=;rotation=:0 270.0 0=;layer=:0=;tag=:a-entity=;closing=:0
id=:40-openwall-left-10-ent=;position=:-0.95 0 0=;layer=:0=;tag=:a-entity=;closing=:0
id=:40-openwall-left-10-int-skirt=;position=:0 -1.45 0.005=;geometry=:width: 1.1000295474186998; height: 0.1; depth: 0.29; =;layer=:0=;tag=:a-box=;closing=:1=;material=:=;component=:2=;partition=:
id=:40-openwall-left-10-int-tile=;position=:0 -0.65 0.005=;geometry=:width: 1.1000295474186998; height: 1.5; depth: 0.29; =;layer=:0=;tag=:a-box=;closing=:1=;material=:=;component=:1=;partition=:
id=:40-openwall-left-10-int-plaster=;position=:0 0.8 0.005=;geometry=:width: 1.1000295474186998; height: 1.4; depth: 0.29; =;layer=:0=;tag=:a-box=;closing=:1=;material=:=;component=:0=;partition=:
id=:40-openwall-left-10-ext-skirt=;position=:0 -1.45 -0.145=;geometry=:width: 1.1000295474186998; height: 0.1; depth: 0.01; =;layer=:0=;tag=:a-box=;closing=:1=;material=:=;component=:2=;partition=:
id=:40-openwall-left-10-ext-tile=;position=:0 -0.65 -0.145=;geometry=:width: 1.1000295474186998; height: 1.5; depth: 0.01; =;layer=:0=;tag=:a-box=;closing=:1=;material=:=;component=:1=;partition=:
id=:40-openwall-left-10-ext-plaster=;position=:0 0.8 -0.145=;geometry=:width: 1.1000295474186998; height: 1.4; depth: 0.01; =;layer=:0=;tag=:a-box=;closing=:2=;material=:=;component=:0=;partition=:
id=:40-openwall-above-10-ent=;position=:0.0 2.4 0=;layer=:0=;tag=:a-entity=;closing=:0
id=:40-openwall-above-10-int-plaster=;position=:0 -1.2 0.005=;geometry=:width: 0.7999999999999998; height: 0.6000000000000001; depth: 0.29; =;layer=:0=;tag=:a-box=;closing=:1=;material=:=;component=:0=;partition=:
id=:40-openwall-above-10-ext-plaster=;position=:0 -1.2 -0.145=;geometry=:width: 0.7999999999999998; height: 0.6000000000000001; depth: 0.01; =;layer=:0=;tag=:a-box=;closing=:2=;material=:=;component=:0=;partition=:
id=:40-openwall-right-10-ent=;position=:0.95 0 0=;layer=:0=;tag=:a-entity=;closing=:0
id=:40-openwall-right-10-int-skirt=;position=:0 -1.45 0.005=;geometry=:width: 1.0999704525813003; height: 0.1; depth: 0.29; =;layer=:0=;tag=:a-box=;closing=:1=;material=:=;component=:2=;partition=:
id=:40-openwall-right-10-int-tile=;position=:0 -0.65 0.005=;geometry=:width: 1.0999704525813003; height: 1.5; depth: 0.29; =;layer=:0=;tag=:a-box=;closing=:1=;material=:=;component=:1=;partition=:
id=:40-openwall-right-10-int-plaster=;position=:0 0.8 0.005=;geometry=:width: 1.0999704525813003; height: 1.4; depth: 0.29; =;layer=:0=;tag=:a-box=;closing=:1=;material=:=;component=:0=;partition=:
id=:40-openwall-right-10-ext-skirt=;position=:0 -1.45 -0.145=;geometry=:width: 1.0999704525813003; height: 0.1; depth: 0.01; =;layer=:0=;tag=:a-box=;closing=:1=;material=:=;component=:2=;partition=:
id=:40-openwall-right-10-ext-tile=;position=:0 -0.65 -0.145=;geometry=:width: 1.0999704525813003; height: 1.5; depth: 0.01; =;layer=:0=;tag=:a-box=;closing=:1=;material=:=;component=:1=;partition=:
id=:40-openwall-right-10-ext-plaster=;position=:0 0.8 -0.145=;geometry=:width: 1.0999704525813003; height: 1.4; depth: 0.01; =;layer=:0=;tag=:a-box=;closing=:3=;material=:=;component=:0=;partition=:"""
    return material

def get_grl_blob():
    grl = """id=:upper=;position=:0 0 0=;rotation=:0 0 0=;tag=:a-entity=;closing=:0=;animation=:upper
id=:chest=;geometry=:primitive: cone; radius-bottom: 1; radius-top: 0.74; =;position=:-0.0 0.077 -0.0064=;rotation=:4.8166 -180.0 -180.0=;scale=:0.132 0.1658 0.088=;repeat=:0.132 0.088=;material=:=;component=:0=;tag=:a-entity=;closing=:1
id=:sternum=;geometry=:primitive: sphere; =;position=:-0.0 0.1596 -0.0134=;rotation=:-4.8166 -0.0 0.0=;scale=:0.132 0.121 0.088=;repeat=:0.132 0.088=;material=:=;component=:0=;tag=:a-entity=;closing=:1
id=:r-tit=;geometry=:primitive: sphere; =;position=:-0.0729 0.126 0.0441=;rotation=:15.3957 -25.9985 -7.3774=;scale=:0.055 0.055 0.077=;repeat=:0.055 0.077=;material=:=;component=:3=;tag=:a-entity=;closing=:1=;animation=:r-tit
id=:l-tit=;geometry=:primitive: sphere; =;position=:0.0729 0.126 0.0441=;rotation=:15.3957 25.9985 7.3774=;scale=:0.055 0.055 0.077=;repeat=:0.055 0.077=;material=:=;component=:3=;tag=:a-entity=;closing=:1=;animation=:l-tit
id=:neck-ent=;position=:0 0.2287 -0.0315=;rotation=:0 0 0=;tag=:a-entity=;closing=:0=;animation=:neck-ent
id=:neck=;geometry=:primitive: cylinder; =;position=:0 0.066 0=;rotation=:0 0 0=;scale=:0.0385 0.132 0.0385=;repeat=:0.0385 0.0385=;material=:=;component=:0=;tag=:a-entity=;closing=:1
id=:head=;geometry=:primitive: sphere; radius: 0.1045; =;position=:0.0 0.1896 0.0124=;rotation=:0 0 0=;repeat=:0.1045 0.1045=;material=:=;component=:1=;tag=:a-entity=;closing=:0=;animation=:head
id=:hair=;geometry=:primitive: sphere; radius: 0.121; theta-length: 90;theta-start: 0; =;position=:0 0 0=;rotation=:0 0 0=;repeat=:0.121 0.121=;material=:=;component=:2=;tag=:a-entity=;closing=:1=;side=:double
id=:fringe=;geometry=:primitive: cylinder; radius: 0.121; height: 0.121; open-ended: true; theta-length: 180; theta-start: 90; =;position=:0.0 -0.0605 0=;rotation=:0 0 0=;repeat=:0.121 0.121=;material=:=;component=:2=;tag=:a-entity=;closing=:3=;side=:double
id=:r-scapula=;geometry=:primitive: cone; radius-bottom: 0.055; radius-top: 0.0385; height: 0.11; =;position=:-0.1016 0.2105 -0.0357=;rotation=:85.0 -92.0 3.1651=;repeat=:0.055 0.055=;material=:=;component=:0=;tag=:a-entity=;closing=:0
id=:r-shoulder=;geometry=:primitive: sphere; radius: 0.0385; =;position=:0 0.055 0=;rotation=:5.1575 90.175 -84.9873=;repeat=:0.0385 0.0385=;material=:=;component=:0=;tag=:a-entity=;closing=:0=;animation=:r-shoulder
id=:r-arm=;geometry=:primitive: cone; radius-bottom: 0.033; radius-top: 0.028; height: 0.2365 =;position=:0 -0.1182 0=;rotation=:0.0 -180.0 -180.0=;repeat=:0.033 0.033=;material=:=;component=:0=;tag=:a-entity=;closing=:1
id=:r-elbow=;geometry=:primitive: sphere; radius: 0.033; =;position=:0 -0.2365 0=;rotation=:0 0 0=;repeat=:0.033 0.033=;material=:=;component=:0=;tag=:a-entity=;closing=:0=;animation=:r-elbow
id=:r-forearm=;geometry=:primitive: cone; radius-bottom: 0.033; radius-top: 0.0165; height: 0.2; =;position=:0 -0.1 0=;rotation=:0.0 -180.0 -180.0=;repeat=:0.033 0.033=;material=:=;component=:0=;tag=:a-entity=;closing=:1
id=:r-wrist=;geometry=:primitive: sphere; radius: 0.0165; =;position=:0 -0.2 0=;rotation=:0 0 0=;repeat=:0.0165 0.0165=;material=:=;component=:0=;tag=:a-entity=;closing=:0=;animation=:r-wrist
id=:r-hand=;geometry=:primitive: sphere; =;position=:0 -0.03 0=;rotation=:0.0 -180.0 -180.0=;scale=:0.025 0.06 0.012=;repeat=:0.025 0.012=;material=:=;component=:0=;tag=:a-entity=;closing=:5=;animation=:r-hand
id=:l-scapula=;geometry=:primitive: cone; radius-bottom: 0.055; radius-top: 0.0385; height: 0.11; =;position=:0.1016 0.2105 -0.0357=;rotation=:85.0 92.0 -3.1651=;repeat=:0.055 0.055=;material=:=;component=:0=;tag=:a-entity=;closing=:0
id=:l-shoulder=;geometry=:primitive: sphere; radius: 0.0385; =;position=:0 0.055 0=;rotation=:5.1575 -90.175 84.9873=;repeat=:0.0385 0.0385=;material=:=;component=:0=;tag=:a-entity=;closing=:0=;animation=:l-shoulder
id=:l-arm=;geometry=:primitive: cone; radius-bottom: 0.033; radius-top: 0.028; height: 0.2365 =;position=:0 -0.1182 0=;rotation=:0.0 -180.0 -180.0=;repeat=:0.033 0.033=;material=:=;component=:0=;tag=:a-entity=;closing=:1
id=:l-elbow=;geometry=:primitive: sphere; radius: 0.033; =;position=:0 -0.2365 0=;rotation=:0 0 0=;repeat=:0.033 0.033=;material=:=;component=:0=;tag=:a-entity=;closing=:0=;animation=:l-elbow
id=:l-forearm=;geometry=:primitive: cone; radius-bottom: 0.033; radius-top: 0.0165; height: 0.2; =;position=:0 -0.1 0=;rotation=:0.0 -180.0 -180.0=;repeat=:0.033 0.033=;material=:=;component=:0=;tag=:a-entity=;closing=:1
id=:l-wrist=;geometry=:primitive: sphere; radius: 0.0165; =;position=:0 -0.2 0=;rotation=:0 0 0=;repeat=:0.0165 0.0165=;material=:=;component=:0=;tag=:a-entity=;closing=:0=;animation=:l-wrist
id=:l-hand=;geometry=:primitive: sphere; =;position=:0 -0.03 0=;rotation=:0.0 -180.0 -180.0=;scale=:0.025 0.06 0.012=;repeat=:0.025 0.012=;material=:=;component=:0=;tag=:a-entity=;closing=:6=;animation=:l-hand
id=:downer=;position=:0 0 0=;rotation=:0 0 0=;tag=:a-entity=;closing=:0=;animation=:downer
id=:belly=;geometry=:primitive: sphere; =;position=:0.0 -0.0 0.0=;rotation=:10.0 0.0 0.0=;scale=:0.099 0.0495 0.066=;repeat=:0.099 0.066=;material=:=;component=:0=;tag=:a-entity=;closing=:1
id=:pelvis=;geometry=:primitive: cone; radius-bottom: 1; radius-top: 0.74; =;position=:0.0 -0.0844 -0.0149=;rotation=:10.0 0.0 0.0=;scale=:0.132 0.1826 0.088=;repeat=:0.132 0.088=;material=:=;component=:0=;tag=:a-entity=;closing=:1
id=:pubes=;geometry=:primitive: sphere; =;position=:0.0 -0.1835 -0.0324=;rotation=:10.0 0.0 0.0=;scale=:0.132 0.066 0.088=;repeat=:0.132 0.088=;material=:=;component=:4=;tag=:a-entity=;closing=:1
id=:r-gluteus=;geometry=:primitive: sphere; radius: 0.099; =;position=:-0.0546 -0.1662 -0.0463=;rotation=:0 0 0=;repeat=:0.099 0.099=;material=:=;component=:0=;tag=:a-entity=;closing=:0=;animation=:r-gluteus
id=:r-thigh=;geometry=:primitive: cone; radius-bottom: 0.077; radius-top: 0.0385; height: 0.418; =;position=:-0.0191 -0.209 0.0111=;rotation=:0.0 -180.0 -180.0=;repeat=:0.077 0.077=;material=:=;component=:0=;tag=:a-entity=;closing=:1
id=:r-knee=;geometry=:primitive: sphere; radius: 0.0385; =;position=:-0.0191 -0.418 0.0111=;rotation=:0 0 0=;repeat=:0.0385 0.0385=;material=:=;component=:0=;tag=:a-entity=;closing=:0=;animation=:r-knee
id=:r-tibia=;geometry=:primitive: cone; radius-bottom: 0.0385; radius-top: 0.0308; height: 0.33; =;position=:0 -0.165 0=;rotation=:0.0 -180.0 -180.0=;repeat=:0.0385 0.0385=;material=:=;component=:0=;tag=:a-entity=;closing=:1
id=:r-calf=;geometry=:primitive: sphere; =;position=:0 -0.0621 -0.0222=;rotation=:0 0 0=;scale=:0.033 0.088 0.033=;repeat=:0.033 0.033=;material=:=;component=:0=;tag=:a-entity=;closing=:1
id=:r-heel=;geometry=:primitive: sphere; radius: 0.0385; =;position=:0 -0.33 0=;rotation=:0 0 0=;repeat=:0.0385 0.0385=;material=:=;component=:0=;tag=:a-entity=;closing=:0=;animation=:r-heel
id=:r-foot=;geometry=:primitive: sphere; =;position=:-0.0078 -0.0165 0.0411=;rotation=:0 350.0 0=;scale=:0.0385 0.022 0.11=;repeat=:0.0385 0.11=;material=:=;component=:0=;tag=:a-entity=;closing=:4=;animation=:r-foot
id=:l-gluteus=;geometry=:primitive: sphere; radius: 0.099; =;position=:0.0546 -0.1662 -0.0463=;rotation=:0 0 0=;repeat=:0.099 0.099=;material=:=;component=:0=;tag=:a-entity=;closing=:0=;animation=:l-gluteus
id=:l-thigh=;geometry=:primitive: cone; radius-bottom: 0.077; radius-top: 0.0385; height: 0.418; =;position=:0.0191 -0.209 0.0111=;rotation=:0.0 -180.0 -180.0=;repeat=:0.077 0.077=;material=:=;component=:0=;tag=:a-entity=;closing=:1
id=:l-knee=;geometry=:primitive: sphere; radius: 0.0385; =;position=:0.0191 -0.418 0.0111=;rotation=:0 0 0=;repeat=:0.0385 0.0385=;material=:=;component=:0=;tag=:a-entity=;closing=:0=;animation=:l-knee
id=:l-tibia=;geometry=:primitive: cone; radius-bottom: 0.0385; radius-top: 0.0308; height: 0.33; =;position=:0 -0.165 0=;rotation=:0.0 -180.0 -180.0=;repeat=:0.0385 0.0385=;material=:=;component=:0=;tag=:a-entity=;closing=:1
id=:l-calf=;geometry=:primitive: sphere; =;position=:0 -0.0621 -0.0222=;rotation=:0 0 0=;scale=:0.033 0.088 0.033=;repeat=:0.033 0.033=;material=:=;component=:0=;tag=:a-entity=;closing=:1
id=:l-heel=;geometry=:primitive: sphere; radius: 0.0385; =;position=:0 -0.33 0=;rotation=:0 0 0=;repeat=:0.0385 0.0385=;material=:=;component=:0=;tag=:a-entity=;closing=:0=;animation=:l-heel
id=:l-foot=;geometry=:primitive: sphere; =;position=:0.0078 -0.0165 0.0411=;rotation=:0 10.0 0=;scale=:0.0385 0.022 0.11=;repeat=:0.0385 0.11=;material=:=;component=:0=;tag=:a-entity=;closing=:6=;animation=:l-foot
"""
    return grl

def get_grl_anime(param1):
    anime = {}
    if param1 == 'nodding':
        anime = {'head': 'property: rotation; from: 10 0 0; to: -10 0 0; easing: easeInOutQuad; loop: true; autoplay: true; dir: alternate; '}
    return anime
