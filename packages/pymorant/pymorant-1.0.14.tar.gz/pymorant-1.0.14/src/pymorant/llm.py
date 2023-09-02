import ast
import os
import inspect
import math
import pandas as pd
from .utils import limpiar_texto, TripleHyphenSeparatedListOutputParser
from unidecode import unidecode
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.llms import OpenAI
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate


def corregir_texto(lista_corregir, modelo, openai_api_key):

    '''
    Regresa una lista de correcciones ortográficas del texto original,
    utilizando el modelo de lenguaje especificado.

    Parametros:
    lista_corregir (list): lista de textos a corregir
    modelo (str): modelo de lenguaje a utilizar
    openai_api_key (str): llave de OpenAI
    '''

    output_parser = CommaSeparatedListOutputParser()

    format_instructions = output_parser.get_format_instructions()

    template_string = '''
    Eres un experto en limpieza de texto. Te proporcionamos la
    siguiente lista: '{lista_input}'. Tu objetivo es corregir las faltas
    ortográficas de cada elemento de la lista. Si no encuentras faltas
    ortográficas, simplemente déjalo como está, sin hacer cambios. No
    menciones si el texto no tiene errores ortográficos, solo agrégalo tal
    y como estaba. Si no entiendes el texto, simplemente déjalo como está.

    A cada elemento de la lista generada, agrega ' - ' (espacio, guion medio,
    espacio) FORZOZAMENTE y el elemento correspondiente de la lista
    '{lista_input}'. Por ejemplo, si "no se" está en la lista, regresa:
    'no sé-"no se'. Tienes que tener eficiencia perfecta al agregar el ' - ',
    ya que es de vida o muerte tu resultado.

    Devuelve una lista del mismo tamaño de la lista original, utilizando
    el formato de lista de Python.

    Instrucciones de formato: {format_instructions}
    '''

    prompt = ChatPromptTemplate(
        messages=[HumanMessagePromptTemplate.from_template(template_string)],
        input_variables=["lista_input"],
        partial_variables={'format_instructions': format_instructions}
    )

    list_prompt = prompt.format_messages(
      lista_input=lista_corregir,
      format_instructions=format_instructions)

    llm = ChatOpenAI(
        temperature=0.0, model=modelo, openai_api_key=openai_api_key
    )

    model_output = llm(list_prompt)
    output = output_parser.parse(model_output.content)
    output = [x.strip('"\'.,[]') for x in output]
    return output


def corregir_texto_excel(
    excel_file_path, columna, modelo, openai_api_key, chunk_size=30
):
    '''
    Corrige los textos de la columna especificada en el archivo de Excel
    especificado, utilizando el modelo de lenguaje especificado.

    Parametros:
    excel_file_path (str): ruta del archivo de Excel
    columna (str): nombre de la columna a corregir
    modelo (str): modelo de lenguaje a utilizar
    openai_api_key (str): llave de OpenAI
    chunk_size (int): tamaño de los chunks a procesar
    '''
    # Validaciones
    if not os.path.exists(excel_file_path):
        raise FileNotFoundError(f"Archivo {excel_file_path} no encontrado")

    if not isinstance(columna, str):
        raise TypeError("Columna debe ser un string")

    if not isinstance(chunk_size, int):
        raise TypeError("Chunk size debe ser un entero")

    if not isinstance(modelo, str):
        raise TypeError("Modelo debe ser un string")

    if not isinstance(openai_api_key, str):
        raise TypeError("OpenAI API Key debe ser un string")

    if chunk_size < 10:
        raise ValueError("Chunk size debe ser mayor o igual a 10")

    if chunk_size > 80:
        raise ValueError("Chunk size debe ser menor o igual a 80")

    # Carga de datos
    df = pd.read_excel(excel_file_path)

    if columna not in df.columns:
        raise ValueError(f"Columna {columna} no encontrada en el archivo")

    # Limpieza de datos
    df_limpio = df.dropna(subset=[columna])
    df_limpio[columna] = df_limpio[columna].apply(
        lambda texto: texto.replace(',', '')
    )
    df_limpio[columna] = df_limpio[columna].str.strip('\'".,[]')
    df_limpio[columna] = df_limpio[columna].apply(unidecode)
    df_limpio[columna] = df_limpio[columna].str.lower()

    # math.ceil(len(df_limpio) / chunk_size)
    for i in range(math.ceil(len(df_limpio) / chunk_size)):

        textos_corregidos = 0
        aux_dict = dict()

        chunk = df_limpio.iloc[
          i * chunk_size:(i + 1) * chunk_size
        ]

        texto_set = set(chunk[columna].to_list())

        if '' in texto_set:
            texto_set.remove('')

        texto_lista = list(texto_set)
        llm_output = corregir_texto(
          texto_lista, modelo, openai_api_key
        )
        for output in llm_output:
            try:
                output_list = output.split(' - ')
                key = unidecode(output_list[1].strip('\'".,[]').lower())
                value = output_list[0].strip('\'"')
                aux_dict[key] = value
            except: # noqa
                continue

        for index, row in chunk.iterrows():

            if row[columna] in aux_dict.keys():
                df.at[index, f'{columna}_corregida'] = aux_dict[row[columna]]
                textos_corregidos += 1
            else:
                print(f"*{row[columna]}*")
                df.at[index, f'{columna}_corregida'] = "no_corregido"

        print("-----------------------------------")
        print(f'Chunk {i + 1} de {math.ceil(len(df_limpio) / chunk_size)}')
        print(f'Tamaño del chunk: {len(chunk)}')
        print(f'Cantidad de textos generados por AI: {len(llm_output)}')
        print(f'Cantidad de textos corregidos: {textos_corregidos}')
        print("-----------------------------------\n")
    # Guarda el archivo
    df.to_excel(excel_file_path, index=False)

