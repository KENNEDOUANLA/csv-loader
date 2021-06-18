from Aide import *
import  copy

#la classe transition
class Transition():
    """docstring for Transition"""
    def __init__(self,symbole,destinations):
        self.Symbole=symbole
        self.Destinations=destinations


 #la classe etat
class Etat():
    """docstring for Etat"""
    def __init__(self,numEtat,transition,isInitial=False,isFinale=False):
        self.NumEtat=numEtat
        self.IsInitial=isInitial
        self.IsFinale=isFinale
        self.Transition=transition

    def setFinal(self):
        self.IsFinale=True

    def setInitial(self):
        self.IsInitial=True   

    def getNextState(self,symbole):
        transitions=self.Transition

        for transition in transitions:
            if symbole == transition.Symbole:
                return transition.Destinations

        return []      
    
    def getTransition(self,symbole):

        for transition in self.Transition:
            if symbole == transition.Symbole:
                return transition.Destinations
        return [-1]	

    def getsymboleDeEtat(self):
        listeSymbole=[]

        for transition  in self.Transition:
            listeSymbole.append(transition.Symbole)

        return listeSymbole

            
        

class Automate():

    def __init__(self,nbEtat,etatsInitiaux,listeEtats):
        self.EtatsInitiaux=etatsInitiaux
        self.ListeEtats=listeEtats
        self.NbEtat=nbEtat

    def ReturnEtat(self,numero):

        for etat in self.ListeEtats:
            if etat.NumEtat==numero:
                return etat
            
        return None 

    def getAllSymbole(self):
        etats=self.ListeEtats
        ListeSymbole=[]

        for etat in etats:
            transitions=etat.Transition

            for transition in transitions:
                symbole=transition.Symbole
                if symbole in ListeSymbole:
                    pass
                else:
                    ListeSymbole.append(symbole) 
                   
        return ListeSymbole       
        
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


    """---------------------------------------LES ALGORITHMES -----------------------------------"""
   
    #TYPE D'AUTOMATE
    def TypeAutomate(self):
        listeSymbole=self.getAllSymbole()
        if 'eps' in listeSymbole:
            return "EPS"
        else:

            for Etat in self.ListeEtats:

                for transition in Etat.Transition:
                    if len(transition.Destinations)>1:
                        return "AFN"

            return "AFD" 

    #RECONNAISSANCE DU MOT
    def reconnaisanceAFD(self,mot):
        if self.TypeAutomate() == "AFD":        
            i=0
            etatActuel=self.EtatsInitiaux[0]
            while i<len(mot) and etatActuel != None:
                destination=etatActuel.getTransition(mot[i])
                
                etatActuel=self.ReturnEtat(destination[0])
                i+=1

            if(etatActuel !=None and etatActuel.IsFinale):return True
            else: return False

        elif self.TypeAutomate() == "EPS":
            self.Construction_des_sous_ensembles().Determinisation().reconnaisanceAFD(mot)

        else:
            self.Determinisation().reconnaisanceAFD(mot)
                 
    # EPS - FERMETURE D'UN ETAT
    def eps_Fermeture(self,etat):
        Listenumero=[etat.NumEtat]
        ListeEtat=[etat]

        while ListeEtat:
            etat=ListeEtat.pop()
            numeroSuivant=etat.getNextState('eps')

            for numero in numeroSuivant:
                if numero not in Listenumero:
                    Listenumero.append(numero)
                    ListeEtat.insert(0,self.ReturnEtat(numero))
        
        return Listenumero              

    #NOUVEAUX AUTOMATE APRES LA SUPPRESSION DES eps-TRANSITIONS   
    def Construction_des_sous_ensembles(self):
        ListeEtatsInit=[]
        ListeSymbole=self.getAllSymbole()
        ListeSymbole.remove("eps")
        ListeEtats=[]

        for etat in self.ListeEtats:
            listeNumero = self.eps_Fermeture(etat)
            dictionnaire={}
            newTransition=[]

            for numero in listeNumero:
                etat2=self.ReturnEtat(numero)
                if etat2.IsFinale:
                    etat.setFinal()
                    
                for symbole in ListeSymbole:
                    liste=etat.getNextState(symbole)
                    liste=liste+etat2.getNextState(symbole)
                    if liste:
                        if symbole in dictionnaire:
                            dictionnaire[symbole]=SansDoublon(dictionnaire[symbole]+liste)
                        else:
                            dictionnaire[symbole]=SansDoublon(liste)

                        liste=[]

            for symbole,liste in dictionnaire.items():
                newTransition.append(Transition(symbole,liste))
            ListeEtats.append(Etat(etat.NumEtat,newTransition,etat.IsInitial,etat.IsFinale))

        for etat in ListeEtats:
            if etat.IsInitial:
                ListeEtatsInit.append(etat)

        return Automate(self.NbEtat,ListeEtatsInit,ListeEtats)                   

    def Determinisation(self):
        if self.TypeAutomate() == "AFN":    
            listeEtats=[] 
            Pile =[self.EtatsInitiaux]
            AutomateDeterminiser=[]
            symboles=self.getAllSymbole()

            while Pile:
                etats=Pile.pop()
                numbers=convertToNumber(etats)
                if numbers:
                    if not InListeOfListe(numbers,AutomateDeterminiser):
                        AutomateDeterminiser.append(numbers)
                        dictionnaire={}
                        symboleExistants=[]
                        transition=[]

                        for symbole in symboles:
                            newNumero=[]
                    
                            for etat in etats:
                                newNumero=newNumero+etat.getNextState(symbole)
                            if newNumero:
                                newNumero=SansDoublon(newNumero)
                                if InListeOfListe(newNumero,AutomateDeterminiser):
                                    transition.append(Transition(symbole,[sorted(newNumero)]))    
                                if not InListeOfListe(newNumero,AutomateDeterminiser):
                                    newNumero = sorted(newNumero)
                                    dictionnaire[symbole]= newNumero
                                    newEtats=[]

                                    for numero in newNumero:
                                        newEtats.append(self.ReturnEtat(numero))
                                    
                                    if newEtats:
                                        Pile.insert(0,newEtats)

                        ListeTransition=[]
                        for key,valeur in dictionnaire.items():
                            ListeTransition.append(Transition(key,[valeur]))
                        if ListeTransition:
                            listeEtats.append(Etat(numbers,ListeTransition))

                        if transition :
                            if ListeTransition:
                                for trans in transition:    
                                    listeEtats[len(listeEtats)-1].Transition.append(trans)
                            else:
                                listeEtats.append(Etat(numbers,transition))  

            liste=setInitialAndFinal(listeEtats,self.ListeEtats) 
            
            for etat in listeEtats:
                print(etat.NumEtat)
                for transition in etat.Transition:
                    print("symbole {} ----->  {}".format(transition.Symbole,transition.Destinations))
                    
                
            return Automate(len(AutomateDeterminiser),liste,listeEtats)                
        else: 
            return self                        
                      
        
    def CompleterAutomate(self):
        ListeSymbole=self.getAllSymbole()
        puisTransition=[]
        entrer=False
        newListeEtats=[]
        EtatInit=[]
        newtransition=[]

        for etat in self.ListeEtats:

            for transition in etat.Transition:
                newtransition.append(transition)
            newListeEtats.insert(0,Etat(etat.NumEtat,newtransition,etat.IsInitial,etat.IsFinale))
            newtransition=[]
            if len(etat.Transition)!= len(ListeSymbole):
                symboleDeEtat=etat.getsymboleDeEtat()


                for symbole in ListeSymbole:
                    if symbole not in symboleDeEtat:
                        newListeEtats[0].Transition.append(Transition(symbole,["puis"]))
                        entrer=True
            
        if entrer:
            for etat in newListeEtats:
                if etat.IsInitial:
                    EtatInit.append(etat)

            for symbole in ListeSymbole:
                puisTransition.append(Transition(symbole,["puis"]))
            newListeEtats.append(Etat("puis",puisTransition))
            return Automate(len(newListeEtats),EtatInit ,newListeEtats)
        else:
            return self    

 #LES  CLOTURES SUR LES AUTOMATES
    def Cloture_par_complementation(self):
        self.CompleterAutomate()

        for etat in self.ListeEtats:
            if etat.IsFinale:
                etat.IsFinale=False
            else:
                etat.setFinal() 

        return self 

    def produit(self,automate):
        listeTotal=[]

        for etat in self.ListeEtats:
            for etat2 in automate.ListeEtats:
                listeTotal.append([etat.NumEtat,etat2.NumEtat])

        return listeTotal
                
    def Cloture_par_union_ou_intersection_ensembliste(self,AutomateFD,choix):
        AFD1=self.CompleterAutomate()
        AFD2=AutomateFD.CompleterAutomate()
        NewEtats=AFD1.produit(AFD2)
        ListeEtats=[]
        string=""
        nom=""
        EtatInit=[]
        for liste in NewEtats:
            etat1=AFD1.ReturnEtat(liste[0])
            etat2=AFD2.ReturnEtat(liste[1])
            
            nom=','.join(str(elem) for elem in liste)
            ListeTransaction=[]
            for symbole in self.getAllSymbole():
                FinalListe=etat1.getNextState(symbole)+etat2.getNextState(symbole)
                string=','.join(str(elem) for elem in FinalListe)
                ListeTransaction.append(Transition(symbole,[string]))
                string=""
            if choix:
                ListeEtats.append(Etat(nom,ListeTransaction,(etat1.IsInitial and etat2.IsInitial),(etat1.IsFinale or etat2.IsFinale)))
            else:
                ListeEtats.append(Etat(nom,ListeTransaction,(etat1.IsInitial and etat2.IsInitial),(etat1.IsFinale and etat2.IsFinale)))
            nom=""

        for etat in ListeEtats:
            if etat.IsInitial:
                EtatInit.append(etat)  

        return Automate(len(NewEtats),EtatInit,ListeEtats)

    def getAllFinal(self):
        AllFinal=[]

        for etat in self.ListeEtats:
            if etat.IsFinale:
                AllFinal.append(etat)

        return AllFinal        
                
    def Cloture_par_miroir(self): 
        
        if len(self.getAllFinal())>1:
            return " CLOTURE PAR MIROIR IMPOSSIBLE "
        else:
            
            dictionnaire={}
            listeEtats=[]

            for etat in self.ListeEtats:
                
                for transition in etat.Transition:
                    numeros=etat.getNextState(transition.Symbole)
                    print(numeros)
                    for numero in numeros:
                        if numero in dictionnaire:
                            dictionnaire[numero].append(Transition(transition.Symbole,[etat.NumEtat]))
                        else:
                            dictionnaire[numero]=[Transition(transition.Symbole,[etat.NumEtat])]    

            ListeInit=[]
    
            for key, valeur in dictionnaire.items():
                Final=False
                Initial=False
                self.ReturnEtat(key)
                if self.ReturnEtat(key).IsInitial:
                    Final=True
                if self.ReturnEtat(key).IsFinale:
                    Initial=True
                    ListeInit.append(Etat(key,valeur,Initial,Final))

                listeEtats.append(Etat(key,valeur,Initial,Final))
                
            return Automate(self.NbEtat,ListeInit,listeEtats)
                                
    def Cloture_par_etoile(self):

        for etat in self.ListeEtats:
            if etat.IsFinale:
                etat.Transition.append(Transition("eps",[self.EtatsInitiaux[0].NumEtat]))

        return self        


    def Cloture_par_concatenation(self,automate):
        final1=self.getAllFinal()
        if len(final1)!= 1 or final1[0].Transition :
              return "impossible de faire la concatenation des deux automates"
        else:
            Final=None 
            initial=None       
            FinalAutomate=copy.deepcopy(self)

            for etat in automate.ListeEtats:
                if etat.IsInitial:
                    initial=etat
                etat.IsInitial=False

            for etat in FinalAutomate.ListeEtats:
                if etat.IsFinale:
                    etat.Transition=[Transition("eps",[initial.NumEtat])]
                    
            for etat in automate.ListeEtats:
                FinalAutomate.ListeEtats.append(etat)

            return FinalAutomate
    
    def getAllNotFinal(self):
        retour=[]
        for etat in self.ListeEtats:
            if not etat.IsFinale:
                retour.append(etat)
        return retour 
    

    def Minimisation(self):
        Classe00=self.getAllFinal()
        Classe01=self.getAllNotFinal()
        ClasseEquivalence={1:Classe00,2:Classe01}
        maxkey=2
        terminer=False
        Symbole=self.getAllSymbole()

        while not terminer:
            i=1 
            entrer=False
            while i<=maxkey: 
                classeActuel=ClasseEquivalence[i]
                if len(classeActuel)>1: 
                    newListe=self.MemeDestination(classeActuel,ClasseEquivalence,Symbole,i)
                    if type(newListe)==dict:
                        entrer=True
                        del ClasseEquivalence[i]
                        dicAide=dict(ClasseEquivalence)
                        cle=1
                        ClasseEquivalence={}
                        for key,valeur in dicAide.items():
                            ClasseEquivalence[cle]=valeur
                            cle+=1
                        for key,valeur in newListe.items():
                            ClasseEquivalence[cle]=valeur
                            cle+=1

                        maxkey=cle-1
                        i=maxkey+1
                            
                i+=1    
            if not entrer:
                terminer=True
        ListeEtatsNew=[]
        NewInitial=[]

        return self.constructionApresMinimiser(ClasseEquivalence)
    

    def MemeDestination(self,listeEtats,dictCouple,Symboles,i):
        continuer=True
        sousListes={}  
        i=0
        while i<len(Symboles) and continuer:
            symbole=Symboles[i]
            ListeKle=[]
            for etat in listeEtats:
                numeros=etat.getNextState(symbole)
                nextState=self.ReturnEtat(numeros[0])
    
                for key in dictCouple:
                    if nextState in dictCouple[key]:
                        if key in ListeKle:
                            sousListes[key].append(etat)
                        else:
                            ListeKle.append(key)
                            sousListes[key]=[etat]
                        break    
            i+=1
            if len(sousListes)>1:
                continuer=False
            else:
                sousListes={}  
                  
        if continuer:
            return listeEtats
        else:
            return sousListes    

    def constructionApresMinimiser(self,ClasseEquivalence):
        symboles=self.getAllSymbole()
        ListeEtatsNew=[]
        EtatInit=[]
        for key,etats in ClasseEquivalence.items():
            etat=etats[0]
            TransitionFinaux=[]
            for symbole in symboles:
                numero=etat.getNextState(symbole)
                if numero :
                    nextState=self.ReturnEtat(numero[0])
                    name=''
                    for key2,etats2 in ClasseEquivalence.items():
                        if nextState in etats2:
                            if len(etats2) >1:
                                newName=[]
                                for state in etats2:
                                    newName.append(state.NumEtat)
                                sorted(newName)
                                name=','.join(str(elem) for elem in newName)
                                TransitionFinaux.append(Transition(symbole,[name]))
                            else:
                                TransitionFinaux.append(Transition(symbole,[str(numero[0])]))
                            break
            initial=False
            final=False
            newName=[]
            name=''
            if len(etats) > 1:
                for state in etats:
                    if state.IsInitial:
                        initial=True
                        EtatInit.append(state)
                    if state.IsFinale:
                        final=True 
                    newName.append(state.NumEtat)
                    sorted(newName)
                name=','.join(str(elem) for elem in newName)
            else:
                name=str(etats[0].NumEtat)
                if etat.IsInitial:
                    initial=True
                    EtatInit.append(etat)
                if etat.IsFinale:
                    pass
                    final=True      
            ListeEtatsNew.append(Etat(name,TransitionFinaux,initial,final))
                
            
        return Automate(len(ClasseEquivalence),EtatInit,ListeEtatsNew)                    
                        

