from vpython import *

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

def connect(bar , i , j , points) : 
    aVec = points[i]
    bVec = points[j]
    bar.pos = aVec
    bar.axis = bVec - aVec

class Vector4() : 
    def __init__(self , x,y,z,w) : 
        self.x = x
        self.y = y 
        self.z = z
        self.w = w


points = [n for n in range(8)]

points[0] = [[-1],[1],[1]]
points[1] = [[1],[1],[1]]
points[2] = [[1],[-1],[1]]
points[3] = [[-1],[-1],[1]]
points[4] = [[-1],[1],[-1]]
points[5] = [[1],[1],[-1]]
points[6] = [[1],[-1],[-1]]
points[7] = [[-1],[-1],[-1]]

theta_x = theta_y = theta_z = 0
rot_speed = 0.001

project_mat = [[1,0,0],
               [0,1,0],               
               [0,0,0]]

spheres = [sphere(radius=.1) for i in range(8)]

lines = [cylinder(radius=.02) for i in range(12)]

for i in range(8) : 
    point = points[i]
    x = point[0][0]
    y = point[1][0]
    z = point[2][0]
    spheres[i].pos = vector(x,y,z)

projected = []

while True :
    rate(50)
    rotmat_x = [[1,0,0],
                [0,cos(theta_x),-sin(theta_x)],
                [0,sin(theta_x),cos(theta_x)]]
    rotmat_y = [[cos(theta_y),0,sin(theta_y)],
                [0,1,0],
                [-sin(theta_y),0,cos(theta_y)]]
    rotmat_z = [[cos(theta_z),-sin(theta_z),0],
                [sin(theta_z),cos(theta_z),0],
                [0,0,1]]
    projected = []
    for i in range(len(points)) : 
        rot_x = matMulti(rotmat_x , points[i])
        rot_y = matMulti(rotmat_y , rot_x)
        rot_z = matMulti(rotmat_z , rot_y)
        dist = 4
        z = 1/(dist - rot_z[2][0])
        project_mat = [[z,0,0],
                        [0,z,0],               
                        [0,0,0]]
        # point_2d = matMulti(project_mat, rot_z)
        point_2d = rot_z
        x = point_2d[0][0] 
        y = point_2d[1][0] 
        z = point_2d[2][0] 
        spheres[i].pos = vector(x,y,z)
        # theta_x += rot_speed
        theta_y += rot_speed
        projected.append(vector(x,y,z))



    linesIndex = 0
    for i in range(4) : 
        connect(lines[linesIndex] , i , (i+1)%4 , projected) 
        linesIndex +=  1
        connect(lines[linesIndex] , i + 4 , ((i+1)%4)+4 , projected) 
        linesIndex += 1
        connect(lines[linesIndex] , i , i+4 , projected) 
        linesIndex += 1
