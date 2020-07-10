def direction(p,q,r):
    return (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1]) 

def adjacent(p, q):
    return abs(p[0] - q[0] <= 1) and abs(p[1] - q[1] <= 1)

def convexHull(points):
    
    minn = 0
    for i in range(1,len(points)): 
        if points[i][0] < points[minn][0]: 
            minn = i 
        elif points[i][0] == points[minn][0]: 
            if points[i][1] > points[minn][1]: 
                minn = i 
    
    hull = []
    
    p = minn
    q = 0
    while(True):
        hull.append(p)
        q = (p + 1) % len(points)

        for i in range(len(points)):
            if(direction(points[p],points[i],points[q]) < 0):
                q = i
        
        p = q

        if p == minn:
            break
    
    hull_points = []
    for pos in hull: 
        hull_points.append((points[pos][0], points[pos][1])) 
    return hull_points

