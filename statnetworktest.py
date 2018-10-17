# -*- coding: utf-8 -*-
__version__='0.1.1'
"""
Created on Wed Aug 22 22:00:23 2018

help from 
ftp://ftp.ics.uci.edu/pub/centos0/ics-custom-build/BUILD/PyQt-x11-gpl-4.7.2/examples/graphicsview/diagramscene/diagramscene.py !!!!!!!!
http://www.windel.nl/?section=pyqtdiagrameditor
https://graphviz.gitlab.io/_pages/Documentation/TSE93.pdf
https://www.qtcentre.org/threads/5609-Drawing-grids-efficiently-in-QGraphicsScene
http://www.davidwdrell.net/wordpress/?page_id=46
https://stackoverflow.com/questions/3810245/how-to-select-multiple-items-without-pressing-ctrl-key-within-qgraphicsscene#3839127
https://stackoverflow.com/questions/32192607/how-to-use-itemchange-from-qgraphicsitem-in-qt/32198716#32198716
https://github.com/cb109/qtnodes
https://het.as.utexas.edu/HET/Software/html/graphicsview-elasticnodes.html
https://www.qtcentre.org/threads/43649-QGraphicsScene-is-SLOW-with-a-lot-of-items-!
https://adared.ch/qnodeseditor-qt-nodesports-based-data-processing-flow-editor/
https://stackoverflow.com/questions/20771965/qt-graph-drawing
http://blog.tjwakeham.com/pyqt4-node-editor/
https://github.com/rochus/qt5-node-editor
http://austinjbaker.com/node-editor-prototype
https://github.com/EricTRocks/pyflowgraph

0.
    0.2 - started logging
    0.3 - edges work & track
    1.0 - added first few special nodes, added (buggy) arrow, process flow substantiated, lots of modularization
    1.1 - changeable node graphic, graphicPancakes working & ugly, skeleton for terminal hover events



TODO:
    some widgets can be overridden by inputs
    FFT node
    Usable w/o gui
    Make signal its own object? - helpful to trace
    upload to github
    constrainable lengths (blegh) - rigidity value 0-1 as some half tangent fn
    Datasources as Ngons? Torminals on points as distinct dims of data 
    create new connected node on click 
    hold on edge/terminal adjusts/dels? connections
    selectbox
    have startup net (customizable)
    Node types - 
        Circles - 
            "scoots over" as more terminals added
        Polygons
            -fixed # of nodes
            -sources?
        Boxes (rounded)
            clear distinction between in/out
        
    
    ctrl T on several nodes makes total connection (undir?)
    Drag & drop for nodes - long press to move, short to highlight, doubleclick to edit?
    Edges go from term(interface) to term, not nodes to nodes
    place nodes from forces/etc
    generate net from adjmat
    order of selection
    sub?terminal STDev 
    encode strength in size/aspect in color
    simplex coloring - low opacity & stacks
    clean up code
    max num of nodes able to b added (1000? - editable)
    select two nodes then key combo to add edge between em  (j?e?f?f?)
    keycombo for new nodes (a?shifta?)
    deleteable/breakable (x)
    "show network metrics"
    processing nodes
        start @ sources (data/topological sense)
        
    cache (short+long?) calculated paths/subpaths to save time - need to figure out how to handle different ways of inputting new data
    have custom "group" node as object w cache checkbox? 
    make able to "act like singularities" for DS? 
    
    graphs: holoviews? 
    
    
    
------
Each Network tracks all nodes & their connections - Animations/Edge Forces go here 
Each Node has a fn and has a list of terminals (shortcut to list of edges)
Each Terminal has list of edges "hooked" to` 
Each Edge knows From/To, Signal, and effect of edge (usually none if just transmission)

@todo implement bokeh for web dashboard
@todo merge array node 
@todo SQL nodes - graphic automatically converts on detect, SELECT, WHERE, etc nodes? if implemented then single Pancakess

    #@todo fill in Pancakes sides better 
@todo signal path makes new threads for parallelicity

"""
import math

from PyQt5.QtWidgets import * #GUI (Graphical User Interface) library
from PyQt5 import QtGui, QtCore
#from pyqtgraph import flowchart
from .Nodes import *

import numpy as np
import sys
from OHLib import *
#

##################################################
        #SPECIFIC NODE TYPES:
        #@todo implement a general handler for widget/s/
        #@todo - put default colors here? or maybe in network. not in window tho.
