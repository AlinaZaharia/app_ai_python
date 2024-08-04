


# pip install pt importuri
# cont la openai API
# generaza cheie API
# environment variable in terminal
    # export OPENAI_API_KEY='cheia_ta'

import openai
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os

client = openai.OpenAI()


# print(os.getenv('OPENAI_API_KEY'))

with open('date.txt', 'r', encoding="utf8") as file:
    text = file.read()
    split_text = text.split('Art.')
    split_text_art = []
    for chunk in split_text:
        chunk = 'Art. ' + chunk
        split_text_art.append(chunk)



# texte = ['ana are mere', 'azi merg la munte']
array_vectori = []
# print(len(split_text_art))

# for propozitie in split_text_art:
#
#     response = client.embeddings.create(
#         input=propozitie,
#         model="text-embedding-3-large"
#     )
#
    # numpy_vectors = np.array(response.data[0].embedding)

    # array_vectori.append(numpy_vectors)
#
# numpy_arr_vectori = np.array(array_vectori)
# print(len(numpy_arr_vectori))
# numpy_texte = np.array(split_text_art)
# print(numpy_texte)
# np.savetxt('vectors.txt', numpy_arr_vectori)
# np.savetxt('texte.txt', numpy_texte, fmt='%s')

def returneaza_top10raspunsuri (string):
    intrebare = string
    print('intrebarea:', intrebare)
    response = client.embeddings.create(
        input=intrebare,
        model="text-embedding-3-large"
    )
    intrebare_embedding = response.data[0].embedding
    numpy_arr_vectori = np.loadtxt('vectors.txt', dtype='float')
    # print(len(numpy_arr_vectori))
    # numpy_arr_texte = np.loadtxt('texte.txt', dtype='str')
    # print('arr_numpy', numpy_arr_texte)
    with open ('texte.txt', 'r') as file:
        text_art = file.readlines()
        # print(text_art)
    text_art_ok = []
    for element in text_art:
        element_nou = element.replace('\n', '')
        text_art_ok.append(element_nou)
    # print('arr cu articole', text_art_ok)

    similarity_scores = cosine_similarity([intrebare_embedding], numpy_arr_vectori)
    print(type(similarity_scores), len(similarity_scores[0]))
    arr_obiecte_scores = []
    counter = 0
    for item in similarity_scores[0]:
        obiect = {}
        obiect['score'] = item
        obiect['indice'] = counter
        counter += 1
        arr_obiecte_scores.append(obiect)
    # print(arr_obiecte_scores)

    sorted_list = sorted(arr_obiecte_scores, key=lambda x: x['score'], reverse=True)
    print("Asta e noua lista sortata", sorted_list)

    top_10_indices = []
    for obj in sorted_list[:10]:
        if obj['score'] > 0.35:
            top_10_indices.append(obj['indice'])

    print('top 10', top_10_indices)


    arr_rez = []
    for indice in top_10_indices:
        arr_rez.append(text_art_ok[indice])
    # print('arr cu texte top 10', arr_rez)
    return arr_rez

    # print("Indices of the highest 10 scores:", top_10_indices)
intrebare_client = "Cand se publica Monitorul Oficial?"


# print(rez_final)


# print('ASTA ESTE REZULTATUL', rez_final_string)
# # Get the index of the most similar document
# most_similar_index = np.argmax(similarity_scores)
# print(text_art_ok[most_similar_index])

# # Retrieve and display the most similar vector
#most_similar_vector = document_vectors[most_similar_index]

# with open('vector.txt', 'w') as file:
#     file.write(response.data[0].embedding)



def returneaza_raspuns_final (intrebare_client, este_titlu):
    try:
        rez_final = returneaza_top10raspunsuri(intrebare_client)
        print('intrebare client', intrebare_client)
        print('top10', rez_final)
        rez_final_string = ",".join(rez_final)
        print('AAA', rez_final_string)
        content = ''
        if este_titlu == True:
            content = 'Generează un titlu descriptiv și informativ care să reflecte corect conținutul și să atragă cititorii interesați de Codul penal roman. Titlul trebuie să includă cuvinte-cheie relevante și să indice faptul că articolul va aborda atât explicații despre infracțiune, cât și consecințele legale. '
        else:
            content = 'Esti un specialist in drept. Transmiti catre user raspunsuri doar din contextul dat. Nu transmiti informatii suplimentare. Maxim 150 de cuvinte.'
        response = client.chat.completions.create(
            model="gpt-4o-mini",

            messages=[
                {"role": "system",
                 "content": content},
                {"role": "user", "content": f"[INTREBARE]{intrebare_client} context: [CONTEXT]{rez_final_string}"},
            ],
            temperature=0.2,
            stream = True
        )
        # print(response)
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                response_text = chunk.choices[0].delta.content + "[ss]"
                # print(response_text)
                yield response_text
        # if response_text:
        #     # Return the response text
        #     return response_text

    except Exception as e:
        print(f"An error occurred: {e}")
        return {"status": False, "error": "Something went wrong"}

        # return response.choices[0].message.content
    # print(returneaza_raspuns_final(intrebare_client))