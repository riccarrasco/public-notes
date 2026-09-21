import html
import re
import unicodedata
from pathlib import Path
from typing import Iterable

SOURCE = Path(__file__).parent / "tutis-airfryer-recipes-cleaned.txt"
OUTPUT_DIR = Path(__file__).parent
LOCKED_RECIPE_FILES = {"chicken-soup.html", "curried-lentils.html"}

EXISTING_FILENAME_MAP = {
    "TOSTADAS FRANCESAS DULCES": "tostadas-francesas-dulces.html",
    "OMELETTE O TORTILLA DE HUEVO": "omelette-tortilla-huevo.html",
    "HUEVOS AL PLATO": "huevos-al-plato.html",
    "TOSTADAS FRANCESAS EN CUPCAKES CON FRAMBUESAS": "tostadas-francesas-en-cupcakes.html",
}

SECTION_HEADERS = {
    "RECETAS EN FREIDORA DE AIRE",
    "ABREVIATURAS",
    "DESAYUNOS",
    "ENTRADAS O PIQUEOS",
    "PESCADO Y MARISCOS",
    "CARNE DE CERDO",
    "VEGETALES Y RECETAS VEGETARIANAS",
    "ACOMPA\u00d1ANTES",
    "POSTRES",
}

IGNORED_HEADINGS = {
    "CARNE DE RES",
    "PLATOS DE POLLO",
}

CATEGORY_LABELS = {
    "DESAYUNOS": ("Breakfast", "Desayunos"),
    "ENTRADAS O PIQUEOS": ("Appetizers and Snacks", "Entradas y piqueos"),
    "PESCADO Y MARISCOS": ("Fish and Seafood", "Pescado y mariscos"),
    "CARNE DE CERDO": ("Pork and Meat", "Cerdo y carnes"),
    "VEGETALES Y RECETAS VEGETARIANAS": ("Vegetables and Vegetarian", "Vegetales y recetas vegetarianas"),
    "ACOMPA\u00d1ANTES": ("Sides", "Acompa\u00f1antes"),
    "POSTRES": ("Desserts", "Postres"),
    "SPECIAL": ("Specials", "Especiales"),
}

TITLE_TRANSLATIONS = {
    "TOSTADAS FRANCESAS DULCES": "Sweet French Toast",
    "OMELETTE O TORTILLA DE HUEVO": "Air Fryer Omelet",
    "HUEVOS AL PLATO": "Baked Eggs with Potatoes and Pancetta",
    "TOSTADAS FRANCESAS EN CUPCAKES CON FRAMBUESAS": "French Toast Cupcakes",
    "CR\u00c8ME BR\u00dbL\u00c9E CON MERMELADA DE BERRIES": "Creme Brulee with Berry Jam",
    "GRANOLA": "Granola",
    "PL\u00c1TANO CARAMELIZADO": "Caramelized Banana",
    "TOSTADAS CON NATILLA": "Custard Toast",
    "TOSTADAS FRANCESAS SALADAS": "Savory French Toast",
    "PANINIS": "Paninis",
    "BOLITAS DE QUINUA": "Quinoa Balls",
    "NAPOLITANAS": "Napolitanas",
    "EMPANADAS": "Empanadas",
    "EMPANADAS GALLEGAS": "Galician Empanadas",
    "FALAFEL": "Falafel",
    "QUEQUITOS DE GARBANZO": "Chickpea Croquettes",
    "CROQUETAS DE AT\u00daN": "Tuna Croquettes",
    "CROQUETAS CON TOCINO O JAM\u00d3N": "Bacon or Ham Croquettes",
    "CROQUETAS DE QUESO": "Cheese Croquettes",
    "PAPA RELLENA": "Stuffed Potato",
    "SAN JACOBOS": "San Jacobos",
    "ESP\u00c1RRAGOS CON JAM\u00d3N": "Asparagus with Ham",
    "CHIPS DE KALE": "Kale Chips",
    "PAN CASERO": "Homemade Bread",
    "BROCHETAS DE POLLO": "Chicken Skewers",
    "PECHUGA A LA PARRILLA": "Grilled Chicken Breast",
    "BROCHETAS DE POLLO CON PI\u00d1A Y PIMIENTO": "Chicken Skewers with Pineapple and Peppers",
    "POLLO CRUJIENTE": "Crispy Chicken",
    "POLLO EMPANIZADO CON SALSA DE LIM\u00d3N": "Breaded Chicken with Lemon Sauce",
    "VARIEDADES DE POLLO EMPANIZADO": "Breaded Chicken Variations",
    "ALITAS DE POLLO": "Chicken Wings",
    "PIERNAS DE POLLO CON VEGETALES": "Chicken Legs with Vegetables",
    "POLLO CRUJIENTE CON PARMESANO": "Crispy Parmesan Chicken",
    "CORDON BLEU DE POLLO": "Chicken Cordon Bleu",
    "PECHUGAS RELLENAS CON QUESO BOURSIN Y ESPINACA": "Boursin and Spinach Stuffed Chicken",
    "ALB\u00d3NDIGAS DE POLLO THAI": "Thai Chicken Meatballs",
    "PECHUGAS RELLENAS ITALIANAS": "Italian Stuffed Chicken",
    "ALB\u00d3NDIGAS DE POLLO CON ZUCCHINI": "Chicken Meatballs with Zucchini",
    "SALM\u00d3N CON MANTEQUILLA Y LIM\u00d3N": "Salmon with Butter and Lemon",
    "PESCADO REBOZADO": "Breaded Fish",
    "PESCADO A LA MENIER": "Fish Meuniere",
    "PINCHOS DE SALM\u00d3N CON PI\u00d1A Y TOMATES CHERRY": "Salmon Skewers with Pineapple and Cherry Tomatoes",
    "SALM\u00d3N CON GLASEADO DE DURAZNO": "Salmon with Peach Glaze",
    "PESCADO AL VAPOR EN PAQUETITOS": "Steamed Fish Parcels",
    "CAMARONES AL AJILLO": "Garlic Shrimp",
    "CALAMARES REBOZADOS": "Battered Squid",
    "CAMARONES PO\u2019 BOYS": "Shrimp Po' Boys",
    "HAMBURGUESAS": "Burgers",
    "FILETES RUSOS O ALB\u00d3NDIGAS": "Russian Steaks or Meatballs",
    "ALB\u00d3NDIGAS EN SALSA DE TOMATE": "Meatballs in Tomato Sauce",
    "STEAK PANZANELLA": "Steak Panzanella",
    "PARRILLADA DE RES": "Beef Grill Platter",
    "FILETES DE CERDO CON JAM\u00d3N Y QUESO": "Pork Cutlets with Ham and Cheese",
    "CHICHARR\u00d3N DE CHANCHO": "Crispy Pork Chunks",
    "COSTILLAR DE CERDO GLASEADO": "Glazed Pork Ribs",
    "CHANCHO THAI DULCE": "Sweet Thai Pork",
    "TEMPURA DE COLIFLOR Y BR\u00d3COLI": "Cauliflower and Broccoli Tempura",
    "BASTONES DE ZUCCHINI CRUJIENTES": "Crispy Zucchini Sticks",
    "COCA DE HOJALDRE Y VERDURAS": "Puff Pastry Vegetable Tart",
    "TORTILLA DE PATATAS": "Potato Tortilla",
    "VERDURAS SALTEADAS": "Sauteed Vegetables",
    "TACOS DE SETAS": "Mushroom Tacos",
    "PIMIENTOS RELLENOS": "Stuffed Peppers",
    "CROQUETAS DE VERDURAS": "Vegetable Croquettes",
    "COLIFLOR GRATINADA": "Cauliflower Gratin",
    "COLIFLOR GRATINADA ASI\u00c1TICA": "Asian Cauliflower Gratin",
    "PAPAS CON LENTEJAS": "Potatoes with Lentils",
    "HAMBURGUESAS DE GARBANZOS Y ESPINACAS": "Chickpea and Spinach Burgers",
    "BERENJENAS RELLENAS": "Stuffed Eggplant",
    "VAINITAS CON TOF\u00da": "Green Beans with Tofu",
    "TOF\u00da EMPANIZADO": "Breaded Tofu",
    "TOSTADAS CON PESTO": "Pesto Toast",
    "FAJITAS DE SETAS Y VERDURAS": "Mushroom and Vegetable Fajitas",
    "PAPAS FRITAS": "French Fries",
    "PAPAS FRITAS CONGELADAS": "Frozen French Fries",
    "PAPAS HASSELBACK": "Hasselback Potatoes",
    "CAMOTE FRITO": "Fried Sweet Potato",
    "CAMOTES ESTILO CAJ\u00daN": "Cajun Style Sweet Potatoes",
    "CRUTONES": "Croutons",
    "PL\u00c1TANO FRITO": "Fried Plantain",
    "CHIPS DE PL\u00c1TANO": "Plantain Chips",
    "TOSTONES": "Tostones",
    "MINI CROISSANTS": "Mini Croissants",
    "CHURROS": "Churros",
    "MAGDALENAS": "Spanish Muffins",
    "BROWNIES": "Brownies",
    "CRUMBLE DE MANZANA": "Apple Crumble",
    "MUFFINS DE ZAPALLO Y ZUCCHINI": "Pumpkin and Zucchini Muffins",
}

