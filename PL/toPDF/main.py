from manim import config, tempconfig
from Plot import Graphique
from simplex import simplexTableTypst
from fractions import *
import os

def methodeGraphique(programme,index='',file_name='image',scale=1):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(script_dir, "images")
    os.makedirs(images_dir, exist_ok=True)
    config.output_file = os.path.join(images_dir, file_name)
    with tempconfig({"quality": "high_quality"}): 
        scene=Graphique(programme,scale)
        scene.render()
        
    return f''' \n= {index} Methode Graphique \n \ 
    #figure(
  image("images/{file_name}.png", width: 80%),
)\n \ \n \ \n \ '''

def formCanonique(programme,index=''):
    f=programme['function']
    sc = programme['contraintes']
    text1=' =  Form Canonique (primal)\n $ \M\\ax F('
    text2=''
    for i in range(len(f)):
        text1+=f'X_{i+1}'
        text2+=f'{f[i]} X_{i+1}'
        if i !=len(f)-1:
            text1+=','
            text2+='+'
    text=text1+') = '+text2 +' $'
    text+='\n $ \n \sc=cases('
    for c in sc:
        line=''
        i=1
        for item in c[0]:
            if item !=0:
                line +=f'{item} X_{i}'
                if i != len(c[0]):
                    line+='+'
            i+=1
        line+=f' &<= {c[1]} ,\n  '
        text+=line
    text+=') $'

    return text



f=[1200,1000]

sc=[
    [[10,5],200],
    [[2,3],60],
    [[1,1],34],
    # [[6,7],30],
]
programme={"function":f,"contraintes":sc}

text=''
text+=formCanonique(programme)
text+=methodeGraphique(programme,scale=4)
text+='\n\n =  Methode Simplexe \n\n'
text+=simplexTableTypst(programme)


script_dir = os.path.dirname(os.path.abspath(__file__))
with open(f'{script_dir}/file.typ','w',encoding='utf-8') as f:
    f.write(text)