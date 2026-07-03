import psutil
import win32com.client
import os
from pptx import Presentation
from configs.manager_doc_config import get_ruta_a_carpeta_de_guardado_del_documento


def reemplazar_en_slide(slide, diccionario):
    for shape in slide.shapes:
        if shape.has_text_frame:
            for paragraph in shape.text_frame.paragraphs:
                for run in paragraph.runs:
                    for k, v in diccionario.items():
                        if k in run.text:
                            run.text = run.text.replace(k, str(v))
        if shape.has_table:
            table = shape.table
            for row in table.rows:
                for cell in row.cells:
                    for k, v in diccionario.items():
                        if k in cell.text:
                            cell.text = cell.text.replace(k, str(v))
                            
from copy import deepcopy

def duplicar_slide(ppt, slide):
    xml_slides = ppt.slides._sldIdLst
    new_slide = ppt.slides.add_slide(slide.slide_layout)

    for shape in slide.shapes:
        new_slide.shapes._spTree.append(deepcopy(shape.element))

    return new_slide
                           

def generar_ppt_por_sondas(ppt, diccionario_sondas):
    template_slide = ppt.slides[0]

    slides_generados = {}

    for serial, data in diccionario_sondas.items():

        slide = duplicar_slide(ppt, template_slide)

        reemplazar_en_slide(slide, data)

        slides_generados[serial] = slide

    xml_slides = ppt.slides._sldIdLst
    ppt.slides._sldIdLst.remove(xml_slides[0])
    return ppt, slides_generados



import shutil
import os
import time

def cerrar_powerpoint_si_existe():
    for p in psutil.process_iter(["name"]):
        if p.info.get("name") and "POWERPNT.EXE" in p.info["name"]:
            p.kill()
            
def exportar_ppt(ppt_path, output_folder):

    ppt_path = os.path.abspath(ppt_path)

    staging_ppt = os.path.join(os.getcwd(), "staging.pptx")
    shutil.copy2(ppt_path, staging_ppt)

    ppt_app = win32com.client.Dispatch("PowerPoint.Application")
    ppt_app.Visible = 1

    presentation = None

    try:
        presentation = ppt_app.Presentations.Open(staging_ppt, WithWindow=False)

        os.makedirs(output_folder, exist_ok=True)
        pdf_path = os.path.join(output_folder, "reporte_sondas.pdf")

        presentation.SaveAs(pdf_path, 32)

    finally:
        # 🔥 CIERRE GARANTIZADO
        if presentation is not None:
            try:
                presentation.Close()
            except:
                pass

        try:
            ppt_app.Quit()
        except:
            pass

        del presentation
        del ppt_app

        import gc
        gc.collect()

        time.sleep(2)
    

def ppt_sondas(ppt, diccionario_sondas):

    ppt, slides = generar_ppt_por_sondas(ppt, diccionario_sondas)

    ruta = get_ruta_a_carpeta_de_guardado_del_documento()

    # nombre del archivo de salida (define explícitamente)
    nombre_archivo = "output.pptx"

    # ruta completa del ppt
    output_ppt = os.path.join(ruta, nombre_archivo)

    # asegurar que la carpeta exista
    os.makedirs(os.path.dirname(output_ppt), exist_ok=True)

    ppt.save(output_ppt)

    import time
    time.sleep(2)

    exportar_ppt(output_ppt, ruta)

    return output_ppt, ruta