MANUAL_INGREDIENT_OVERRIDES_ES = {
    "PL\u00c1TANO CARAMELIZADO": [
        "1 pl\u00e1tano",
        "Aceite de palta o de coco",
        "Az\u00facar moreno",
    ],
    "VARIEDADES DE POLLO EMPANIZADO": [
        "Filetes o cuadrados de pechuga de pollo no muy delgados, o solomillos de pollo",
        "Salsa de soya, jugo de lim\u00f3n, p\u00e1prika, comino, jengibre, c\u00farcuma, aj\u00ed en polvo o hierbas a elecci\u00f3n",
        "Harina o maizena",
        "Huevos batidos con los condimentos elegidos",
        "Pan rallado, panko o corn flakes triturados",
        "Aceite para rociar o pincelar",
    ],
    "PAPAS FRITAS": [
        "Papas",
        "Aceite en spray",
        "Sal",
    ],
    "PAPAS FRITAS CONGELADAS": [
        "Papas fritas congeladas",
        "Sal",
    ],
    "PAPAS HASSELBACK": [
        "4 papas con cáscara",
        "2 palitos de brocheta",
        "3 cucharadas de mantequilla blanda",
        "Sal y pimienta",
        "1 ajo picado",
        "Tomillo u otra hierba de su preferencia",
    ],
    "CAMOTE FRITO": [
        "1 camote",
        "1 cucharadita de aceite",
        "Sal o hierbas al gusto",
    ],
    "CAMOTES ESTILO CAJ\u00daN": [
        "1 camote",
        "1 cucharada de aceite de oliva",
        "Cebolla y ajo en polvo opcionales",
        "Sal",
        "Pimienta",
        "Paprika",
        "Pimienta de Cayena",
    ],
    "CRUTONES": [
        "Pan de molde o el pan de su gusto",
        "Sal",
        "Aceite de oliva en spray",
    ],
    "PL\u00c1TANO FRITO": [
        "1 pl\u00e1tano bellaco",
        "Aceite de palta o de girasol",
    ],
    "CHIPS DE PL\u00c1TANO": [
        "1 pl\u00e1tano bellaco verde",
        "Aceite en spray",
        "Sal",
    ],
    "TOSTONES": [
        "1 pl\u00e1tano macho verde",
        "1 cucharada de aceite de palta",
        "Agua",
        "1 cucharadita de sal",
    ],
}

SUMMARY_OVERRIDES_EN = {
    "CAMARONES AL AJILLO": "Garlic Shrimp is a quick air fryer recipe with shrimp, garlic, olive oil, and bright citrus notes.",
    "CALAMARES REBOZADOS": "Battered Squid is a crisp air fryer seafood recipe served with lemon and simple seasoning.",
    "CAMARONES PO’ BOYS": "Shrimp Po' Boys combines crispy Cajun-style shrimp with lettuce, tomato, and a creamy spread.",
    "FAJITAS DE SETAS Y VERDURAS": "Mushroom and Vegetable Fajitas pair seasoned air-fried vegetables with a creamy avocado sauce.",
    "PAPAS FRITAS": "French Fries are classic air fryer potatoes with a crisp exterior and tender center.",
    "CHIPS DE PLÁTANO": "Plantain Chips are thin, crunchy slices cooked in the air fryer with simple seasoning.",
    "CRUMBLE DE MANZANA": "Apple Crumble is a warm fruit dessert with a sweet crumb topping and citrus aroma.",
}

EXTRA_RECIPES = [
    {
        "heading": "CURRIED LENTILS",
        "category": "SPECIAL",
        "owner": "Lobo",
        "filename": "curried-lentils.html",
        "title_en": "Curried Beef, Lentils and Kale Stew",
        "title_es": "Guiso de carne, lentejas y col rizada con curry",
        "summary_en": "A Michelin-inspired one-pot stew built with beef, soaked lentils, kale, and warming curry spices. It’s designed to be deeply savory, nourishing, and easy to follow on a phone while cooking.",
        "summary_es": "Un guiso de una sola olla inspirado en la cocina Michelin, hecho con carne de res, lentejas remojadas, col rizada y especias de curry. Está pensado para ser sabroso, nutritivo y fácil de seguir desde el celular mientras cocinas.",
        "ingredients_es": [
            "1 lb ground beef (85/15 for flavor)",
            "1 cup green lentils, soaked 4 hours",
            "1 cup cooked chickpeas (optional)",
            "1 large yellow onion, diced",
            "3 cloves garlic, minced",
            "1 inch ginger, grated",
            "1 carrot, diced",
            "1 red bell pepper, diced",
            "1–2 cups chopped kale (stems removed)",
            "1 cup diced tomatoes",
            "2 medium potatoes, cubed (optional)",
            "1½ tsp curry powder",
            "1 tsp ground cumin",
            "1 tsp ground coriander",
            "½ tsp turmeric",
            "½ tsp smoked paprika",
            "½ tsp garam masala",
            "¼ tsp cayenne (optional)",
            "4 cups beef or vegetable broth",
            "1 tbsp tomato paste",
            "½ cup coconut milk",
            "Juice of ½ lemon",
            "1 tbsp olive oil",
            "Salt and black pepper",
            "Fresh cilantro or parsley",
        ],
        "instructions_es": [
            "Prep first: Dice vegetables, rinse lentils, and chop kale. Keep kale in cold water until later.",
            "Brown the beef: Heat oil in a large pot over medium-high heat. Add beef and let it brown without stirring for 2 minutes, then break it apart and cook until deep brown.",
            "Build the base: Add onion, carrot, and bell pepper. Cook 6–8 minutes until caramelized. Stir in garlic and ginger, cook 1 minute.",
            "Bloom the spices: Add curry powder, cumin, coriander, turmeric, paprika, and cayenne. Toast for 30–45 seconds until fragrant.",
            "Add tomatoes & broth: Stir in tomato paste, diced tomatoes, soaked lentils, and broth. Bring to a gentle boil, then reduce to a simmer.",
            "Simmer: Cook 25–30 minutes until lentils are tender and stew is thickening.",
            "Add greens: Stir in chickpeas (if using) and kale. Simmer 5–7 minutes until kale softens.",
            "Finish: Add coconut milk, lemon juice, salt, and pepper. Sprinkle fresh cilantro on top and serve warm.",
        ],
    },
    {
        "heading": "CHICKEN SOUP",
        "category": "SPECIAL",
        "owner": "Lobo",
        "filename": "chicken-soup.html",
        "title_en": "Hearty Chicken and Vegetable Soup",
        "title_es": "Sopa reconfortante de pollo y verduras",
        "summary_en": "A classic chicken soup built for easy weeknight cooking, with tender chicken breasts, potatoes, small pasta, and a colorful blend of vegetables. Made for mobile-friendly reading and simple follow-along prep.",
        "summary_es": "Una sopa clásica de pollo ideal para cenas entre semana, con pechugas tiernas, papas, pasta pequeña y una mezcla colorida de verduras. Pensada para leerla en el celular y seguirla paso a paso.",
        "ingredients_es": [
            "2 chicken breasts (1–1.5 lb)",
            "1 tbsp olive oil or butter",
            "1 medium onion, diced",
            "3 celery stalks, sliced",
            "2 cloves garlic, minced (optional)",
            "2 medium potatoes, ½-inch cubes",
            "1½–2 cups frozen mixed vegetables",
            "1 cup small pasta (ditalini, elbow, shells, rotini)",
            "32 oz chicken broth",
            "4 cups water (or extra broth for richer soup)",
            "1 tsp dried thyme",
            "1 tsp dried parsley",
            "½ tsp black pepper",
            "Salt to taste",
            "1 bay leaf (optional)",
        ],
        "instructions_es": [
            "Sauté aromatics: Heat oil in a large pot over medium heat. Add onion and celery, cook 5–7 minutes until soft. Add garlic and cook 30 seconds.",
            "Simmer soup base: Add broth, water, thyme, parsley, pepper, and bay leaf. Bring to a gentle boil, then reduce to a simmer for 10 minutes.",
            "Add chicken: Place the chicken breasts into the pot. Simmer gently for 15–20 minutes until they reach 165°F (74°C).",
            "Add potatoes: Add cubed potatoes and simmer 10–12 minutes until nearly tender.",
            "Add vegetables & pasta: Stir in frozen vegetables and pasta. Simmer 8–10 minutes until pasta is al dente and potatoes are tender.",
            "Finish: Remove the chicken, shred it with forks, and return to the pot. Taste, adjust salt and pepper, remove bay leaf, and rest 5 minutes before serving.",
        ],
    },
]

