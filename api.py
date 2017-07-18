#!/usr/bin/env python
# -*- coding: UTF-8 -*-# enable debugging
import main
import cgi, cgitb
cgitb.enable()   
print("Content-Type: text/html;charset=utf-8\r\n")
print("Hello World!") 





form = cgi.FieldStorage()
question=form.getvalue('question')
mat, maxLength, glove, patty = main.processPatty()
vectors, parts, pos, gen_question, similarities, unweighted, weighted, result = main.processQuestion(glove,maxLength, patty, mat,question )
print("vectors\r\n")
print (vectors)
print("parts\r\n")
print (parts)
print("pos\r\n")
print (pos)
print("gen_question\r\n")
print (gen_question)
print("result\r\n")
print (result)



