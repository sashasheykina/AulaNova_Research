import json
import os

from pptx import Presentation
from pptx.util import Pt
import copy
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.util import Inches

import Utility_last
from merge_slides import insert_slides_at_tag, remove_slide_with_tag


#Funzione utilizzata per caricare il file JSON da utilizziare
def loadJsonData(jsonFile):
    with open(jsonFile, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def getJsonDataRec(data, keyPath):
    print("KEYPATH", keyPath)
    keyPath = keyPath.replace(".0","")
    keys = keyPath.split('.')
    currentData = data
    for k in keys:
        if isinstance(currentData, list):
            currentData = currentData[0]
        try:
            if isinstance(currentData, dict):
                currentData = currentData.get(k, None)
            elif isinstance(currentData, list):
                currentData = currentData[0]
        except Exception as e:
            return None
        if currentData is None:
            return None
        
    return currentData

#Funzione per ottenere le singole chiavi JSON da utilizziare
def getJsonData(data, keyPath):
    keys = keyPath.split('.')
    currentData = data
    if keyPath == "metodologie_aggiuntive.metodologie.metodologia":
        print(f"getJsonData: {keys}, {keyPath}")
    for key in keys:
        if keyPath == "metodologie_aggiuntive.metodologie.metodologia":
            print(f"key {key}")
        if isinstance(currentData, list):
            try:
                index = int(key)
                currentData = currentData[index]
            except (ValueError, IndexError):
                try:
                    # Proviamo a prendere il valore così come è
                    if keyPath == "metodologie_aggiuntive.metodologie.metodologia":
                        print("PRendo ", key)
                    currentData = currentData.get(key, None)
                except Exception as e:
                    return None
        elif isinstance(currentData, dict):
            currentData = currentData.get(key, None)
        else:
            return None
    if keyPath == "metodologie_aggiuntive.metodologie.metodologia":
        print(currentData)
    return currentData



def clone_slide(prs, slide):
    new_slide = prs.slides.add_slide(slide.slide_layout)
    
    # Rimuovi tutti i placeholder predefiniti dalla nuova slide
    for placeholder in new_slide.placeholders:
        sp = placeholder.element
        sp.getparent().remove(sp)
        
    for shape in slide.shapes:
        # Clona solo gli elementi non-placeholder e non vuoti
        if shape.is_placeholder and not shape.has_text_frame:
            continue
        
        el = copy.deepcopy(shape.element)
        new_slide.shapes._spTree.insert_element_before(el, 'p:extLst')

    return new_slide

def move_slide(prs, old_index, new_index):
    slides = list(prs.slides._sldIdLst)
    slide = slides.pop(old_index)
    slides.insert(new_index, slide)
    prs.slides._sldIdLst[:] = slides

def get_parent_key(key):
    parts = key.split('.')
    if len(parts) > 1:
        return '.'.join(parts[:-1])
    return None

def get_leaf_key(key):
    parts = key.split('.')
    if parts:
        return parts[-1]
    return None



def create_bullet_list(value, k, shape, contentFontSize, use=False):
    for i, item in enumerate(value, start=1):
        try:
            if k:
                item = item.get(k)
        except Exception as ee:
            pass
        if isinstance(item, dict):
            item_text = ', '.join(str(v) for v in item.values())
        else:
            item_text = str(item)

        new_paragraph = shape.text_frame.add_paragraph()
        if use:
            new_paragraph.text = f"• {item_text}"
            new_paragraph.font.size = Pt(contentFontSize)
        else:
            new_paragraph.text = item_text
        #new_paragraph.font.size = Pt(contentFontSize)

def handle_slide_to_duplicate(jsonData, contentFontSize, paragraph, values_list, prs, slideIndex, slide):
    paragraph.clear()  # Rimuove il paragrafo contenente il tag
    print("HANLDE SLIDE DUPLICATION")
    for i, value in enumerate(values_list):
        new_slide = clone_slide(prs, slide)

        for new_shape in new_slide.shapes:
            if not new_shape.has_text_frame:
                continue

            new_paragraphs = new_shape.text_frame.paragraphs
            for new_para in new_paragraphs:
                para_text = new_para.text
                parts = para_text.split('<#')
                new_para.text = parts[0]

                for part in parts[1:]:
                    if '#>' in part:
                        tag_name, rest_of_text = part.split('#>', 1)
                        print("TAGNAME", tag_name)
                        if tag_name.startswith("$$LISTA."):
                            tag_name = tag_name[8:]
                            tag_value = getJsonData(value, tag_name.strip())
                        else:
                            tag_value = getJsonData(jsonData, tag_name)

                        if tag_value is None:
                            # Vediamo se il padre era una lista e qui si sta facendo riferimento ad un attributo del dict figlio
                            parentKey = get_parent_key(tag_name)
                            val = getJsonDataRec(jsonData, parentKey)
                            if val:
                                k = get_leaf_key(tag_name)
                                create_bullet_list(val, k, new_shape, contentFontSize)
                        elif isinstance(tag_value, str):
                            new_para.text += str(tag_value or "") + rest_of_text
                        else:
                            # Se il padre dell'elemento ha un attributo type
                            parentKeyType = get_parent_key(tag_name)+".type"
                            typeValue = getJsonData(tag_value, parentKeyType)
                            if typeValue == 1: # Elenco puntato
                                create_bullet_list(tag_value, None, new_shape, contentFontSize)
                            else:
                                val = str(tag_value)
                                new_para.text += str(tag_value or "") + rest_of_text
                    else:
                        new_para.text += part

        move_slide(prs, len(prs.slides) - 1, slideIndex + 1 + i)

    rId = prs.slides._sldIdLst[slideIndex].rId
    prs.part.drop_rel(rId)
    del prs.slides._sldIdLst[slideIndex]


def cleanup_presentation(prs):
    from pptx.opc.packuri import PackURI
    for i, slide in enumerate(prs.slides, 1):
        new_partname = PackURI(f'/ppt/slides/slide{i}.xml')
        slide.part.partname = new_partname
    return prs

def add_table_to_slide(slide, data, params, x, y, cx, cy, col_widths=[2.75, 2.75, 4.0]):
    """
    Aggiunge una tabella a una slide utilizzando i dati forniti.

    :param slide: La slide a cui aggiungere la tabella.
    :param data: Lista di liste, dove ogni lista interna rappresenta una riga.
    :param x: Posizione orizzontale della tabella (inches).
    :param y: Posizione verticale della tabella (inches).
    :param cx: Larghezza della tabella (inches).
    :param cy: Altezza della tabella (inches).
    """
    # Determina il numero di righe e colonne
    headers = params.split("|")
    rows = len(data)
    rows += 1 #if params else 0
    cols = len(headers) if headers else 1

    print("NUMBER OF COLS", cols, "NUMBER OF ROWS", rows, len(params))

    # Aggiungi la tabella alla slide
    table_shape = slide.shapes.add_table(rows, cols, x, y, cx, cy)
    table = table_shape.table

    if col_widths:
        for i, width in enumerate(col_widths):
            print("stampo: ")
            print(i)
            table.columns[i].width = width
    

    data_values = []
    data_values.extend([headers])
    for da in data:
        if isinstance(da, str):
            d = str(da)
        elif isinstance(da,dict):
            d = next(iter(da.values()))
        else:
            d = str(da)
        print("D=",d)
        i = d.find("/")
        if i !=-1:
            col1 = d[0:i].strip()
            
            col2 = d[i+1:]
            j = col2.find("(")
            if j != -1:
                col2 = col2[0:j].strip()
                k = d.find(")")
                if k !=-1:
                    j = d.find("(")
                    col3 = d[j+1:k]
                    data_values.append([col1, col2, col3])
                else:
                    data_values.append([col1,col2])
            else:
                data_values.append([col1,col2])
        else:
            data_values.append([d])


    print("===============")
    print(data_values)
    print("===============")

    # Inserisci i dati nella tabella
    for i, row_data in enumerate(data_values):
        for j, cell_data in enumerate(row_data):
            print(i,j, cell_data)
            table.cell(i, j).text = cell_data
            print("\n====")
    if params:
        table.rows[0].height = Inches(0.47)
    else:
        table._tbl.remove(table.rows[0]._tr)

def replaceTag(layoutPPTX, jsonData, formattingData, outputPPTX):
    prs = Presentation(layoutPPTX)

    # Impostazioni di formattazione dal file JSON
    titleFontSize = getJsonData(formattingData, 'titleFontSize')
    contentFontSize = getJsonData(formattingData, 'contentFontSize')
    titleFontColor = getJsonData(formattingData, 'titleFontColor')
    contentFontColor = getJsonData(formattingData, 'contentFontColor')


    slideIndex = 0
    while slideIndex < len(prs.slides):
        slide = prs.slides[slideIndex]
        #print("SLIDE ",slideIndex)
        found = False
        for shapeIndex, shape in enumerate(slide.shapes):
            if not shape.has_text_frame:
                continue
            paragraphs = shape.text_frame.paragraphs
            for p in paragraphs:
                originalText = p.text.strip()
                if originalText.startswith("{#") and originalText.endswith("#}"):
                    found = True
                    break

        for shapeIndex, shape in enumerate(slide.shapes):
            if not shape.has_text_frame:
                continue
            
            paragraphs = shape.text_frame.paragraphs

            paragraphIndex = 0
            while paragraphIndex < len(paragraphs):
                paragraph = paragraphs[paragraphIndex]

                originalText = paragraph.text.strip()
                print(originalText)
                # Verifica di aver trovato un tag
                if originalText.startswith("{#") and originalText.endswith("#}"):
                    #print("TROVATO TAG DUPLICA")
                    key = originalText[2:-2]
                    values_list = getJsonData(jsonData, key)

                    if isinstance(values_list, list):
                        handle_slide_to_duplicate(jsonData, contentFontSize, paragraph, values_list, prs, slideIndex, slide)
                        break  # Esci dal ciclo dei paragrafi
                elif not found and originalText.startswith("<#") and originalText.endswith("#>"):
                    key = originalText[2:-2]
                    params = "" # x, y, width, height, col1w, col2w, ...
                    width = [Inches(2.75), Inches(2.75), Inches(4.0)]
                    tab_dim = [Inches(0.25), Inches(1.3), Inches(9.54), Inches(3.85)]
                    isTable = False
                    if key.find("(") !=-1:
                        p_start = key.find("(")
                        p_end = key.find(")")
                        params = key[p_start+1:p_end]
                        key = key[0:p_start]
                        p_end = originalText.find(")")
                        rest = originalText[p_end+1:-2]
                        print("PARAMS", params, "\nKEY",key,"\nREST", rest)
                        p_start = rest.find("(")
                        p_end = rest.find(")")
                        if p_start != -1:
                            w = rest[p_start+1:p_end]
                            wd = w.split("|")
                            width_s = [Inches(float(w)) for w in wd]
                            num_cols = len(params.split("|"))
                            if num_cols < 1:
                                num_cols =1
                            print("\nBEFORE", width_s, len(width_s), num_cols)
                            if len(width_s) > num_cols:
                                i = 0
                                j = 0
                                width = [1.0 for s in range(0,num_cols)]
                                for l in width_s:
                                    if i < 4:
                                        tab_dim[i] = width_s[i]
                                    else:
                                        width[j] = width_s[i]
                                        j +=1
                                    i +=1
                            else:
                                width = width_s
                        print("tab_dim", tab_dim)
                        print("width", width)
                        isTable = True

                    value = getJsonData(jsonData, key)

                    if isinstance(value, list):
                        
                        typeKeyPath = key.rsplit('.', 1)[0] + '.type'
                        typeValue = getJsonData(jsonData, typeKeyPath)

                        print("SI è una LISTA ========>", typeValue, key)
                        if typeValue == 1 and not isTable: # Elenco puntato
                            paragraph.clear()
                            create_bullet_list(value, None, shape,contentFontSize, True)
                            #print(f"Sostituito il tag '{originalText}' con un elenco numerato")
                        elif isTable: # Tabella
                            print("TROVATA TABELLA=====>", value)
                            paragraph.clear()
                            add_table_to_slide(slide, value, params, tab_dim[0], tab_dim[1], tab_dim[2], tab_dim[3], col_widths=width)
                        elif typeValue == 0: # Duplica slide
                            originalTitle = slide.shapes.title.text if slide.shapes.title else "titolo_lezione"
                            if value:
                                firstItem = value[0]
                                paragraph.clear()
                                if isinstance(firstItem, dict):
                                    firstValueOnly = list(firstItem.values())
                                    paragraph.text = '\n• '.join(map(str, firstValueOnly))
                                else:
                                    paragraph.text = str(firstItem)

                                paragraph.font.size = Pt(contentFontSize)
                                #print(f"Sostituito il tag '{originalText}' con il valore '{firstItem}'")

                                # Inizia ad inserire le nuove slide dopo quella corrente
                                insert_after = slideIndex
                                for item in value[1:]:
                                    insert_after += 1
                                    newSlide = prs.slides.add_slide(prs.slide_layouts[1])
                                    newSlide.shapes.title.text = originalTitle

                                    for shape in slide.shapes:
                                        if not shape.has_text_frame:
                                            continue
                                        new_shape = newSlide.placeholders[1]
                                        new_paragraph = new_shape.text_frame.add_paragraph()
                                        values_only = list(item.values()) if isinstance(item, dict) else [str(item)]
                                        new_paragraph.text = ', '.join(map(str, values_only))
                                        new_paragraph.font.size = Pt(contentFontSize)

                                    # Sposta la nuova slide appena creata nella posizione desiderata
                                    move_slide(prs, len(prs.slides) - 1, insert_after)
                        paragraphIndex += 1
                        continue
                    elif value is not None:
                        paragraph.clear()
                        paragraph.text = str(value)
                        if originalText == "<#titolo_lezione#>":
                            paragraph.font.size = Pt(titleFontSize)
                            paragraph.font.color.rgb = RGBColor(*titleFontColor)

                    else:
                        print(f"Nessun valore trovato per il tag '{originalText}'")
                else:
                    # Processing per qualsiasi altro paragrafo senza tag specifico
                    pass  # Mantieni eventuali altre logiche di processamento

                paragraphIndex += 1

        slideIndex += 1

    prs = cleanup_presentation(prs)
    prs.save(outputPPTX)


if __name__ == "__main__":
    formatting_file = "formatting.json"
    template_pptx = "LayoutLezioneSimulata.pptx"
    json_file = "progettazione_finale.json"
    output_pptx = "lezioneSimulata.pptx"

    # Load JSON data from file
    try:
        with open(json_file, 'r') as f_json:
            json_data = json.load(f_json)  # Correctly load JSON data from file
    except FileNotFoundError:
        print(f"Error: File {json_file} not found.")
        exit(1)  # Exit if the JSON file cannot be found
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {json_file}: {e}")
        exit(1)  # Exit if there's a JSON parsing error

    # Load formatting data from json file
    try:
        with open(formatting_file, 'r') as f_format:
            formattingData = json.load(f_format)  # Load formatting data
    except FileNotFoundError:
        print(f"Error: File {formatting_file} not found.")
        exit(1)  # Exit if the JSON file cannot be found
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {formatting_file}: {e}")
        exit(1)  # Exit if there's a JSON parsing error

    replaceTag("LayoutLezioneSimulata.pptx", loadJsonData("progettazione_finale.json"), formattingData, "lezioneSimulata.pptx")
    Utility_last.replaceTag('LayoutPrerequisiti.pptx',
                            loadJsonData("esposizione.json"),
                            formattingData, "verificaPrerequisiti.pptx")
    insert_slides_at_tag("lezioneSimulata.pptx",
                         "verificaPrerequisiti.pptx",
                         "lezioneSimulata.pptx",
                         "{{{verificaPrerequisiti.pptx}}}")
    Utility_last.replaceTag('LayoutNucleoCentrale.pptx',
                            loadJsonData("esposizione.json"),
                            formattingData, "nucleoCentrale.pptx")
    insert_slides_at_tag("lezioneSimulata.pptx",
                         "nucleoCentrale.pptx",
                         "lezioneSimulata.pptx",
                         "{{{nucleoCentrale.pptx}}}")
    remove_slide_with_tag("lezioneSimulata.pptx",
                          "lezioneSimulata.pptx", "{{{compitoProdotto.pptx}}}")

    replaceTag("LayoutAttivita.pptx",
               loadJsonData("riepilogo.json"),
               formattingData,
               "riepilogoAttivita.pptx")
    insert_slides_at_tag("lezioneSimulata.pptx",
                         "riepilogoAttivita.pptx",
                         "lezioneSimulata.pptx",
                         "{{{riepilogoAttivita.pptx}}}")