PHRASE_REPLACEMENTS = {
    "freidora de aire": "air fryer",
    "sal y pimienta": "salt and pepper",
    "aceite de oliva": "olive oil",
    "azucar moreno": "brown sugar",
    "queso rallado": "grated cheese",
    "huevo duro": "hard-boiled egg",
    "huevos": "eggs",
    "huevo": "egg",
    "ajo": "garlic",
    "cebolla": "onion",
    "pimiento": "bell pepper",
    "tomate": "tomato",
    "perejil": "parsley",
    "limon": "lemon",
    "platano": "plantain",
    "papas": "potatoes",
    "papa": "potato",
    "pollo": "chicken",
    "atun": "tuna",
    "carne": "beef",
    "queso": "cheese",
    "cocinar": "cook",
    "mezclar": "mix",
    "agregar": "add",
    "poner": "place",
    "precalentar": "preheat",
    "voltear": "flip",
}

INSTRUCTION_PHRASE_REPLACEMENTS_EN = {
    "papel de hornear": "parchment paper",
    "freidora de aire": "air fryer",
    "fuego medio": "medium heat",
    "fuego bajo": "low heat",
    "fuego alto": "high heat",
    "dejar reposar": "let rest",
    "darle vueltas": "stir",
    "volver a darle vueltas": "stir again",
    "picada en cuadritos": "diced",
    "picado en cuadritos": "diced",
    "sal y pimienta": "salt and pepper",
}

INSTRUCTION_WORD_REPLACEMENTS_EN = {
    "rejilla": "rack",
    "huequitos": "small holes",
    "rociarlo": "spray it",
    "pincelarlo": "brush it",
    "revolver": "stir",
    "mezclar": "mix",
    "agregar": "add",
    "anadir": "add",
    "incorporar": "add",
    "continuar": "continue",
    "cocinar": "cook",
    "precalentar": "preheat",
    "retirar": "remove",
    "envolver": "wrap",
    "dejar": "let",
    "servir": "serve",
    "colocar": "place",
    "poner": "place",
    "nevera": "fridge",
    "minutos": "minutes",
    "minuto": "minute",
    "grados": "degrees",
    "mas": "more",
    "hasta": "until",
    "luego": "then",
    "despues": "after",
    "mientras": "while",
    "sin": "without",
    "todo": "everything",
    "la": "the",
    "el": "the",
    "los": "the",
    "las": "the",
}

UNIT_REPLACEMENTS_EN = {
    "cucharada": "tablespoon",
    "cucharadas": "tablespoons",
    "cucharadita": "teaspoon",
    "cucharaditas": "teaspoons",
    "taza": "cup",
    "tazas": "cups",
    "gramos": "grams",
    "gramo": "gram",
    "mililitros": "milliliters",
    "litro": "liter",
    "litros": "liters",
}

INSTRUCTION_VERBS = (
    "precalentar", "poner", "mezclar", "batir", "agregar", "anadir", "a\u00f1adir", "cortar", "cocinar", "abrir",
    "voltear", "dejar", "sazonar", "espolvorear", "sofreir", "sofreir", "dorar", "rellenar", "servir",
)

RE_AMOUNT = re.compile(r"(?:\b\d+[\d/.,]*|[¼½¾⅓⅔⅛⅜⅝⅞])\s*(?:c\.|c|cucharada|cucharadita|t\.|t|taza|gr|gramos|ml|oz|lb|kg|k|litro|litros)?\b", re.IGNORECASE)
RE_MULTISPACE = re.compile(r"\s{2,}")
RE_SPLIT_COLS = re.compile(r"\t+|\s{3,}")
RE_SENTENCE_END = re.compile(r"[.!?]$")
RE_SPANISH_STOP = re.compile(r"\b(de|la|el|los|las|con|para|por|una|un|y|en|del|al)\b", re.IGNORECASE)

SPANISH_MARKERS = {
    "de", "la", "el", "los", "las", "con", "para", "por", "una", "un", "del", "al", "y",
    "pollo", "papa", "papas", "cebolla", "ajo", "pimiento", "tomate", "queso", "huevo", "huevos",
    "mezclar", "agregar", "poner", "cocinar", "sazonar", "freidora", "aire", "minutos", "grados",
}

