# Programátorská dokumentace
Program využívá velkého množství dat pro vytvoření slovníku a statistik, které využívá pro doplňování diakritiky. Konkrétně pro každé slovo bez diakritiky (`wa_word`) si program udržuje všechny viděné varianty doplnění. Pro každou variantu si pak udržuje charakteristický vektor, který je průměrem přes všechny výskyty dané varianty. Charakteristický vektor závisí na větě a pozici slova ve větě. Vektor je vytvářen indikátory: velikost prvního písmene slova, je slovo v přímé řeči, pozice slova ve větě, znaménko ukončující větu, slovní druh předchozího slova a další. Vektor zahrnuje i četnost výskytu daně varianty.

Při doplňování diakritiky se vždy zkontroluje zda má slovo více variant doplnění. Pokud má slovo více variant doplnění spočítá se charakteristický vektor a vybere nejbližší varianta (pro zlepšení přesnosti mohou mít indikátory odlišnou váhu).

## Příprava dat
Pro vytvoření statistik byl využit korpus (Syn2015) dostupný na adrese: [https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-1593](https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-1593) Data jsou zpracovávána pomocí Python skriput, napsaném v Python 3.

Korpus má přesně danou strukturu, která vymezuje jednotlivé věty a tokeny (slova, tečky, čárky a speciální znaky). Každý token také obsahuje tag, který určuje slovní druh a příslušné vlastnosti. Pro zpracování těchto dat je určen skript `parser.py`. Tento skript vybírá jednotlivé věty které dále zpracovává a přidává do slovníku.

Výsledný slovník je uložený do souboru `obj/dictionary.dic`. Jedná se vlastně o CSV souboru (ve formátu UTF-8), který pro oddělení polí využívá mezery (protože ty se nikde v datech vyskytovat nemohou). Na každém řádku souboru je uložené postupně: slovo bez diakritiky, počet variant, (pro každou variantu:) slovo s diakritikou, tag a jednotlivé hodnoty charakteristického vektoru.

Skript `parser.py` využívá indikátorů definovaných v souboru indicators.py. Pro definování nového indikátoru stačí vytvořit novou třídu (která je podtřídou třídy Indicator). A v této třídě definovat počet polí ve vector a název indikátoru. Dále je nutné definovat funkci increment, která na vstupu dostane token, pozici a větu. A na konci incrementuje příslušné pole v tokenu. Třídu indikátoru je ještě nutné přidat do seznamu indicatorů.

Jistým nebezpečím je fakt, že v datech se mohou vyskytovat chyby a překlepy. Například slovo s nejvíce variantami (9) je slovo ježíšmarjá, kdy varianty jsou: ježíšmarjá, ježišmarjá, ježišmarja, jéžišmarjá, ježíšmarja, ježišmárja, jéžišmarja, ježísmarjá, jéžíšmarjá

## Aplikace pro doplňování diakritiky
Aplikace je rozdělena do několika souborů. Je napsána v c++ s využitím GTK 3, konkrétně knihovny gtkmm určené pro c++. Grafické rozložení celé aplikace je v souboru main.glade.

Soubor `main.cc` obsahuje základní funkce ovládání grafického rozhraní. Tento soubor definuje okno aplikace, tlačítka a jejich obsluhující funkce. Dále obsahuje některé základní funkce pro editaci textu, načítání textu a ukládání do souboru.

Soubor `data.cc` poskytuje třídu pro načtení slovníku. Pokud je to možné, tak je načítání prováděno ve vlastním vlákně se sdíleno pamětí, což umožňuje fungování zbytku aplikace. Data jsou načítáná do hashovací tabulky, která umožňuje pro dané slovo bez diakritiky vyhledat všechny možné doplnění. Jedná se o vlastní implementaci hashovací tabulky (v souboru `hashmap.cc`), která využívá otevřeného adresování.

Tabulka je tak implementována pomocí tří polí, což do budoucna umožňuje ještě rychlejší načítání, pokud by se uložila celá struktura. Tabulka má danou velikost. Pro zrychlení zápisu a omezení kopírování při načítání dat, tabulka vrací pointr do příslušného místa v poli. O proti využití standardní hashovací tabulky je tak načítání až 3 krát rychlejší a zabírá méně místa.

Samotné doplnění diakritiky po stisknutí tlačítka "apply" zajišťují funkce definované v souboru `parser.cc`. V tomto soubor probíhá rozdělení textu na jednotlivé věty a slova. Pro každé slovo jsou pak nalezeny jednotlivé varianty a pomocí indikátorů je vybrána nejpravděpodobnější. Následně je text poskládán do původní podoby v četně velkých a malých písmen. Všechny varianty jsou uložené pomocí malých písmen pro snížení množství variant, a proto je nutné písmena převádět.

Indikátory jsou uložené v souboru indicators.cc a jejich implementace je podobná indikatorům že souboru `indicators.py`. Pro snazší převádění tagů (znaků určující vlastnosti slova) je soubor s indikátory doplně o soubor `tagmaper.cc`.
