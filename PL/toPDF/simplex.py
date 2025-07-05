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
        
def Typst_table(table, index, piv=None):
    if piv:
        x_pv=piv[1]
        y_pv=piv[0]
    else:
        x_pv=12
        y_pv=12

    text = f"""#figure(table(\n  columns: {len(table[0])},\n  align: center,\n  inset: 10pt,\n  fill: (x, y) =>if x == {x_pv} or y == {y_pv} {{rgb(255,0,0,150)}},\n"""

    text += " "
    for i, row in enumerate(table):
        text += "    "
        text+=''
        for j, item in enumerate(row):
            if '$' in str(item):
                r=True
            else:
                r=False
                text+='$'

            if piv and i == piv[0] and j == piv[1]:
                text += f"{item}"
            else:
                text += f"{item}"
            if r:
                text+=','
            else:
                text+='$,'
    text += "\n"

    text += f")\n,caption:[simplex-{index}])\n \\ \n \\ \n "
    return text

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
        lis.append(f'$X_{i+1}$')

    for i in range(nb_eps):
        lis.append(f'$e_{i+1}$')
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
    
def simplexTableTypst(programme):
    f = programme['function']
    sc = programme['contraintes']
    t=[]
    t.append(header_helper(len(f),len(sc)))
    i=0
    for line in sc:
        t.append([
            fr'$e_{i+1}$',*line_helper(line,i,len(sc)),line[1]
        ])
        i+=1
    t.append(footer_helper(f,len(sc)))
    tables=next_simplex(t)
    
    text=r'''
    '''
    for i in range(len(lis_tables)):
        text+=Typst_table(lis_tables[i]['table'],i,lis_tables[i]['piv'])
    return text



