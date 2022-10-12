from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, NextPageTemplate, Image, LongTable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

def foot2(pdf,doc):
    width,height = A4
    pdf.saveState()
    pdf.setFont('Times-Bold',28)
    pdf.drawCentredString(width/2.0, height-63, "REPORTE DE PRUEBA CDG")
    pdf.setFont('Times-Roman',9)
    #pdf.drawString(width-1*inch, 0.1 * inch,'Página '+"%d" % doc.page+' de '+"%d" % 3)

width,height = A4

doc = BaseDocTemplate("ReporteCDG1210.pdf",showBoundary=1, pagesize= A4)
contents =[]
styleSheet = getSampleStyleSheet()
TopCenter = Frame(0.4*inch,height-1.2*inch,width-0.8*inch,0.8*inch,showBoundary=1,id='normal')
leftlogoframe = Frame(0.2*inch,height-1.2*inch,1*inch,1*inch,showBoundary = 1)
rightlogoframe = Frame((width-1.2*inch),height-1.2*inch,1*inch,1*inch,showBoundary = 1)
frame1later = Frame(0.4*inch,0.6*inch,width-0.8*inch, height-2*inch,leftPadding=0,topPadding=0,showBoundary = 1,id='col1later')
frame2later = Frame(0.4*inch,0.6*inch,width-0.8*inch, height-2*inch,showBoundary = 1,id='col2later' )

frame_params = Frame(0.4*inch,0.6*inch,width-0.8*inch, height-2*inch,leftPadding=0,topPadding=0, showBoundary = 1,id='col')

firstpage = PageTemplate(id='firstpage',frames=[TopCenter,frame_params],onPage=foot2)

laterpages = PageTemplate(id='laterpages',frames=[TopCenter,frame1later],onPage=foot2)

contents.append(NextPageTemplate('laterpages'))

archivo_imagen = 'icons/Univalle.png'
logoleft = Image(archivo_imagen)
logoleft._restrictSize(0.5*inch, 0.5*inch)

logoleft.hAlign = 'LEFT'
logoleft.vAlign = 'CENTER'

contents.append(logoleft)
Datos_vehiculo=['KIA', 'SOUL LX 1.591 cc, 2011', 'Auto de pasajeros','cm','cm','psi','psi']
datos = (
                ('','Fabricante:' , Datos_vehiculo[0]),
                ('Identificación', 'Modelo:' ,Datos_vehiculo[1]),
                ('del vehículo', 'Tipo:',Datos_vehiculo[2]),
                ("",'Tamaño llantas: ','Delantera: '+ Datos_vehiculo[3]+ 'Trasera: '+Datos_vehiculo[4]),
                ("",'Presión llantas: ','Delantera: '+Datos_vehiculo[5] +'Trasera: '+Datos_vehiculo[6]),
                )
table = LongTable(data = datos,colWidths=(1.0*inch,3.5*inch,2.95*inch),
                    style = [
                            ('GRID',(1,0),(2,4),0.5,colors.grey),
                            ('GRID',(0,5),(0,5),0.5,colors.grey),
                            ],
                    hAlign='LEFT'
                    ,splitByRow=True
                    ,repeatRows=True
                            )
contents.append(table)
Datos_alistamiento=['', 'Sin carga', 'No','Neutro','Liberado','Tacos de caucho']
datos = (
                    ('','Nivel de combustible:' , Datos_alistamiento[0]),
                    ('Alistamiento', 'Condición de carga:' , Datos_alistamiento[1]),
                    ('previo', 'Bloqueo de suspensión (Si/No):',Datos_alistamiento[2]),
                    ('del vehículo', 'Posición de caja de cambios:',Datos_alistamiento[3]),
                    ('', 'Posición de freno de aparcamiento:',Datos_alistamiento[4]),
                    ('', 'Tipo de bloque de ruedas traseras\nen medición inclinada:',Datos_alistamiento[5]),
                    )