TERM_REPLACEMENTS_EN = {
    "orégano seco": "dried oregano",
    "oregano seco": "dried oregano",
    "rociar o pincelar": "spray or brush",
    "rociar": "spray",
    "pincelar": "brush",
    "seco": "dried",
    "carne de res": "beef",
    "sin grasa": "lean",
    "pechugas de pollo": "chicken breasts",
    "pechuga de pollo": "chicken breast",
    "camarones": "shrimp",
    "camaron": "shrimp",
    "calamares": "squid",
    "calamar": "squid",
    "salsa tartara": "tartar sauce",
    "panes de molde": "sandwich rolls",
    "panes": "rolls",
    "panko sazonado": "seasoned panko",
    "setas shiitake frescas": "fresh shiitake mushrooms",
    "manzanas amarillas": "yellow apples",
    "copos de avena": "rolled oats",
    "pimenton dulce": "sweet paprika",
    "pimentón dulce": "sweet paprika",
    "pimenton": "paprika",
    "pimentón": "paprika",
    "mayonesa": "mayonnaise",
    "jengibre": "ginger",
    "canela": "cinnamon",
    "nueces": "walnuts",
    "pecanas": "pecans",
    "agua": "water",
    "madura": "ripe",
    "fria": "cold",
    "fría": "cold",
    "frescas": "fresh",
    "fresca": "fresh",
    "amarillas": "yellow",
    "aceite de palta o de coco": "avocado or coconut oil",
    "aceite de oliva en spray": "olive oil cooking spray",
    "pan de su gusto": "bread of your choice",
    "para la salsa": "for the sauce",
    "sazonador de fajitas": "fajita seasoning",
    "sazonador cajun": "cajun seasoning",
    "en rodajas": "sliced",
    "en cuadritos": "diced",
    "en cuadrados": "diced",
    "en tiritas": "thin strips",
    "en tiras": "strips",
    "en anillos": "rings",
    "en laminas": "sliced",
    "pan de molde": "sandwich bread",
    "jugo de limon": "lemon juice",
    "jugo de limón": "lemon juice",
    "vinagre blanco": "white vinegar",
    "azucar moreno": "brown sugar",
    "azúcar moreno": "brown sugar",
    "queso rallado": "grated cheese",
    "de su preferencia": "of your choice",
    "de su gusto": "of your choice",
    "aceite de oliva": "olive oil",
    "aceite de palta": "avocado oil",
    "aceite de coco": "coconut oil",
    "aceite neutro": "neutral oil",
    "aceite en spray": "cooking spray",
    "sillao dulce": "sweet soy sauce",
    "sillao": "soy sauce",
    "salsa de soya": "soy sauce",
    "salsa picante": "hot sauce",
    "maizena": "cornstarch",
    "palta": "avocado",
    "setas": "mushrooms",
    "tofu": "tofu",
    "vainitas": "green beans",
    "lenteja": "lentils",
    "lentejas": "lentils",
    "camote": "sweet potato",
    "zapallo": "pumpkin",
    "mantequilla": "butter",
    "leche": "milk",
    "miel": "honey",
    "frambuesas": "raspberries",
    "frambuesa": "raspberry",
    "arandanos": "blueberries",
    "fresas": "strawberries",
    "couscous": "couscous",
    "garbanzos": "chickpeas",
    "lata": "can",
    "jugo": "juice",
    "zumo": "juice",
    "naranja": "orange",
    "vainilla": "vanilla",
    "zanahoria": "carrot",
    "tomillo": "thyme",
    "tilapia": "tilapia",
    "tilapias": "tilapia fillets",
    "filetes": "fillets",
    "costillas": "ribs",
    "vinagre": "vinegar",
    "hierbas": "herbs",
    "azucar": "sugar",
    "ralladura": "zest",
    "limon": "lemon",
    "limón": "lemon",
    "mediana": "medium",
    "medianas": "medium",
    "grande": "large",
    "grandes": "large",
    "gruesa": "thick",
    "gruesas": "thick",
    "grosor": "thickness",
    "blanco": "white",
    "rojo": "red",
    "roja": "red",
    "blanca": "white",
    "blanco": "white",
    "mediano": "medium",
    "medianos": "medium",
    "opcional": "optional",
    "empanizar": "breading",
    "eleccion": "choice",
    "ají": "chili",
    "aji": "chili",
    "ají colorado": "red chili",
    "jamón": "ham",
    "jamon": "ham",
    "lechuga": "lettuce",
    "integral": "whole wheat",
    "ajonjolí": "sesame",
    "ajonjoli": "sesame",
    "corn flakes": "cornflakes",
    "hojaldre": "puff pastry",
    "quark": "quark",
    "tocino": "bacon",
    "pancetta": "pancetta",
    "salame": "salami",
    "provolone": "provolone",
    "hierbabuena": "mint",
    "cebollinos": "scallions",
    "maní": "peanuts",
    "mani": "peanuts",
    "masa de hojaldre": "puff pastry",
    "masa para empanadas": "empanada dough",
    "aceite": "oil",
    "sal": "salt",
    "pimienta": "pepper",
    "ajo": "garlic",
    "cebolla": "onion",
    "pimiento": "bell pepper",
    "tomate": "tomato",
    "tomates": "tomatoes",
    "papas": "potatoes",
    "papa": "potato",
    "pollo": "chicken",
    "carne": "beef",
    "cerdo": "pork",
    "pescado": "fish",
    "camarones": "shrimp",
    "queso": "cheese",
    "huevo": "egg",
    "huevos": "eggs",
    "harina": "flour",
    "pan rallado": "breadcrumbs",
    "pan": "bread",
    "perejil": "parsley",
    "oregano": "oregano",
    "orégano": "oregano",
    "comino": "cumin",
    "paprika": "paprika",
    "yogurt": "yogurt",
    "platano": "plantain",
    "plátano": "plantain",
    "zucchini": "zucchini",
    "champiñones": "mushrooms",
    "champiñon": "mushroom",
    "espinaca": "spinach",
    "freidora de aire": "air fryer",
    "pechuga": "chicken breast",
    "pechugas": "chicken breasts",
    "alitas": "wings",
    "dientes": "cloves",
    "caldo": "broth",
    "verduras": "vegetables",
    "mediana": "medium",
    "medianas": "medium",
    "picado": "chopped",
    "picada": "chopped",
    "picados": "chopped",
    "picadas": "chopped",
    "cortado": "cut",
    "cortada": "cut",
    "cortados": "cut",
    "cortadas": "cut",
    "en cubos": "diced",
    "en polvo": "powder",
    "al gusto": "to taste",
    "sin piel": "skinless",
    "desmenuzado": "shredded",
    "desmenuzada": "shredded",
    "mezcla": "mixture",
    "tajadas": "slices",
    "tajada": "slice",
    "trozos": "pieces",
    "trozo": "piece",
    "molida": "ground",
    "molido": "ground",
    "cocido": "cooked",
    "cocida": "cooked",
    "cocidos": "cooked",
    "cocidas": "cooked",
    "rallado": "grated",
    "rallada": "grated",
    "verde": "green",
    "dulce": "sweet",
}

UNIT_MAP_EN = {
    "cucharada": "tbsp",
    "cucharadas": "tbsp",
    "cucharadita": "tsp",
    "cucharaditas": "tsp",
    "taza": "cup",
    "tazas": "cups",
    "gramos": "g",
    "gramo": "g",
    "mililitros": "ml",
    "litro": "L",
    "litros": "L",
    "onzas": "oz",
    "libras": "lb",
}

STOP_WORDS_ES = {
    "de", "del", "la", "las", "el", "los", "con", "para", "por", "y", "o", "en", "al", "a", "un", "una"
}


def quote(text: str) -> str:
    return html.escape(text, quote=False)


def normalize_text(text: str) -> str:
    text = text.replace("\u2019", "'")
    text = RE_MULTISPACE.sub(" ", text.replace("\t", " ")).strip()
    return text


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = value.lower()
    value = re.sub(r"[^a-z0-9\s-]", "", value)
    value = re.sub(r"\s+", "-", value).strip("-")
    return f"{value}.html"


def normalize_heading(line: str) -> str:
    return line.strip().upper()


def is_section_header(line: str) -> bool:
    return normalize_heading(line) in SECTION_HEADERS


def is_recipe_heading(line: str) -> bool:
    text = line.strip()
    if not text or text != text.upper():
        return False
    normalized = normalize_heading(text)
    if normalized in SECTION_HEADERS or normalized in IGNORED_HEADINGS:
        return False
    if len(normalized) > 120:
        return False
    if re.search(r"\d", normalized):
        return False
    return any(ch.isalpha() for ch in normalized) and all(not ch.isalpha() or ch.isupper() for ch in text)


def english_title_from_spanish(title: str) -> str:
    key = title.strip().upper()
    if key in TITLE_TRANSLATIONS:
        return TITLE_TRANSLATIONS[key]
    words = [w.capitalize() for w in title.lower().split()]
    return " ".join(words)


def parse_recipes(raw_text: str) -> list[dict]:
    lines = raw_text.splitlines()
    current_category = "DESAYUNOS"
    recipe_markers = []
    boundary_indexes = []

    for idx, line in enumerate(lines):
        if not line.strip():
            continue
        if normalize_heading(line) in IGNORED_HEADINGS:
            boundary_indexes.append(idx)
            continue
        if is_section_header(line):
            current_category = normalize_heading(line)
            boundary_indexes.append(idx)
            continue
        if is_recipe_heading(line):
            recipe_markers.append((idx, normalize_heading(line), current_category))
            boundary_indexes.append(idx)

    boundary_indexes = sorted(set(boundary_indexes))

    recipes = []
    for i, (start_idx, heading, category) in enumerate(recipe_markers):
        end_idx = next((idx for idx in boundary_indexes if idx > start_idx), len(lines))
        block = [lines[j].rstrip() for j in range(start_idx + 1, end_idx) if lines[j].strip()]
        if not block:
            continue
        recipes.append(
            {
                "heading": heading,
                "category": category,
                "owner": "Tuti",
                "lines": block,
                "filename": EXISTING_FILENAME_MAP.get(heading, slugify(heading)),
            }
        )
    return recipes


def strip_accents(text: str) -> str:
    n = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in n if not unicodedata.combining(ch))


