import rhinoscriptsyntax as rs

#rs.MessageBox("The hull must be closed and the surfaces joined together")

################################
####                        ####
#### Getting data from user ####
####                        ####
################################

for i in range(0, 90, 5):
    rs.AddLayer("Heel_" + str(i))

hull = rs.GetObject("Select the hull")

draft = rs.RealBox("Enter the draft of the boat")
depth = 2.133

currentl = rs.CurrentLayer("Heel_0")

copy0 = rs.CopyObject(hull)
rs.ObjectLayer(copy0, "Heel_0")

rs.LayerVisible("Default", False)

#####################################################
####                                             ####
#### Creating DWL and obtaining submerged volume ####
####                                             ####
#####################################################

aux_plane = rs.PlaneFromFrame( [-5,-50,draft], [1,0,0], [0,1,0] )
dwl = rs.AddPlaneSurface(aux_plane, 100, 100)

inter = rs.BooleanIntersection(copy0, dwl, False)

Nabla = rs.SurfaceVolumeCentroid(inter)
if Nabla:
    cb = rs.AddPoint(Nabla[0])

Volume0 = rs.SurfaceVolume(inter)
Initial_Volume = Volume0[0]

####################################
####                            ####
#### Heeled volume calculations ####
####                            ####
####################################

currentl2 = rs.CurrentLayer("Heel_20")

copyh = rs.CopyObject(copy0)

rs.ObjectLayer(copyh, "Heel_20")

rs.LayerVisible("Heel_0", False)

aux_plane = rs.PlaneFromFrame( [-5,-50,draft], [1,0,0], [0,1,0] )
dwl = rs.AddPlaneSurface(aux_plane, 100, 100)

heel = 20
heeled = rs.RotateObject(copyh, cb, heel, [1,0,0], False)
inter_h = rs.BooleanIntersection(heeled, dwl, False)
Volume1 = rs.SurfaceVolume(inter_h)
Volume_h = Volume1[0]

#######################################
####                               ####
#### Getting longitudinal position ####
####                               ####
#######################################

cg = rs.AddPoint(5.577,0,0)
cg_coord = rs.PointCoordinates(cg)

if (Volume_h - Initial_Volume > 0.01):
    
    while (Volume_h - Initial_Volume > 0.01):
        draft = draft - 0.001
            
        aux_plane = rs.PlaneFromFrame( [-5,-50,draft], [1,0,0], [0,1,0] )
        dwl = rs.AddPlaneSurface(aux_plane, 100, 100)
            
        inter2 = rs.BooleanIntersection(heeled, dwl, False)
        Volume = rs.SurfaceVolume(inter2)
        Volume_h = Volume[0]
        
        if (Volume_h - Initial_Volume > 0.01):
            rs.DeleteObject(inter2)
            rs.DeleteObject(dwl)
            rs.DeleteObject(cbh)
            continue
        
        Nablah = rs.SurfaceVolumeCentroid(inter2)
        if Nablah:
            cbh = rs.AddPoint(Nablah[0])
        
        cbh_coord = rs.PointCoordinates(cbh)
        lever = cg_coord[0] - cbh_coord[0]
        trim = 0
        cbt = ""
        cbt_coord = [0,0,0]
        
        if (lever > 0):
    
            while (lever > 0.01):
                
                trim = trim + 0.1
                trimmed = rs.RotateObject(heeled, cg, trim, [0,1,0], True)
                intersect = rs.BooleanIntersection(trimmed, dwl, False)
                tvolume = rs.SurfaceVolumeCentroid(intersect)
                cbt = rs.AddPoint(tvolume[0])
                cbt_coord = rs.PointCoordinates(cbt)
                Volumet = rs.SurfaceVolume(intersect)
                Volume_t = Volumet[0]
                lever = cg_coord[0] - cbt_coord[0]
                
                if (lever > 0.01):
                    rs.DeleteObject(trimmed)
                    rs.DeleteObject(intersect)
                    rs.DeleteObject(cbt)
                    continue
                
                diff = Initial_Volume - Volumet
                if ( diff > 0 ):
                    
        elif (lever < 0):
            while (lever < -0.01):
            trim = trim - 0.1
            trimmed = rs.RotateObject(heeled, cg, trim, [0,1,0], False)
            intersect = rs.BooleanIntersection(trimmed, dwl, False)
            trimmed_cb(intersect)
            cbt = rs.AddPoint(cbh_coord)
            Volumet = rs.SurfaceVolume(intersect)
            Volume_t = Volumet[0]
            
            if (cg_coord[0] - cbh_coord[0] > 0.001):
                rs.DeleteObject(trimmed)
                rs.DeleteObject(intersect)
                rs.DeleteObject(cbt)
                continue
                
elif (Volume_h - Initial_Volume < 0):
    
    while (Initial_Volume - Volume_h > 0.01):
        draft = draft + 0.001
            
        aux_plane = rs.PlaneFromFrame( [-5,-50,draft], [1,0,0], [0,1,0] )
        dwl = rs.AddPlaneSurface(aux_plane, 100, 100)
            
        inter2 = rs.BooleanIntersection(heeled, dwl, False)
        Volume = rs.SurfaceVolume(inter2)
        Volume_h = Volume[0]
        
        Nablah = rs.SurfaceVolumeCentroid(inter2)
        if Nablah:
            cbh = rs.AddPoint(Nablah[0])
    
        if (Initial_Volume - Volume_h > 0.01):
            rs.DeleteObject(inter2)
            rs.DeleteObject(dwl)
            rs.DeleteObject(cbh)



#def trimmed_cb(heeled):
#    tvolume = rs.SurfaceVolumeCentroid(heeled)
#    cbt = rs.AddPoint(tvolume[0])
#    cbt_coord = rs.PointCoordinates(cbt)
#    result.append(cbt)
#    result.append(cbt_coord)
#    rs.MessageBox(result[1])
#    return result
    

        #if (Initial_Volume - Volume_t < 0):
            
            
            


#rs.MessageBox("Volume difference:" + str(Initial_Volume - Volume_t))
        
