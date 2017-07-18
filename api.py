#!/usr/bin/env python
# -*- coding: UTF-8 -*-# enable debugging
import main
import cgi, cgitb
import json
import numpy as np
cgitb.enable()   
print("Content-Type: text/html;charset=utf-8\r\n")






form = cgi.FieldStorage()
question=form.getvalue('question')
mat=np.load('mat.dat')
maxLength=np.load('maxLength.dat')
glove = main.load_data('glove.dat')
patty = main.load_data('patty.dat')
patty.processData()
vectors, parts, pos, gen_question, similarities, unweighted, weighted, result = main.processQuestion(glove,maxLength, patty, mat,question )

vectors_json=json.dumps(vectors[0].tolist())
o={}
o["vectors"]=[]
for vec in vectors:
	o["vectors"].append(vec.tolist())
o["parts"]=parts
o["pos"]=pos
o["gen_question"]=gen_question
o["result"]=result
print (json.dumps(o))