#@todo make sure everything plays nice with pandas - maybe numpy?
defnode=graphicNode#@todo better way of doing this

##################################################
class netWindow(QMainWindow):
    def __init__(self): 
        super(netWindow,self).__init__()
        self.wind=QWidget()
        self.setCentralWidget(self.wind)
        self.layout=QGridLayout()
        self.wind.setLayout(self.layout)
#        QtGui.QShortcutEvent()
        self.Window()
        self.show()
        self.setMinimumSize(500,500)
    def Window(self):
        self.undir=False
        class gridscene(QGraphicsScene):
            nodeMoved=QtCore.pyqtSignal(int)
            def __init__(self,*args):
                super(gridscene,self).__init__(*args)
                self.keylist=[]
            def keyPressEvent(self,event):
                self.firstRelease=True
                self.keylist.append(event.key())#16777248 shift
                if QtCore.Qt.ShiftModifier in self.keylist:
                    
#                    print('shift')
#                    if 
                    print([i for i in self.keylist])
#                    print(event.count())
            def keyReleaseEvent(self,event):
                if self.firstRelease==True:
#                    print(self.keylist)
                    pass
                self.firstRelease=False
                del self.keylist[-1]
            def drawBackground(self,painter,rect,*args):
                pen=QtGui.QPen(QtGui.QColor('lightgray'))
                pen.setStyle(QtCore.Qt.DotLine)
                painter.setPen(pen)
                painter.drawLines(self.makebg())
            def makebg(self):
                gridsize=20
                lines=[]
        #        scene.
                
#                print(self.scene.sceneRect().right())
                mn,mx=-1000,1000
                ax,ay=50,50#anchor offset
                n=100
                for i in range(n):
                    
                    lines.append(QtCore.QLineF((i-ax)*gridsize,mn,(i-ax)*gridsize,mx))
                    
                    lines.append(QtCore.QLineF(mn,(i-ay)*gridsize,mx,(i-ay)*gridsize))
                return lines
        
        self.scene=gridscene()
#        self.scene.addItem(graphicPancakes())
        self.view=QGraphicsView(self.scene)
#        short=QtGui.QShortcutEvent(QtGui.QKeySequence("Shift+A"),self.view)
#        short.activated.connect(lambda:print('testing'))
        self.view.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        self.layout.addWidget(self.view)
        self.toolbox=QToolBox()
#        self.toolbox.setMinimumWidth()
        self.nodes=dict()
        def updatenodefn(i,*args):
         
#            print(self.nodes[i].edges.keys())
            for j in self.nodes[i].edges.keys():
                if (i,j) in self.edges.keys():
                    self.edges[(i,j)].updatePos()
#                    print(self.edges.keys(),(j,i))
                else:
                    if (j,i) in self.edges.keys():
#                     print('test')
                     self.edges[(j,i)].updatePos()
       
        self.scene.nodeMoved.connect(updatenodefn)
#        self.scene.selectionChanged.connect(lambda:print(self.scene.selectedItems()))
        self.edges=dict()
        buttgrp=QGroupBox()
        buttgrp.setLayout(QHBoxLayout())
        self.btns=dict()
        self.grps=dict()
        self.btnfns=dict()
        def addBtn(text,fn,grp=None,order=None):
            self.btnfns[text]=fn
            if grp is None:
                self.btns[text]=QPushButton(text=text)
                self.btns[text].clicked.connect(self.btnfns[text])
                buttgrp.layout().addWidget(self.btns[text])
            else:
                if grp not in self.grps.keys():
                    self.grps[grp]=QComboBox()
                    buttgrp.layout().addWidget(self.grps[grp])
                    self.grps[grp].addItem(grp.upper()+' group')      
                    self.grps[grp].activated[str].connect(lambda i:self.btnfns[i]())
                
                self.grps[grp].addItem(text)
                #@todo have a label area on page for errors
            #@todo make a "repeat action" per group?
            #add all buttons here
            #{groupname:{buttonname:fn}}
        btndict={'inputs':{'inputbox':lambda:self.createNode(nodetype=InputNode,color="#aaaaaa"),
                          'source':lambda:self.createNode(nodetype=SourceNode,color="#000000")},
                 'filters':{'SQL':lambda:self.createNode(nodetype=SQLCommandNode,color='Red'),
                            'split':lambda:self.createNode(nodetype=SplitNode,color="fuchsia")},
                 'math':{'+':lambda:self.createNode(nodetype=AdditionNode,color="#ffffff"),
                         '-':lambda:self.createNode(nodetype=SubtractionNode,color="cyan"),
                         'average':lambda:self.createNode(nodetype=AverageNode,color="#987654")},
                 'basics':{'node':lambda:self.createNode(color=rainbow[len(self.nodes)%len(rainbow)]),
                           'edge':lambda:self.createConnect(),
                           'terminal':lambda:self.scene.selectedItems()[0].nodeobj.createTerminal()},
                 'utils':{'delete':lambda:self.deleteNode(self.scene.selectedItems()[0].nodeobj.name),
                          'flip':lambda: self.scene.selectedItems()[0].flipEdge()},
                 'outputs':{'print':lambda:self.createNode(nodetype=PrintNode,color="Pink")},
                'SQL':{},
                'arraytools':{},
                'HoloViews tools':{},#@todo show as tree-view if somehow is indicated w parent
                }#@todo make able to check if selected object(s?) are edges before initiating flip
        for g in btndict.keys():
            for t in btndict[g].keys():
                addBtn(grp=g,text=t,fn=btndict[g][t])
        self.layout.addWidget(buttgrp)