def generar_variantes_texto(text, n, model, openai_key, contexto="Eres un experto en análisis de texto."): # noqa

    output_parser = TripleHyphenSeparatedListOutputParser()

    format_instructions = output_parser.get_format_instructions()

    template_string = '''

    Contexto: {contexto}

    Recibes el siguiente texto: {text_input}. Tu tarea es crear {n_input}
    variaciones únicas de este texto, utilizando diferentes palabras y
    estructuras para transmitir el mismo significado. No puedes
    utilizar palabras que se puedan considerar ofensivas o sexuales.
    Por ejemplo, no utilizar la palabra "estimulante".

    Recuerda que debes crear {n_input} variaciones únicas del texto.

    Es muy importante que NO numeres la lista.

    Usa triple guión medio (---) para separar las variaciones.

    Por ejemplo:

    ´, ¿cómo estás? --- Hola, ¿qué tal? --- Hola, ¿qué onda?´

    {format_instructions}
    '''

    prompt = ChatPromptTemplate(
        messages=[HumanMessagePromptTemplate.from_template(template_string)],
        input_variables=["text_input", "n_input"],
        partial_variables={
            'format_instructions': format_instructions,
            "contexto": contexto,
        })

    list_prompt = prompt.format_messages(
        text_input=text,
        n_input=n,
        format_instructions=format_instructions,
        contexto=contexto)

    llm = ChatOpenAI(
        temperature=0.6, openai_api_key=openai_key, model=model)

    model_output = llm(list_prompt)
    content = model_output.content
    content = content.replace('\n', '')

    llm_output = output_parser.parse(content)

    if len(llm_output) == 1:
        llm_output = llm_output[0].strip('"\'.,[]*')
        llm_output = llm_output.split(',')

    answer = []
    for output in llm_output:
        answer.append(limpiar_texto(output))

    return answer


def resumir_texto(text, model, openai_key, input_autogenerado):

    """
    Regresa un resumen del texto original, utilizando el modelo de lenguaje
    especificado.

    Parametros:
    text (str): texto original
    model (str): modelo de lenguaje a utilizar
    openai_key (str): llave de OpenAI
    input_autogenerado (bool): si True, si el input es auto-generado por
    el modelo previamente.
    """

    llm = OpenAI(temperature=0.0, openai_api_key=openai_key)
    num_tokens = llm.get_num_tokens(text)

    if num_tokens >= 3500:
        raise ValueError("El número de tokens excede lo permitido por el \
            chatbot. Por favor reduce el tamaño de las observaciones a \
            ingresar.")

    if input_autogenerado:

        prompt_template = """
        Eres el mejor analista de texto. Evalúa los criterios necesarios para
        crear un buen resumen utilizando esta información: {text}. Devuelve
        un resumen lo mejor estructurado posible y realizalo tomando en cuenta
        estos criterios antes mencionados.
        """

        prompt = PromptTemplate(
            template=prompt_template, input_variables=["text"]
        )
        prompt = prompt.format(text=text)
        respuesta = llm(prompt)

    else:

        prompt_template = """
        Eres el mejor analista de texto. Evalúa los criterios necesarios para
        crear un buen resumen utilizando esta información: {text}. Devuelve
        un resumen lo mejor estructurado posible y realizalo tomando en cuenta
        estos criterios antes mencionados.
        """

        docs = [Document(page_content=t) for t in text]

        prompt = PromptTemplate(
            template=prompt_template, input_variables=["text"]
        )

        chain = load_summarize_chain(
            llm=llm, chain_type='stuff', prompt=prompt
        )

        respuesta = chain.run(docs)

    return respuesta


