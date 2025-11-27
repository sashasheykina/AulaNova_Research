import json
from pptx import Presentation
from pptx.util import Pt
import copy

from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE_TYPE

from merge_slides import insert_slides_at_tag


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

def duplicate_slide(pres, template):
    import io
    # Add a new slide
    copied_slide = pres.slides.add_slide(template.slide_layout)
    
    # Delete the existing shapes that are part of the layout
    for shp in copied_slide.shapes:
        copied_slide.shapes.element.remove(shp.element)        
    
    # Perform a deep copy of the shapes from the template
    for shp in template.shapes:
        if "Picture" in shp.name:
            img = io.BytesIO(shp.image.blob)
            copied_slide.shapes.add_picture(image_file = img,
                                            left = shp.left,
                                            top = shp.top,
                                            width = shp.width,
                                            height = shp.height)
        else:
            el = shp.element
            newel = copy.deepcopy(el)
            copied_slide.shapes._spTree.insert_element_before(newel, 'p:extLst')
 
    return copied_slide

def clone_slide(prs, slide):
    return duplicate_slide(prs,slide)

def clone_slide_(prs, slide):
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

def handle_slide_to_duplicate(jsonData, contentFontSize, paragraph, values_list, prs, slideIndex, slide, remove=True):
    old_val = paragraph.text
    paragraph.clear()  # Rimuove il paragrafo contenente il tag

    to_remove = set()
    print("HANLDE SLIDE DUPLICATION", slideIndex)
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
                        print("TAGNAME handle_slide_to_duplicate", tag_name)
                        if tag_name.startswith("$$LISTA."):
                            tag_name = tag_name[8:]
                            tag_value = getJsonData(value, tag_name.strip())
                        else:
                            tag_value = getJsonData(jsonData, tag_name)

                        print("CON TAGVALUE handle_slide_to_duplicate", tag_value)
                        if tag_value is None:
                            # Vediamo se il padre era una lista e qui si sta facendo riferimento ad un attributo del dict figlio
                            parentKey = get_parent_key(tag_name)
                            if parentKey:
                                val = getJsonDataRec(jsonData, parentKey)
                                if val:
                                    k = get_leaf_key(tag_name)
                                    create_bullet_list(val, k, new_shape, contentFontSize)
                        elif isinstance(tag_value, str):
                            #VEDI
                            #new_para.text += str(tag_value or "") + rest_of_text
                            replace_paragraph_text_retaining_initial_formatting(new_para, str(tag_value or "") + rest_of_text)
                        else:
                            # Se il padre dell'elemento ha un attributo type
                            parentKeyType = get_parent_key(tag_name)+".type"
                            typeValue = getJsonData(tag_value, parentKeyType)
                            if typeValue == 1: # Elenco puntato
                                create_bullet_list(tag_value, None, new_shape, contentFontSize)
                            else:
                                #VEDI
                                val = str(tag_value)
                                #new_para.text += str(tag_value or "") + rest_of_text
                                replace_paragraph_text_retaining_initial_formatting(new_para, str(tag_value or "") + rest_of_text)
                    else:
                        #VEDI
                        #new_para.text += part
                        replace_paragraph_text_retaining_initial_formatting(new_para, part)

        if remove:
            move_slide(prs, len(prs.slides) - 1, slideIndex + 1 + i)
        else:
            to_remove.add(slideIndex)

    if remove:
        rId = prs.slides._sldIdLst[slideIndex].rId
        prs.part.drop_rel(rId)
        del prs.slides._sldIdLst[slideIndex]
    else:
        paragraph.text = old_val
    print("FINE HANDE SLIDE DUPLICATION==>")
    return to_remove

def replace_paragraph_text_retaining_initial_formatting(paragraph, new_text):
    if paragraph.runs:
        font = copy.deepcopy(paragraph.runs[0].font)
    else:
        font = None
    paragraph.text = new_text
    if font:
        for run in paragraph.runs:
            run._r.insert(0, copy.deepcopy(font._rPr))

def cleanup_presentation(prs):
    from pptx.opc.packuri import PackURI
    for i, slide in enumerate(prs.slides, 1):
        new_partname = PackURI(f'/ppt/slides/slide{i}.xml')
        slide.part.partname = new_partname
    return prs