#        
    def generateAdjMat(self,root=0):
        n=len(self.nodes)
        A=np.zeros((n,n))
        for i in self.edges.keys():
            ii=(i[0]-1,i[1]-1)
            A[ii]=1
            if self.undir:
                A[ii[1],ii[0]]=1
        return A
            
   
    def createNode(self,nodetype=Node,label=None,defloc=None,color='red'):
        
        if label is None:
            label=len(self.nodes)+1
#            print(label)
        self.nodes[label]=nodetype(name=label)
        r=self.nodes[label].retqt(loc=(10,10))
        if self.nodes[label].widget is not None:
            proxy=QGraphicsProxyWidget(r)
            #@todo center graphicsproxy
            proxy.setZValue(999)#should display on top no matter what
            proxy.setWidget(self.nodes[label].widget)
#        print(r)
        r.setBrush(QtGui.QBrush(QtGui.QColor(color)))
        self.scene.addItem(r)
#        print(self.generateAdjMat())
        
    def createConnect(self,nfrom=1,nto=2):
        if len(self.scene.selectedItems())==2:#if selection is obvious  ---- can do smth w selectionChanged to figure out order selected for from/to
            nfrom,nto=[i.name for i in self.scene.selectedItems()]
        narr=(nfrom,nto)
        nd={'from':self.nodes[nfrom],'to':self.nodes[nto]}
#        xto,yto=senarr=ndlf.nodes[nto].gnode.pos()
#        xfrom,yfrom=self.nodes[nfrom].gnode.pos()
        if narr in self.edges.keys():#checks if refers right
#        
            self.edges[narr].updatePos()
#            self.scene.removeItem(self.edges[narr])
            edge=self.edges[narr]
        else:#@todo clean up this fn
            edgeobj=Edge(self.nodes[nfrom],self.nodes[nto])
            edge=arrowEdge(self.nodes[nfrom].gnode.x()+self.nodes[nfrom].sz['x'],self.nodes[nfrom].gnode.y()+self.nodes[nfrom].sz['y'],self.nodes[nto].gnode.x()+self.nodes[nfrom].sz['x'],self.nodes[nto].gnode.y()+self.nodes[nfrom].sz['y'],narr=nd,edgeobj=edgeobj)
#        edge.setParentItem(self.nodes[1].gnode)
        self.edges[(nfrom,nto)]=edge
        self.nodes[nfrom].edges[nto]=edge
#        rpg
        self.nodes[nto].edges[nfrom]=edge
        
        self.scene.addItem(edge)
#        print(self.edges)
#        print(self.generateAdjMat())
       
    def breakConnect(self,nfrom,nto):
        pass
    def deleteNode(self,label):
        print(label)
        pass
    #@todo flesh out deletenode
    
    
    
    
    
    
    
    
    
    
def netrun():
    app=0         
    #windthread=QtCore.QThread()
    
    app=QApplication(sys.argv)
    wind=netWindow()
    app.exec_()
rainbow
    
    
    
    
types=['sources','fns','restricts','categories','outputs']
{'fns':{'meta':{},'add':{},'sub':{}},
 'outputs':{'heatmap','scatterrel','timeline'},
 'restricts':{'single','quotient/category','range'}}