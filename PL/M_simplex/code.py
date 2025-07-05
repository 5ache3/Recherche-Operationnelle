from manim import * 
from fractions import *

def get_pivot(lis):
    col_pivot=0
    m=0
    for i in range(1,len(lis[-1])):
        item=lis[-1][i]
        if item>m:
            m=item
            col_pivot=i
    row_pivot=-15
    m=-1
    for i in range(1,len(lis)-1):
        if lis[i][col_pivot]==0:
            continue
        item=lis[i][-1]/lis[i][col_pivot]
        if m==-1 and item >=0:
            m=item
            row_pivot=i
        if item >= 0 and item <m:
            m=item
            row_pivot=i
    return [row_pivot,col_pivot]

lis_tables=[]

def next_simplex(lis,pivot=None):
    if not pivot:
        pivot=get_pivot(lis)
        lis_tables.append({
            'piv':pivot,
            'table':lis
        })
        return next_simplex(lis,pivot)
    lis2=[]
    for i in range(len(lis)):
        lis2.append([])
        for j in range(len(lis[i])):
            lis2[i].append(lis[i][j])

    r_p,c_p=pivot
    lis2[r_p][0]=lis2[0][c_p]
    for i in range(1,len(lis)):
        lis2[i][c_p]=0

    for i in range(1,len(lis[r_p])):
        lis2[r_p][i]=Fraction(lis[r_p][i],lis[r_p][c_p])
    
    for i in range(1,len(lis)):
        if i== r_p:
            continue
        for j in range(1,len(lis[i])):
            if j== c_p:
                continue
            lis2[i][j] = lis[i][j] - Fraction(lis[r_p][j]*lis[i][c_p],lis[r_p][c_p])
    
    final=True
    for i in range(1,len(lis2[-1])):
        if float(lis2[-1][i]) > 0:
            final=False

    if not final:
        pivot=get_pivot(lis2)
        lis_tables.append({
            'piv':pivot,
            'table':lis2
        })
        return next_simplex(lis2,pivot)
    lis_tables.append({
        'piv':None,
        'table':lis2
    })
    return lis2
        
