import spacy
from spacy.matcher import Matcher
import multiprocessing as mp
import os
nlp = spacy.load('en_core_web_sm')
matcher = Matcher(nlp.vocab)

absolute_path = os.path.dirname(__file__)
#a=list(D.noun_chunks)

def extract_name(nlp_text, matcher=matcher):
	
    nlp_text=nlp(nlp_text)
    '''
    Helper function to extract name from spacy nlp text

    :param nlp_text: object of `spacy.tokens.doc.Doc`
    :param matcher: object of `spacy.matcher.Matcher`
    :return: string of full name
    '''
    pattern =[{'POS': 'PROPN'}]

    matcher.add('NAME', [pattern])

    matches = matcher(nlp_text)
    

    for _, start, end in matches:
        span = nlp_text[start:end]
        if 'name' not in span.text.lower():
            return span.text

def extract_skilles(text,skills_file=absolute_path+'//'+'a.txt'):
    all_skills=[]
    with open(skills_file,'r') as file:
        skills=file.read()
    for i in skills.split(','):
        if i in text and i not in ['p', 'eve', 'sci']:
            all_skills.append(i)
    return all_skills
            
def get_hotwords(text):
    result = []
    pos_tag = ['PROPN', 'ADJ', 'NOUN'] # 1
    doc = nlp(text.lower()) # 2
    for token in doc:
        # 3
        if(token.text in nlp.Defaults.stop_words):
            continue
        # 4
        if(token.pos_ in pos_tag):
            result.append(token.text)
                
    return result # 5

def extract_adp_experience_2(doc):
    for np in doc.noun_chunks:
        start_tok = np[0].i
        if start_tok >= 2 and doc[start_tok - 2].lower_ == 'experience' and doc[start_tok - 1].pos_ == 'ADP':
            yield 'EXPERIENCE', start_tok, start_tok + len(np)
            
def get_conjugations(tok):
    new = [tok]
    while new:
        tok = new.pop()
        yield tok
        for child in tok.children:
            if child.dep_ == 'conj':
                new.append(child)
                
def get_left_span(tok, label='', include=True):
    offset = 1 if include else 0
    idx = tok.i
    while idx > tok.left_edge.i:
        if tok.doc[idx - 1].pos_ in ('NOUN', 'PROPN', 'ADJ', 'X'):
            idx -= 1
        else:
            break
    return label, idx, tok.i+offset


EXP_TERMS = ['experience']
def extract_adp_conj_experience(doc, label='EXPERIENCE'):
    for tok in doc:
        if tok.lower_ in EXP_TERMS:
            for child in tok.rights:
                if child.dep_ == 'prep':
                    for obj in child.children:
                        if obj.dep_ == 'pobj':
                            for conj in get_conjugations(obj):
                                yield get_left_span(conj, label)

    
#print('name: ',[extract_name('''Hi everyone it's been a long time since you seen this face on this channel so i thought. Introduce myself my name is rosie i'm 21. Even buckinghamshire. My favourite colour is yellow to the sims and i love singing in the shower. I wish i could draw but instead i stick to colouring i do cross stitch. Crochet embroidery. How to make things. Decorating my house to my room with fresh cut flowers. Netflix. My favourite band to the postman wolf as my favourite book and the cross is my. When is this one is this impossible to pick just one. At least a little bit about me i hope your stick around to find out more maybe two. You some more videos and i'll see you again soon bye.''',matcher)])
#print('skills: ',list(set(extract_skilles(text,'a.txt'))))
