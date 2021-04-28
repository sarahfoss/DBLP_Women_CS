# -*- coding: utf-8 -*-
"""

@author: Sarah Foss
 Using Wikipedia's definition of Computer Science fields, generate a
 dataset comprising of each field and content strings about each field.
 
 Clean the content strings by setting to lowercase, removing URLs, 
 removing non-alphabetic characters, removing stop words,
 stemming, and discarding any string less than 20 characters.

Source of data: https://en.wikipedia.org/wiki/Outline_of_computer_science

"""


import wikipedia
import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
nltk.download('stopwords')

# function to remove URLs from a string
def remove_urls(text):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(r'', text)

# function to remove stop-words from a string containing 1 or more words
stop_words = set(stopwords.words('english')) 
def remove_stopwords(text):
    return " ".join([word for word in str(text).split() if word not in stop_words])

# function to stem word from a string containing 1 or more words
stem = PorterStemmer()
def stem_words(text):
    return " ".join([stem.stem(word) for word in text.split()])

# fields will be used as lables for classification
# subfields are used as titles to scrap Wikipedia pages

fields = {}
fields['Mathematical foundations'] = {
'Coding theory':"Useful in networking and other areas where computers communicate with each other.",
'Game theory':"Useful in artificial intelligence and cybernetics.",
'Discrete Mathematics':"",
'Graph theory':"Foundations for data structures and searching algorithms.",
'Mathematical logic':"Boolean logic and other ways of modeling logical queries; the uses and limitations of formal proof methods",
'Number theory':"Theory of the integers. Used in cryptography as well as a test domain in artificial intelligence."
}
fields['Algorithms and data structures'] = {
'Algorithms':"Sequential and parallel computational procedures for solving a wide range of problems.",
'Data structures':"The organization and manipulation of data."
}
fields['Artificial intelligence']= {
'Artificial intelligence':"The implementation and study of systems that exhibit an autonomous intelligence or behavior of their own.",
'Automated reasoning':"Solving engines, such as used in Prolog, which produce steps to a result given a query on a fact and rule database, and automated theorem provers that aim to prove mathematical theorems with some assistance from a programmer.",
"Vision computer":"Algorithms for identifying three-dimensional objects from a two-dimensional picture.",
'Soft computing':"the use of inexact solutions for otherwise extremely difficult problems:",
'Learning Machine':"Automated creation of a set of rules and axioms based on input.",
'Evolutionary computing':"Biologically inspired algorithms.",
'Natural language processing':"Building systems and algorithms that analyze, understand, and generate natural (human) languages.",
'Robotics':"Algorithms for controlling the behaviour of robots."
}
fields['Communication and security']= {
'Computer network':"Algorithms and protocols for reliably communicating data across different shared or dedicated media, often including error correction.",
'Computer security':"Practical aspects of securing computer systems and computer networks.",
'Cryptography':"Applies results from complexity, probability, algebra and number theory to invent and break codes, and analyze the security of cryptographic protocols."
}
fields['Computer architecture']= {
'Computer architecture':"The design, organization, optimization and verification of a computer system, mostly about CPUs and Memory subsystem (and the bus connecting them).",
'Operating systems':"Systems for managing computer programs and providing the basis of a usable system."
}
fields['Computer graphics']= {
'Computer graphics':"Algorithms both for generating visual images synthetically, and for integrating or altering visual and spatial information sampled from the real world.",
'Image processing':"Determining information from an image through computation.",
'Information visualization':"Methods for representing and displaying abstract data to facilitate human interaction for exploration and understanding."
}
fields['Concurrent, parallel, and distributed systems']= {
'Parallel computing':"The theory and practice of simultaneous computation; data safety in any multitasking or multithreaded environment.",
'Concurrent computing':"Computing using multiple concurrent threads of execution, devising algorithms for solving problems on multiple processors to achieve maximal speed-up compared to sequential execution.",
'Distributed computing':"Computing using multiple computing devices over a network to accomplish a common objective or task and thereby reducing the latency involved in single processor contributions for any task."
}
fields['Databases']= {
'Relational databases':"the set theoretic and algorithmic foundation of databases.",
'Structured Storage':"non-relational databases such as NoSQL databases.",
'Data mining':"Study of algorithms for searching and processing information in documents and databases; closely related to information retrieval."
}
fields['Programming languages and compilers']= {
'Compiler theory':"Theory of compiler design, based on Automata theory.",
'Programming language pragmatics':"Taxonomy of programming languages, their strength and weaknesses. Various programming paradigms, such as object-oriented programming.",
'Programming language theory':"",
'Semantics Computer Science':"rigorous mathematical study of the meaning of programs.",
'Type theory':"Formal analysis of the types of data, and the use of these types to understand properties of programs — especially program safety."
}
fields['Scientific computing']= {
'Computational science':"constructing mathematical models and quantitative analysis techniques and using computers to analyze and solve scientific problems.",
'Numerical analysis':"Approximate numerical solution of mathematical problems such as root-finding, integration, the solution of ordinary differential equations; the approximation of special functions.",
'Symbolic computation':"Manipulation and solution of expressions in symbolic form, also known as Computer algebra.",
'Computational physics':"Numerical simulations of large non-analytic systems",
'Computational chemistry':"Computational modelling of theoretical chemistry in order to determine chemical structures and properties",
'Bioinformatics and Computational biology':"The use of computer science to maintain, analyse, store biological data and to assist in solving biological problems such as Protein folding, function prediction and Phylogeny.",
'Computational neuroscience':"Computational modelling of neurophysiology."
}
fields['Software engineering']= {
'Formal methods':"Mathematical approaches for describing and reasoning about software design.",
'Software engineering':"The principles and practice of designing, developing, and testing programs, as well as proper engineering practices.",
'Algorithm design':"Using ideas from algorithm theory to creatively design solutions to real tasks.",
'Computer programming':"The practice of using a programming language to implement algorithms.",
'Human–computer interaction':"The study and design of computer interfaces that people use.",
'Reverse engineering':"The application of the scientific method to the understanding of arbitrary existing software."
}
fields['Theory of computation']= {
'Automata theory':"Different logical structures for solving problems.",
'Computability theory':"What is calculable with the current models of computers. Proofs developed by Alan Turing and others provide insight into the possibilities of what may be computed and what may not.",
'Computational complexity theory':"Fundamental bounds (especially time and storage space) on classes of computations.",
'Quantum computing theory':"Explores computational models involving quantum superposition of bits."
}


data = []

for field in fields:
    for subfield in fields[field]:
        # scrap Wikipedia content using subfield titles
        # split all sentences into seperate strings
        description = fields[field][subfield]
        page = wikipedia.page(subfield)
        contentLower = page.content.lower()
        content = contentLower.split('.')
        
        # preprocess the data for classification
        for sentence in content:
            sentence = sentence.strip()
            sentence = remove_urls(sentence)
            sentence = re.sub("[^A-Za-z]+", ' ', sentence)
            sentence = remove_stopwords(sentence)
            sentence = stem_words(sentence)
            
            
            if(len(sentence) > 20):
                info = {
                        "subfield":subfield,
                        "description":description,
                        "field":field,
                        "url":page.url,
                        "content":sentence
                        }
                data.append(info)

df = pd.DataFrame(data)        
df.to_csv('dataset.csv')


