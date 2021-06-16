from CLASSES import *
from graphviz import Digraph


def convertToNumber(listeEtats):
    numbers=[]
    for etat in listeEtats:
        numbers.append(etat.NumEtat)
    return numbers    
        
def InListeOfListe(liste1,ListeOfListe):

    for liste in ListeOfListe:
        if SameListe(liste1,liste):
            return True

    return False
            
        
def SameListe(liste1,liste2):
    if (len(liste1) != len(liste2)):
        return False
    for numero in liste1:
        if numero in liste2:
            pass
        else:
            return False

    return True       
 
        
def SansDoublon(args):
    sorti=[]
    for item in args:
        if item not in sorti:
            sorti.append(item)
    return sorti

def  createEtat(numero,transition):
    dejapresent=[]
    ListeTransition=[]
    liste=transition.split(":")
    symbols=liste[0].split(",")
    destination=liste[1].split(",")
    i=0

    for x in symbols:
        if x in dejapresent:
            j=dejapresent.index(x)
            ListeTransition[j].Destinations.append(destination[i])
        else:
            ListeTransition.append(Transition(x,[destination[i]]))
            dejapresent.append(x)
        i+=1	 
    return Etat(numero,ListeTransition)	

def setInitialAndFinal(listeEtats,listeEtatsPresedente):
    numeroEtatsInitiaux=[]
    numeroEtatsFinaux=[]
    initial=[]

    for etat in listeEtatsPresedente:
        if etat.IsInitial:
            numeroEtatsInitiaux.append(etat.NumEtat) 
        if etat.IsFinale :  
            numeroEtatsFinaux.append(etat.NumEtat) 

    for etat in listeEtats:
        i=0

        for numero in numeroEtatsInitiaux:
            if numero in etat.NumEtat:
                i+=1
        if i == len(etat.NumEtat):
            initial.append(etat)
            etat.setInitial()
                
        for numero  in numeroEtatsFinaux:
            if numero in etat.NumEtat:
                etat.setFinal()
    
    return initial

def printAutomate(automate):
    visualisationAutomate=Digraph(format="pdf")
    #typeAutomate=automate.EstDeterministe()

    for etat  in automate.ListeEtats:
        if etat.IsInitial:
            visualisationAutomate.node(str(etat.NumEtat),label=str(etat.NumEtat),color='green')
        if etat.IsFinale:
            visualisationAutomate.node(str(etat.NumEtat),label=str(etat.NumEtat),shape='doublecircle')
        else:
            visualisationAutomate.node(str(etat.NumEtat),label=str(etat.NumEtat))
    for etat in automate.ListeEtats:
        
        for transition in etat.Transition:
            for suivant in transition.Destinations:
                visualisationAutomate.edge(str(etat.NumEtat),str(suivant),label=transition.Symbole)

    visualisationAutomate.render(filename="TEST", view=True)    

"""PRINT APRES DETERMINISATION"""
def printAutomate2(automate):
    visualisationAutomate=Digraph(format="png")
    #typeAutomate=automate.EstDeterministe()
    
    for etat  in automate.ListeEtats:
        if etat.IsInitial:
            numero=' '.join(str(elem) for elem in sorted(etat.NumEtat))	
            visualisationAutomate.node(str(numero),label=str(numero),color='green')
        if etat.IsFinale:
            final=sorted(etat.NumEtat)
            numero=' '.join(str(elem) for elem in sorted(etat.NumEtat))	
            visualisationAutomate.node(str(numero),label=str(numero),shape='doublecircle')
        else:
            numero=' '.join(str(elem) for elem in sorted(etat.NumEtat))
            visualisationAutomate.node(str(numero),label=str(numero))
        
    for etat  in automate.ListeEtats:
        numero=' '.join(str(elem) for elem in sorted(etat.NumEtat))

        for transition in etat.Transition:
            if type(transition.Destinations)==list:
                dest=' '.join(str(elem) for elem in sorted(transition.Destinations))
                visualisationAutomate.edge(str(numero),str(dest),label=transition.Symbole)
            else:
                
                dest=ordonnement(transition)
                i=0
                for symbole in transition.Symbole:
                    visualisationAutomate.edge(str(numero),str(dest[i]),label=symbole)
                    i+=1

    visualisationAutomate.render(filename="determiniser", view=True)		