def Thompson(expressions):
    SYMBOLES=[]
    EtatFinalInitial=[]
    SPECIAL=['(',')','+','*']
    ListeSousAutomate=[]
    sousEtatsFinalInitial=[]
    SousEtats=[]
    sous=[expressions[0]]
    numeroEtat=0
    newInit=None
    newFinal=None
    GLOBAL=None
    FINALAUTOMATE=None
    FINALPRECEDENTE=None
    INITIALPRECEDENTE=None
    i=1
    while i<len(expressions):
        if expressions[i] == '(':
            ListeSousAutomate.append(sous)
            sous=[]
        sous.append(expressions[i])    
        i+=1
    ListeSousAutomate.append(sous)
    SousCompteur=-1
    print(ListeSousAutomate)
    i=0
    for sousAUtomate in ListeSousAutomate:
        j=0
        for symbole in sousAUtomate:
            if symbole not in SPECIAL:
                etat1=Etat(numeroEtat,[Transition(symbole,[numeroEtat+1])],True,False)
                etat2=Etat(numeroEtat+1,[],False,True)
                SousEtats.append(etat1)
                SousEtats.append(etat2)
                if sousAUtomate[j-1] =='(':
                    GLOBAL=numeroEtat   
                numeroEtat+=2
                if  not sousEtatsFinalInitial:
                    sousEtatsFinalInitial=[etat1,etat2]
                else:
                    if sousAUtomate[j-1] == '+':
                        oldEtatInit=sousEtatsFinalInitial[0]
                        oldEtatFinal=sousEtatsFinalInitial[1]
                        newInit=Etat(numeroEtat,[Transition('eps',[numeroEtat-2]),Transition('eps',[numeroEtat-4])],True,False)
                        newFinal=Etat(numeroEtat+1,[],False,True)
                        SousEtats.append(newInit)
                        SousEtats.append(newFinal)
                        oldEtatInit.IsInitial=False
                        oldEtatFinal.IsFinale=False
                        oldEtatFinal.Transition=[Transition('eps',[numeroEtat+1])]
                        etat1.IsInitial=False
                        etat2.IsFinale=False
                        etat2.Transition=[Transition('eps',[numeroEtat+1])]
                        sousEtatsFinalInitial[0]=newInit
                        sousEtatsFinalInitial[1]=newFinal
                        numeroEtat+=2
                    elif (sousAUtomate[j-1] not in SPECIAL) or (sousAUtomate[j-1] == '*') or (sousAUtomate[j-1] == ')'):
                        oldEtatFinal=sousEtatsFinalInitial[1]
                        oldEtatFinal.Transition=[Transition('eps',[numeroEtat-2])]
                        etat1.IsInitial=False  
                        oldEtatFinal.IsFinale=False
                        sousEtatsFinalInitial[1]=etat2

            elif symbole == '*':
                newInit=Etat(numeroEtat,[Transition('eps',[numeroEtat+1])],True,False)
                newFinal=Etat(numeroEtat+1,[],False,True)
                oldEtatInit=sousEtatsFinalInitial[0]
                oldEtatInit.IsInitial=False
                newInit.Transition.append(Transition('eps',[oldEtatInit.NumEtat]))
                oldEtatFinal=sousEtatsFinalInitial[1]
                oldEtatFinal.Transition=[Transition('eps',[numeroEtat+1])]
                oldEtatFinal.IsFinale=False
                SousEtats.append(newInit)
                SousEtats.append(newFinal)
                sousEtatsFinalInitial[0]=newInit
                sousEtatsFinalInitial[1]=newFinal
                numeroEtat+=2            
            i+=1 
            j+=1
        if not FINALAUTOMATE:
            FINALAUTOMATE=Automate(len(SousEtats),[sousEtatsFinalInitial[0]],SousEtats)
        else:       
            sousListe=ListeSousAutomate[SousCompteur]
            dernierSymbole=sousListe[len(sousListe)-1]
            if dernierSymbole == '+':
                for etat in SousEtats:
                    FINALAUTOMATE.ListeEtats.append(etat) 
                numero1=sousEtatsFinalInitial[0].NumEtat
                numero2=FINALAUTOMATE.EtatsInitiaux[0].NumEtat
                newInit=Etat(numeroEtat,[Transition('eps',[numero1]),Transition('eps',[numero2])],True,False)
                newFinal=Etat(numeroEtat+1,[],False,True)
                FINALAUTOMATE.ListeEtats.append(newInit)
                FINALAUTOMATE.ListeEtats.append(newFinal)
                INITIALPRECEDENTE.IsInitial=False
                for etat in FINALAUTOMATE.ListeEtats:
                    if etat.IsFinale and etat.NumEtat != numeroEtat+1:
                        print(etat.NumEtat)
                        etat.Transition=[Transition('eps',[numeroEtat+1])]
                        etat.IsFinale=False
                sousEtatsFinalInitial[0].IsInitial=False
                sousEtatsFinalInitial[0]=newInit
                sousEtatsFinalInitial[1]=newFinal
                numeroEtat+=2
            else:
                for etat in FINALAUTOMATE.ListeEtats:
                    if etat.IsFinale :
                        etat.Transition=[Transition('eps',[sousEtatsFinalInitial[0].NumEtat])]
                        etat.IsFinale=False
                        sousEtatsFinalInitial[0].IsInitial=False
                for etat in SousEtats:
                    FINALAUTOMATE.ListeEtats.append(etat)

        SousEtats=[] 
        INITIALPRECEDENTE=sousEtatsFinalInitial[0]
        FINALPRECEDENTE =sousEtatsFinalInitial[1]
        sousEtatsFinalInitial=[] 
        SousCompteur+=1       

                  
    return FINALAUTOMATE
            
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



            
                        
                    


                    

            

        
            

                
                
            
        
                        
                    

                



            

        
            


            

           
           