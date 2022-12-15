from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, NextPageTemplate, Image, LongTable, Paragraph
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.styles import (ParagraphStyle, getSampleStyleSheet)
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.platypus import PageBreak
class Report_CDG:
        def foot2(self,pdf,doc):
                width,height = A4
                pdf.saveState()
                pdf.setFont('Times-Bold',28)
                pdf.drawCentredString(width/2.0, height-63, "REPORTE DE PRUEBA CDG")
                pdf.setFont('Times-Roman',9)
                pdf.setTitle("REPORTE DE PRUEBA CDG")
                pdf.setAuthor("Universidad del Valle")
                #pdf.drawString(width-1*inch, 0.1 * inch,'Página '+"%d" % doc.page+' de '+"%d" % 3)

        def get_doc(self, buffer, encargado, codigo, fecha, Datos_vehiculo, Datos_alistamiento, Datos_medidos, Resultados_pruebas):
                #print("Generando PDF")
                width,height = A4

                doc = BaseDocTemplate(buffer, showBoundary=1, pagesize= A4)
                contents =[]
                TopCenter = Frame(0.4*inch,height-1.2*inch,width-0.8*inch,0.8*inch,showBoundary=1,id='normal')
                frame1later = Frame(0.4*inch,0.6*inch,width-0.8*inch, height-2*inch,leftPadding=0,topPadding=0,showBoundary = 1,id='col1later')

                frame_params = Frame(0.4*inch,0.6*inch,width-0.8*inch, height-2*inch,leftPadding=0,topPadding=0, showBoundary = 1,id='col')

                firstpage = PageTemplate(id='firstpage',frames=[TopCenter,frame_params],onPage=self.foot2)

                laterpages = PageTemplate(id='laterpages',frames=[frame1later],onPage=self.foot2)

                contents.append(NextPageTemplate('laterpages'))

                archivo_imagen = 'icons/Univalle.png'
                logoleft = Image(archivo_imagen)
                logoleft._restrictSize(0.5*inch, 0.5*inch)

                logoleft.hAlign = 'LEFT'
                logoleft.vAlign = 'CENTER'

                contents.append(logoleft)
                datos = (
                                ('Código de prueba:', 'GCD'+codigo),
                                ('Encargado de la prueba:', encargado),
                                )
                table = LongTable(data = datos,colWidths=((1.0+3.5)*inch,2.95*inch),
                                style = [
                                        #('GRID',(1,0),(1,1),0.5,colors.grey),
                                        ('GRID',(0,0),(2,2),0.5,colors.grey),
                                        ('SPAN',(0,0),(0,1)),
                                        ('SPAN',(1,0),(1,1)),
                                        ('GRID',(0,2),(2,2),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,1), 'Helvetica-Bold'),
                                        #('GRID',(1,1),(2,1),0.5,colors.grey),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                contents.append(table)
                datos = (
                                ('Fecha y hora de elaboración de la prueba:', fecha[0]),
                                ('Fecha y hora de elaboración del reporte:', fecha[1]),
                                ('Fecha de calibración sensores:', fecha[2]),
                                )
                table = LongTable(data = datos,colWidths=((1.0+3.5)*inch,2.95*inch),
                                style = [
                                        #('GRID',(1,0),(1,1),0.5,colors.grey),
                                        ('GRID',(0,0),(2,2),0.5,colors.grey),
                                        #('SPAN',(0,0),(0,1)),
                                        #('SPAN',(1,0),(1,1)),
                                        ('GRID',(0,2),(2,2),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,2), 'Helvetica-Bold'),
                                        #('GRID',(1,1),(2,1),0.5,colors.grey),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                contents.append(table)
                datos = (
                                ('','Fabricante:' , Datos_vehiculo[0]),
                                ('Identificación', 'Modelo:' ,Datos_vehiculo[1]),
                                ('del vehículo', 'Tipo:',Datos_vehiculo[2]),
                                ("",'Tamaño llantas: ','Delantera: '+ Datos_vehiculo[3]+ ' Trasera: '+Datos_vehiculo[4]),
                                ("",'Presión llantas: ','Delantera: '+Datos_vehiculo[5] +' Trasera: '+Datos_vehiculo[6]),
                                )
                table = LongTable(data = datos,colWidths=(1.0*inch,3.5*inch,2.95*inch),
                                style = [
                                        ('GRID',(1,0),(2,4),0.5,colors.grey),
                                        ('GRID',(0,5),(0,5),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,5), 'Helvetica-Bold'),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                contents.append(table)
                
                datos = (
                                ('','Nivel de combustible:' , Datos_alistamiento[0]),
                                ('Alistamiento', 'Condición de carga:' , Datos_alistamiento[1]),
                                ('previo', 'Bloqueo de suspensión (Si/No):',Datos_alistamiento[2]),
                                ('del vehículo', 'Posición de caja de cambios:',Datos_alistamiento[3]),
                                ('', 'Posición de freno de aparcamiento:',Datos_alistamiento[4]),
                                ('', 'Tipo de bloqueo de ruedas traseras\nen medición inclinada:',Datos_alistamiento[5]),
                                )
                table = LongTable(data = datos,colWidths=(1*inch,3.5*inch,2.95*inch),
                                style = [
                                        ('GRID',(1,0),(2,6),0.5,colors.grey),
                                        ('GRID',(0,7),(0,6),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,7), 'Helvetica-Bold'),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                contents.append(table)
                
                datos = (
                                ('','Reacción eje delantero en (kg):' , 'Derecha: '+ Datos_medidos[0] + ' kg'+ '/ Izquierda: '+ Datos_medidos[1] + ' kg'),
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
                                        ('FONTNAME', (0,0), (0,7), 'Helvetica-Bold'),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                contents.append(table)
                
                datos = (
                                ('','Xcg:' , Resultados_pruebas[0]+' mm\n(respecto a eje delantero del vehículo,\npositivo hacia atrás)'),
                                ('','Ycg:' ,Resultados_pruebas[1]+' mm\n(respecto a eje longitudinal del vehículo,\npositivo hacia la izquierda)'),
                                ('','Zcg:',Resultados_pruebas[2]+' mm\n(respecto al suelo, positivo hacia arriba)'),
                                ('','Prueba de eje Delantero elevado',''),
                                ('Resultados', 'Ángulo máximo de elevación:',Resultados_pruebas[3]+' °'),
                                ('de prueba', 'Masa en eje trasero\n(con vehículo inclinado):',Resultados_pruebas[4]+' kg'),
                                ('','Zcg, prueba eje delantero elevado:',Resultados_pruebas[5]+' mm'),
                                ('','Prueba de eje Trasero elevado (Opcional)',''),
                                ('','Ángulo máximo de elevación:',Resultados_pruebas[6]+' °'),
                                ('','Masa en eje delantero (con vehículo inclinado):',Resultados_pruebas[7]+' kg'),
                                ('','Zcg, prueba eje trasero elevado:',Resultados_pruebas[8]+' mm'),
                                )
                table = LongTable(data = datos,colWidths=(1*inch,3.5*inch,2.95*inch),
                                style = [
                                        ('GRID',(1,0),(2,10),0.5,colors.grey),
                                        ('GRID',(0,11),(0,11),0.5,colors.grey),
                                        ('SPAN',(1,3),(2,3)),
                                        ('SPAN',(1,7),(2,7)),
                                        ('FONTNAME', (0,0), (0,11), 'Helvetica-Bold'),
                                        ('FONTNAME', (1,3), (2,3), 'Helvetica-Bold'),
                                        ('FONTNAME', (1,7), (2,7), 'Helvetica-Bold'),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                contents.append(table)
                doc.addPageTemplates([firstpage, laterpages])
                doc.build(contents)

class Report_rigidez:
        def foot2(self,pdf,doc):
                width,height = A4
                pdf.saveState()
                pdf.setTitle("REPORTE DE PRUEBA DE RIGIDEZ")
                pdf.setAuthor("Universidad del Valle")
                pdf.setFont('Helvetica-Bold',24)
                pdf.drawCentredString(width/2.0, height-63, "REPORTE DE PRUEBA DE RIGIDEZ")
                pdf.setFont('Times-Roman',9)
                #pdf.drawString(width-1*inch, 0.1 * inch,'Página '+"%d" % doc.page+' de '+"%d" % 3)

        def get_doc(self, buffer, encargado, codigo, fecha, Datos_vehiculo, Datos_rigidez, Dato_rigidezTotal, data_graph, Datos_rigidezT, Dato_rigidezTTotal , data_graphT):
                width,height = A4

                doc = BaseDocTemplate(buffer, showBoundary=1, pagesize= A4)
                contents =[]
                TopCenter = Frame(0.4*inch,height-1.2*inch,width-0.8*inch,0.8*inch,showBoundary=1,id='normal')
                frame1later = Frame(0.4*inch,0.6*inch,width-0.8*inch, height-2*inch,leftPadding=0,topPadding=0,showBoundary = 1,id='col1later')

                frame_params = Frame(0.4*inch,0.6*inch,width-0.8*inch, height-2*inch,leftPadding=0,topPadding=0, showBoundary = 1,id='col')

                firstpage = PageTemplate(id='firstpage',frames=[TopCenter,frame_params],onPage=self.foot2)

                laterpages = PageTemplate(id='laterpages',frames=[TopCenter,frame1later],onPage=self.foot2)

                contents.append(NextPageTemplate('laterpages'))

                archivo_imagen = 'icons/Univalle.png'
                logoleft = Image(archivo_imagen)
                logoleft._restrictSize(0.5*inch, 0.5*inch)

                logoleft.hAlign = 'LEFT'
                logoleft.vAlign = 'CENTER'
                
                contents.append(logoleft)                
                
                datos = (
                                ('Código de prueba:', codigo),
                                ('Encargado de la prueba:', encargado),
                                )
                table = LongTable(data = datos,colWidths=((1.0+3.5)*inch,2.95*inch),
                                style = [
                                        #('GRID',(1,0),(1,1),0.5,colors.grey),
                                        ('GRID',(0,0),(2,2),0.5,colors.grey),
                                        ('SPAN',(0,0),(0,1)),
                                        ('SPAN',(1,0),(1,1)),
                                        ('GRID',(0,2),(2,2),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,1), 'Helvetica-Bold'),
                                        #('GRID',(1,1),(2,1),0.5,colors.grey),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                contents.append(table)
                datos = (
                                ('Fecha y hora de elaboración de la prueba:', fecha[0]),
                                ('Fecha y hora de elaboración del reporte:', fecha[1]),
                                ('Fecha de calibración sensores:', fecha[2]),
                                )
                table = LongTable(data = datos,colWidths=((1.0+3.5)*inch,2.95*inch),
                                style = [
                                        #('GRID',(1,0),(1,1),0.5,colors.grey),
                                        ('GRID',(0,0),(2,2),0.5,colors.grey),
                                        #('SPAN',(0,0),(0,1)),
                                        #('SPAN',(1,0),(1,1)),
                                        ('GRID',(0,2),(2,2),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,2), 'Helvetica-Bold'),
                                        #('GRID',(1,1),(2,1),0.5,colors.grey),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                contents.append(table)
                datos = (
                                ('','Fabricante:' , Datos_vehiculo[0]),
                                ('Identificación', 'Modelo:' ,Datos_vehiculo[1]),
                                ('del vehículo', 'Tipo:',Datos_vehiculo[2]),
                                )
                table = LongTable(data = datos,colWidths=(1.0*inch,3.5*inch,2.95*inch),
                                style = [
                                        ('GRID',(1,0),(2,2),0.5,colors.grey),
                                        ('GRID',(0,3),(0,3),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,3), 'Helvetica-Bold'),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                contents.append(table)
                style = getSampleStyleSheet()
                style_title = ParagraphStyle('Titulos',
                           fontName="Helvetica-Bold",
                           fontSize=16,
                           parent=style['Heading2'],
                           alignment=1,
                           spaceAfter=14)

                """style_table = ParagraphStyle('Titulos',
                           fontName="Helvetica-Bold",
                           #fontSize=16,
                           parent=style['Heading2'],
                           alignment=1,
                           #spaceAfter=14
                           )"""
                Title=Paragraph("Rigidez a torsión", style_title)
                contents.append(Title)
                datos = (
                                ('Parámetro o característica' , 'Registro'),
                                ('Estructura de chasis / carrocería del vehículo evaluado' , Datos_rigidez[0]),
                                ('Posición del LVDT (mm)',Datos_rigidez[1]),
                                ('Posición de aplicación de la carga (mm)',Datos_rigidez[2]),
                                )
                table = LongTable(data = datos,colWidths=(4*inch,3.45*inch),
                                style = [
                                        ('GRID',(0,0),(1,3),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (2,0), 'Helvetica-Bold'),
                                        ('ALIGN', (1, 1), (1, 1), "CENTER"), 
                                        ('VALIGN', (0, 1), (1, 1), "MIDDLE"),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                contents.append(table)
                """Title=Paragraph("Registro de deflexión h<sub>n</sub> (mm) y de ángulo de torsión &theta <sub>n</sub> (grad) para cada nivel de carga", style_title)
                contents.append(Title)
                datos = (
                                ('i' ,Paragraph('P<sub>n</sub>\n(kg)',style_table), Paragraph('M<sub>T</sub><sub>n</sub>\n(N-m)',style_table),Paragraph('h<sub>n</sub>\n(mm)',style_table),Paragraph('&theta<sub>n</sub>\n(mm)',style_table)),
                                ('1',str(Dato_peso[0]),str(Dato_m[0]),str(Dato_desplazamiento[0]),str(Dato_angulo[0])),
                                ('2',str(Dato_peso[1]),str(Dato_m[1]),str(Dato_desplazamiento[1]),str(Dato_angulo[1])),
                                ('3',str(Dato_peso[2]),str(Dato_m[2]),str(Dato_desplazamiento[2]),str(Dato_angulo[2])),
                                ('4',str(Dato_peso[3]),str(Dato_m[3]),str(Dato_desplazamiento[3]),str(Dato_angulo[3])),
                                ('5',str(Dato_peso[4]),str(Dato_m[4]),str(Dato_desplazamiento[4]),str(Dato_angulo[4])),
                                ('6',str(Dato_peso[5]),str(Dato_m[5]),str(Dato_desplazamiento[5]),str(Dato_angulo[5])),
                                ('7',str(Dato_peso[6]),str(Dato_m[6]),str(Dato_desplazamiento[6]),str(Dato_angulo[6])),
                                ('8',str(Dato_peso[7]),str(Dato_m[7]),str(Dato_desplazamiento[7]),str(Dato_angulo[7])),
                                )
                table = LongTable(data = datos,
                                style = [
                                        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (3,0), 'Helvetica-Bold'),
                                        ('ALIGN', (0, 0), (-1, -1), "CENTER"),
                                        ],
                                hAlign='CENTER'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                contents.append(table)"""
                #contents.append(PageBreak())
                Title=Paragraph("Gráfica de momento de torsor máximo M<sub>T</sub><sub>n</sub> (N-m) vs ángulo de deflexión &theta <sub>n</sub>", style_title)
                contents.append(Title)
                
                drawing = Drawing(400, 200)
                lp = LinePlot()
                lp.x = 50
                lp.y = 50
                lp.height = 125
                lp.width = 450
                lp.data = data_graph
                lp.joinedLines = 1
                lp.lines[0].symbol = makeMarker('FilledCircle')
                lp.lines[1].symbol = makeMarker('Circle')
                lp.lineLabelFormat = '%2.0f'
                lp.strokeColor = colors.black
                """lp.xValueAxis.valueMin = 0
                lp.xValueAxis.valueMax = 5
                lp.xValueAxis.valueSteps = [1, 2, 2.5, 3, 4, 5]
                lp.xValueAxis.labelTextFormat = '%2.1f'
                lp.yValueAxis.valueMin = 0
                lp.yValueAxis.valueMax = 7
                lp.yValueAxis.valueSteps = [1, 2, 3, 5, 6]"""
                drawing.add(lp)
                contents.append(drawing)
                #contents.append(PageBreak())
                datos = (
                                ('Rigidez torsional experimental (N-mm)' , Dato_rigidezTotal[0]),
                                ('¿Está la rigidez torsional dentro de los límites permisibles?' , Dato_rigidezTotal[1]),
                                
                        )
                table = LongTable(data = datos,colWidths=(4*inch,3.45*inch),
                                style = [
                                        ('GRID',(0,0),(1,3),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,1), 'Helvetica-Bold'),
                                        ('ALIGN', (1, 0), (1, 1), "CENTER"), 
                                        ('VALIGN', (1, 0), (1, 1), "MIDDLE"),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                if (Dato_rigidezTotal[1]=='Sobredimensionado'):
                        table.setStyle(([
                                        ('GRID',(0,0),(1,3),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,1), 'Helvetica-Bold'),
                                        ('BACKGROUND', (0,1),(1,1),colors.orange),
                                        ('ALIGN', (1, 0), (1, 1), "CENTER"), 
                                        ('VALIGN', (1, 0), (1, 1), "MIDDLE"),
                                        ]))
                elif (Dato_rigidezTotal[1]=='Si'):
                        table.setStyle(([
                                        ('GRID',(0,0),(1,3),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,1), 'Helvetica-Bold'),
                                        ('BACKGROUND', (0,1),(1,1),colors.green),
                                        ('ALIGN', (1, 0), (1, 1), "CENTER"), 
                                        ('VALIGN', (1, 0), (1, 1), "MIDDLE"),
                                        ]))
                elif (Dato_rigidezTotal[1]=='No'):
                        table.setStyle(([
                                        ('GRID',(0,0),(1,3),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,1), 'Helvetica-Bold'),
                                        ('BACKGROUND', (0,1),(1,1),colors.red),
                                        ('ALIGN', (1, 0), (1, 1), "CENTER"), 
                                        ('VALIGN', (1, 0), (1, 1), "MIDDLE"),
                                        ]))
                
                contents.append(table)
                Title=Paragraph("", style_title)
                contents.append(Title)
                Title=Paragraph("", style_title)
                contents.append(Title)
                Title=Paragraph("", style_title)
                contents.append(Title)
                Title=Paragraph("", style_title)
                contents.append(Title)
                Title=Paragraph("Rigidez a flexión", style_title)
                contents.append(Title)
                datos = (
                                ('Parámetro o característica' , 'Registro'),
                                ('Estructura de chasis / carrocería del vehículo evaluado' , Datos_rigidezT[0]),
                                ('Posición del LVDT (mm)',Datos_rigidezT[1]),
                                ('Posición de aplicación de la carga (mm)',Datos_rigidezT[2]),
                                )
                table = LongTable(data = datos,colWidths=(4*inch,3.45*inch),
                                style = [
                                        ('GRID',(0,0),(1,3),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (2,0), 'Helvetica-Bold'),
                                        ('ALIGN', (1, 1), (1, 1), "CENTER"), 
                                        ('VALIGN', (0, 1), (1, 1), "MIDDLE"),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                contents.append(table)
                """Title=Paragraph("Registro de deflexión h<sub>n</sub> (mm) y de ángulo de torsión &theta <sub>n</sub> (grad) para cada nivel de carga", style_title)
                contents.append(Title)
                datos = (
                                ('i' ,Paragraph('P<sub>n</sub>\n(kg)',style_table), Paragraph('M<sub>T</sub><sub>n</sub>\n(N-m)',style_table),Paragraph('h<sub>n</sub>\n(mm)',style_table),Paragraph('&theta<sub>n</sub>\n(mm)',style_table)),
                                ('1',str(Dato_peso[0]),str(Dato_m[0]),str(Dato_desplazamiento[0]),str(Dato_angulo[0])),
                                ('2',str(Dato_peso[1]),str(Dato_m[1]),str(Dato_desplazamiento[1]),str(Dato_angulo[1])),
                                ('3',str(Dato_peso[2]),str(Dato_m[2]),str(Dato_desplazamiento[2]),str(Dato_angulo[2])),
                                ('4',str(Dato_peso[3]),str(Dato_m[3]),str(Dato_desplazamiento[3]),str(Dato_angulo[3])),
                                ('5',str(Dato_peso[4]),str(Dato_m[4]),str(Dato_desplazamiento[4]),str(Dato_angulo[4])),
                                ('6',str(Dato_peso[5]),str(Dato_m[5]),str(Dato_desplazamiento[5]),str(Dato_angulo[5])),
                                ('7',str(Dato_peso[6]),str(Dato_m[6]),str(Dato_desplazamiento[6]),str(Dato_angulo[6])),
                                ('8',str(Dato_peso[7]),str(Dato_m[7]),str(Dato_desplazamiento[7]),str(Dato_angulo[7])),
                                )
                table = LongTable(data = datos,
                                style = [
                                        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (3,0), 'Helvetica-Bold'),
                                        ('ALIGN', (0, 0), (-1, -1), "CENTER"),
                                        ],
                                hAlign='CENTER'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                contents.append(table)"""
                #contents.append(PageBreak())
                Title=Paragraph("Gráfica de momento de flector máximo M<sub>T</sub><sub>n</sub> (N-m) vs ángulo de deflexión &theta <sub>n</sub>", style_title)
                contents.append(Title)
                
                drawing = Drawing(400, 200)
                lp = LinePlot()
                lp.x = 50
                lp.y = 50
                lp.height = 125
                lp.width = 450
                lp.data = data_graphT
                lp.joinedLines = 1
                lp.lines[0].symbol = makeMarker('FilledCircle')
                lp.lines[1].symbol = makeMarker('Circle')
                lp.lineLabelFormat = '%2.0f'
                lp.strokeColor = colors.black
                """lp.xValueAxis.valueMin = 0
                lp.xValueAxis.valueMax = 5
                lp.xValueAxis.valueSteps = [1, 2, 2.5, 3, 4, 5]
                lp.xValueAxis.labelTextFormat = '%2.1f'
                lp.yValueAxis.valueMin = 0
                lp.yValueAxis.valueMax = 7
                lp.yValueAxis.valueSteps = [1, 2, 3, 5, 6]"""
                drawing.add(lp)
                contents.append(drawing)
                #contents.append(PageBreak())
                datos = (
                                ('Rigidez flectora experimental (N-mm)' , Dato_rigidezTTotal[0]),
                                ('¿Está la rigidez flectora dentro de los límites permisibles?' , Dato_rigidezTTotal[1]),
                                
                        )
                table = LongTable(data = datos,colWidths=(4*inch,3.45*inch),
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                if (Dato_rigidezTTotal[1]=='Sobredimensionado'):
                        table.setStyle(([
                                        ('GRID',(0,0),(1,3),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,1), 'Helvetica-Bold'),
                                        ('BACKGROUND', (0,1),(1,1),colors.orange),
                                        ('ALIGN', (1, 0), (1, 1), "CENTER"), 
                                        ('VALIGN', (1, 0), (1, 1), "MIDDLE"),
                                        ]))
                elif (Dato_rigidezTTotal[1]=='Cumple'):
                        table.setStyle(([
                                        ('GRID',(0,0),(1,3),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,1), 'Helvetica-Bold'),
                                        ('BACKGROUND', (0,1),(1,1),colors.green),
                                        ('ALIGN', (1, 0), (1, 1), "CENTER"), 
                                        ('VALIGN', (1, 0), (1, 1), "MIDDLE"),
                                        ]))
                elif (Dato_rigidezTTotal[1]=='No cumple'):
                        table.setStyle(([
                                        ('GRID',(0,0),(1,3),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,1), 'Helvetica-Bold'),
                                        ('BACKGROUND', (0,1),(1,1),colors.red),
                                        ('ALIGN', (1, 0), (1, 1), "CENTER"), 
                                        ('VALIGN', (1, 0), (1, 1), "MIDDLE"),
                                        ]))
                        
                contents.append(table)
                
                doc.addPageTemplates([firstpage, laterpages])
                doc.build(contents)

class Report_confort:
        def foot2(self,pdf,doc):
                width,height = A4
                pdf.saveState()
                pdf.setFont('Times-Bold',22)
                pdf.drawCentredString(width/2.0, height-63, "REPORTE DE PRUEBA DE CONFORT")
                pdf.setFont('Times-Roman',9)
                pdf.setTitle("REPORTE DE PRUEBA DE CONFORT")
                pdf.setAuthor("Universidad del Valle")
                #pdf.drawString(width-1*inch, 0.1 * inch,'Página '+"%d" % doc.page+' de '+"%d" % 3)

        def get_doc(self, buffer, encargado, codigo, fecha, Datos_vehiculo, Datos_via, Datos_resultados):
                #print("Generando PDF")
                width,height = A4

                doc = BaseDocTemplate(buffer, showBoundary=1, pagesize= A4)
                contents =[]
                TopCenter = Frame(0.4*inch,height-1.2*inch,width-0.8*inch,0.8*inch,showBoundary=1,id='normal')
                frame1later = Frame(0.4*inch,0.6*inch,width-0.8*inch, height-2*inch,leftPadding=0,topPadding=0,showBoundary = 1,id='col1later')

                frame_params = Frame(0.4*inch,0.6*inch,width-0.8*inch, height-2*inch,leftPadding=0,topPadding=0, showBoundary = 1,id='col')

                firstpage = PageTemplate(id='firstpage',frames=[TopCenter,frame_params],onPage=self.foot2)

                laterpages = PageTemplate(id='laterpages',frames=[TopCenter,frame1later],onPage=self.foot2)

                contents.append(NextPageTemplate('laterpages'))

                archivo_imagen = 'icons/Univalle.png'
                logoleft = Image(archivo_imagen)
                logoleft._restrictSize(0.5*inch, 0.5*inch)

                logoleft.hAlign = 'LEFT'
                logoleft.vAlign = 'CENTER'

                contents.append(logoleft)
                datos = (       ('','Código de prueba:', codigo),
                                ('Equipo','Encargado de la prueba:', encargado[0]),
                                ('de','Conductor:',encargado[1]),
                                ('pruebas','Observador:',encargado[2]),
                                )
                table = LongTable(data = datos,colWidths=(1.0*inch,3.5*inch,2.95*inch),
                                style = [
                                        #('GRID',(1,0),(1,1),0.5,colors.grey),
                                        ('GRID',(1,0),(2,3),0.5,colors.grey),
                                        #('GRID',(0,3),(2,3),0.5,colors.grey),
                                        #('SPAN',(0,0),(0,2)),
                                        #('SPAN',(1,0),(1,1)),
                                        #('GRID',(0,2),(2,2),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,3), 'Helvetica-Bold'),
                                        #('GRID',(1,1),(2,1),0.5,colors.grey),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                contents.append(table)
                
                datos = (       
                                ('Equipo','Encargado de la prueba:', encargado[0]),
                                ('de','Conductor:',encargado[1]),
                                ('pruebas','Observador:',encargado[2]),
                                )
                table = LongTable(data = datos,colWidths=(1.0*inch,3.5*inch,2.95*inch),
                                style = [
                                        #('GRID',(1,0),(1,1),0.5,colors.grey),
                                        ('GRID',(1,0),(2,2),0.5,colors.grey),
                                        ('GRID',(0,3),(2,3),0.5,colors.grey),
                                        #('SPAN',(0,0),(0,2)),
                                        #('SPAN',(1,0),(1,1)),
                                        #('GRID',(0,2),(2,2),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,2), 'Helvetica-Bold'),
                                        #('GRID',(1,1),(2,1),0.5,colors.grey),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                datos = (
                                ('Fecha y hora de elaboración de la prueba:', fecha[0]),
                                ('Fecha y hora de elaboración del reporte:', fecha[1]),
                                ('Fecha de calibración sensores:', fecha[2]),
                                )
                table = LongTable(data = datos,colWidths=((1.0+3.5)*inch,2.95*inch),
                                style = [
                                        #('GRID',(1,0),(1,1),0.5,colors.grey),
                                        ('GRID',(0,0),(2,2),0.5,colors.grey),
                                        #('SPAN',(0,0),(0,1)),
                                        #('SPAN',(1,0),(1,1)),
                                        ('GRID',(0,2),(2,2),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,2), 'Helvetica-Bold'),
                                        #('GRID',(1,1),(2,1),0.5,colors.grey),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                contents.append(table)
                datos = (
                                ('Identificación','Fabricante:' , Datos_vehiculo[0]),
                                ('', 'Modelo:' ,Datos_vehiculo[1]),
                                ('del vehículo', 'Tipo:',Datos_vehiculo[2]),
                                )
                table = LongTable(data = datos,colWidths=(1.0*inch,3.5*inch,2.95*inch),
                                style = [
                                        ('GRID',(1,0),(2,4),0.5,colors.grey),
                                        ('GRID',(0,3),(0,3),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,3), 'Helvetica-Bold'),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                contents.append(table)
                
                datos = (
                                ('Condición', 'Zona de pruebas, pista o espacio de\npruebas (Dirección y/o nombre):', Datos_via[0]),
                                ('del', 'Distancia de la trayectoria utilizada\npara las pruebas (km):', Datos_via[1]),
                                ('entorno','Tipo de Vía:', Datos_via[2]),
                                )
                table = LongTable(data = datos,colWidths=(1.0*inch,3.5*inch,2.95*inch),
                                style = [
                                        ('GRID',(1,0),(2,4),0.5,colors.grey),
                                        ('GRID',(0,3),(0,3),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,3), 'Helvetica-Bold'),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                contents.append(table)
                
                datos = (
                                ('Resultados', 'Tiempo de duración (hh:mm):', Datos_resultados[0]),
                                ('de', 'Exposición diaria A(8) (m/s^2):', str(Datos_resultados[1])),
                                ('prueba','Valor de dosis de vibración VDV (m/s^1.7):', str(Datos_resultados[2])),
                                ('vibraciones','Exposición a vibraciones:', Datos_resultados[3]),
                                )
                table = LongTable(data = datos,colWidths=(1.0*inch,3.5*inch,2.95*inch),
                                style = [
                                        ('GRID',(1,0),(2,4),0.5,colors.grey),
                                        ('GRID',(0,4),(0,4),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,4), 'Helvetica-Bold'),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                if (Datos_resultados[3]=='Niveles de vibración dentro de limites seguros.'):
                        table.setStyle(([
                                        ('BACKGROUND', (1,3),(2,3),colors.green),
                                        ]))
                elif (Datos_resultados[3]=='Niveles de vibración fuera de limites seguros.'):
                        table.setStyle(([
                                        ('BACKGROUND', (1,3),(2,3),colors.orange),
                                        ]))
                elif (Datos_resultados[3]=='Se corren riesgos de salud.'):
                        table.setStyle(([
                                        ('BACKGROUND', (1,3),(2,3),colors.red),
                                        ]))
                contents.append(table)

                datos = (
                                ('Resultados\nde', 'Aceleración eficaz ponderada en\nfrecuencia total (m/s^2):', Datos_resultados[4]),
                                ('prueba\nconfort', 'Grado de confort:', Datos_resultados[5]),
                                )
                table = LongTable(data = datos,colWidths=(1.0*inch,3.5*inch,2.95*inch),
                                style = [
                                        ('GRID',(1,0),(2,4),0.5,colors.grey),
                                        ('GRID',(0,4),(0,4),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,4), 'Helvetica-Bold'),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                if (Datos_resultados[5]=='No incómodo'):
                        table.setStyle(([
                                        ('BACKGROUND', (1,1),(2,1),colors.green),
                                        ]))
                elif (Datos_resultados[5]=='Muy poco incómodo'):
                        table.setStyle(([
                                        ('BACKGROUND', (1,1),(2,1),colors.lightgreen),
                                        ]))
                elif (Datos_resultados[5]=='Algo incómodo'):
                        table.setStyle(([
                                        ('BACKGROUND', (1,1),(2,1),colors.orange),
                                        ]))
                elif (Datos_resultados[5]=='Incómodo'):
                        table.setStyle(([
                                        ('BACKGROUND', (1,1),(2,1),colors.orange),
                                        ]))
                elif (Datos_resultados[5]=='Muy incómodo'):
                        table.setStyle(([
                                        ('BACKGROUND', (1,1),(2,1),colors.red),
                                        ]))
                elif (Datos_resultados[5]=='Extremadamente incómodo'):
                        table.setStyle(([
                                        ('BACKGROUND', (1,1),(2,1),colors.red),
                                        ]))
                contents.append(table)
                doc.addPageTemplates([firstpage, laterpages])
                doc.build(contents)

"""Reporte de estabilidad: Aparte de las variables comunes que tienen todas las pruebas, se necesitan reportar las
los datos correspondientes a la prueba las cuales son:
-datos_espacio[ubicacion, radio de curvatura (mm)]
-datos_calazada[tipo de calzada, temperatura de calzada (°C), coeficiente de fricción pico Calzada-llanta]
-Llantas fecha de manufactura[0], Llantas profundida[1], Llantas presion[2]=Datos_vehiculo_est[0..2]
-Condiciones de conduccion transmision manual[3], transmision automatica[4], Modo electrico/hibrido [5],
Estado de carga inicio prueba [6], Sistema de segurida activos [7]=Datos_vehiculo_est[3..7]
-Propulsion tipo [8], Eje propulsor[9], caracteristicas especiales [10]=Datos_vehiculo_est[8..10]
-motor combustion interna tipo[11], control mezcla aire-combustible[12], sistema turbo cargador[13], 
cilindrada[14], numero de cilindros[15], potencia maxima (hp)[16], torque maximo[17]= Datos_vehiculo_est[11..17]
-transmision tipo[18], numero de marchas [19]= Datos_vehiculo_est[18..19]
-Eje trasero tipo[20], suspencion amortiguadro[21], barra estabilizadora[22], sistemas activos[23]= Datos_vehiculo_est[20..23]
-Eje delantero tipo[24], suspencion amortiguadro[25], barra estabilizadora[26], sistemas activos[27]= Datos_vehiculo_est[24..27]
-Dirección eje dirigido[28], direccion delantera activa[29], dirección trasera activa[30], direccion asistida[31], 
tipo de asistencia[32], overall steering delantero[33], diametro voltante[34]=Datos_vehiculo_est[28..34]
-sistema de frenos asistido[35], control de estabilidad[36], tipo control[37], frenos eje delantero[38], frenos eje trasero[39]=Datos_vehiculo_est[35..39]
-tamaño rin delantero [40], tamaño rin trasero [41]=Datos_vehiculo_est[40..41]
-llantas tamaño delantero [42], tamaño trasero [43], profundidad labrado delantero [44], profundidad labrado trasero (mm)[45]
presion llantas delantero vacio[46], presion llantas trasero vacio[47],presion llantas delantero peso bruto[48], 
presion llantas peso bruto[49] =Datos_vehiculo_est[42..49]
"""
class Report_estabilidad:
        def foot2(self,pdf,doc):
                width,height = A4
                pdf.saveState()
                pdf.setFont('Times-Bold',22)
                pdf.drawCentredString(width/2.0, height-63, "REPORTE DE PRUEBA DE ESTABILIDAD")
                pdf.setFont('Times-Roman',9)
                pdf.setTitle("REPORTE DE PRUEBA DE ESTABILIDAD")
                pdf.setAuthor("Universidad del Valle")
                #pdf.drawString(width-1*inch, 0.1 * inch,'Página '+"%d" % doc.page+' de '+"%d" % 3)

        def get_doc(self, buffer, encargado, codigo, fecha, Datos_vehiculo, datos_espacio, Datos_vehiculo_est, datos_calazada, datos_clima, datos_llantas, datos_conduccion, SSF, datos_ISO4138, data_graph_volante, data_graph_volcamiento, datos_ISO4138i, data_graph_volantei, data_graph_volcamientoi):
                #print("Generando PDF")
                width,height = A4

                doc = BaseDocTemplate(buffer, showBoundary=1, pagesize= A4)
                contents =[]
                TopCenter = Frame(0.4*inch,height-1.2*inch,width-0.8*inch,0.8*inch,showBoundary=1,id='normal')
                frame1later = Frame(0.4*inch,0.6*inch,width-0.8*inch, height-2*inch,leftPadding=0,topPadding=0,showBoundary = 1,id='col1later')

                frame_params = Frame(0.4*inch,0.6*inch,width-0.8*inch, height-2*inch,leftPadding=0,topPadding=0, showBoundary = 1,id='col')

                firstpage = PageTemplate(id='firstpage',frames=[TopCenter,frame_params],onPage=self.foot2)

                laterpages = PageTemplate(id='laterpages',frames=[frame1later],onPage=self.foot2)

                contents.append(NextPageTemplate('laterpages'))

                archivo_imagen = 'icons/Univalle.png'
                logoleft = Image(archivo_imagen)
                logoleft._restrictSize(0.5*inch, 0.5*inch)

                logoleft.hAlign = 'LEFT'
                logoleft.vAlign = 'CENTER'

                contents.append(logoleft)
                datos = (       ('','Código de prueba:', codigo),
                                ('Equipo','Encargado de la prueba:', encargado[0]),
                                ('de','Conductor:',encargado[1]),
                                ('pruebas','Observador:',encargado[2]),
                                )
                table = LongTable(data = datos,colWidths=(1.0*inch,3.5*inch,2.95*inch),
                                style = [
                                        #('GRID',(1,0),(1,1),0.5,colors.grey),
                                        ('GRID',(1,0),(2,3),0.5,colors.grey),
                                        #('GRID',(0,3),(2,3),0.5,colors.grey),
                                        #('SPAN',(0,0),(0,2)),
                                        #('SPAN',(1,0),(1,1)),
                                        #('GRID',(0,2),(2,2),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,3), 'Helvetica-Bold'),
                                        #('GRID',(1,1),(2,1),0.5,colors.grey),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                contents.append(table)
                
                datos = (       
                                ('Equipo','Encargado de la prueba:', encargado[0]),
                                ('de','Conductor:',encargado[1]),
                                ('pruebas','Observador:',encargado[2]),
                                )
                table = LongTable(data = datos,colWidths=(1.0*inch,3.5*inch,2.95*inch),
                                style = [
                                        #('GRID',(1,0),(1,1),0.5,colors.grey),
                                        ('GRID',(1,0),(2,2),0.5,colors.grey),
                                        ('GRID',(0,3),(2,3),0.5,colors.grey),
                                        #('SPAN',(0,0),(0,2)),
                                        #('SPAN',(1,0),(1,1)),
                                        #('GRID',(0,2),(2,2),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,2), 'Helvetica-Bold'),
                                        #('GRID',(1,1),(2,1),0.5,colors.grey),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                datos = (
                                ('Fecha y hora de elaboración de la prueba:', fecha[0]),
                                ('Fecha y hora de elaboración del reporte:', fecha[1]),
                                ('Fecha de calibración sensores:', fecha[2]),
                                )
                table = LongTable(data = datos,colWidths=((1.0+3.5)*inch,2.95*inch),
                                style = [
                                        #('GRID',(1,0),(1,1),0.5,colors.grey),
                                        ('GRID',(0,0),(2,2),0.5,colors.grey),
                                        #('SPAN',(0,0),(0,1)),
                                        #('SPAN',(1,0),(1,1)),
                                        ('GRID',(0,2),(2,2),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,2), 'Helvetica-Bold'),
                                        #('GRID',(1,1),(2,1),0.5,colors.grey),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                contents.append(table)
                datos = (
                                ('Identificación','Fabricante:' , Datos_vehiculo[0]),
                                ('', 'Modelo:' ,Datos_vehiculo[1]),
                                ('del vehículo', 'Tipo:',Datos_vehiculo[2]),
                                )
                table = LongTable(data = datos,colWidths=(1.0*inch,3.5*inch,2.95*inch),
                                style = [
                                        ('GRID',(1,0),(2,4),0.5,colors.grey),
                                        ('GRID',(0,3),(0,3),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,3), 'Helvetica-Bold'),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                contents.append(table)
                datos = (
                                ('Espacio' , 'Ubicación:',datos_espacio[0]),
                                ('de pruebas', 'Radio de curvatura (mm):' ,datos_espacio[1]),
                                )
                table = LongTable(data = datos,colWidths=(1.0*inch,3.5*inch,2.95*inch),
                                style = [
                                        ('GRID',(1,0),(2,1),0.5,colors.grey),
                                        ('GRID',(0,2),(0,2),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,2), 'Helvetica-Bold'),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                contents.append(table)
                datos = (
                                ('Condiciones','Tipo calzada:' , datos_calazada[0]),
                                ('ambiente', 'Temperatura calzada (°C):' ,datos_calazada[1]),
                                ('(Superficie)', 'Coeficiente de fricción pico Calzada-Llanta:',datos_calazada[2]),
                                )
                table = LongTable(data = datos,colWidths=(1.0*inch,3.5*inch,2.95*inch),
                                style = [
                                        ('GRID',(1,0),(2,3),0.5,colors.grey),
                                        ('GRID',(0,4),(0,4),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,3), 'Helvetica-Bold'),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                contents.append(table)
                datos = (
                                ('','Temperatura del aire (°C):' , datos_clima[0]),
                                ('Condiciones', 'Humedad relativa (%):' ,datos_clima[1]),
                                ('ambiente', 'Velocidad del viento (m/s):',datos_clima[2]),
                                ('(Clima)','Dirección del viento:' , datos_clima[3]),
                                )
                table = LongTable(data = datos,colWidths=(1.0*inch,3.5*inch,2.95*inch),
                                style = [
                                        ('GRID',(1,0),(2,3),0.5,colors.grey),
                                        ('GRID',(0,4),(0,4),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,3), 'Helvetica-Bold'),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                contents.append(table)
                datos = (
                                ('','Transmisión manual\n(El # de marcha más alto posible engranado):' , datos_conduccion[0]),
                                ('Condiciones', 'Transmisión automática (Posición D, Drive):' ,datos_conduccion[1]),
                                ('de', 'Modo eléctrico/híbrido:',datos_conduccion[2]),
                                ('conducción', 'Estado de carga al inicio de la prueba (Si aplica):' , datos_conduccion[3]),
                                ('', 'Sistemas de seguridad activos (si aplica):' ,datos_conduccion[4]),
                                )
                table = LongTable(data = datos,colWidths=(1.0*inch,3.5*inch,2.95*inch),
                                style = [
                                        ('GRID',(1,0),(2,4),0.5,colors.grey),
                                        ('GRID',(0,5),(0,5),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,4), 'Helvetica-Bold'),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                contents.append(table)
                
                datos = (
                                ('','Tipo (Combustión/Eléctrico/Híbrido):' , Datos_vehiculo_est[0]),
                                ('Propulsión', 'Eje propulsor (Delantero/Trasero):' ,Datos_vehiculo_est[1]),
                                ('', 'Características especiales (Ej. Frenado regenerativo):',Datos_vehiculo_est[2]),
                                )
                table = LongTable(data = datos,colWidths=(1.0*inch,3.5*inch,2.95*inch),
                                style = [
                                        ('GRID',(1,0),(2,4),0.5,colors.grey),
                                        ('GRID',(0,3),(0,3),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,3), 'Helvetica-Bold'),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                contents.append(table)
                datos = (
                                ('','Tipo (Encendido por chispa/Diesel):' , Datos_vehiculo_est[3]),
                                ('', 'Control de mezcla aire-combustible\n(Carburador/Inyección):' ,Datos_vehiculo_est[4]),
                                ('Motor', 'Sistema turbo cargador\n(Ninguno/Turbo-cargado/Super-cargado):',Datos_vehiculo_est[5]),
                                ('de','Cilindrada (cm3):' , Datos_vehiculo_est[6]),
                                ('combustión', 'Número de cilindros:' ,Datos_vehiculo_est[7]),
                                ('interna', 'Potencia máxima (Hp) / rpm del motor:',Datos_vehiculo_est[8]),
                                ('', 'Torque máximo (Hp) / rpm del motor:',Datos_vehiculo_est[9]),
                                )
                table = LongTable(data = datos,colWidths=(1.0*inch,3.5*inch,2.95*inch),
                                style = [
                                        ('GRID',(1,0),(2,6),0.5,colors.grey),
                                        ('GRID',(0,7),(0,7),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,6), 'Helvetica-Bold'),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                        )
                contents.append(table)
                datos = (
                                ('Transmisión','Tipo (Manual / Automática):' , Datos_vehiculo_est[10]),
                                ('', 'Número de velocidades o marchas:' ,Datos_vehiculo_est[11]),
                                )
                table = LongTable(data = datos,colWidths=(1.0*inch,3.5*inch,2.95*inch),
                                style = [
                                        ('GRID',(1,0),(2,1),0.5,colors.grey),
                                        ('GRID',(0,2),(0,2),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,2), 'Helvetica-Bold'),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                contents.append(table)
                datos = (
                                ('','Tipo de eje trasero:' , Datos_vehiculo_est[12]),
                                ('Eje', 'Suspensión / Amortiguador:' ,Datos_vehiculo_est[13]),
                                ('trasero', 'Barra estabilizadora o barra de torsión (Si / No):',Datos_vehiculo_est[14]),
                                ('','Sistemas activos (Dirección activa / Control de\nestabilidad electrónica / Suspensión activa):' , Datos_vehiculo_est[15]),
                                )
                table = LongTable(data = datos,colWidths=(1.0*inch,3.5*inch,2.95*inch),
                                style = [
                                        ('GRID',(1,0),(2,3),0.5,colors.grey),
                                        ('GRID',(0,4),(0,4),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,3), 'Helvetica-Bold'),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                contents.append(table)
                datos = (
                                ('','Tipo de eje delantero:' , Datos_vehiculo_est[15]),
                                ('Eje', 'Suspensión / Amortiguador:' ,Datos_vehiculo_est[16]),
                                ('delantero', 'Barra estabilizadora o barra de torsión (Si / No):',Datos_vehiculo_est[17]),
                                ('','Sistemas activos (Dirección activa / Control de\nestabilidad electrónica / Suspensión activa):' , Datos_vehiculo_est[18]),
                                )
                table = LongTable(data = datos,colWidths=(1.0*inch,3.5*inch,2.95*inch),
                                style = [
                                        ('GRID',(1,0),(2,3),0.5,colors.grey),
                                        ('GRID',(0,4),(0,4),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,3), 'Helvetica-Bold'),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                contents.append(table)
                datos = (
                                ('','Eje dirigido (Delantero / Trasero):' , Datos_vehiculo_est[19]),
                                ('', 'Dirección delantera activa (Si / No):' ,Datos_vehiculo_est[20]),
                                ('', 'Dirección trasera activa (Si / No):',Datos_vehiculo_est[21]),
                                ('Dirección', 'Dirección asistida (Si / No):' , Datos_vehiculo_est[22]),
                                ('', 'Tipo de asistencia (Hidráulica / Eléctrica\n/ Electro-hidráulica):' ,Datos_vehiculo_est[23]),
                                ('', 'Overall steering ratio Delantero (i_S):',Datos_vehiculo_est[24]),
                                ('','Diámetro del volante (mm):' , Datos_vehiculo_est[25]),
                                )
                table = LongTable(data = datos,colWidths=(1.0*inch,3.5*inch,2.95*inch),
                                style = [
                                        ('GRID',(1,0),(2,6),0.5,colors.grey),
                                        ('GRID',(0,7),(0,7),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,6), 'Helvetica-Bold'),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                        )
                contents.append(table)
                datos = (
                                ('','Frenado asistido (Si / No):' , Datos_vehiculo_est[26]),
                                ('Sistema', 'Sistema de control de estabilidad electrónico (Si / No):' ,Datos_vehiculo_est[27]),
                                ('de frenos', 'Tipo de control de estabilidad (Ej. ABS):',Datos_vehiculo_est[28]),
                                ('', 'Frenos en eje delantero (Tambor / Disco):' , Datos_vehiculo_est[29]),
                                ('', 'Frenos en eje trasero (Tambor / Disco):' ,Datos_vehiculo_est[30]),
                                )
                table = LongTable(data = datos,colWidths=(1.0*inch,3.5*inch,2.95*inch),
                                style = [
                                        ('GRID',(1,0),(2,4),0.5,colors.grey),
                                        ('GRID',(0,5),(0,5),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,4), 'Helvetica-Bold'),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                contents.append(table)
                datos = (
                                ('Ruedas','Tamaño de rin (in):' , ' Delanteras: '+Datos_vehiculo_est[31]+' / Traseras: '+Datos_vehiculo_est[32]),
                                )
                table = LongTable(data = datos,colWidths=(1.0*inch,3.5*inch,2.95*inch),
                                style = [
                                        ('GRID',(1,0),(2,0),0.5,colors.grey),
                                        ('GRID',(0,1),(0,1),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,0), 'Helvetica-Bold'),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                contents.append(table)
                datos = (
                                ('','Fecha de manufactura (AAAA/MM/DD):' , datos_llantas[0]),
                                ('','Tamaño de llantas (in):' , ' Delanteras: '+Datos_vehiculo_est[33]+' / Traseras: '+Datos_vehiculo_est[34]),
                                ('Llantas', 'Profundidad del labrado de llantas (mm):' ,' Delanteras: '+Datos_vehiculo_est[35]+' / Traseras: '+Datos_vehiculo_est[36]),
                                ('', 'Presión de llantas en Vacío (kPa):',' Delanteras: '+Datos_vehiculo_est[37]+' / Traseras: '+Datos_vehiculo_est[38]+ '\n(*De acuerdo a ficha técnica):'),
                                ('', 'Presión de llantas en Peso Bruto (kPa):' , ' Delanteras: '+Datos_vehiculo_est[40]+' / Traseras: '+Datos_vehiculo_est[41]+'\n(*De acuerdo a ficha técnica):'),
                                )
                table = LongTable(data = datos,colWidths=(1.0*inch,3.5*inch,2.95*inch),
                                style = [
                                        ('GRID',(1,0),(2,4),0.5,colors.grey),
                                        ('GRID',(0,5),(0,5),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,4), 'Helvetica-Bold'),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                contents.append(table)
                
                datos = (
                                ('Factor de estabilidad SSF (g):' ,SSF),)
                table = LongTable(data = datos,colWidths=((1.0+3.5)*inch,2.95*inch),
                                style = [
                                        ('GRID',(1,0),(2,3),0.5,colors.grey),
                                        ('GRID',(0,4),(0,4),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,3), 'Helvetica-Bold'),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                        )
                contents.append(table)
                style = getSampleStyleSheet()
                style_title = ParagraphStyle('Titulos',
                           fontName="Helvetica-Bold",
                           fontSize=16,
                           parent=style['Heading2'],
                           alignment=1,
                           spaceAfter=14)
                Title=Paragraph("Prueba hacia la dirección de las manecillas del reloj", style_title)
                contents.append(Title)
                datos = (
                                ('Resultados', 'Gradiente de subviraje/sobreviraje\n(Understeer/oversteer gradient, U):' ,str(datos_ISO4138[0])),
                                ('de la prueba', 'Factor de estabilidad\n(Stability factor, K):',str(datos_ISO4138[1])),
                                ('ISO 4138', 'Steering ratio (is):' , str(datos_ISO4138[2])),
                                )
                table = LongTable(data = datos,colWidths=(1.0*inch,3.5*inch,2.95*inch),
                                style = [
                                        ('LINEABOVE', (0,0), (-1,0),0.5,colors.grey),
                                        ('GRID',(1,0),(2,2),0.5,colors.grey),
                                        ('GRID',(0,3),(0,3),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,2), 'Helvetica-Bold'),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                        )
                contents.append(table)
                Title=Paragraph("Gráfica de aceleración lateral a<sub>y</sub> (m/s<sup>y</sup>) vs ángulo de volante &delta (°)", style_title)
                contents.append(Title)
                
                drawing = Drawing(400, 200)
                lp = LinePlot()
                lp.x = 50
                lp.y = 50
                lp.height = 125
                lp.width = 450
                lp.data = data_graph_volante
                lp.joinedLines = 1
                lp.lines[0].symbol = makeMarker('FilledCircle')
                lp.lines[1].symbol = makeMarker('Circle')
                lp.lineLabelFormat = '%2.0f'
                lp.strokeColor = colors.black
                drawing.add(lp)
                contents.append(drawing)

                Title=Paragraph("Gráfica de aceleración lateral ángulo de volcamiento &#966 (°) vs a<sub>y</sub> (m/s<sup>2</sup>)", style_title)
                contents.append(Title)
                
                drawing = Drawing(400, 200)
                lp = LinePlot()
                lp.x = 50
                lp.y = 50
                lp.height = 125
                lp.width = 450
                lp.data = data_graph_volcamiento
                lp.joinedLines = 1
                lp.lines[0].symbol = makeMarker('FilledCircle')
                lp.lines[1].symbol = makeMarker('Circle')
                lp.lineLabelFormat = '%2.0f'
                lp.strokeColor = colors.black
                drawing.add(lp)
                contents.append(drawing)
                Title=Paragraph("Prueba hacia la dirección de las contra las manecillas del reloj", style_title)
                contents.append(Title)
                datos = (
                                ('Resultados', 'Gradiente de subviraje/sobreviraje\n(Understeer/oversteer gradient, U):' ,str(datos_ISO4138i[0])),
                                ('de la prueba', 'Factor de estabilidad\n(Stability factor, K):',str(datos_ISO4138i[1])),
                                ('ISO 4138', 'Steering ratio (is):' , str(datos_ISO4138i[2])),
                                )
                table = LongTable(data = datos,colWidths=(1.0*inch,3.5*inch,2.95*inch),
                                style = [
                                        ('LINEABOVE', (0,0), (-1,0),0.5,colors.grey),
                                        ('GRID',(1,0),(2,2),0.5,colors.grey),
                                        ('GRID',(0,3),(0,3),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,2), 'Helvetica-Bold'),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                        )
                contents.append(table)
                Title=Paragraph("Gráfica de aceleración lateral a<sub>y</sub> (m/s<sup>y</sup>) vs ángulo de volante &delta (°)", style_title)
                contents.append(Title)
                
                drawing = Drawing(400, 200)
                lp = LinePlot()
                lp.x = 50
                lp.y = 50
                lp.height = 125
                lp.width = 450
                lp.data = data_graph_volantei
                lp.joinedLines = 1
                lp.lines[0].symbol = makeMarker('FilledCircle')
                lp.lines[1].symbol = makeMarker('Circle')
                lp.lineLabelFormat = '%2.0f'
                lp.strokeColor = colors.black
                drawing.add(lp)
                contents.append(drawing)

                Title=Paragraph("Gráfica de aceleración lateral ángulo de volcamiento &#966 (°) vs a<sub>y</sub> (m/s<sup>2</sup>)", style_title)
                contents.append(Title)
                
                drawing = Drawing(400, 200)
                lp = LinePlot()
                lp.x = 50
                lp.y = 50
                lp.height = 125
                lp.width = 450
                lp.data = data_graph_volcamientoi
                lp.joinedLines = 1
                lp.lines[0].symbol = makeMarker('FilledCircle')
                lp.lines[1].symbol = makeMarker('Circle')
                lp.lineLabelFormat = '%2.0f'
                lp.strokeColor = colors.black
                drawing.add(lp)
                contents.append(drawing)
                doc.addPageTemplates([firstpage, laterpages])
                doc.build(contents)

"""Aparte de los campos comunes de las demás pruebas en la prueba de frenado se tiene las siguientes listas:
-Entorno: Zona de pruebas, Distancia de la trayectoria, Velocidad del viento maxima.
-Temperatura: (ET0 para el ensayo tipo 0, ET1 para el ensayo tipo 1, ET2 para el ensayo tipo 2)_TM
-Fuerza aplicada en el pedal de frenos: (ET0 para el ensayo tipo 0, ET1 para el ensayo tipo 1, ET2 para el ensayo tipo 2, Ensayo estático, Ensayo dinamico)_FP
-Velocidad inicial: (ET0 para el ensayo tipo 0, ET1 para el ensayo tipo 1, ET2 para el ensayo tipo 2, Ensayo dinamico)_v1
-Distancia de frenado: (ET0 para el ensayo tipo 0, ET1 para el ensayo tipo 1, ET2 para el ensayo tipo 2, Ensayo dinamico)_s
-Deceleración media estabilizada :(ET0 para el ensayo tipo 0, ET1 para el ensayo tipo 1, ET2 para el ensayo tipo 2, Ensayo dinamico)_d"""
class Report_frenado:
        def foot2(self,pdf,doc):
                width,height = A4
                pdf.saveState()
                pdf.setFont('Times-Bold',22)
                pdf.drawCentredString(width/2.0, height-63, "REPORTE DE PRUEBA DE FRENADO")
                pdf.setFont('Times-Roman',9)
                pdf.setTitle("REPORTE DE PRUEBA DE FRENADO")
                pdf.setAuthor("Universidad del Valle")
                #pdf.drawString(width-1*inch, 0.1 * inch,'Página '+"%d" % doc.page+' de '+"%d" % 3)

        def get_doc(self, buffer, encargado, codigo, fecha, Datos_vehiculo, Entorno, ET0_TM, ET0_FP, ET0_v1, ET0_s, ET0_d, 
                        ET1_TM, ET1_FP, ET1_v1, ET1_s, ET1_d, ET2_TM, ET2_FP, ET2_v1, ET2_s, ET2_d, Sistema_emergencia_Fp, Sistema_emergencia_dinamico):
                #print("Generando PDF")
                width,height = A4

                doc = BaseDocTemplate(buffer, showBoundary=1, pagesize= A4)
                contents =[]
                TopCenter = Frame(0.4*inch,height-1.2*inch,width-0.8*inch,0.8*inch,showBoundary=1,id='normal')
                frame1later = Frame(0.4*inch,0.6*inch,width-0.8*inch, height-2*inch,leftPadding=0,topPadding=0,showBoundary = 1,id='col1later')

                frame_params = Frame(0.4*inch,0.6*inch,width-0.8*inch, height-2*inch,leftPadding=0,topPadding=0, showBoundary = 1,id='col')

                firstpage = PageTemplate(id='firstpage',frames=[TopCenter,frame_params],onPage=self.foot2)

                laterpages = PageTemplate(id='laterpages',frames=[TopCenter,frame1later],onPage=self.foot2)

                contents.append(NextPageTemplate('laterpages'))

                archivo_imagen = 'icons/Univalle.png'
                logoleft = Image(archivo_imagen)
                logoleft._restrictSize(0.5*inch, 0.5*inch)

                logoleft.hAlign = 'LEFT'
                logoleft.vAlign = 'CENTER'

                contents.append(logoleft)
                datos = (       ('','Código de prueba:', codigo),
                                ('Equipo','Encargado de la prueba:', encargado[0]),
                                ('de','Conductor:',encargado[1]),
                                ('pruebas','Observador:',encargado[2]),
                                )
                table = LongTable(data = datos,colWidths=(1.0*inch,3.5*inch,2.95*inch),
                                style = [
                                        #('GRID',(1,0),(1,1),0.5,colors.grey),
                                        ('GRID',(1,0),(2,3),0.5,colors.grey),
                                        #('GRID',(0,3),(2,3),0.5,colors.grey),
                                        #('SPAN',(0,0),(0,2)),
                                        #('SPAN',(1,0),(1,1)),
                                        #('GRID',(0,2),(2,2),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,3), 'Helvetica-Bold'),
                                        #('GRID',(1,1),(2,1),0.5,colors.grey),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                contents.append(table)
                
                datos = (       
                                ('Equipo','Encargado de la prueba:', encargado[0]),
                                ('de','Conductor:',encargado[1]),
                                ('pruebas','Observador:',encargado[2]),
                                )
                table = LongTable(data = datos,colWidths=(1.0*inch,3.5*inch,2.95*inch),
                                style = [
                                        #('GRID',(1,0),(1,1),0.5,colors.grey),
                                        ('GRID',(1,0),(2,2),0.5,colors.grey),
                                        ('GRID',(0,3),(2,3),0.5,colors.grey),
                                        #('SPAN',(0,0),(0,2)),
                                        #('SPAN',(1,0),(1,1)),
                                        #('GRID',(0,2),(2,2),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,2), 'Helvetica-Bold'),
                                        #('GRID',(1,1),(2,1),0.5,colors.grey),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                datos = (
                                ('Fecha y hora de elaboración de la prueba:', fecha[0]),
                                ('Fecha y hora de elaboración del reporte:', fecha[1]),
                                ('Fecha de calibración sensores:', fecha[2]),
                                )
                table = LongTable(data = datos,colWidths=((1.0+3.5)*inch,2.95*inch),
                                style = [
                                        #('GRID',(1,0),(1,1),0.5,colors.grey),
                                        ('GRID',(0,0),(2,2),0.5,colors.grey),
                                        #('SPAN',(0,0),(0,1)),
                                        #('SPAN',(1,0),(1,1)),
                                        ('GRID',(0,2),(2,2),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,2), 'Helvetica-Bold'),
                                        #('GRID',(1,1),(2,1),0.5,colors.grey),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                contents.append(table)
                datos = (
                                ('Identificación','Fabricante:' , Datos_vehiculo[0]),
                                ('', 'Modelo:' ,Datos_vehiculo[1]),
                                ('del vehículo', 'Tipo:',Datos_vehiculo[2]),
                                )
                table = LongTable(data = datos,colWidths=(1.0*inch,3.5*inch,2.95*inch),
                                style = [
                                        ('GRID',(1,0),(2,4),0.5,colors.grey),
                                        ('GRID',(0,3),(0,3),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,3), 'Helvetica-Bold'),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                ,repeatRows=True
                                        )
                datos = (
                                ('Condición' , 'Zona de pruebas, pista o espacio de pruebas\n(Dirección y/o nombre):', Entorno[0]),
                                ('del', 'Distancia de la trayectoria utilizada\npara las pruebas (km):' , Entorno[1]),
                                ('entorno', 'Velocidad máxima del viento (m/s):' , Entorno[2]),
                                )
                table = LongTable(data = datos,colWidths=(1.0*inch,3.5*inch,2.95*inch),
                                style = [
                                        ('GRID',(1,0),(2,2),0.5,colors.grey),
                                        ('GRID',(0,3),(0,3),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (0,3), 'Helvetica-Bold'),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                        )
                contents.append(table)

                style = getSampleStyleSheet()
                style_title = ParagraphStyle('Titulos',
                           fontName="Helvetica-Bold",
                           fontSize=16,
                           parent=style['Heading2'],
                           alignment=1,
                           spaceAfter=14)
                Title=Paragraph("Ensayo tipo 0-Frenos en frío", style_title)
                contents.append(Title)
                datos = (
                        ('Nombre de\nensayo','Vehículo Cargado/\nDescargado' ,'Motor Embragado/\nDesembragado', 'Ciclo de\nfrenado #', 'Variables\ncontroladas','','','Requisitos'),
                        ('','','','','T_m(°C)','F_p(N)','v_1\n(km/h)','s(m)','d_m\n(m/s^2)'),
                        ('ET0','Descargado','Desembragado','1',str(ET0_TM[0]),str(ET0_FP[0]),str(ET0_v1[0]),str(ET0_s[0]),str(ET0_d[0])),
                        ('ET0','Descargado','Embragado','1',str(ET0_TM[1]),str(ET0_FP[1]),str(ET0_v1[1]),str(ET0_s[1]),str(ET0_d[1])),
                        ('ET0','Cargado','Desembragado','1',str(ET0_TM[2]),str(ET0_FP[2]),str(ET0_v1[2]),str(ET0_s[2]),str(ET0_d[2])),
                        ('ET0','Cargado','Embragado','1',str(ET0_TM[3]),str(ET0_FP[3]),str(ET0_v1[3]),str(ET0_s[3]),str(ET0_d[3])),
                        )
                table = LongTable(data = datos, colWidths=(0.9*inch,1.4*inch,1.4*inch,0.8*inch,0.7*inch,0.6*inch,
                                                           0.6*inch,0.45*inch,0.6*inch),
                                style = [
                                        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                                        ('SPAN', (4, 0), (6, 0)),
                                        ('SPAN', (7, 0), (8, 0)),
                                        ('SPAN', (0, 0), (0, 1)),
                                        ('SPAN', (1, 0), (1, 1)),
                                        ('SPAN', (2, 0), (2, 1)),
                                        ('SPAN', (3, 0), (3, 1)),
                                        ('FONTNAME', (0,0), (8,1), 'Helvetica-Bold'),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                        )
                contents.append(table)
                Title=Paragraph("Ensayo tipo 1-Frenos en perdida", style_title)
                contents.append(Title)
                datos = (
                        ('Nombre de\nensayo','Vehículo Cargado/\nDescargado' ,'Motor Embragado/\nDesembragado', 'Ciclo de\nfrenado #', 'Variables\ncontroladas','','','Requisitos'),
                        ('','','','','T_m(°C)','F_p(N)','v_1\n(km/h)','s(m)','d_m\n(m/s^2)'),
                        #('ET1','Cargado','Embragado','16','','','','',''),
                        ('Calentamiento','Cargado','Embragado','15',str(ET1_TM[0]),str(ET1_FP[0]),str(ET1_v1[0]),str(ET1_s[0]),str(ET1_d[0])),
                        #('ET1','Descargado','Embragado','16','','','','',''),
                        ('ET1','Cargado','Desembragado','1',str(ET1_TM[1]),str(ET1_FP[1]),str(ET1_v1[1]),str(ET1_s[1]),str(ET1_d[1])),
                        )
                table = LongTable(data = datos, colWidths=(0.9*inch,1.4*inch,1.4*inch,0.8*inch,0.7*inch,0.6*inch,
                                                           0.6*inch,0.45*inch,0.6*inch),
                                style = [
                                        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                                        ('SPAN', (4, 0), (6, 0)),
                                        ('SPAN', (7, 0), (8, 0)),
                                        ('SPAN', (0, 0), (0, 1)),
                                        ('SPAN', (1, 0), (1, 1)),
                                        ('SPAN', (2, 0), (2, 1)),
                                        ('SPAN', (3, 0), (3, 1)),
                                        ('FONTNAME', (0,0), (8,1), 'Helvetica-Bold'),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                        )
                contents.append(table)
                Title=Paragraph("Ensayo tipo 2", style_title)
                contents.append(Title)
                datos = (
                        ('Nombre de\nensayo','Vehículo Cargado/\nDescargado' ,'Motor Embragado/\nDesembragado', 'Ciclo de\nfrenado #', 'Variables\ncontroladas','','','Requisitos'),
                        ('','','','','T_m(°C)','F_p(N)','v_1\n(km/h)','s(m)','d_m\n(m/s^2)'),
                        #('ET2','Cargado','Embragado','20','','','','',''),
                        ('Recuperación','Cargado','Embragado','4',str(ET2_TM[0]),str(ET2_FP[0]),str(ET2_v1[0]),str(ET2_s[0]),str(ET2_d[0])),
                        #('ET2','Descargado','Embragado','20','','','','',''),
                        ('ET2','Cargado','Desembragado','1',str(ET2_TM[1]),str(ET2_FP[1]),str(ET2_v1[1]),str(ET2_s[1]),str(ET2_d[1])),
                        )
                table = LongTable(data = datos, colWidths=(0.9*inch,1.4*inch,1.4*inch,0.8*inch,0.7*inch,0.6*inch,
                                                           0.6*inch,0.45*inch,0.6*inch),
                                style = [
                                        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                                        ('SPAN', (4, 0), (6, 0)),
                                        ('SPAN', (7, 0), (8, 0)),
                                        ('SPAN', (0, 0), (0, 1)),
                                        ('SPAN', (1, 0), (1, 1)),
                                        ('SPAN', (2, 0), (2, 1)),
                                        ('SPAN', (3, 0), (3, 1)),
                                        ('FONTNAME', (0,0), (8,1), 'Helvetica-Bold'),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                        )
                contents.append(table)
                contents.append(PageBreak())
                Title=Paragraph("", style_title)
                contents.append(Title)
                Title=Paragraph("", style_title)
                contents.append(Title)
                Title=Paragraph("Ensayo sistema de parada de emergencia", style_title)
                contents.append(Title)
                datos = (
                        ('Nombre de ensayo','Motor Embragado\n/Desembragado', 'Ciclo de\nfrenado #', 'Variables controladas','','Requisitos'),
                        ('','','','F_p(N)','v_1\n(km/h)','s(m)','d_m\n(m/s^2)'),
                        ('Ensayo estático','No aplica','1',str(Sistema_emergencia_Fp),'NO\nAPLICA','NO\nAPLICA','NO\nAPLICA'),
                        ('Ensayo dinamico','Desembragado','1',str(Sistema_emergencia_dinamico[0]),str(Sistema_emergencia_dinamico[1]),str(Sistema_emergencia_dinamico[2]),str(Sistema_emergencia_dinamico[3])),
                        )
                table = LongTable(data = datos, colWidths=(1.4*inch,2*inch,0.76*inch,0.82*inch,0.82*inch,0.82*inch,0.82*inch),
                                style = [
                                        ('SPAN', (3, 0), (4, 0)),
                                        ('SPAN', (5, 0), (6, 0)),
                                        ('SPAN', (0, 0), (0, 1)),
                                        ('SPAN', (1, 0), (1, 1)),
                                        ('SPAN', (2, 0), (2, 1)),
                                        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                                        ('FONTNAME', (0,0), (8,1), 'Helvetica-Bold'),
                                        ],
                                hAlign='LEFT'
                                ,splitByRow=True
                                        )
                contents.append(table)
                doc.addPageTemplates([firstpage, laterpages])
                doc.build(contents)

from reportlab.pdfgen import canvas #Se importa en el main del programa el paquete para generar el importe.

"""Metodo para probar el generar pdfs cuando se vaya unir se comenta para que se importe el paquete PDFTemplate
se trabaja asi por facilidad para que sea modular y se copia en el programa principal el contenido de la clase main,
exceptuando las listas. La importancion se realiza con 'from .PDFTemplate import Report_CDG'."""
def main():
        #Estas listas se comentan cuando se integren.
        codigo='00001'
        Nombre_archivo="ReporteCDG.pdf"
        Encargado_prueba=["Juan Carlos Noguera Ramírez", "Luis Garcia", "Esteban Velez"] #[Encargado de la prueba, conductor, observador o copitolo]
        fecha=['27 de noviembre de 2022 14:30','27 de noviembre de 2022 14:45','20 septiembre de 2022 13:00'] #[fecha prueba, fecha reporte, fecha calibracion sensores]
        Datos_vehiculo=['KIA', 'SOUL LX 1.591 cc, 2011', 'Auto de pasajeros','Tamaño cm','Tamaño cm','Presión psi','Presión psi'] 
        Datos_alistamiento=['Lleno/Vacio', 'Sin carga', 'No','Neutro','Liberado','Tacos de caucho']
        
        #Datos_medidos[masa rueda delantera, masa rueda izquierda, masa total, ancho de via delantero, ancho de via trasero, 
        # distancia entre centros derecho, distancia entre centros izquierdo, Radio en carga estática delantero derecho, Radio en carga estática delantero izquierdo, 
        # Radio en carga estática trasero derecho, Radio en carga estática trasero izquierdo]
        Datos_medidos=['', '', '','','','', '', '','','','','','']

        #Resultados_pruebas[Xcg,Ycg,Zcg,prueba eje delantero elevado grados, masa en eje trasero, Zcg calculado, se dejan vacios el resto'','','']
        Resultados_pruebas=['', '', '','','','', '', '','','','']
        
        Datos_via=['Recta Cali-Palmira','7km','Pavimentada'] #[Via o direccion de la prueba, distancia recorrida de la prueba, tipo de via pavimentada/destapada]
        #De aqui en adelante es lo que se debe copiar para generar el archivo pdf desde el programa principal        
        #report=Report_CDG()
        #report.get_doc(Nombre_archivo,Encargado_prueba,codigo,fecha,Datos_vehiculo, Datos_alistamiento, Datos_medidos, Resultados_pruebas)
        """equipo_pruebas=['Luis Garcia', 'Esteban Velez', 'Juan Noguera']
        Datos_ambiente=['','','','','','','','']
        report=Report_estabilidad()
        report.get_doc(Nombre_archivo,equipo_pruebas,codigo,fecha,Datos_vehiculo, Datos_ambiente, Datos_medidos, Resultados_pruebas)"""
        
        #Descomentar para probar el informe de rigidez
        """imagen_prueba = Image('Rigidez.jpeg',width=170, height=150) # Aqui va la dirección donde esta la imagen con la prueba para rigidez a torsion
        Datos_rigidez=[imagen_prueba,'',''] [Imagen, posicion LVDT, posición de la carga]
        Dato_peso=['0','20','40','60','80','100','120','140'] #Esto es cuando ponia la tabla por el momento con la grafica se presentan los datos.
        Dato_m=['0','252','458','686','915','1144','1373','1601'] #Esto es cuando ponia la tabla por el momento con la grafica se presentan los datos.
        Dato_desplazamiento=['0,0000','0,0020','0,3818','0,7551','1,1668','1,6000','2,0436','2,3860'] #Esto es cuando ponia la tabla por el momento con la grafica se presentan los datos.
        Dato_angulo=['0,0000','0,0002','0,0312','0,0618','0,0955','0,1310','0,1673','0,1953'] #Esto es cuando ponia la tabla por el momento con la grafica se presentan los datos.
        report=Report_rigidez()
        data = [
                ((0.0000,0.0000), (0.0049,114.4), (0.0119,228.8), (0.0181,343.2), (0.0220,457.5), (0.0253,571.9), (0.0308,686.3), (0.0354,800.7)),
                ] #Aqui estan los datos para graficar a torsión 
        Dato_rigidezTotal=[14635.19,'Sobredimensionado'] rigidez torsional 
        imagen_prueba1 = Image('Rigidez2.jpeg',width=170, height=150)
        Datos_rigidezT=[imagen_prueba1,'','']
        dataT = [
                ((0.0000,0.0000), (0.0029,346.69), (0.0075,693.37), (0.0093,1040.06), (0.0115,1386.74), (0.0171,1733.43)),
                ] #Aqui estan los datos para graficar a flexión 
        Dato_rigidezTTotal=[48078.88,'Sobredimensionado'] rigidez flexion
        #print(Dato_rigidezTTotal)
        report.get_doc(Nombre_archivo,Encargado_prueba,codigo,fecha,Datos_vehiculo, Datos_rigidez, Dato_rigidezTotal, data, Datos_rigidezT, Dato_rigidezTTotal, dataT)"""
        
        #Descomentar para generar el informe de confort.
        """Datos_resultados=['00:10',0.4,8.0,'Niveles de vibración dentro de limites seguros.',0.300,'No incómodo'] #resultados confort [tiempo de prueba hh:mm, exposicion diaria A(8), VDV, Niveles de vibracion(en codigo Matlab estan definidos), Aceleración eficaz ponderada en
                                                                                                                 #'frecuencia total', 'Niveles de comodida (en el codigo de matlab de JP esta igualmente)']
        report=Report_estabilidad()
        report.get_doc(Nombre_archivo,Encargado_prueba,codigo,fecha, Datos_vehiculo, Datos_via, Datos_resultados)"""

        #Datos_resultados=['00:10',0.4,8.0,'Niveles de vibración dentro de limites seguros.',0.300,'No incómodo'] #resultados confort [tiempo de prueba hh:mm, exposicion diaria A(8), VDV, Niveles de vibracion(en codigo Matlab estan definidos), Aceleración eficaz ponderada en
        """                                                                                                         #'frecuencia total', 'Niveles de comodida (en el codigo de matlab de JP esta igualmente)']
        data = [
                ((0.231,5.1), (0.642,60.8), (1.366,6.2), (2.2205,136.8), (2.3283,-13.4))
                ]
        data_volcamiento = [
                ((-13.4,2.3283),(6.2, 2.2205), (5.1,1.366),(60.8,0.642),(136.8,0.231))
                ]
        
        datai = [
                ((0.231,5.1), (0.642,60.8), (1.366,6.2), (2.2205,136.8), (2.3283,-13.4))
                ]
        data_volcamientoi = [
                ((-13.4,2.3283),(6.2, 2.2205), (5.1,1.366),(60.8,0.642),(136.8,0.231))
                ]
        datos_espacio=['','']
        datos_calazada=['','','','']
        datos_clima=['','','','']
        datos_llantas=['','','']
        datos_conduccion=['','','','','']
        datos_volcamiento=0.94
        datos_derrape=['','','','']
        datos_derrapei=['','','','']
        Datos_vehiculo_est=['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','']"""
        ET0_TM=['','','','']
        ET0_FP=['','','','']
        ET0_v1=['','','','']
        ET0_s=['','','','']
        ET0_d=['','','','']
        ET1_TM=['','']
        ET1_FP=['','']
        ET1_v1=['','']
        ET1_s=['','']
        ET1_d=['','']
        ET2_TM=['','']
        ET2_FP=['','']
        ET2_v1=['','']
        ET2_s=['','']
        ET2_d=['','']
        Entorno=['','','']
        Sistema_emergencia_Fp=''
        Sistema_emergencia_dinamico=['','','','']
        report=Report_frenado()
        report.get_doc(Nombre_archivo,Encargado_prueba, codigo,fecha, Datos_vehiculo, Entorno, ET0_TM, ET0_FP, ET0_v1, ET0_s, ET0_d, ET1_TM, ET1_FP, ET1_v1, ET1_s, ET1_d, ET2_TM, ET2_FP, ET2_v1, ET2_s, ET2_d, Sistema_emergencia_Fp, Sistema_emergencia_dinamico)

if __name__ == "__main__":
    main()