def _normalize_common_units_es(text: str) -> str:
    text = re.sub(r"\bgr\b", "gramos", text, flags=re.IGNORECASE)
    text = re.sub(r"\bml\.?\b", "mililitros", text, flags=re.IGNORECASE)
    text = re.sub(r"\boz\b", "onzas", text, flags=re.IGNORECASE)
    text = re.sub(r"\blb\b", "libras", text, flags=re.IGNORECASE)
    text = re.sub(r"\bl\.\b", "litro", text, flags=re.IGNORECASE)
    text = re.sub(r"\bk\b", "kilo", text, flags=re.IGNORECASE)
    return text


def normalize_ingredient_spanish(text: str) -> str:
    text = re.sub(r"\bC\.(?=\s|$)", "cucharada", text)
    text = re.sub(r"\bc\.(?=\s|$)", "cucharadita", text)
    text = re.sub(r"\bt\.(?=\s|$)", "taza", text)
    text = re.sub(r"\bC(?=\s+de\b|\s+[A-Za-zÁÉÍÓÚáéíóúñÑ])", "cucharada", text)
    text = re.sub(r"\bc(?=\s+de\b|\s+[A-Za-zÁÉÍÓÚáéíóúñÑ])", "cucharadita", text)
    text = re.sub(r"\bt(?=\s+de\b|\s+[A-Za-zÁÉÍÓÚáéíóúñÑ])", "taza", text)
    text = _normalize_common_units_es(text)
    text = text.replace(" de taza", " taza de")
    text = re.sub(r"\bcucharadita\s+([A-Za-zÁÉÍÓÚáéíóúñÑ])", r"cucharadita de \1", text)
    text = re.sub(r"\bcucharada\s+([A-Za-zÁÉÍÓÚáéíóúñÑ])", r"cucharada de \1", text)
    text = re.sub(r"\bde\s+de\b", "de", text)
    return normalize_text(text).rstrip(".")


def protect_temperatures(text: str) -> tuple[str, dict[str, str]]:
    replacements: dict[str, str] = {}

    def repl(match: re.Match[str]) -> str:
        token = f"__TEMP_{len(replacements)}__"
        replacements[token] = match.group(0)
        return token

    protected = re.sub(r"\b\d{2,3}\s*(?:grados\s*)?[CF]\b", repl, text, flags=re.IGNORECASE)
    return protected, replacements


def restore_temperatures(text: str, replacements: dict[str, str]) -> str:
    for token, original in replacements.items():
        text = text.replace(token, original)
    return text


def normalize_instruction_spanish(text: str) -> str:
    protected, replacements = protect_temperatures(text)
    protected = re.sub(r"\bC\.(?=\s|$)", "cucharada", protected)
    protected = re.sub(r"\bc\.(?=\s|$)", "cucharadita", protected)
    protected = re.sub(r"\bt\.(?=\s|$)", "taza", protected)
    protected = re.sub(r"\bC(?=\s+de\b|\s+[A-Za-zÁÉÍÓÚáéíóúñÑ])", "cucharada", protected)
    protected = re.sub(r"\bc(?=\s+de\b|\s+[A-Za-zÁÉÍÓÚáéíóúñÑ])", "cucharadita", protected)
    protected = re.sub(r"\bt(?=\s+de\b|\s+[A-Za-zÁÉÍÓÚáéíóúñÑ])", "taza", protected)
    protected = _normalize_common_units_es(protected)
    protected = protected.replace(" de taza", " taza de")
    protected = re.sub(r"\bde\s+de\b", "de", protected)
    protected = restore_temperatures(protected, replacements)
    text = protected
    return normalize_text(text)


def looks_like_instruction(line: str) -> bool:
    compact = normalize_text(line)
    lower = strip_accents(compact.lower())
    if any(v in lower for v in INSTRUCTION_VERBS):
        return True
    if "grado" in lower or "minuto" in lower:
        return True
    if RE_SENTENCE_END.search(compact) and len(compact.split()) >= 8:
        return True
    return False


def split_ingredient_chunks(line: str) -> list[str]:
    parts = [p.strip(" ,") for p in RE_SPLIT_COLS.split(line) if p.strip(" ,")]
    cleaned = []
    for part in parts:
        if "," in part and part.count(",") > 1 and len(part) > 45:
            sub = [s.strip() for s in part.split(",") if s.strip()]
            cleaned.extend(sub)
        else:
            cleaned.append(part)
    return [normalize_ingredient_spanish(c) for c in cleaned if normalize_ingredient_spanish(c)]


def split_leading_ingredient_sentence(line: str) -> tuple[str | None, str | None]:
    compact = normalize_text(line)
    if not RE_AMOUNT.match(compact):
        return None, None

    parts = re.split(r"(?<=[.!?])\s+", compact, maxsplit=1)
    first = normalize_ingredient_spanish(parts[0].rstrip(".")) if parts else ""
    remainder = normalize_instruction_spanish(parts[1]) if len(parts) > 1 else None
    if not first:
        return None, remainder
    return first, remainder


def split_instruction_sentences_es(line: str) -> list[str]:
    text = normalize_instruction_spanish(line)
    text = text.replace(";", ". ")
    text = re.sub(r"\s+", " ", text).strip()
    parts = re.split(r"(?<=[.!?])\s+", text)
    out = []
    for part in parts:
        clean = part.strip()
        if not clean:
            continue
        if not RE_SENTENCE_END.search(clean):
            clean += "."
        out.append(clean)
    return out if out else [text]


def split_ingredients_instructions(lines: list[str]) -> tuple[list[str], list[str]]:
    ingredients: list[str] = []
    instructions: list[str] = []

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue

        if RE_SPLIT_COLS.search(raw_line):
            chunks = split_ingredient_chunks(line)
            if chunks:
                ingredients.extend(chunks)
                continue

        leading_ingredient, remainder = split_leading_ingredient_sentence(line)
        if leading_ingredient:
            ingredients.append(leading_ingredient)
            if remainder:
                instructions.extend(split_instruction_sentences_es(remainder))
            continue

        if looks_like_instruction(line):
            instructions.extend(split_instruction_sentences_es(line))
            continue

        chunks = split_ingredient_chunks(line)
        if not chunks:
            continue

        # Ingredient lines usually carry quantities or short noun phrases.
        if any(RE_AMOUNT.search(c) for c in chunks) or all(len(c.split()) <= 7 for c in chunks):
            ingredients.extend(chunks)
        else:
            instructions.extend(split_instruction_sentences_es(line))

    if not instructions and lines:
        # Do not hallucinate instructions, preserve source wording when structure is ambiguous.
        merged = " ".join(normalize_instruction_spanish(x) for x in lines if x.strip())
        if merged:
            instructions = [merged]

    if not ingredients:
        ingredients = ["Sin ingredientes claros en la fuente original."]
    if not instructions:
        instructions = ["Sin instrucciones claras en la fuente original."]

    return dedupe_preserve_order(ingredients), dedupe_preserve_order(instructions)


def dedupe_preserve_order(items: Iterable[str]) -> list[str]:
    seen = set()
    out = []
    for item in items:
        key = item.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def translate_es_to_en(text: str) -> str:
    base = normalize_text(text)
    low = strip_accents(base.lower())

    for es, en in sorted(INSTRUCTION_PHRASE_REPLACEMENTS_EN.items(), key=lambda kv: len(kv[0]), reverse=True):
        low = re.sub(rf"\b{re.escape(strip_accents(es))}\b", en, low)

    for es, en in sorted(PHRASE_REPLACEMENTS.items(), key=lambda kv: len(kv[0]), reverse=True):
        low = low.replace(strip_accents(es), en)

    for es, en in sorted(INSTRUCTION_WORD_REPLACEMENTS_EN.items(), key=lambda kv: len(kv[0]), reverse=True):
        low = re.sub(rf"\b{re.escape(strip_accents(es))}\b", en, low)

    # Light grammar cleanup.
    low = re.sub(r"\bde\b", "of", low)
    low = re.sub(r"\bcon\b", "with", low)
    low = re.sub(r"\by\b", "and", low)
    low = re.sub(r"\bo\b", "or", low)
    low = re.sub(r"\bpara\b", "for", low)
    low = re.sub(r"\ben\b", "in", low)
    low = re.sub(r"\bpor\b", "for", low)
    low = re.sub(r"\bal\b", "to the", low)
    low = re.sub(r"\bdel\b", "of the", low)
    low = re.sub(r"\ba\s+(\d+\s*degrees\s*[cf])\b", r"at \1", low)
    low = re.sub(r"\s+", " ", low)
    low = low.replace("of of", "of")

    for es_unit, en_unit in UNIT_REPLACEMENTS_EN.items():
        low = re.sub(rf"\b{es_unit}\b", en_unit, low)

    low = re.sub(r"\s+", " ", low).strip()
    if not low:
        return "Follow the recipe steps with your air fryer until fully cooked."

    low = low[0].upper() + low[1:]
    if not RE_SENTENCE_END.search(low):
        low += "."
    return low