def replaceTag(layoutPPTX, jsonData, formattingData, outputPPTX, insert_position=17):
    prs = Presentation(layoutPPTX)

    # Impostazioni di formattazione dal file JSON
    titleFontSize = getJsonData(formattingData, 'titleFontSize')
    contentFontSize = getJsonData(formattingData, 'contentFontSize')
    titleFontColor = getJsonData(formattingData, 'titleFontColor')
    contentFontColor = getJsonData(formattingData, 'contentFontColor')

    nested_loop = False

    slideIndex = 0
    while slideIndex < len(prs.slides):
        slide = prs.slides[slideIndex]
        found = False
        for shapeIndex, shape in enumerate(slide.shapes):
            if not shape.has_text_frame:
                continue
            paragraphs = shape.text_frame.paragraphs
            for p in paragraphs:
                originalText = p.text.strip()
                if originalText.startswith("{##") and originalText.endswith("##}"):
                    nested_loop = True
                    break
                if originalText.startswith("{#") and originalText.endswith("#}"):
                    found = True
                    break
        if nested_loop:
            print("TROVATO ====>")
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
                    value = getJsonData(jsonData, key)

                    if isinstance(value, list):
                        
                        typeKeyPath = key.rsplit('.', 1)[0] + '.type'
                        typeValue = getJsonData(jsonData, typeKeyPath)
                        if typeValue == 1: # Elenco puntato
                            paragraph.clear()
                            create_bullet_list(value, None, shape,contentFontSize, True)
                            #print(f"Sostituito il tag '{originalText}' con un elenco numerato")
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

    if nested_loop:
        print("PROCESSO NESTED LOOP", slideIndex)
        process_nested_loop(prs, jsonData, contentFontSize, formattingData, slideIndex)
    prs = cleanup_presentation(prs)
    prs.save(outputPPTX)


def handle_slide_to_duplicate_nested(jsonData, contentFontSize, paragraph, values_list, prs, slideIndex, slide, formattingData):
    paragraph.clear()  # Rimuove il paragrafo contenente il tag
    print("HANLDE SLIDE DUPLICATION NESTED")
    to_remove = set()
    first = True
    for i, value in enumerate(values_list):
        print("INDICE LISTA PRINCIPALE", i)
        new_slide = clone_slide(prs, slide)

        for new_shape in new_slide.shapes:
            if not new_shape.has_text_frame:
                continue

            new_paragraphs = new_shape.text_frame.paragraphs
            for new_para in new_paragraphs:
                para_text = new_para.text
                parts = para_text.split('<#')
                #VEDI
                #new_para.text = parts[0]
                replace_paragraph_text_retaining_initial_formatting(new_para, parts[0])

                for part in parts[1:]:
                    if '#>' in part:
                        tag_name, rest_of_text = part.split('#>', 1)
                        print("TAGNAME handle_slide_to_duplicate_nested", tag_name)
                        if tag_name.startswith("$$LISTA."):
                            tag_name = tag_name[8:]

                            tag_value = getJsonData(value, tag_name.strip())
                        else:
                            tag_value = getJsonData(jsonData, tag_name)

                        print("TAG VALUE handle_slide_to_duplicate_nested", tag_value)
                        if tag_value is None:
                            # Vediamo se il padre era una lista e qui si sta facendo riferimento ad un attributo del dict figlio
                            parentKey = get_parent_key(tag_name)
                            print("PARENT KEY ===> handle_slide_to_duplicate_nested", parentKey)
                            if parentKey:
                                val = getJsonDataRec(jsonData, parentKey)
                                if val:
                                    k = get_leaf_key(tag_name)
                                    create_bullet_list(val, k, new_shape, contentFontSize)
                        elif isinstance(tag_value, str):
                            # VEDI
                            #new_para.text += str(tag_value or "") + rest_of_text
                            replace_paragraph_text_retaining_initial_formatting(new_para, str(tag_value or "") + rest_of_text)
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
                        #VEDI
                        #new_para.text += part
                        replace_paragraph_text_retaining_initial_formatting(new_para, part)

        # Dopo aver duplicato la slide chiamiamo nuovamente _replaceTag_main_logic
        
        start = slideIndex + 1 + i
        end = len(prs.slides) - 1
        print("VADO ALLA SLIDE", slideIndex + 1 , "SLIDE CORRENTE", slideIndex)
        res = _replaceTag_main_logic(prs, value, formattingData, slideIndex + 1) # + i)
        if res:
            to_remove.update(res)

        if first:
            #move_slide(prs, end, start)
            first = False


    to_remove.add(slideIndex)
    return to_remove

