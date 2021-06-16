from CLASSES import *
from Aide import *

def contructionAFD():
    
    """creation des transition"""
    Liste1=[Transition('a',[1]),Transition('b',[0])]
    Liste2=[Transition('a',[2]),Transition('b',[1])]
    Liste3=[]

    """ creation des etats"""
    ListeEtats=[Etat(0,Liste1,True,False),Etat(1,Liste2,False,False),Etat(2,Liste3,False,True)]
    
    """creation automate"""  
    return Automate(3,[ListeEtats[0]],ListeEtats)

def test1():
    Liste1=[Transition('a',[2, 3])]
    Liste2=[Transition('a',[4])]
    Liste3=[Transition('a',[3]),Transition('b',[4])]
    Liste4=[Transition('b',[2])]

    """ creation des etats"""
    ListeEtats=[Etat(1,Liste1,True,False),Etat(2,Liste2),Etat(3,Liste3),Etat(4,Liste4,False,True)]
    
    """creation automate"""  
    return Automate(4,[ListeEtats[0]],ListeEtats)

def test2():
    Liste1=[Transition('a',[1,3]),Transition('b',[1])]
    Liste2=[Transition('b',[1]),Transition('a',[0])]
    Liste3=[Transition('a',[3]),Transition('b',[1])]
    Liste4=[Transition('a',[3,1]),Transition('b',[1])]



    """ creation des etats"""
    ListeEtats=[Etat(0,Liste1,True,True),Etat(1,Liste2),Etat(2,Liste3,False,True),Etat(3,Liste4,False,True)]
    
    """creation automate"""  
    return Automate(4,[ListeEtats[0]],ListeEtats)

    
    
def contructionAFN():
    """creation des transition"""
    Liste1=[Transition('eps',[1]),Transition('a',[0])]
    Liste2=[Transition('b',[1]),Transition('eps',[2])]
    Liste3=[Transition('c',[2])]
    #Liste4=[Transition('a',[3])]

    """ creation des etats"""
    ListeEtats=[Etat(0,Liste1,True,False),Etat(1,Liste2,False,False),Etat(2,Liste3,False,True)]

    """creation automate"""  
    return Automate(3,[ListeEtats[0],ListeEtats[1]],ListeEtats)
automateTest2=test2()
def main():
    automate=contructionAFD()
    automate3=contructionAFD()
    automate2=contructionAFN()
    automateTest1=test1()
    
    print("***************************** BIENVENUE ***********************************")
    print("1- type d'automate")
    print("2- reconnaissance du mot")
    print("3- eps-fermeture d'un etat")
    print("4- eps-fermeture de l'automate")
    print("5- automate sans les eps-transitions")
    print("6- determinisation de l'automate")
    print("7- completer l'automate")
    print("8- cloture par complementation ")
    print("9- Cloture_par_union_ensembliste")
    print("10- Cloture_par_intersection_ensembliste")
    print("11- Cloture_par_miroir")
    print("12- Cloture_par_etoile")
    print("13- Cloture_par_concatenation")
    print("") 
    choix=int(input("choix  ---->"))
    if choix==1:
        print("") 
        print("AUTOMATE DE TYPE {}".format(automate.TypeAutomate()))
        print("") 
    elif choix == 2:
        mot=input(" entrez le mot  :")
        print("")
        if automate.reconnaisanceAFD(mot):
            print("LE MOT {} EST RECONNU PAR NOTRE AUTOMATE".format(mot))
        else:
            print("LE MOT {} N'EST PAS RECONNU PAR NOTRE AUTOMATE".format(mot))
        print("")          
    elif choix == 3:
        print("dilane fais attention aux types type de données")
        numero=int(input("entrez le numero de l'etat :"))
        etat=automate2.ReturnEtat(numero)
        if etat:
            print("eps-fermeture({}) = {}".format(numero ,automate2.eps_Fermeture(etat)))
        else:
            print("l'etat {} etat n'exite pas".format(numero)) 
    elif choix == 4:

        for etat in automate2.ListeEtats:
            print("eps-fermeture({}) = {}".format(etat.NumEtat ,automate2.eps_Fermeture(etat)))
    elif choix == 5 :
        automate=automate2.Construction_des_sous_ensembles()
        printAutomate(automate.Determinisation())
    elif choix == 6:
        printAutomate(automateTest2.Determinisation())
    elif choix == 7: 
        printAutomate(automate.CompleterAutomate())
    elif choix == 8:
        printAutomate(automate.Cloture_par_complementation())
    elif choix ==9:
        printAutomate(automateTest1.Cloture_par_union_ou_intersection_ensembliste(automateTest2,True))
    elif choix == 10:
        printAutomate(automateTest1.Cloture_par_union_ou_intersection_ensembliste(automateTest2,False))
    elif choix ==11:
        newAutomate=automate.Cloture_par_miroir()
        if type(newAutomate) == str:
            print(newAutomate)
        else:       
            printAutomate(newAutomate)
    elif choix == 12:
        printAutomate(automate.Cloture_par_etoile())
    elif choix == 13:
        #printAutomate(automateTest2)
        printAutomate(automate.Cloture_par_concatenation(automateTest1))
                
                
            
            
 
                        

              

if __name__ == '__main__':
    main()
       