def summarize_recipe(title_en: str, title_es: str, ingredients_es: list[str], instructions_es: list[str]) -> tuple[str, str]:
    en = f"{title_en} is a home-style air fryer recipe with clear steps and practical ingredients for everyday cooking."

    ks1 = ingredient_keyword_es(ingredients_es[0]) if ingredients_es else "ingredientes de casa"
    ks2 = ingredient_keyword_es(ingredients_es[1]) if len(ingredients_es) > 1 else "sazon simple"
    es = f"{title_es} es una receta casera en freidora de aire hecha con {ks1} y {ks2}."
    return en, es


def ingredient_keyword_es(line: str) -> str:
    text = normalize_text(line).lower()
    text = re.sub(r"\b\d+[\d/.,]*\b", "", text)
    text = re.sub(r"\b(cucharada|cucharadita|taza|gramos|mililitros|litro|litros|onzas|libras)\b", "", text)
    words = [w for w in re.findall(r"[a-záéíóúñ]+", text) if w not in STOP_WORDS_ES]
    if not words:
        return "ingredientes caseros"
    return " ".join(words[:3])


def ingredient_keyword_en(line: str) -> str:
    translated = translate_ingredient_line_en(line).rstrip(".")
    words = [
        w
        for w in re.findall(r"[a-z]+", translated.lower())
        if w not in {
            "of", "and", "or", "with", "to", "the", "a", "an",
            "cup", "cups", "tbsp", "tsp", "g", "ml", "oz", "lb",
            "large", "medium", "small", "cooked", "chopped", "grated",
            "ground", "green", "sweet", "optional", "your", "choice",
            "spray", "taste", "for", "white", "thick", "neutral",
            "cooking", "can", "juice", "breading",
        }
    ]
    if not words:
        return "everyday ingredients"
    return " ".join(words[:2])


def translate_spanish_phrase(text: str) -> str:
    out = strip_accents(normalize_text(text).lower())

    for unit_es, unit_en in UNIT_MAP_EN.items():
        out = re.sub(rf"\b{unit_es}\b", unit_en, out)

    for es, en in sorted(TERM_REPLACEMENTS_EN.items(), key=lambda kv: len(kv[0]), reverse=True):
        out = re.sub(rf"\b{re.escape(strip_accents(es))}\b", en, out)

    out = re.sub(r"\s+", " ", out).strip(" ,.;")
    return out


def translate_ingredient_line_en(es_line: str) -> str:
    out = translate_spanish_phrase(es_line)
    out = re.sub(r"\bde\b", "of", out)
    out = re.sub(r"\bcon\b", "with", out)
    out = re.sub(r"\by\b", "and", out)
    out = re.sub(r"\bo\b", "or", out)
    out = re.sub(r"\bpara\b", "for", out)
    out = re.sub(r"\bal gusto\b", "to taste", out)
    out = re.sub(r"\s+", " ", out).strip(" ,.;")
    out = out.replace("of of", "of")
    out = out.replace(" or el ", " or ").replace(" or la ", " or ").replace(" or las ", " or ")
    out = out.replace(" for la salsa", " for the sauce")
    out = out.replace(" for el ", " for ")
    out = out.replace(" en ", " ")
    out = out.replace("tomato large", "large tomato")
    out = out.replace("bell pepper red", "red bell pepper")
    out = out.replace("bell pepper green", "green bell pepper")
    out = out.replace("onion white", "white onion")
    out = out.replace("avocado ripe", "ripe avocado")
    out = out.replace("lettuce thin strips", "thin lettuce strips")
    out = out.replace("rolls of sandwich", "sandwich rolls")
    out = out.replace("broth of chicken", "chicken broth")
    out = out.replace("cheese crema", "cream cheese")
    out = out.replace("butter fria diced", "cold butter, diced")
    out = out.replace("For the sauce:.", "For the sauce:")
    out = out.replace("or of coco", "or coconut")
    out = out.replace("  ", " ")
    if out.lower().startswith("para la salsa"):
        out = "For the sauce"
    if not out:
        return fallback_ingredient_en(es_line)
    out = out[0].upper() + out[1:]
    if not out.endswith("."):
        out += "."
    return out


def clean_amount_token(token: str) -> str:
    t = token.strip()
    t = t.replace("½", "1/2").replace("¼", "1/4").replace("¾", "3/4")
    t = t.replace("⅓", "1/3").replace("⅔", "2/3")
    t = t.replace("⁄", "/")
    return t


def contains_spanish_markers(text: str) -> bool:
    words = re.findall(r"[a-z]+", strip_accents(text.lower()))
    return any(w in SPANISH_MARKERS for w in words)


def normalize_qty_to_en(qty: str) -> str:
    q = strip_accents(clean_amount_token(qty).lower())
    for es_unit, en_unit in UNIT_MAP_EN.items():
        q = re.sub(rf"\b{es_unit}\b", en_unit, q)
    q = re.sub(r"\s+", " ", q).strip()
    return q


def spanish_marker_ratio(text: str) -> float:
    words = re.findall(r"[a-zA-Z]+", strip_accents(text.lower()))
    if not words:
        return 0.0
    hits = sum(1 for w in words if w in SPANISH_MARKERS)
    return hits / len(words)


def fallback_instruction_en(es_line: str) -> str:
    low = strip_accents(es_line.lower())
    minute_match = re.search(r"(\d+\s*(?:a\s*\d+\s*)?minutos?)", low)
    temp_match = re.search(r"(\d+\s*grados\s*[cf])", low)
    if minute_match:
        raw_time = minute_match.group(1).replace(" a ", "-")
        raw_time = raw_time.replace("minutos", "minutes").replace("minuto", "minute")
        time_hint = f" for about {raw_time}"
    else:
        time_hint = ""
    temp_hint = ""
    if temp_match:
        temp_hint = f" at about {temp_match.group(1).replace('grados', 'degrees').upper()}"

    if any(k in low for k in ("dora", "sellar")):
        return f"Brown the protein{time_hint} until it develops color and aroma.".replace("  ", " ")
    if any(k in low for k in ("sofrie", "saltea")):
        return f"Saute the aromatics{time_hint} until softened and fragrant.".replace("  ", " ")
    if any(k in low for k in ("tuesta", "activar el aroma")):
        return f"Toast the spices briefly{time_hint} to develop deeper flavor.".replace("  ", " ")

    if "precalentar" in low:
        return f"Preheat to the target temperature{temp_hint if temp_hint else ''} before starting this step.".replace("  ", " ")
    if any(k in low for k in ("reemplazar", "vegetar")):
        return "For a vegetarian variation, swap the protein and keep the same timing and texture targets."
    if any(k in low for k in ("agrega", "agregar", "anade", "añade", "incorpora")):
        return f"Add the next ingredients and combine well{time_hint} so everything cooks evenly.".replace("  ", " ")
    if any(k in low for k in ("hierve", "hervor")):
        return f"Bring to a gentle boil{time_hint}, then lower the heat to continue cooking.".replace("  ", " ")
    if any(k in low for k in ("baja a fuego", "fuego medio", "fuego bajo")):
        return f"Lower the heat and continue cooking{time_hint}, stirring as needed.".replace("  ", " ")
    if any(k in low for k in ("reposar", "dejar")):
        return f"Let it rest{time_hint if time_hint else ' for a few minutes'} so flavors settle before serving.".replace("  ", " ")
    if any(k in low for k in ("mezclar", "batir", "remover")):
        return "Mix everything well in a bowl until the texture is even and fully combined."
    if any(k in low for k in ("cortar", "picar", "rallar")):
        return "Cut and prep the ingredients into uniform pieces so they cook evenly."
    if any(k in low for k in ("cocinar", "hornear", "freidora")):
        return f"Cook{temp_hint}{time_hint} until fully done, flipping halfway if needed.".replace("  ", " ")
    if any(k in low for k in ("retira", "saca")):
        return "Remove from heat and set aside briefly before the next step."
    if any(k in low for k in ("servir", "acompanar", "acompa")):
        return "Serve warm and finish with your preferred garnish or side."
    if time_hint or temp_hint:
        return f"Follow this step{temp_hint}{time_hint}, watching texture and doneness as you go.".replace("  ", " ")
    return "Follow this step in sequence, keeping texture and doneness cues in mind."