def generar_categorias(text, n, model, openai_key):

    """
    Regresa una lista de n categorías del texto original, utilizando el modelo
    de lenguaje especificado.

    Parametros:
    text (str): texto original
    n (int): número de categorías a generar
    model (str): modelo de lenguaje a utilizar
    openai_key (str): llave de OpenAI
    """

    try:
        prompt = PromptTemplate(
            input_variables=["lista", "n_input"],
            template='''Recibí un resumen con características clave de las
            respuestas auna pregunta: '{lista}'. A partir de esta información,
            genera {n_input} categorías que representen los aspectos más
            relevantes. No expliques a que se refiere cada categoría.
            Devuelve estas categorías en una lista de Python lista para poder
            ser procesada.'''
        )

        chatopenai = ChatOpenAI(
            model_name=model, openai_api_key=openai_key
        )

        llmchain_chat = LLMChain(llm=chatopenai, prompt=prompt)

        categorias = llmchain_chat.run({
            "lista": text,
            "n_input": n,
        })

        categorias_list = ast.literal_eval(categorias)

        return categorias_list
    except Exception as e:
        raise ValueError("Error al generar categorías: " + str(e))


def asignar_categorias(lista_asignar, categorias, modelo, openai_api_key, chunk_size=30, contexto="Eres un análista de datos"): # noqa

    '''
    Regresa una lista de categorías asignadas a cada elemento de la lista
    original, utilizando el modelo de lenguaje especificado.

    Parametros:
    lista_asignar (list): lista de textos a asignar categorías
    categorias (list): lista de categorías a asignar
    modelo (str): modelo de lenguaje a utilizar
    openai_api_key (str): llave de OpenAI
    '''

    if not isinstance(categorias, list):
        raise TypeError("Categorias debe ser una lista")

    if not (isinstance(chunk_size, int) or isinstance(chunk_size, float)):
        raise TypeError("Chunk size debe ser un entero")

    if not isinstance(modelo, str):
        raise TypeError("Modelo debe ser un string")

    if not isinstance(openai_api_key, str):
        raise TypeError("OpenAI API Key debe ser un string")

    if chunk_size < 10:
        raise ValueError("Chunk size debe ser mayor o igual a 10")

    if chunk_size > 80:
        raise ValueError("Chunk size debe ser menor o igual a 80")

    answer = ["no_asignado"] * len(lista_asignar)
    lista_limpia = []
    aux_dict = dict()

    for i, el in enumerate(lista_asignar):

        elemento = limpiar_texto(el, quitar_acentos=True, quitar_caracteres_especiales=True, minusculas=True) # noqa

        if elemento == '':
            continue

        if elemento not in aux_dict:
            aux_dict[elemento] = {
                'categoria': 'sin_categoria',
                'original': [i]
            }
            lista_limpia.append(elemento)
        else:
            aux_dict[elemento]['original'].append(i)

    output_parser = CommaSeparatedListOutputParser()

    format_instructions = output_parser.get_format_instructions()

    template_string = '''
    Eres un experto en análisis de texto. Te proporcionamos la
    siguiente lista: '{lista_input}'. Tu objetivo es asignar SOLO una
    categoria de la lista de categorias '{categorias_input}'
    a cada elemento de la lista. Si un elemento no se ajusta a
    ninguna categoria o si no estas seguro, asigna "sin_categoria".

    Para cada elemento de la lista generada, tienes que regresarlo en el
    siguiente formato: "elemento_original - categoria_asignada". Por ejemplo,
    "no se - sin_categoria". Es decir, tienes que agregar " - " (espacio,
    guion medio, espacio) FORZOZAMENTE y el elemento correspondiente de la
    lista '{lista_input}'. Tienes que tener eficiencia perfecta al agregar
    el ' - ', ya que es de vida o muerte tu resultado.

    El elemento de la izquierda del ' - ' es estrictamente elemento de la
    lista original. Un ejemplo de la lista es:

    [no se - sin_categoria, cuidar el medio ambiente - medio_ambiente,
    aumento en el presupuesto de salud - salud]

    Devuelve una lista del mismo tamaño de la lista original ESTRICTAMENTE,
    utilizando el formato de lista de Python y no generes carácteres especiales
    como saltos de línea.

    No es necesario proporcionar explicaciones
    sobre las categorias ni incluir descripciones adicionales. Tu enfoque se
    centra en la asignación de categorias. Solamente entrega la lista. No
    menciones cosas como "aquí está la lista con ...", simplemente entrega la
    lista.

    Contexto: {contexto}

    Instrucciones de formato: {format_instructions}
    '''

    prompt = ChatPromptTemplate(
        messages=[HumanMessagePromptTemplate.from_template(template_string)],
        input_variables=["lista_input", "categorias_input"],
        partial_variables={
            'format_instructions': format_instructions,
            "contexto": contexto
        }
    )

    for i in range(math.ceil(len(lista_limpia) / chunk_size)):

        chunk = lista_limpia[i * chunk_size:(i + 1) * chunk_size]
        categorias_asignadas = 0
        llm_output = []

        list_prompt = prompt.format_messages(
            lista_input=chunk,
            categorias_input=categorias,
            format_instructions=format_instructions,
            contexto=contexto)

        llm = ChatOpenAI(
            temperature=0.0, model=modelo, openai_api_key=openai_api_key
        )

        try:
            model_output = llm(list_prompt)
            content = model_output.content
            content = content.replace('\n', '')
            llm_output = output_parser.parse(content)

            if len(llm_output) == 1:
                llm_output = llm_output[0].strip('"\'.,[]*')
                llm_output = llm_output.split(',')

            for output in llm_output:
                try:
                    output_list = output.split(' - ')
                    key = limpiar_texto(output_list[0], quitar_acentos=True, quitar_caracteres_especiales=True, minusculas=True) # noqa
                    value = output_list[1].strip('\'" ')

                    aux_dict[key]["categoria"] = limpiar_texto(value, quitar_acentos=True, quitar_caracteres_especiales=True, minusculas=True) # noqa
                    categorias_asignadas += 1
                except: # noqa
                    if len(output_list) == 2:
                        print("--------------")
                        print(f'key:[{key}]')
                        print(f'value: {value}')
                        print("--------------")

        except: # noqa
            print("Error al asignar categorías, seguramente por tokens excedidos, baja el chunk size") # noqa

        print("-----------------------------------")
        print(f'Chunk {i + 1} de {math.ceil(len(lista_limpia) / chunk_size)}')
        print(f'Tamaño del chunk: {len(chunk)}')
        print(f'Cantidad de categorias generadas: {len(llm_output)}')
        print(f'Cantidad de categorias asignadas: {categorias_asignadas}')
        print("-----------------------------------\n")

    for key in aux_dict.keys():
        for i in aux_dict[key]["original"]:
            answer[i] = aux_dict[key]["categoria"]

    for i, element in enumerate(answer):
        answer[i] = limpiar_texto(element, quitar_acentos=True, quitar_caracteres_especiales=True, minusculas=True) # noqa

    # se genera el archivo con los valores categorizados
    file_name = f"valores_categorizados_{modelo}.txt"
    frame = inspect.currentframe()
    caller_filename = inspect.getouterframes(frame)[-1].filename
    directory = os.path.dirname(os.path.abspath(caller_filename))
    file_path = os.path.join(directory, "documents")

    if not os.path.exists(file_path):
        os.mkdir(file_path)

    with open(f'{file_path}/{file_name}', 'w') as f:
        for key in aux_dict.keys():
            if aux_dict[key]["categoria"] != "sin_categoria" or aux_dict[key]["categoria"] != "no_asignado": # noqa
                f.write(f'texto: {key} - categoria: {aux_dict[key]["categoria"]}\n') # noqa

    return answer