def _replaceTag_main_logic(prs, jsonData, formattingData, slideIndex = 0):
    # Impostazioni di formattazione dal file JSON
    titleFontSize = getJsonData(formattingData, 'titleFontSize')
    contentFontSize = getJsonData(formattingData, 'contentFontSize')
    titleFontColor = getJsonData(formattingData, 'titleFontColor')

    to_remove = set()

    to_break = False
    slide = prs.slides[slideIndex]
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
            if originalText.startswith("{##") and originalText.endswith("##}"):
                print("TROVATO MAIN TAG")
                # Qui duplichiamo la slide, ma poi eseguiamo un loop per le slide successive
                # tante volte per quanti sono gli elementi della lista {##lista##}
                key = originalText[3:-3]
                values_list = getJsonData(jsonData, key)
                if isinstance(values_list, list):
                    res = handle_slide_to_duplicate_nested(jsonData, contentFontSize, paragraph, values_list, prs, slideIndex, slide, formattingData)
                    if res:
                        to_remove.update(res)
                    break  # Esci dal ciclo dei paragrafi
            elif originalText.startswith("{#") and originalText.endswith("#}"):
                print("TROVATO TAG DUPLICA in _replaceTag_main_logic")
                key = originalText[2:-2]
                values_list = getJsonData(jsonData, key)
                #print("KEY, VALUE",key, values_list)
                if isinstance(values_list, list):
                    res = handle_slide_to_duplicate(jsonData, contentFontSize, paragraph, values_list, prs, slideIndex, slide, False)
                    if res:
                        to_remove.update(res)
                    to_break = True
                    break  # Esci dal ciclo dei paragrafi
                print("CAPITA===>")
            elif originalText.startswith("<#") and originalText.endswith("#>"):
                key = originalText[2:-2]
                lista = False
                if key.startswith("$$LISTA."):
                    key = key[8:]
                    key = key.strip()
                    print("IN _replaceTag_main_logic key inizia con LISTA", key)
                    lista = True
                value = getJsonData(jsonData, key)

                if isinstance(value, list):
                    paragraph.clear()
                    create_bullet_list(value, None, shape,contentFontSize, True)
                    paragraphIndex += 1
                    continue
                elif value is not None:
                    #VEDI
                    #paragraph.clear()
                    #paragraph.text = str(value)
                    replace_paragraph_text_retaining_initial_formatting(paragraph, str(value))
                    if originalText == "<#titolo_lezione#>":
                        paragraph.font.size = Pt(titleFontSize)
                        paragraph.font.color.rgb = RGBColor(*titleFontColor)

                else:
                    print(f"Nessun valore trovato per il tag in _replaceTag_main_logic'{originalText} {value}'")
                    #if lista:
                    #    print(jsonData)
            else:
                # Processing per qualsiasi altro paragrafo senza tag specifico
                pass  # Mantieni eventuali altre logiche di processamento

            paragraphIndex += 1
        if to_break:
            break
    return to_remove


def process_nested_loop(prs, jsonData, contentFontSize, formattingData, slideIndex):
    slide = prs.slides[slideIndex]
    to_remove = set()
    for shapeIndex, shape in enumerate(slide.shapes):
        if not shape.has_text_frame:
            continue
            
        paragraphs = shape.text_frame.paragraphs

        paragraphIndex = 0
        while paragraphIndex < len(paragraphs):
            paragraph = paragraphs[paragraphIndex]

            originalText = paragraph.text.strip()
            print(originalText, " nestedloop")
            # Verifica di aver trovato un tag
            if originalText.startswith("{##") and originalText.endswith("##}"):
                #print("TROVATO TAG DUPLICA")
                key = originalText[3:-3]
                values_list = getJsonData(jsonData, key)

                if isinstance(values_list, list):
                    res = handle_slide_to_duplicate_nested(jsonData, contentFontSize, paragraph, values_list, prs, slideIndex, slide, formattingData)
                    if res:
                        to_remove.update(res)
                    break  # Esci dal ciclo dei paragrafi
            paragraphIndex += 1

    print("DA RIMUOVERE", to_remove)
    
    for index in sorted(to_remove, reverse=True):
        if index < len(prs.slides):  # Assicurati che l'indice sia valido
            rId = prs.slides._sldIdLst[index].rId
            prs.part.drop_rel(rId)
            del prs.slides._sldIdLst[index]
    
if __name__ == "__main__":
    template_pptx = "LayoutNucleoCentrale.pptx"
    json_file = "esposizione.json"
    output_pptx = "nucleo.pptx"
    formatting_file = "formatting.json"
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
    
    replaceTag(template_pptx, json_data, formattingData, output_pptx)