def fallback_ingredient_en(es_line: str) -> str:
    line = normalize_ingredient_spanish(es_line)
    low = strip_accents(line.lower())

    if "sal y pimienta" in low:
        return "Salt and pepper to taste."

    amount = RE_AMOUNT.search(low)
    qty = normalize_qty_to_en(amount.group(0)) if amount else ""

    terms = []
    for es, en in sorted(TERM_REPLACEMENTS_EN.items(), key=lambda kv: len(kv[0]), reverse=True):
        key = strip_accents(es)
        if re.search(rf"\b{re.escape(key)}\b", low) and en not in terms:
            terms.append(en)
    terms = [t for t in terms if t not in {"air fryer", "mix"}]

    detail = ""
    if "diced" in terms:
        terms = [t for t in terms if t != "diced"]
        detail = "diced"
    elif "chopped" in terms:
        terms = [t for t in terms if t != "chopped"]
        detail = "chopped"
    elif "powder" in terms:
        terms = [t for t in terms if t != "powder"]
        detail = "powder"

    core = ""
    if terms:
        core = " and ".join(terms[:2])
    else:
        core = "ingredient from source"

    phrase = f"{qty} {core}".strip() if qty else core
    if detail:
        phrase = f"{phrase}, {detail}"

    phrase = re.sub(r"\s+", " ", phrase).strip(" ,.;")
    phrase = phrase[0].upper() + phrase[1:] if phrase else "Listed ingredient"
    if not phrase.endswith("."):
        phrase += "."
    return phrase


def sanitize_english(es_line: str, translated_en: str, kind: str) -> str:
    words = re.findall(r"[a-zA-Z]+", strip_accents(translated_en.lower()))
    hits = sum(1 for w in words if w in SPANISH_MARKERS)
    ratio = spanish_marker_ratio(translated_en)
    if kind == "instruction" and (hits >= 1 or ratio >= 0.05):
        return fallback_instruction_en(es_line)
    if kind == "ingredient" and (hits >= 1 or ratio >= 0.08):
        return fallback_ingredient_en(es_line)
    if kind not in {"instruction", "ingredient"} and (hits >= 1 or ratio >= 0.08):
        if kind == "instruction":
            return fallback_instruction_en(es_line)
        return fallback_ingredient_en(es_line)
    return translated_en


def build_recipe_payload(recipe: dict) -> dict:
    if "ingredients_es" in recipe and "instructions_es" in recipe:
        ingredients_es = [normalize_ingredient_spanish(x) for x in recipe["ingredients_es"]]
        instructions_es = []
        for step in recipe["instructions_es"]:
            instructions_es.extend(split_instruction_sentences_es(step))
    else:
        ingredients_es, instructions_es = split_ingredients_instructions(recipe["lines"])

    override_ingredients = MANUAL_INGREDIENT_OVERRIDES_ES.get(recipe["heading"])
    if override_ingredients:
        should_override = ingredients_es == ["Sin ingredientes claros en la fuente original."]
        if len(ingredients_es) == 1 and len(ingredients_es[0].split()) >= 10 and looks_like_instruction(ingredients_es[0]):
            should_override = True
        if should_override:
            ingredients_es = override_ingredients

    title_es = recipe.get("title_es", recipe["heading"].title())
    title_en = recipe.get("title_en", english_title_from_spanish(recipe["heading"]))

    summary_en, summary_es = recipe.get("summary_en"), recipe.get("summary_es")
    if not summary_en or not summary_es:
        summary_en, summary_es = summarize_recipe(title_en, title_es, ingredients_es, instructions_es)

    summary_en = SUMMARY_OVERRIDES_EN.get(recipe["heading"], summary_en)

    payload = {
        "filename": recipe["filename"],
        "owner": recipe.get("owner", "Tuti"),
        "category": recipe["category"],
        "title_en": title_en,
        "title_es": title_es,
        "summary_en": summary_en,
        "summary_es": summary_es,
        "ingredients_en": [sanitize_english(x, translate_ingredient_line_en(x), "ingredient") for x in ingredients_es],
        "ingredients_es": ingredients_es,
        "instructions_en": [fallback_instruction_en(x) for x in instructions_es],
        "instructions_es": instructions_es,
    }
    return payload


def render_recipe_page(payload: dict) -> str:
    owner = payload["owner"]
    owner_badge_en = f"{owner}'s recipe"
    owner_badge_es = f"Receta de {owner}"
    hero_class = "hero category-tuti" if owner == "Tuti" else "hero"

    lines = [
        "<!DOCTYPE html>",
        "<html lang=\"en\">",
        "<head>",
        "  <meta charset=\"UTF-8\" />",
        "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />",
        f"  <title data-i18n=\"{quote(payload['title_en'])}\" data-i18n-es=\"{quote(payload['title_es'])}\">{quote(payload['title_en'])}</title>",
        "  <link rel=\"stylesheet\" href=\"styles.css\" />",
        "  <script src=\"lang-switcher.js\" defer></script>",
        "</head>",
        f"<body data-page=\"{Path(payload['filename']).stem}\">",
        "  <article class=\"page\">",
        f"    <div class=\"{hero_class}\">",
        "      <div class=\"language-switcher\">",
        "        <label data-i18n=\"Language\" data-i18n-es=\"Idioma\">Language</label>",
        "        <select id=\"language-select\">",
        "          <option value=\"en\">English</option>",
        "          <option value=\"es\">Espa\u00f1ol</option>",
        "        </select>",
        "      </div>",
        "      <a class=\"back-link\" href=\"index.html\" data-i18n=\"Back to recipes\" data-i18n-es=\"Volver a recetas\">Back to recipes</a>",
        f"      <h1 data-i18n=\"{quote(payload['title_en'])}\" data-i18n-es=\"{quote(payload['title_es'])}\">{quote(payload['title_en'])}</h1>",
        "      <div class=\"meta\">",
        "        <span class=\"badge\" data-i18n=\"Air fryer recipe\" data-i18n-es=\"Receta en freidora de aire\">Air fryer recipe</span>",
        f"        <span class=\"badge owner-badge\" data-i18n=\"{quote(owner_badge_en)}\" data-i18n-es=\"{quote(owner_badge_es)}\">{quote(owner_badge_en)}</span>",
        "      </div>",
        f"      <p class=\"summary\" data-i18n=\"{quote(payload['summary_en'])}\" data-i18n-es=\"{quote(payload['summary_es'])}\">{quote(payload['summary_en'])}</p>",
        "    </div>",
        "    <div class=\"grid\">",
        "      <section class=\"card\">",
        "        <div class=\"section-title\" data-i18n=\"Ingredients\" data-i18n-es=\"Ingredientes\">Ingredients</div>",
        "        <ul>",
    ]

    for en, es in zip(payload["ingredients_en"], payload["ingredients_es"]):
        lines.append(f"          <li data-i18n=\"{quote(en)}\" data-i18n-es=\"{quote(es)}\">{quote(en)}</li>")

    lines.extend([
        "        </ul>",
        "      </section>",
        "      <section class=\"card\">",
        "        <div class=\"section-title\" data-i18n=\"Instructions\" data-i18n-es=\"Instrucciones\">Instructions</div>",
        "        <ol>",
    ])

    for en, es in zip(payload["instructions_en"], payload["instructions_es"]):
        lines.append(f"          <li data-i18n=\"{quote(en)}\" data-i18n-es=\"{quote(es)}\">{quote(en)}</li>")

    lines.extend([
        "        </ol>",
        "      </section>",
        "    </div>",
        "    <div class=\"footer\" data-i18n=\"Use the language switcher to read this recipe in English or Spanish.\" data-i18n-es=\"Usa el selector de idioma para leer esta receta en ingles o espanol.\">Use the language switcher to read this recipe in English or Spanish.</div>",
        "  </article>",
        "</body>",
        "</html>",
    ])

    return "\n".join(lines)