class SimplexVideo(Scene):
    def __init__(self, t0, **kwargs):
        self.t0=t0
        super().__init__(**kwargs)
    def construct(self):
        def create_table(table):
            data_table = [row[1:] for row in table[1:]]
            row_labels = [MathTex(row[0]) for row in table[1:]]
            col_labels = [MathTex(col) for col in table[0][1:]]
            return MathTable(data_table,row_labels=row_labels,col_labels=col_labels,include_outer_lines=True)
        
        def show_pivot(self,table,pivot):
            
            rect=SurroundingRectangle(table.get_rows()[-1][1:4],color=BLUE,fill_opacity=.1)
            table.get_columns()[pivot[1]]
            # Get column position

            row_pivot = SurroundingRectangle(table.get_rows()[pivot[0]], color=YELLOW, fill_opacity=0.1, fill_color=YELLOW)
            column_pivot= SurroundingRectangle(table.get_columns()[pivot[1]], color=YELLOW, fill_opacity=0.1, fill_color=YELLOW)

            self.play(Create(rect))
            cel_pivot=SurroundingRectangle(table.get_rows()[-1][pivot[1]],color=YELLOW,fill_opacity=.3)
            self.wait(2)
            self.play(Transform(rect,cel_pivot))
            self.wait(2)

            self.play(TransformFromCopy(cel_pivot,column_pivot),FadeOut(rect))
            self.wait(2)
            resultGroup=VGroup()
            s=0
            for i in range(2,len(t0)):
                if t0[i-1][pivot[1]] ==0:
                    oper=MathTex(fr"\frac{{{t0[i-1][-1]}}}{t0[i-1][pivot[1]]}= \varnothing").scale(.5).to_corner(UR)
                else:  
                    oper=MathTex(fr"\frac{{{t0[i-1][-1]}}}{t0[i-1][pivot[1]]}= {t0[i-1][-1]/t0[i-1][pivot[1]]}").scale(.5).to_corner(UR)
                resultGroup.add(oper)
                resultGroup.arrange(DOWN).shift(RIGHT)
                self.play(Indicate(table.get_entries((i+1, 0)),scale=1.5),
                        Indicate(table.get_entries((i, pivot[1]+1)),scale=1.5),
                        Write(resultGroup[s]),
                        run_time=3)
                s+=1
            box=SurroundingRectangle(resultGroup[pivot[0]-1])
            self.wait(3)
            self.play(Create(box),FadeOut(VGroup(resultGroup[:pivot[0]-1],resultGroup[pivot[0]:])))
            self.wait(2)
            self.play(Create(row_pivot),FadeOut(VGroup(box,resultGroup[pivot[0]-1])))
            self.wait(2)

            table.add_highlighted_cell((pivot[0]+1,pivot[1]+1),color=RED)
            table[0].set_opacity(1)
            self.play(FadeOut(VGroup(row_pivot,column_pivot)))
            
            self.wait(2)

        t0=self.t0
        next_simplex(t0)
        for t_index in range(len(lis_tables)):
            t0=lis_tables[t_index]['table']
            table=create_table(lis_tables[t_index]['table']).scale(.4).to_corner(UL)
            pivot=lis_tables[t_index]['piv']
            if not pivot:
                break
            table2=create_table(lis_tables[t_index+1]['table']).scale(.4).to_corner(DL)
            self.add(table)

            show_pivot(self,table,pivot)
            self.add(table2)
            row_pivot = SurroundingRectangle(table2.get_rows()[pivot[0]], color=YELLOW, fill_opacity=0.1, fill_color=YELLOW)
            column_pivot= SurroundingRectangle(table2.get_columns()[pivot[1]], color=YELLOW, fill_opacity=0.1, fill_color=YELLOW)
            self.play(Create(column_pivot))
            self.play(Indicate(table2.get_entries((pivot[0]+1,pivot[1]+1)),scale_factor=2,color=RED),run_time=2)
            self.wait(2)
            self.play(FadeOut(column_pivot),Create(row_pivot))
            for i in range(1,len(t0[0])):
                if i==pivot[1]:
                    continue
                # discription=MathTex(rf'= \frac',t0[pivot[0]][i],'',t0[pivot[0]][pivot[1]],'')
                tex1=MathTex(f'')
                discription=MathTex(fr'= \frac{{{t0[pivot[0]][i]}}}{t0[pivot[0]][pivot[1]]}',tex_to_color_map={'=':RED})
                # discription=Tex(rf"{t0[pivot[0]][i]}", r"\over", rf"{t0[pivot[0]][pivot[1]]}")
                self.play(Write(discription),run_time=.5)
                self.play(Indicate(table2.get_entries((pivot[0]+1,i+1)),scale_factor=2,color=RED),
                        Indicate(table.get_entries((pivot[0]+1,i+1)),scale_factor=2,color=GREEN),
                        Indicate(table.get_entries((pivot[0]+1,pivot[1]+1)),scale_factor=2,color=YELLOW),run_time=2
                        )
                self.remove(discription)
            self.play(FadeOut(row_pivot))
            for i in range(1,len(t0)):
                if i == pivot[0]:
                    continue
                for j in range(1,len(t0[i])):
                    if j == pivot[1]:
                        continue
                    val_piv=t0[pivot[0]][pivot[1]]
                    val_row=t0[pivot[0]][j]
                    val_col=t0[i][pivot[1]]
                    discription=MathTex(fr'={t0[i][j]}- \frac{{{val_col}*{val_row}}}  {{{val_piv}}}',tex_to_color_map={'=':RED})
                    self.play(Write(discription),run_time=.5)
                    self.play(
                        Indicate(table2.get_entries((i+1,j+1)),scale_factor=2,color=RED),
                        Indicate(table.get_entries((i+1,j+1)),scale_factor=2,color=RED),
                        Indicate(table.get_entries((pivot[0]+1,j+1)),scale_factor=2,color=GREEN),
                        Indicate(table.get_entries((i+1,pivot[1]+1)),scale_factor=2,color=GREEN),
                        Indicate(table.get_entries((pivot[0]+1,pivot[1]+1)),scale_factor=2,color=YELLOW),
                        run_time=2)
                    self.remove(discription)
            
            self.remove(table)
            self.play(table2.animate.to_corner(UL))


        self.wait(2)


def line_helper(line,ind,n):
    lis=[]

    for item in line[0]:
        lis.append(item)

    for i in range(n):
        if i == ind:
            lis.append(1)
        else :
            lis.append(0)
    return lis
    
def header_helper(nb_vars,nb_eps):
    lis=['']
    for i in range(nb_vars):
        lis.append(f'X_{{{i+1}}}')

    for i in range(nb_eps):
        lis.append(f'e_{{{i+1}}}')
    lis.append('')
    return lis

def footer_helper(vars,nb_eps):
    lis=['Z']
    for item in vars:
        lis.append(item)

    for i in range(nb_eps):
        lis.append(0)
    lis.append(0)
    return lis


def simplexFirstTable(programme):
    f = programme['function']
    sc = programme['contraintes']
    t=[]
    t.append(header_helper(len(f),len(sc)))
    i=0
    for line in sc:
        t.append([
            fr'e_{{{i+1}}}',*line_helper(line,i,len(sc)),line[1]
        ])
        i+=1
    t.append(footer_helper(f,len(sc)))

    return t



if __name__ == "__main__":
    f=[1200,1000]

    sc=[
        [[10,5],200],
        [[2,3],60],
        [[1,1],34],
    ]
    programme={"function":f,"contraintes":sc}     
    t0=simplexFirstTable(programme)
    with tempconfig({"quality": "high_quality"}): 
        
        scene=SimplexVideo(t0)
        scene.render()