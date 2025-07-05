from manim import *
import math

def convex_hull(points):
    """Computes the convex hull of a set of 2D points using Andrew's monotone chain algorithm."""
    points = sorted(points)  # Sort points lexicographically (by x, then by y)

    def cross_product(o, a, b):
        """Returns the cross product of vector OA and OB (O is the pivot point)."""
        ox, oy = o
        ax, ay = a
        bx, by = b
        return (ax - ox) * (by - oy) - (ay - oy) * (bx - ox)

    # Construct lower hull
    lower = []
    for p in points:
        while len(lower) >= 2 and cross_product(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Construct upper hull
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross_product(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # Remove last point of each half (duplicate)
    return lower[:-1] + upper[:-1]

def to_int(r):
    e=int(r)
    if e-r ==0 :
        return e
    else:
        return r
def func(lis):
    a, b, c = lis
    if b != 0:
        return lambda x: (c - a*x) / b  # Normal case
    else:
        return lambda x: float("inf") if x != c/a else 0
def get_Y_null(lis):
    return lis[2]/lis[0]

def get_intersections(line1,line2):
    [a1,b1,c1]=line1
    c1=-c1
    [a2,b2,c2]=line2
    c2=-c2
    try:
        x=(b1*c2-b2*c1)/(a1*b2-a2*b1)
        y=(c1*a2-c2*a1)/(a1*b2-a2*b1)

        return (to_int(x),to_int(y))
    except :
        return None

def getRegion(axes,scale,lis,col,minim=False):
    a=lis[0]
    b=lis[1]
    c=lis[2]
    try:
        x_val=lis[2]/lis[0]
        if b==0:
            ymax=axes.y_length*scale
            xmax=axes.x_length*scale
            
            if minim:
                pol=Polygon(
                    axes.c2p(0, 0),
                    axes.c2p(0, ymax),
                    axes.c2p(x_val, ymax),
                    axes.c2p(x_val, 0),
                    fill_color=col,
                    fill_opacity=.5,
                    stroke_width=0
                )
            else:
                pol=Polygon(
                    axes.c2p(x_val, 0),
                    axes.c2p(x_val, ymax),
                    axes.c2p(xmax, ymax),
                    axes.c2p(xmax, 0),
                    fill_color=col,
                    fill_opacity=.5,
                    stroke_width=0
                )
        else:        
            if minim:
                y0=c/b
                xmax=c/a
                pol=Polygon(
                    axes.c2p(0, 0),
                    axes.c2p(0, y0),
                    axes.c2p(xmax, 0),
                    axes.c2p(xmax, 0),
                    fill_color=col,
                    fill_opacity=.5,
                    stroke_width=0
                )
            else:
                y0=c/b
                xmax=c/a
                pol=Polygon(
                    axes.c2p(0, y0),
                    axes.c2p(0,axes.y_length*scale),
                    axes.c2p(axes.x_length*scale,axes.y_length*scale),
                    axes.c2p(axes.x_length*scale,axes.y_length*scale),
                    axes.c2p(axes.x_length*scale,0),
                    axes.c2p(xmax,0),
                    fill_color=col,
                    fill_opacity=0.3,
                    stroke_width=0
                )
            
        return pol
    except :
        y_val=lis[2]/lis[1]
        ymax=axes.y_length*scale
        xmax=axes.x_length*scale
        if minim:
            pol=Polygon(
                axes.c2p(0, 0),
                axes.c2p(0, y_val),
                axes.c2p(xmax, y_val),
                axes.c2p(xmax, 0),
                fill_color=col,
                fill_opacity=.5,
                stroke_width=0
            )
        else:
            pol=Polygon(
                axes.c2p(0, y_val),
                axes.c2p(0, ymax),
                axes.c2p(xmax, ymax),
                axes.c2p(xmax, y_val),
                fill_color=col,
                fill_opacity=.5,
                stroke_width=0
            )
        return pol

def above_all_lines(point,lines,minim=False):
    valid=True
    x=point[0]
    y=point[1]
    if minim:
        for line in lines:
            [a,b,c]=line
            c=-c
            if (a*x + b*y +c)<0:
                valid=False
    else:
        for line in lines:
            [a,b,c]=line
            c=-c
            if (a*x + b*y +c)>0:
                valid=False
    return valid

def get_Valid_Region(axes,scale,lis,minim=False,clo=GREEN):
    if minim:
        valid_dots=convex_hull(lis)
        region=Polygon(
                axes.c2p(0, axes.y_length*scale),
                *[axes.c2p(x, y) for x, y in valid_dots],
                axes.c2p(axes.x_length*scale, 0),
                axes.c2p(axes.x_length*scale, axes.y_length*scale),
                fill_color=GREEN,
                fill_opacity=0.6,
                stroke_width=0
            )
    else:
        lis.append((0,0))
        valid_dots=convex_hull(lis)
        region=Polygon(
                *[axes.c2p(x, y) for x, y in valid_dots],
                fill_color=GREEN,
                fill_opacity=0.6,
                stroke_width=0
            )
    return region

def manage_intersections(lines):
    lines=[[1,0,0],*lines,[0,1,0]]
    intersections=[]
    checked=[]
    for i in range(len(lines)):
        line=lines[i]
        for j in range(len(lines)):
            line2=lines[j]
            if line==line2 or str(line2) in checked:
                continue
            inter=get_intersections(line,line2)
            if not inter or inter[0]<0 or inter[1] <0:
                continue
            intersections.append(inter)
        checked.append(str(line))
    return intersections
            

    ...

class Graphique(Scene):
    def __init__(self, programme=[],scale=1,minimizing=False, **kwargs):
        self.programme = programme
        self.scale=scale
        self.minimizing=minimizing
        super().__init__(**kwargs)
    def construct(self):

        scale=self.scale
        # contraintes :
        main_function=self.programme['function']
        minimizing=self.minimizing
        p1=[*self.programme['contraintes'][0][0],self.programme['contraintes'][0][1]]
        p2=[*self.programme['contraintes'][1][0],self.programme['contraintes'][1][1]]
        p3=[*self.programme['contraintes'][2][0],self.programme['contraintes'][2][1]]
        contraintes=[p1,p2,p3]
        intersections=[
            *manage_intersections(contraintes),
        ]
        
        axes = Axes(
            x_range=[0, 10*scale, scale],  # x starts from 0
            y_range=[0, 10*scale, scale],  # y starts from 0
            x_length=10,
            y_length=10,
            axis_config={"include_numbers": True},
        )
        def plott(contrainte,col):
            if contrainte[1]==0:
                x_val = contrainte[2]/contrainte[0]  # The x-value where the vertical line should be
                vertical_line = Line(
                    start=axes.c2p(x_val, axes.y_range[0]),  # Bottom of the vertical line
                    end=axes.c2p(x_val, axes.y_range[1]),    # Top of the vertical line
                    color=col
                )
                return vertical_line
            
            if contrainte[0]==0:
                y_val = contrainte[2]/contrainte[1] 
                horizontal_line = Line(
                    start=axes.c2p(-0.5, y_val),  
                    end=axes.c2p(axes.x_range[1], y_val),
                    color=col
                )
                return horizontal_line
            return axes.plot(func(contrainte), x_range=[-.5,get_Y_null(contrainte)+.5], color=col)

        # line1 = axes.plot(func(contraintes[0]), x_range=[-.5,get_Y_null(contraintes[0])+.5], color=BLUE)
        # line2 = axes.plot(func(contraintes[1]), x_range=[-.5,get_Y_null(contraintes[1])+.5], color=RED)
        # line3 = axes.plot(func(contraintes[2]), x_range=[-.5,get_Y_null(contraintes[2])+.5], color=GREEN)
        line1 = plott(contraintes[0],BLUE)
        line2 = plott(contraintes[1],RED)
        line3 = plott(contraintes[2],GREEN)
        lines=VGroup(line1,line2,line3)
        

        dots=VGroup()
        valid_dots=[]
        for inter in intersections:
            if above_all_lines(inter,contraintes,minimizing):
                valid_dots.append(inter)
                dot = Dot(color=YELLOW, radius=0.07)
                dot.move_to(axes.c2p(inter[0],inter[1])) 
                dots.add(dot)
            # else:
            #     dot = Dot(color=BLUE, radius=0.07)
            #     dot.move_to(axes.c2p(inter[0],inter[1])) 
            #     dots.add(dot)


        
        shaded_region1 = getRegion(axes,scale,p1,RED,minimizing)
        shaded_region2 = getRegion(axes,scale,p2,RED,minimizing)
        shaded_region3 = getRegion(axes,scale,p3,RED,minimizing)
        shaded_regions=VGroup(shaded_region1,shaded_region2,shaded_region3)

        valid_Region=get_Valid_Region(axes,scale,valid_dots,minimizing)
 
        points=VGroup()
        for point in valid_dots:
            if point==(0,0):
                continue
            points.add(MathTex(f"({round(point[0],2)},{round(point[1],2)}),"))
        points.arrange(RIGHT).scale(.7)

        if minimizing:
            character='\geq'
        else:
            character='\leq'
        results=[]
        for point in valid_dots:
            if point==(0,0):
                continue
            s=main_function[0]*point[0]+main_function[1]*point[1]
            results.append(s)
        
        point_results=VGroup()
        for point in valid_dots:
            if point==(0,0):
                continue
            s=main_function[0]*point[0]+main_function[1]*point[1]

            p= MathTex(f'F({round(point[0],2)},{round(point[1],2)})={round(s,2)}')
            if s == min(results) and minimizing:
                box=SurroundingRectangle(p)
                point_results.add(VGroup(p,box))
            elif s == max(results) and not minimizing:
                box=SurroundingRectangle(p)
                point_results.add(VGroup(p,box))
            else:
                point_results.add(VGroup(p))
        point_results.arrange(DOWN)

        if minimizing:
            header=MathTex(f"Min F(X,Y)={main_function[0]}X + {main_function[1]}Y",tex_to_color_map={'Min':BLUE_D}),
        else:
            header=MathTex(f"Max F(X,Y)={main_function[0]}X + {main_function[1]}Y",tex_to_color_map={'Max':BLUE_D}),

        explain=VGroup(
            header,
            Tex("contraintes :"),
            MathTex(f"{contraintes[0][0]}X + {contraintes[0][1]}Y {character} {contraintes[0][2]}",color=BLUE),
            MathTex(f"{contraintes[1][0]}X + {contraintes[1][1]}Y {character} {contraintes[1][2]}",color=RED),
            MathTex(f"{contraintes[2][0]}X + {contraintes[2][1]}Y {character} {contraintes[2][2]}",color=GREEN),
            Tex("les points:"),
            points,
            point_results
        ).arrange(DOWN).to_edge(RIGHT).scale(.7)
        deatailBox=Square(side_length=2,fill_color=WHITE,fill_opacity=1).next_to(
            axes.c2p(axes.x_length*scale,axes.x_length*scale),LEFT,buff=0.5).shift(DOWN)
        box_text=VGroup(
            Square(side_length=1,fill_color=GREEN,fill_opacity=1),Text("Zone faisable",color=BLACK)
        ).arrange(RIGHT).move_to(deatailBox.get_center()).scale(.5)
        r=VGroup(shaded_regions,valid_Region,axes,lines,dots,box_text).scale(.7).to_edge(LEFT)
        self.add(r)
        # self.add()
        self.add(explain)