table = LongTable(data = datos,colWidths=(1*inch,3.5*inch,2.95*inch),
                    style = [
                            ('GRID',(1,0),(2,6),0.5,colors.grey),
                            ('GRID',(0,7),(0,6),0.5,colors.grey),
                            ],
                    hAlign='LEFT'
                    ,splitByRow=True
                    ,repeatRows=True
                            )
contents.append(table)
Datos_medidos=['', '', '','','','', '', '','','','','','']
datos = (
                    ('','Masas ruedas – Eje delantero:' , 'Derecha: '+ Datos_medidos[0] + ' kg'+ '/ Izquierda: '+ Datos_medidos[1] + ' kg'),
                    ('', 'Masas ruedas – Eje trasero:' ,'Derecha: '+ Datos_medidos[2] + ' kg' '/ Izquierda: '+ Datos_medidos[3] + ' kg'),
                    ('', 'Masa total:',Datos_medidos[4] + ' kg'),
                    ('Datos', 'Ancho de vía:','Delantero: '+ Datos_medidos[5]+' mm/ Trasero:'+ Datos_medidos[6]+' mm'),
                    ('medidos', 'Distancia entre centros:','Derecho: '+ Datos_medidos[7]+' mm/ Izquierdo: '+ Datos_medidos[8]+' mm'),
                    ('', 'Radio en carga estática – Eje delantero:','Derecha: '+ Datos_medidos[9]+' mm/ Izquierda: '+ Datos_medidos[10]+' mm'),
                    ('', 'Radio en carga estática – Eje trasero:','Derecha:  '+ Datos_medidos[11]+' mm/ Izquierda: '+ Datos_medidos[12]+' mm'),
                    )
table = LongTable(data = datos,colWidths=(1*inch,3.5*inch,2.95*inch),
                    style = [
                            ('GRID',(1,0),(2,6),0.5,colors.grey),
                            ('GRID',(0,7),(0,7),0.5,colors.grey),
                            ],
                    hAlign='LEFT'
                    ,splitByRow=True
                    ,repeatRows=True
                            )
contents.append(table)
Resultados_pruebas=['', '', '','','','', '', '','','','']
datos = (
                    ('','Xcg:' , Resultados_pruebas[0]+' mm\n(respecto a eje delantero del vehículo)'),
                    ('', 'Ycg:' ,Resultados_pruebas[1]+' mm\n(respecto a eje longitudinal del vehículo,\npositivo hacia la izquierda)'),
                    ('', 'Zcg, vehículo:',Resultados_pruebas[2]+' mm\n(respecto al suelo, positivo hacia arriba)'),
                    ('', 'Prueba de eje Delantero elevado',''),
                    ('Resultados', 'Ángulo de elevación:',Resultados_pruebas[3]+' °'),
                    ('de prueba', 'Masa en eje trasero\n(con vehículo inclinado):',Resultados_pruebas[4]+' kg'),
                    ('', 'Zcg, prueba eje delantero elevado:',Resultados_pruebas[5]+' mm'),
                    ('', 'Prueba de eje Trasero elevado (Opcional)',''),
                    ('', 'Ángulo de elevación:',Resultados_pruebas[6]+' °'),
                    ('', 'Masa en eje delantero (con vehículo inclinado):',Resultados_pruebas[7]+' kg'),
                    ('', 'Zcg, prueba eje trasero elevado:',Resultados_pruebas[8]+' mm'),
                    )
table = LongTable(data = datos,colWidths=(1*inch,3.5*inch,2.95*inch),
                    style = [
                            ('GRID',(1,0),(2,10),0.5,colors.grey),
                            ('GRID',(0,11),(0,11),0.5,colors.grey),
                            ],
                    hAlign='LEFT'
                    ,splitByRow=True
                    ,repeatRows=True
                            )
contents.append(table)
doc.addPageTemplates([firstpage, laterpages])
doc.build(contents)