def build_index(payloads: list[dict]) -> str:
    section_order = [
        "DESAYUNOS",
        "ENTRADAS O PIQUEOS",
        "PESCADO Y MARISCOS",
        "CARNE DE CERDO",
        "VEGETALES Y RECETAS VEGETARIANAS",
        "ACOMPA\u00d1ANTES",
        "POSTRES",
        "SPECIAL",
    ]

    lines = [
        "<!DOCTYPE html>",
        "<html lang=\"en\">",
        "<head>",
        "  <meta charset=\"UTF-8\" />",
        "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />",
        "  <title data-i18n=\"Recipes\" data-i18n-es=\"Recetas\">Recipes</title>",
        "  <link rel=\"stylesheet\" href=\"styles.css\" />",
        "  <script src=\"lang-switcher.js\" defer></script>",
        "  <script src=\"search.js\" defer></script>",
        "</head>",
        "<body data-page=\"recipes-index\">",
        "  <article class=\"page\">",
        "    <div class=\"hero category-tuti\">",
        "      <div class=\"language-switcher\">",
        "        <label data-i18n=\"Language\" data-i18n-es=\"Idioma\">Language</label>",
        "        <select id=\"language-select\">",
        "          <option value=\"en\">English</option>",
        "          <option value=\"es\">Espa\u00f1ol</option>",
        "        </select>",
        "      </div>",
        "      <h1 data-i18n=\"Recipes\" data-i18n-es=\"Recetas\">Recipes</h1>",
        "      <div class=\"meta\">",
        "        <span class=\"badge\" data-i18n=\"Bilingual collection\" data-i18n-es=\"Coleccion bilingue\">Bilingual collection</span>",
        "        <span class=\"badge\" data-i18n=\"Tuti and Lobo recipes\" data-i18n-es=\"Recetas de Tuti y Lobo\">Tuti and Lobo recipes</span>",
        "      </div>",
        "      <p class=\"summary\" data-i18n=\"Every recipe includes cleaned ingredients, clear instructions, owner labels, and concise summaries.\" data-i18n-es=\"Cada receta incluye ingredientes ordenados, instrucciones claras, etiqueta de autor y resumen breve.\">Every recipe includes cleaned ingredients, clear instructions, owner labels, and concise summaries.</p>",
        "      <form id=\"recipe-search-form\" class=\"search-bar\" role=\"search\">",
        "        <label class=\"search-label\" for=\"recipe-search\" data-i18n=\"Search recipes\" data-i18n-es=\"Buscar recetas\">Search recipes</label>",
        "        <div class=\"search-controls\">",
        "          <input id=\"recipe-search\" type=\"search\" data-i18n-placeholder=\"Search recipes by title, category, owner, or ingredient\" data-i18n-placeholder-es=\"Buscar por titulo, categoria, autor o ingrediente\" placeholder=\"Search recipes by title, category, owner, or ingredient\" />",
        "          <button id=\"recipe-search-button\" class=\"search-button\" type=\"submit\" data-i18n=\"Search\" data-i18n-es=\"Buscar\">Search</button>",
        "          <button id=\"recipe-search-clear\" class=\"search-clear\" type=\"button\" data-i18n=\"Clear\" data-i18n-es=\"Limpiar\" hidden>Clear</button>",
        "        </div>",
        "        <p id=\"search-results-status\" class=\"search-results-status\" data-i18n=\"Loading results...\" data-i18n-es=\"Cargando resultados...\">Loading results...</p>",
        "      </form>",
        "      <div id=\"no-results\" class=\"no-results\" data-i18n=\"No recipes match that search.\" data-i18n-es=\"No hay recetas que coincidan con esa busqueda.\" style=\"display:none;\">No recipes match that search.</div>",
        "    </div>",
    ]

    for section in section_order:
        sec_payloads = [p for p in payloads if p["category"] == section]
        if not sec_payloads:
            continue
        label_en, label_es = CATEGORY_LABELS.get(section, (section.title(), section.title()))

        section_class = "category-section category-tuti" if any(p["owner"] == "Tuti" for p in sec_payloads) else "category-section"
        lines.extend([
            f"    <section class=\"{section_class}\">",
            "      <div class=\"category-header\">",
            f"        <h2 data-i18n=\"{quote(label_en)}\" data-i18n-es=\"{quote(label_es)}\">{quote(label_en)}</h2>",
            f"        <p data-i18n=\"Browse {quote(label_en)} recipes.\" data-i18n-es=\"Explora recetas de {quote(label_es)}.\">Browse {quote(label_en)} recipes.</p>",
            "      </div>",
            "      <div class=\"recipe-grid grid-2\">",
        ])

        for payload in sec_payloads:
            owner = payload["owner"]
            owner_en = f"{owner}'s recipe"
            owner_es = f"Receta de {owner}"
            card_class = "recipe-card recipe-card-tuti" if owner == "Tuti" else "recipe-card"
            lines.extend([
                f"        <a class=\"{card_class}\" href=\"{quote(payload['filename'])}\" data-title=\"{quote(payload['title_en'])}\" data-title-es=\"{quote(payload['title_es'])}\" data-description=\"{quote(payload['summary_en'])}\" data-description-es=\"{quote(payload['summary_es'])}\" data-category=\"{quote(label_en)}\" data-category-es=\"{quote(label_es)}\" data-owner=\"{quote(owner)}\">",
                "          <div class=\"section-title\">",
                f"            <span data-i18n=\"{quote(payload['title_en'])}\" data-i18n-es=\"{quote(payload['title_es'])}\">{quote(payload['title_en'])}</span>",
                "          </div>",
                "          <div class=\"recipe-meta\">",
                f"            <span class=\"recipe-badge\" data-i18n=\"{quote(label_en)}\" data-i18n-es=\"{quote(label_es)}\">{quote(label_en)}</span>",
                f"            <span class=\"recipe-badge owner-badge\" data-i18n=\"{quote(owner_en)}\" data-i18n-es=\"{quote(owner_es)}\">{quote(owner_en)}</span>",
                "          </div>",
                "        </a>",
            ])

        lines.extend([
            "      </div>",
            "    </section>",
        ])

    lines.extend([
        "    <div class=\"footer\" data-i18n=\"Open any card to view the bilingual recipe page with cleaned ingredients and instructions.\" data-i18n-es=\"Abre cualquier receta para ver su pagina bilingue con ingredientes e instrucciones ordenadas.\">Open any card to view the bilingual recipe page with cleaned ingredients and instructions.</div>",
        "  </article>",
        "</body>",
        "</html>",
    ])

    return "\n".join(lines)


def main() -> None:
    raw = SOURCE.read_text(encoding="utf-8")
    recipes = parse_recipes(raw)

    all_recipes = recipes + EXTRA_RECIPES
    payloads = [build_recipe_payload(r) for r in all_recipes]

    for payload in payloads:
        if payload["filename"] in LOCKED_RECIPE_FILES and (OUTPUT_DIR / payload["filename"]).exists():
            continue
        html_page = render_recipe_page(payload)
        (OUTPUT_DIR / payload["filename"]).write_text(html_page, encoding="utf-8")

    index_html = build_index(payloads)
    (OUTPUT_DIR / "index.html").write_text(index_html, encoding="utf-8")

    print(f"Recipes parsed from source: {len(recipes)}")
    print(f"Extra recipes included: {len(EXTRA_RECIPES)}")
    print(f"Total recipe pages written: {len(payloads)}")


if __name__ == "__main__":
    main()
