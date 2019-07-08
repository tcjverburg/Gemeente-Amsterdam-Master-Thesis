# Comments go/no go

* M. Marx
* 2019-05-15


## Algemeen

*  

## Specifiek

### notebook

1. cell 6: dit is toch een **bimodal** distributie? Waarom zeg je bijna normaal???
2. cell 7: woorden zijn onleesbaar. Misschien horizontaal??
3. Leuk die 40 top woorden per klasse, maar doet dit echt wat? Je zou misschien mutual information feature selectie kunne gebruiken om per klasse de 40 beste woorden te pakken. Dat geeft veel meer inzicht, dan de 40 meest voorkomende. Kijk maar, "amsterdam" is natuurlijk een stopwoord in dit corpus.
4. Het was fijn geweest als je boven aan had gegeven wat er eigenlijk gaat gebeuren en welke RQ je in je notebook aanpakt. Dit is een hutspot van dingen, en het duizelt me. 
5. Ik zou ook een karakter ngram zonder stemmen of tokenizen loslaten en kijken wat die doet. Meestal zijn 2 en 3 grammen genoeg. Je kan ook 4 grammen proberen. Ik verwacht dat die het nog beter gaat doen.
6. Is je train-test-opzet wel valide? Je zit te tunen met CV grid search. Prima. Maar heb je ook een echte held out test-set waarop je dan uiteindelijk test? Eigenlijk hoort dat wel.  
7. De grafek dimred_k tegen F1 is het leukst. Graag een veel betere uitleg en caption: Zijn dit nou het aantal woorden per klasse? Of het totaal aantal woorden? Ik zou graag de grafiek nog wat verder zien op de x-as om zelf te zien wat er gebeurt. Ik verwacht dat het op een gegeven moment ook veel slechter gaat worden, en wil dat graag zien.

#### Conclusie

* Je bent goed bezig, maar het is nog best rommelig. Ik denk dat je jezelf structuur moet egven, en dat het dan verbetert. Heel erg jammer dat je niet aan de coaching sessies meedoet. Je lijkt jezelf te overschatten.


### Thesis 

1. Graag regelnummers 
2. Je schrijft goed, en het leest prettig. Maar er zitten best veel taalfouten in. ZOEK HULP. LAAT HET LEZEN DOOR ANDEREN.
3. Ik vind deze sectie eigenlijk wat te wollig, en wil liever sneller de feiten zien. Denk eerst na **waarom** je een sectie schrijft en maak daar bullet points van.
    4. Ik wil hier leren hoe de data eruit ziet en wat er in zit dat jij als features kunt gebruiken.
    5. geef dus meteen een helder voorbeeld, van zo'n PDF, van de geOCRde tekst, en de highlights, en van de bijbehorende rijen uit de manual annotatie en de filenaam.
    6. Dan wil ik EDA feitjes. Lekker in tabelletjes en grafiekjes, die me helpen om te begrijpen hoe lastig de classificatie taak is.
        7. Iets typisch dat ik hier wil zien is een PDF met bladzij nummers en hoe vaak daar een annotatie op staat. Dat geeft dus meteen aan of dat een goede feature is.
        8. Ook het aantal annotaties per pagina
        9. Dus kijk naar wat je je classifier voedt als features en zorg dat je die hier allemaal "laat zien".
10. **Volgorde**
    11. Ik zou eerst de cleane dataset beschrijven, en allicht even kort de problemen met de ruwe dataset.
    12. Daarna kan je je preprocessing beschrijven.
13. *Two different parsing methods are implemented.* Volgens mij implementeer je niks, maar pas je gewoon hun scripts toe. Vermijd dat woord dus. Ik zou ook *parsing* vermijden. Jij extraheert tekst. *Parsing* betekent "ontleden", gebruik makend van een gramatica.
