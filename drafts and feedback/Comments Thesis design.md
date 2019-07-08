## Comments Thesis design 

* Marx
* 2019-03-29

Leuk onderwerp en leuke vragen.

Ik ben wat benauwd voor de aanpak die je voorstelt. Je hebt vrijwel geen trainingsdata, en de trainingsdata die je hebt lijkt erg ruizig en lastig te matchen tussen het excel sheet en de pdfs

Het lijkt mij dat een eerste opzet juist een handgeschreven regel gebaseerd systeem zou moeten zijn, waarbij ej voor elk type data dat je wilt extraheren een aparte set regels maakt.

Je kunt daarvoor een NLP tool als `spacy` gebruiken, bijvoorbeeld om locaties en eenheden op te sporen. De "signal words" waar je het over hebt kan je natuurlijk ook goed met regexes opsporen.

Ik raad je aan een lijst te maken van eigenschappen die je zou willen extraheren, en voor elke eigenschap aan te geven hoe belangrijk die voor de gemeente is, en hoe lastig die is om er goed uit te halen.

Dan orden je die lijst en gaat aan de slag met de gemakkelijkste eerst. Na het schrijven van je regels doe je steeeds met de hand een evaluatie op een **ongeziene set PDFs**. Ga niet dooremmeren op hele kleine verbeteringen, maar wees tevreden met 60% of zo. Gebruik precisie en recall maten. 

Allicht kan je na deze regelgenaseerde aanpak met een ML aanpak beginnen.

Zelf vind ik `pdftotext` en `pdftohtml --xml` (beide voor linux en macs) heel fijn werken. Je krijgt allicht ook met OCR fouten te maken. Als dat zo is, probeer dan eerst een verzameling "digital born" PDFs te pakken te krijgen. 