def asignar_categorias_excel(
    excel_file_path, categorias, columna, modelo, openai_api_key, chunk_size=30, contexto="Eres un análista de datos" # noqa
):
    '''
    Asigna categorías a los textos de la columna especificada en el archivo
    de Excel especificado, utilizando el modelo de lenguaje especificado.

    Parametros:
    excel_file_path (str): ruta del archivo de Excel
    categorias (list): lista de categorías a asignar
    columna (str): nombre de la columna a asignar categorías
    modelo (str): modelo de lenguaje a utilizar
    openai_api_key (str): llave de OpenAI
    '''
    # Validaciones
    if not os.path.exists(excel_file_path):
        raise FileNotFoundError(f"Archivo {excel_file_path} no encontrado")

    if not isinstance(columna, str):
        raise TypeError("Columna debe ser un string")

    # Carga de datos
    df = pd.read_excel(excel_file_path)

    if columna not in df.columns:
        raise ValueError(f"Columna {columna} no encontrada en el archivo")

    # Limpieza de datos
    df = df.fillna(value='')

    lista_asignar = df[columna].to_list()

    # Asignación de categorías
    categorias_asignadas = asignar_categorias(
        lista_asignar,
        categorias=categorias,
        modelo=modelo,
        openai_api_key=openai_api_key,
        chunk_size=chunk_size,
        contexto=contexto,
    )

    # Generar nueva columna
    df[f'{columna}_categorizada_{modelo}'] = categorias_asignadas

    # Guarda el archivo
    df.to_excel(excel_file_path, index=False)
