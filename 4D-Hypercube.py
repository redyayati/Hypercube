from vpython import *

scene.width = 850
scene.height = 600
scene.background = color.color = vector(0, 0, 0)

def matMulti(a,b) : 
    # For Matrix Mutlitiplication
    c = len(a[0])
    r = len(b)
    result = []
    if c == r : 
        for j in range(len(a)) :
            m=[]
            for i in range(len(b[0])) : 
                m.append(i)
            result.append(m)

        for row in range(len(a)) : 
            for col in range(len(b[0])) : 
                element = 0
                for k in range(r) : 
                    m = a[row][k]*b[k][col]
                    element = element + m
                result[row][col] = element       
    elif c != r : 
        print("cannot be multiplied")
        return 
    return result

def connect(offset, bar , i , j , points) : 
    aVec = points[i+offset]
    bVec = points[j+offset]
    bar.pos = aVec
    bar.axis = bVec - aVec

class Vector4() : 
    def __init__(self , x,y,z,w) : 
        self.x = x
        self.y = y 
        self.z = z
        self.w = w


points = [n for n in range(16)]

points[0] = [[-1],[1],[1],[1]]
points[1] = [[1],[1],[1],[1]]
points[2] = [[1],[-1],[1],[1]]
points[3] = [[-1],[-1],[1],[1]]
points[4] = [[-1],[1],[-1],[1]]
points[5] = [[1],[1],[-1],[1]]
points[6] = [[1],[-1],[-1],[1]]
points[7] = [[-1],[-1],[-1],[1]]
points[8] = [[-1],[1],[1],[-1]]
points[9] = [[1],[1],[1],[-1]]
points[10] = [[1],[-1],[1],[-1]]
points[11] = [[-1],[-1],[1],[-1]]
points[12] = [[-1],[1],[-1],[-1]]
points[13] = [[1],[1],[-1],[-1]]
points[14] = [[1],[-1],[-1],[-1]]
points[15] = [[-1],[-1],[-1],[-1]]

theta = 0
rot_speed = 0.005

project_mat = [[1,0,0],
               [0,1,0],               
               [0,0,0]]

spheres = [sphere(radius=.1) for i in range(16)]

lines = [cylinder(radius=.02) for i in range(12*2 + 8)]

for i in range(16) : 
    point = points[i]
    x = point[0][0]
    y = point[1][0]
    z = point[2][0]
    spheres[i].pos = vector(x,y,z)

projected = []
projDist = 4

def distance(x) : 
    global projDist
    projDist = x.value

slider(bind=distance, vertical=False,min=1.5, max=7, value=4, text="Freq")

while True :
    rate(100)
    rotmat_x = [[1,0,0,0],
                [0,cos(theta),-sin(theta),0],
                [0,sin(theta),cos(theta),0],
                [0,0,0,1]]
    rotmat_y = [[cos(theta),0,sin(theta),0],
                [0,1,0,0],
                [-sin(theta),0,cos(theta),0],
                [0,0,0,1]]
    rotmat_z = [[cos(theta),-sin(theta),0,0],
                [sin(theta),cos(theta),0,0],
                [0,0,1,0],
                [0,0,0,1]]
    rotmat_zw = [[1,0,0,0],
                [0,1,0,0],
                [0,0,cos(theta),-sin(theta)],
                [0,0,sin(theta),cos(theta)]]
    rotmat_yw = [[1,0,0,0],
                [0,cos(theta),0,-sin(theta)],
                [0,0,1,0],
                [0,sin(theta),0,cos(theta)]]
    rotmat_xw = [[cos(theta),0,0,-sin(theta)],
                [0,1,0,0],
                [0,0,1,0],
                [sin(theta),0,0,cos(theta)]]


    projected = []
    dst = projDist 
    # print(dst)
    
    for i in range(len(points)) : 
        # rot_x = matMulti(rotmat_x , points[i])
        # rot_y = matMulti(rotmat_y , rot_x)
        # rot_z = matMulti(rotmat_z , points[i])
        # rot_zw = matMulti(rotmat_zw , points[i])

        # rotated = matMulti(rotmat_y , rot_x)
        # rotated = matMulti(rotmat_z , rotated)
        rotated = matMulti(rotmat_zw , points[i])
        # rotated = matMulti(rotmat_y , rotated)

        # dist = 2
        z = 1/(dst - rotated[3][0])
        # z = 1
        project_mat = [[z,0,0,0],
                        [0,z,0,0],               
                        [0,0,z,0]]
        projected_mat = matMulti(project_mat, rotated)
        x = projected_mat[0][0] * 2
        y = projected_mat[1][0] * 2
        z = projected_mat[2][0] * 2
        spheres[i].pos = vector(x,y,z)
        projected.append(vector(x,y,z))
    theta += rot_speed

    linesIndex = 0
    for i in range(4) : 
        connect(0,lines[linesIndex] , i , (i+1)%4 , projected) 
        linesIndex +=  1
        connect(0,lines[linesIndex] , i + 4 , ((i+1)%4)+4 , projected) 
        linesIndex += 1
        connect(0,lines[linesIndex] , i , i+4 , projected) 
        linesIndex += 1
    for i in range(4) : 
        connect(8,lines[linesIndex] , i , (i+1)%4 , projected) 
        linesIndex +=  1
        connect(8,lines[linesIndex] , i + 4 , ((i+1)%4)+4 , projected) 
        linesIndex += 1
        connect(8,lines[linesIndex] , i , i+4 , projected) 
        linesIndex += 1
    for i in range(8) : 
        connect(0,lines[linesIndex] , i , i+8, projected) 
        linesIndex += 1
