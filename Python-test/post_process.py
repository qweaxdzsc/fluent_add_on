def post_process(angle, out_path):

        final_path = out_path + 'GE2-%s\\' % (angle)       # path
        txt_out = final_path + 'GE2.txt'                      # txt-file output path
        pathline_jpg_out = final_path + 'temp_pathline.jpg'    # picture output path
        pathline_avz_out = final_path + 'temp_pathline.avz'
        clip_jpg_out = final_path + 'clip_temp.jpg'

        post_part = """
;start post-process
/report/surface-integrals/area-weighted-avg outlet_vl outlet_vr()
temperature yes
%s
q


/report/surface-integrals/volume-flow-rate inlet hc_out
outlet_defrost outlet_rfl outlet_rfr outlet_ffl outlet_ffr outlet_vr outlet_vl outlet_rv outlet_vc outlet_vent()
yes
%s
q

/report/fluxes/mass-flow no
inlet outlet_defrost outlet_rfl outlet_rfr outlet_ffl outlet_vent outlet_ffr outlet_vr outlet_vl outlet_vc outlet_rv()
yes
%s
yes
q


/report/surface-integrals/uniformity-index-area-weighted evap_in evap_out hc_out()
velocity-magnitude
yes
%s
yes
q


/report/surface-integrals/area-weighted-avg
inlet fan_in fan_out evap_in evap_out
hc_in hc_out
outlet_deforst outlet_rfl outlet_rfr outlet_ffl outlet_ffr outlet_vr outlet_vl()
total-pressure
yes
%s
yes

/report/surface-integrals/area-weighted-avg
inlet fan_in fan_out evap_in evap_out
hc_in hc_out
outlet_deforst outlet_rfl outlet_rfr outlet_ffl outlet_ffr outlet_vr outlet_vl()
pressure
yes
%s
yes

/report/forces/wall-moments no
fan_blade()
5.27684 0.68831 1.06885
0 1 0
yes
%s
yes

; delete all exist pictures
/display/objects/delete clip_temp q q q
/display/objects/delete hc_out    q q q
/display/objects/delete temp_pathline q q q
/surface/delete contour_surface  q q q

; create picture
display/objects/create pathlines temp_pathline field temperature color-map format %%0.1f size 10 q step 2000 skip 10 surfaces-list evap_out() q
q
q

/surface/iso-surface y-coordinate contour_surface () distrib hc() 0.75()

/display/objects/creat contour clip_temp
surfaces-list contour_surface()    
field temperature
filled yes
range-option auto-range-on 
global-range no
q

color-map size 8 format %%0.1f
q
q

/display/objects/creat contour hc_out
surfaces-list hc_out()    
field velocity-magnitude
filled yes
range-option auto-range-on 
global-range no

q

color-map size 8 format %%0.1f
q
q

;start capture picture

;read saved position
/views/read-views G:\\GE2_REAR\\GE2-rear-vent\\GE2-rear-linearty\\ge2_lin_view

; adjust background setting
/display/set/lights/lights-on no
/display/set/lights/headlight-on no
/views/camera/projection orthographic
/display/set/colors/color-by-type yes
/display/set/filled-mesh no
/display/set/rendering-options/surface-edge-visibility yes no yes no
/display/set/colors/inlet-faces "foreground"
/display/set/colors/outlet-faces "foreground"

q
q

; snip pathline
/display/open-window 7
/display/set/overlays yes
/display/objects/display/temp_pathline
/display/mesh-outline
/views/restore-view temp_pathline
/display/set/picture/driver/jpeg
/display/save-picture %s

; snip avz
/display/set/picture/driver/avz
/display/objects/display/hc_out
/views/restore-view temp_pathline
/display/save-picture %s
/display/close-window 7

; snip clip picture
/display/open-window 8
/display/objects/display/clip_temp
/display/mesh-outline
/views/restore-view temp_pathline
/display/set/picture/driver/jpeg
/display/save-picture %s
/display/close-window 8
/display/set/overlays no

""" % (txt_out, txt_out, txt_out, txt_out, txt_out, txt_out, txt_out, pathline_jpg_out, pathline_avz_out, clip_jpg_out)
        return post_part







