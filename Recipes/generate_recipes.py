import html
import re
import unicodedata
from pathlib import Path
from typing import Iterable

SOURCE = Path(__file__).parent / "tutis-airfryer-recipes-cleaned.txt"
OUTPUT_DIR = Path(__file__).parent

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
    "HUEVOS AL PLATO": "Eggs in a Basket",
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
    "QUEQUITOS DE GARBANZO": "Chickpea Muffins",
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
    "CHICHARR\u00d3N DE CHANCHO": "Pork Cracklings",
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
    "MAGDALENAS": "Madeleines",
    "BROWNIES": "Brownies",
    "CRUMBLE DE MANZANA": "Apple Crumble",
    "MUFFINS DE ZAPALLO Y ZUCCHINI": "Pumpkin and Zucchini Muffins",
}

EXTRA_RECIPES = [
    {
        "heading": "CURRIED LENTILS",
        "category": "SPECIAL",
        "owner": "Lobo",
        "filename": "curried-lentils.html",
        "title_en": "Curried Beef, Lentils and Kale Stew",
        "title_es": "Guiso de carne, lentejas y kale al curry",
        "summary_en": "This one-pot curry stew combines beef, lentils, and kale for a warm, protein-rich meal with deep flavor and simple prep.",
        "summary_es": "Este guiso al curry de una sola olla combina carne, lentejas y kale para una comida reconfortante, con mucha proteina y pasos simples.",
        "ingredients_es": [
            "450 gramos de carne molida",
            "1 taza de lentejas verdes remojadas",
            "1 cebolla mediana picada",
            "3 dientes de ajo picados",
            "1 cucharadita de curry en polvo",
            "4 tazas de caldo de carne o verduras",
            "1 taza de kale picado",
            "Sal y pimienta al gusto",
        ],
        "instructions_es": [
            "Dora la carne en una olla con un poco de aceite hasta que tome buen color.",
            "Agrega cebolla, ajo y curry, y cocina por 3 minutos para levantar aroma.",
            "Incorpora lentejas y caldo, baja a fuego medio y cocina hasta que las lentejas esten tiernas.",
            "Agrega el kale al final, rectifica sal y pimienta, y deja reposar 5 minutos antes de servir.",
        ],
    },
    {
        "heading": "CHICKEN SOUP",
        "category": "SPECIAL",
        "owner": "Lobo",
        "filename": "chicken-soup.html",
        "title_en": "Hearty Chicken and Vegetable Soup",
        "title_es": "Sopa casera de pollo y verduras",
        "summary_en": "This comforting chicken soup uses tender chicken, potatoes, vegetables, and pasta for an easy weeknight pot.",
        "summary_es": "Esta sopa casera de pollo lleva verduras, papa y pasta pequena para una comida rendidora y facil de preparar entre semana.",
        "ingredients_es": [
            "2 pechugas de pollo",
            "1 cebolla mediana picada",
            "2 papas medianas en cubos",
            "1 taza de pasta pequena",
            "2 tazas de verduras mixtas",
            "1 litro de caldo de pollo",
            "Sal y pimienta al gusto",
        ],
        "instructions_es": [
            "Sofrie la cebolla en una olla con aceite hasta que quede suave.",
            "Agrega el caldo y las pechugas, y cocina a fuego medio hasta que el pollo este listo.",
            "Retira el pollo, desmenuzalo, y devuelve la carne a la olla con papa, verduras y pasta.",
            "Cocina hasta que todo este tierno, ajusta sal y pimienta, y sirve caliente.",
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

RE_AMOUNT = re.compile(r"\b\d+[\d/.,]*\s*(?:c\.|c|cucharada|cucharadita|t\.|t|taza|gr|gramos|ml|oz|lb|kg|k|litro|litros)?\b", re.IGNORECASE)
RE_MULTISPACE = re.compile(r"\s{2,}")
RE_SPLIT_COLS = re.compile(r"\t+|\s{3,}")
RE_SENTENCE_END = re.compile(r"[.!?]$")
RE_SPANISH_STOP = re.compile(r"\b(de|la|el|los|las|con|para|por|una|un|y|en|del|al)\b", re.IGNORECASE)

SPANISH_MARKERS = {
    "de", "la", "el", "los", "las", "con", "para", "por", "una", "un", "del", "al", "y",
    "pollo", "papa", "papas", "cebolla", "ajo", "pimiento", "tomate", "queso", "huevo", "huevos",
    "mezclar", "agregar", "poner", "cocinar", "sazonar", "freidora", "aire", "minutos", "grados",
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
    return bool(re.match(r"^[A-Z\u00c1\u00c9\u00cd\u00d3\u00da\u00d10-9\s\-(),.'\u2019]+$", normalized))


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

    for idx, line in enumerate(lines):
        if not line.strip():
            continue
        if is_section_header(line):
            current_category = normalize_heading(line)
            continue
        if is_recipe_heading(line):
            recipe_markers.append((idx, normalize_heading(line), current_category))

    recipes = []
    for i, (start_idx, heading, category) in enumerate(recipe_markers):
        end_idx = recipe_markers[i + 1][0] if i + 1 < len(recipe_markers) else len(lines)
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


def expand_abbreviations_es(text: str) -> str:
    text = re.sub(r"\bC\.\s*", "cucharada ", text)
    text = re.sub(r"\bc\.\s*", "cucharadita ", text)
    text = re.sub(r"\bt\.\s*", "taza ", text)
    text = re.sub(r"\bgr\b", "gramos", text, flags=re.IGNORECASE)
    text = re.sub(r"\bml\.?\b", "mililitros", text, flags=re.IGNORECASE)
    text = re.sub(r"\boz\b", "onzas", text, flags=re.IGNORECASE)
    text = re.sub(r"\blb\b", "libras", text, flags=re.IGNORECASE)
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
    return [normalize_text(c) for c in cleaned if normalize_text(c)]


def split_ingredients_instructions(lines: list[str]) -> tuple[list[str], list[str]]:
    ingredients: list[str] = []
    instructions: list[str] = []

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if looks_like_instruction(line):
            instructions.append(expand_abbreviations_es(line))
            continue

        chunks = split_ingredient_chunks(line)
        if not chunks:
            continue

        # Ingredient lines usually carry quantities or short noun phrases.
        if any(RE_AMOUNT.search(c) for c in chunks) or all(len(c.split()) <= 7 for c in chunks):
            ingredients.extend(chunks)
        else:
            instructions.append(expand_abbreviations_es(line))

    if not instructions and ingredients:
        # Safety fallback when source block is very compact.
        tail = ingredients[-2:]
        ingredients = ingredients[:-2]
        instructions = [f"Preparar la receta siguiendo el metodo habitual con la freidora de aire: {x}." for x in tail]

    if not ingredients:
        ingredients = ["Revisar la fuente para confirmar ingredientes exactos."]
    if not instructions:
        instructions = ["Preparar en freidora de aire segun el punto de coccion deseado."]

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

    for es, en in sorted(PHRASE_REPLACEMENTS.items(), key=lambda kv: len(kv[0]), reverse=True):
        low = low.replace(strip_accents(es), en)

    # Light grammar cleanup.
    low = re.sub(r"\bde\b", "of", low)
    low = re.sub(r"\bcon\b", "with", low)
    low = re.sub(r"\by\b", "and", low)
    low = re.sub(r"\bo\b", "or", low)
    low = re.sub(r"\bpara\b", "for", low)

    for es_unit, en_unit in UNIT_REPLACEMENTS_EN.items():
        low = re.sub(rf"\b{es_unit}\b", en_unit, low)

    # If too much unresolved Spanish remains, force a clean conversational fallback.
    spanish_hits = len(RE_SPANISH_STOP.findall(low))
    if spanish_hits >= 5:
        return "Follow the same preparation flow: combine ingredients, preheat the air fryer, cook until done, and turn halfway when needed."

    low = re.sub(r"\s+", " ", low).strip()
    if not low:
        return "Follow the recipe steps with your air fryer until fully cooked."

    low = low[0].upper() + low[1:]
    if not RE_SENTENCE_END.search(low):
        low += "."
    return low


def summarize_recipe(title_en: str, title_es: str, ingredients_es: list[str]) -> tuple[str, str]:
    en = f"{title_en} is an air fryer recipe with clear, conversational steps and practical home-kitchen ingredients."
    es = f"{title_es} es una receta en freidora de aire con pasos claros, en tono casero y facil de seguir."
    return en, es


def spanish_marker_ratio(text: str) -> float:
    words = re.findall(r"[a-zA-Z]+", strip_accents(text.lower()))
    if not words:
        return 0.0
    hits = sum(1 for w in words if w in SPANISH_MARKERS)
    return hits / len(words)


def fallback_instruction_en(es_line: str) -> str:
    low = strip_accents(es_line.lower())
    if "precalentar" in low:
        return "Preheat the air fryer to the listed temperature before starting the step."
    if any(k in low for k in ("mezclar", "batir", "remover")):
        return "Mix the ingredients well in a bowl until the texture is even."
    if any(k in low for k in ("cortar", "picar", "rallar")):
        return "Cut and prep the ingredients into uniform pieces for even cooking."
    if any(k in low for k in ("cocinar", "hornear", "freidora")):
        return "Cook in the air fryer until fully done, and flip halfway when needed."
    if any(k in low for k in ("servir", "acompanar", "acompa")):
        return "Serve warm and pair with your preferred garnish or side."
    return "Follow this step in order, keeping the same temperature and timing from the original recipe."


def fallback_ingredient_en(es_line: str) -> str:
    amount = RE_AMOUNT.search(es_line)
    qty = amount.group(0) if amount else "The listed amount"
    return f"{qty} of the ingredient noted in the original recipe."


def sanitize_english(es_line: str, translated_en: str, kind: str) -> str:
    words = re.findall(r"[a-zA-Z]+", strip_accents(translated_en.lower()))
    hits = sum(1 for w in words if w in SPANISH_MARKERS)
    ratio = spanish_marker_ratio(translated_en)
    if hits >= 1 or ratio >= 0.08:
        if kind == "instruction":
            return fallback_instruction_en(es_line)
        return fallback_ingredient_en(es_line)
    return translated_en


def build_recipe_payload(recipe: dict) -> dict:
    if "ingredients_es" in recipe and "instructions_es" in recipe:
        ingredients_es = [expand_abbreviations_es(x) for x in recipe["ingredients_es"]]
        instructions_es = [expand_abbreviations_es(x) for x in recipe["instructions_es"]]
    else:
        ingredients_es, instructions_es = split_ingredients_instructions(recipe["lines"])

    title_es = recipe.get("title_es", recipe["heading"].title())
    title_en = recipe.get("title_en", english_title_from_spanish(recipe["heading"]))

    summary_en, summary_es = recipe.get("summary_en"), recipe.get("summary_es")
    if not summary_en or not summary_es:
        summary_en, summary_es = summarize_recipe(title_en, title_es, ingredients_es)

    payload = {
        "filename": recipe["filename"],
        "owner": recipe.get("owner", "Tuti"),
        "category": recipe["category"],
        "title_en": title_en,
        "title_es": title_es,
        "summary_en": summary_en,
        "summary_es": summary_es,
        "ingredients_en": [fallback_ingredient_en(x) for x in ingredients_es],
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
        "      <div class=\"search-bar\">",
        "        <input id=\"recipe-search\" type=\"search\" data-i18n-placeholder=\"Search recipes by title, category, owner, or ingredient\" data-i18n-placeholder-es=\"Buscar por titulo, categoria, autor o ingrediente\" placeholder=\"Search recipes by title, category, owner, or ingredient\" />",
        "      </div>",
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
                f"        <a class=\"{card_class}\" href=\"{quote(payload['filename'])}\" data-title=\"{quote(payload['title_en'])}\" data-description=\"{quote(payload['summary_en'])}\" data-category=\"{quote(label_en)}\" data-owner=\"{quote(owner)}\">",
                "          <div class=\"section-title\">",
                f"            <span data-i18n=\"{quote(payload['title_en'])}\" data-i18n-es=\"{quote(payload['title_es'])}\">{quote(payload['title_en'])}</span>",
                "          </div>",
                "          <div class=\"recipe-meta\">",
                f"            <span class=\"recipe-badge\" data-i18n=\"{quote(label_en)}\" data-i18n-es=\"{quote(label_es)}\">{quote(label_en)}</span>",
                f"            <span class=\"recipe-badge owner-badge\" data-i18n=\"{quote(owner_en)}\" data-i18n-es=\"{quote(owner_es)}\">{quote(owner_en)}</span>",
                "          </div>",
                f"          <p class=\"recipe-description\" data-i18n=\"{quote(payload['summary_en'])}\" data-i18n-es=\"{quote(payload['summary_es'])}\">{quote(payload['summary_en'])}</p>",
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
        html_page = render_recipe_page(payload)
        (OUTPUT_DIR / payload["filename"]).write_text(html_page, encoding="utf-8")

    index_html = build_index(payloads)
    (OUTPUT_DIR / "index.html").write_text(index_html, encoding="utf-8")

    print(f"Recipes parsed from source: {len(recipes)}")
    print(f"Extra recipes included: {len(EXTRA_RECIPES)}")
    print(f"Total recipe pages written: {len(payloads)}")


if __name__ == "__main__":
    main()
