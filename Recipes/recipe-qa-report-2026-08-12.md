# Recipe QA Report

Date: 2026-08-12
Scope: All generated recipe pages except chicken-soup.html and curried-lentils.html
Method: Read-only QA pass over 88 recipe pages, checking English phrasing, Spanish ingredient/instruction breakdown, and write-up quality against the generated HTML and the Spanish source when needed.
Outcome: 0 fully clean pages. Every reviewed page has at least one issue. The most important problems are structural extraction errors on a smaller subset of pages and weak English copy across the entire set.

## Highest Priority Findings

These are the pages where the recipe structure is materially broken, source boundaries leaked, real ingredients were moved into instructions, or content from another recipe was pulled in.

- [Public/Recipes/tostadas-francesas-en-cupcakes.html](Public/Recipes/tostadas-francesas-en-cupcakes.html): Severe cross-recipe contamination. Ingredients include content from the next recipe, Crème brûlée con mermelada de berries, and instructions 10 to 16 belong to a different dish. Instruction 1 is also an ingredient line, not a step.
- [Public/Recipes/fajitas-de-setas-y-verduras.html](Public/Recipes/fajitas-de-setas-y-verduras.html): Multiple Spanish breakdown failures. Lemon juice, salt, pepper, and tortillas were merged into instructions, the heading ACOMPAÑANTES leaked into Ingredients, and the summary was built from an ingredient line instead of a cooking action.
- [Public/Recipes/albondigas-en-salsa-de-tomate.html](Public/Recipes/albondigas-en-salsa-de-tomate.html): A source ingredient row with tomato sauce, white wine, evaporated milk, and breadcrumbs was moved into Instructions, leaving the Ingredients list incomplete.
- [Public/Recipes/albondigas-de-pollo-con-zucchini.html](Public/Recipes/albondigas-de-pollo-con-zucchini.html): The next source heading, PESCADO Y MARISCOS, leaked into Ingredients, so the page carries section-boundary contamination.
- [Public/Recipes/pollo-empanizado-con-salsa-de-limon.html](Public/Recipes/pollo-empanizado-con-salsa-de-limon.html): The marinade line starting with sillao, garlic, and ginger was emitted as instruction 1 instead of staying in Ingredients.
- [Public/Recipes/pollo-crujiente-con-parmesano.html](Public/Recipes/pollo-crujiente-con-parmesano.html): Instruction 1 is actually a garnish or serving ingredient line. Core ingredients are partially lost behind placeholders.
- [Public/Recipes/pechugas-rellenas-italianas.html](Public/Recipes/pechugas-rellenas-italianas.html): Instruction 1 is a broken ingredient or serving line, and the key fillings are obscured in English.
- [Public/Recipes/croquetas-de-verduras.html](Public/Recipes/croquetas-de-verduras.html): Instruction 4 is generic filler that replaces a real Spanish action, so the method loses a necessary step.
- [Public/Recipes/hamburguesas-de-garbanzos-y-espinacas.html](Public/Recipes/hamburguesas-de-garbanzos-y-espinacas.html): Instruction 1 is an ingredient line, and the optional softening or breading note is split awkwardly between Ingredients and Instructions.
- [Public/Recipes/papas-hasselback.html](Public/Recipes/papas-hasselback.html): The ingredient section effectively collapsed. The butter, garlic, and herb mixture appears only in instructions.
- [Public/Recipes/platano-frito.html](Public/Recipes/platano-frito.html): The ingredient section is functionally missing, reduced to a placeholder entry.
- [Public/Recipes/muffins-de-zapallo-y-zucchini.html](Public/Recipes/muffins-de-zapallo-y-zucchini.html): Instruction 1 is an ingredient line, and several core ingredients remain placeholders.
- [Public/Recipes/pechugas-rellenas-con-queso-boursin-y-espinaca.html](Public/Recipes/pechugas-rellenas-con-queso-boursin-y-espinaca.html): The Boursin quantity and substitution note were split out of Ingredients and pushed into the first step or summary area.
- [Public/Recipes/steak-panzanella.html](Public/Recipes/steak-panzanella.html): The summary and instruction 1 absorb potatoes or salad serving notes instead of describing the recipe properly.
- [Public/Recipes/brownies.html](Public/Recipes/brownies.html): The final ingredient line, nuts plus chocolate chips, was moved into the summary and duplicated as instruction 1.
- [Public/Recipes/omelette-tortilla-huevo.html](Public/Recipes/omelette-tortilla-huevo.html): Variant omelet formulas from the source were appended as instruction steps instead of being separated as variations or notes.
- [Public/Recipes/chips-de-kale.html](Public/Recipes/chips-de-kale.html): Ingredient parsing changed meaning. A line containing rice vinegar and salt became 1 tablespoon salt, dropping the vinegar.
- [Public/Recipes/camarones-po-boys.html](Public/Recipes/camarones-po-boys.html): Ingredient list is severely corrupted, including a stray Beef item, and the Cajun seasoning formula is dumped into the main method instead of being clearly separated.
- [Public/Recipes/pan-casero.html](Public/Recipes/pan-casero.html): Ingredient list is materially corrupted, including a phantom Chicken item. A real dough-forming step is replaced with generic filler.
- [Public/Recipes/chancho-thai-dulce.html](Public/Recipes/chancho-thai-dulce.html): Pork is mistranslated as beef, a real removal step is replaced by generic filler, and the ginger sauce subrecipe is muddled into the main method.
- [Public/Recipes/papas-con-lentejas.html](Public/Recipes/papas-con-lentejas.html): The final English instruction invents Serve with the cauliflower, which is not supported by the Spanish source.
- [Public/Recipes/pimientos-rellenos.html](Public/Recipes/pimientos-rellenos.html): The source instruction to mix and season is flattened into generic filler, which drops the explicit seasoning action.
- [Public/Recipes/huevos-al-plato.html](Public/Recipes/huevos-al-plato.html): The English title is wrong for the dish, several ingredients are corrupted, and one real instruction is replaced with boilerplate.
- [Public/Recipes/papa-rellena.html](Public/Recipes/papa-rellena.html): Ingredient meaning is lost in multiple places, including ají colorado, raisins, olives, and oil handling. The English reads like an unfinished draft.

## Significant Editorial Findings

These pages are not structurally destroyed, but they are not publishable yet because the English is inaccurate, overly literal, mixed-language, placeholder-heavy, or the title and summary do not match the dish well.

- [Public/Recipes/magdalenas.html](Public/Recipes/magdalenas.html): English title is misleading as Madeleines. Summary mentions browning protein, which is obviously unrelated to the dessert.
- [Public/Recipes/chicharron-de-chancho.html](Public/Recipes/chicharron-de-chancho.html): Pork Cracklings is a misleading English title for this preparation.
- [Public/Recipes/croquetas-con-tocino-o-jamon.html](Public/Recipes/croquetas-con-tocino-o-jamon.html): Recipe depends on a cross-reference to tuna croquettes instead of standing on its own.
- [Public/Recipes/variedades-de-pollo-empanizado.html](Public/Recipes/variedades-de-pollo-empanizado.html): Ingredients collapse to Sin ingredientes claros en la fuente original, leaving the page unusable.
- [Public/Recipes/camote-frito.html](Public/Recipes/camote-frito.html): Ingredients collapse to Sin ingredientes claros en la fuente original.
- [Public/Recipes/chips-de-platano.html](Public/Recipes/chips-de-platano.html): Ingredients collapse to Sin ingredientes claros en la fuente original.
- [Public/Recipes/platano-caramelizado.html](Public/Recipes/platano-caramelizado.html): Ingredient section collapses to Listed ingredient, and the summary is generic boilerplate.
- [Public/Recipes/bolitas-de-quinua.html](Public/Recipes/bolitas-de-quinua.html): Ingredient list is largely placeholders, which makes the recipe unreliable in English.
- [Public/Recipes/falafel.html](Public/Recipes/falafel.html): Ingredient list loses key names to placeholders, and instructions remain mixed Spanish-English.
- [Public/Recipes/brochetas-de-pollo-con-pina-y-pimiento.html](Public/Recipes/brochetas-de-pollo-con-pina-y-pimiento.html): Ingredient list is degraded by multiple placeholder entries, hiding key items.
- [Public/Recipes/alitas-de-pollo.html](Public/Recipes/alitas-de-pollo.html): Summary is pulled from the first source step, not a summary, and ingredient naming is weak.
- [Public/Recipes/salmon-con-mantequilla-y-limon.html](Public/Recipes/salmon-con-mantequilla-y-limon.html): Ingredient list is mostly placeholders, obscuring core items.
- [Public/Recipes/salmon-con-glaseado-de-durazno.html](Public/Recipes/salmon-con-glaseado-de-durazno.html): Ingredient list is mostly placeholders, and garnish text is corrupted as garlicnjoli.
- [Public/Recipes/costillar-de-cerdo-glaseado.html](Public/Recipes/costillar-de-cerdo-glaseado.html): Ingredient list is mostly placeholders, obscuring the glaze composition.
- [Public/Recipes/bastones-de-zucchini-crujientes.html](Public/Recipes/bastones-de-zucchini-crujientes.html): A generic filler line appears as a real instruction.
- [Public/Recipes/coliflor-gratinada-asiatica.html](Public/Recipes/coliflor-gratinada-asiatica.html): Ingredient list is largely placeholders.
- [Public/Recipes/vainitas-con-tofu.html](Public/Recipes/vainitas-con-tofu.html): Ingredient list is largely placeholders and one line is text-corrupted.
- [Public/Recipes/papas-fritas.html](Public/Recipes/papas-fritas.html): Ingredient section collapses to Listed ingredient and the summary mentions protein.
- [Public/Recipes/camotes-estilo-cajun.html](Public/Recipes/camotes-estilo-cajun.html): Ingredient section collapses to Listed ingredient.
- [Public/Recipes/tostones.html](Public/Recipes/tostones.html): Ingredient section collapses to Listed ingredient, though the method is broadly recoverable.
- [Public/Recipes/croquetas-de-queso.html](Public/Recipes/croquetas-de-queso.html): Source split is mostly intact, but English remains overly literal and mixed-language.
- [Public/Recipes/tostadas-con-natilla.html](Public/Recipes/tostadas-con-natilla.html): Summary is unrelated, several ingredients are placeholders, and the method is heavily mixed-language.
- [Public/Recipes/napolitanas.html](Public/Recipes/napolitanas.html): Summary is generic and unrelated, and the English stays mixed-language.
- [Public/Recipes/quequitos-de-garbanzo.html](Public/Recipes/quequitos-de-garbanzo.html): Chickpea Muffins is misleading. The source reads more like balls or croquettes than muffins.
- [Public/Recipes/pollo-crujiente.html](Public/Recipes/pollo-crujiente.html): Ingredient list obscures milk, lemon juice, and cornflakes behind placeholders.
- [Public/Recipes/piernas-de-pollo-con-vegetales.html](Public/Recipes/piernas-de-pollo-con-vegetales.html): Ingredient list weakens several items and the summary is unrelated to the dish.
- [Public/Recipes/albondigas-de-pollo-thai.html](Public/Recipes/albondigas-de-pollo-thai.html): First instruction is really a serving note, ingredient naming is degraded, and ajonjolí is corrupted.
- [Public/Recipes/pescado-rebozado.html](Public/Recipes/pescado-rebozado.html): English title remains in Spanish, summary is irrelevant, ingredient entries are vague.
- [Public/Recipes/pescado-al-vapor-en-paquetitos.html](Public/Recipes/pescado-al-vapor-en-paquetitos.html): Structure is decent, but the English remains heavily mixed-language.
- [Public/Recipes/hamburguesas.html](Public/Recipes/hamburguesas.html): Summary is pulled from an optional note instead of describing the burger, and garnish items are reduced to weak placeholders.
- [Public/Recipes/parrillada-de-res.html](Public/Recipes/parrillada-de-res.html): Title is awkward, summary is generic, and key ingredients are flattened into placeholders.
- [Public/Recipes/coca-de-hojaldre-y-verduras.html](Public/Recipes/coca-de-hojaldre-y-verduras.html): Sequence survives, but ingredient lines are weakened and English remains literal.
- [Public/Recipes/tofu-empanizado.html](Public/Recipes/tofu-empanizado.html): Tofu, sauces, and sesame are obscured by placeholders.
- [Public/Recipes/papas-fritas-congeladas.html](Public/Recipes/papas-fritas-congeladas.html): Summary is wrong for fries, and Ingredients fall back to Listed ingredient.
- [Public/Recipes/crutones.html](Public/Recipes/crutones.html): Ingredients are reduced to a placeholder rather than a compact honest list.
- [Public/Recipes/mini-croissants.html](Public/Recipes/mini-croissants.html): Structurally sound, but summary is generic, ingredients are vague, and method carries obvious Spanish words.
- [Public/Recipes/crumble-de-manzana.html](Public/Recipes/crumble-de-manzana.html): Ingredient list is flattened into placeholders, even though the method sequence survives.
- [Public/Recipes/tostadas-francesas-saladas.html](Public/Recipes/tostadas-francesas-saladas.html): Split is mostly intact, but nearly every step is mixed Spanish-English.
- [Public/Recipes/empanadas.html](Public/Recipes/empanadas.html): Ingredient list is oversimplified, cheese filling disappears, and ajonjolí is corrupted.
- [Public/Recipes/croquetas-de-atun.html](Public/Recipes/croquetas-de-atun.html): Split is intact, but the English is heavily calqued and the recipe remains incomplete for a cook.
- [Public/Recipes/san-jacobos.html](Public/Recipes/san-jacobos.html): Ham is lost as a placeholder, and the method is half untranslated.
- [Public/Recipes/brochetas-de-pollo.html](Public/Recipes/brochetas-de-pollo.html): Method order is fine, but the English is very literal and awkward.
- [Public/Recipes/pescado-a-la-menier.html](Public/Recipes/pescado-a-la-menier.html): Title is not normalized in English and key ingredients are placeholders.
- [Public/Recipes/camarones-al-ajillo.html](Public/Recipes/camarones-al-ajillo.html): Step sequence is correct, but shrimp is hidden as a placeholder and the instructions remain mixed-language.
- [Public/Recipes/filetes-rusos-o-albondigas.html](Public/Recipes/filetes-rusos-o-albondigas.html): Structure is intact, but seasoning lines degrade into placeholder phrasing.
- [Public/Recipes/filetes-de-cerdo-con-jamon-y-queso.html](Public/Recipes/filetes-de-cerdo-con-jamon-y-queso.html): Basic method survives, but ham is obscured and the coating steps are word-for-word rather than natural English.
- [Public/Recipes/pasta-carbonara.html](Public/Recipes/pasta-carbonara.html): Several core ingredients remain placeholders, so the page is understandable only with guesswork.
- [Public/Recipes/tortilla-de-patatas.html](Public/Recipes/tortilla-de-patatas.html): Split is fine, but Potato Tortilla is a weak English title and the prose is stiff.
- [Public/Recipes/tostadas-con-pesto.html](Public/Recipes/tostadas-con-pesto.html): Ingredient list hides pesto and cheese, while the instruction suddenly specifies vegan cheese.
- [Public/Recipes/churros.html](Public/Recipes/churros.html): Method order is intact, but the page is still mixed-language and unpolished.
- [Public/Recipes/tostadas-francesas-dulces.html](Public/Recipes/tostadas-francesas-dulces.html): Spanish split is usable, but English is not publication-ready and still contains machine-like phrasing.
- [Public/Recipes/granola.html](Public/Recipes/granola.html): Spanish split is usable, but English remains placeholder-like and generic.
- [Public/Recipes/paninis.html](Public/Recipes/paninis.html): Spanish split is usable, but English remains mixed-language and weak.
- [Public/Recipes/empanadas-gallegas.html](Public/Recipes/empanadas-gallegas.html): Split is mostly usable, but English is not publishable yet.
- [Public/Recipes/esparragos-con-jamon.html](Public/Recipes/esparragos-con-jamon.html): Split is usable, but English phrasing stays mechanical.
- [Public/Recipes/pechuga-a-la-parrilla.html](Public/Recipes/pechuga-a-la-parrilla.html): Split is usable, but English remains literal rather than kitchen-natural.
- [Public/Recipes/cordon-bleu-de-pollo.html](Public/Recipes/cordon-bleu-de-pollo.html): Split is usable, but English remains mixed-language.
- [Public/Recipes/pinchos-de-salmon-con-pina-y-tomates-cherry.html](Public/Recipes/pinchos-de-salmon-con-pina-y-tomates-cherry.html): Split is usable, but English still sounds machine-translated.
- [Public/Recipes/calamares-rebozados.html](Public/Recipes/calamares-rebozados.html): Split is usable, but English is overly literal.
- [Public/Recipes/tempura-de-coliflor-y-brocoli.html](Public/Recipes/tempura-de-coliflor-y-brocoli.html): Split is usable, but English phrasing is not publishable.
- [Public/Recipes/verduras-salteadas.html](Public/Recipes/verduras-salteadas.html): Split is usable, but English remains mixed-language.
- [Public/Recipes/coliflor-gratinada.html](Public/Recipes/coliflor-gratinada.html): Split is usable, but English is still awkward.
- [Public/Recipes/berenjenas-rellenas.html](Public/Recipes/berenjenas-rellenas.html): Split is usable, but English is still machine-like.

## Coverage Notes

These pages were reviewed and found problematic, but their main issue is English quality rather than a clearly broken Spanish split. They still need editorial attention even when the underlying Spanish structure is mostly usable.

- [Public/Recipes/tostadas-francesas-dulces.html](Public/Recipes/tostadas-francesas-dulces.html)
- [Public/Recipes/granola.html](Public/Recipes/granola.html)
- [Public/Recipes/paninis.html](Public/Recipes/paninis.html)
- [Public/Recipes/empanadas-gallegas.html](Public/Recipes/empanadas-gallegas.html)
- [Public/Recipes/esparragos-con-jamon.html](Public/Recipes/esparragos-con-jamon.html)
- [Public/Recipes/pechuga-a-la-parrilla.html](Public/Recipes/pechuga-a-la-parrilla.html)
- [Public/Recipes/cordon-bleu-de-pollo.html](Public/Recipes/cordon-bleu-de-pollo.html)
- [Public/Recipes/pinchos-de-salmon-con-pina-y-tomates-cherry.html](Public/Recipes/pinchos-de-salmon-con-pina-y-tomates-cherry.html)
- [Public/Recipes/calamares-rebozados.html](Public/Recipes/calamares-rebozados.html)
- [Public/Recipes/tempura-de-coliflor-y-brocoli.html](Public/Recipes/tempura-de-coliflor-y-brocoli.html)
- [Public/Recipes/verduras-salteadas.html](Public/Recipes/verduras-salteadas.html)
- [Public/Recipes/coliflor-gratinada.html](Public/Recipes/coliflor-gratinada.html)
- [Public/Recipes/berenjenas-rellenas.html](Public/Recipes/berenjenas-rellenas.html)

## Chef Recommendations, Not Approved For Execution

These are editorial recommendations only. They have not been applied.

- Rewrite English titles, summaries, ingredients, and instructions as proper recipe prose, not token-by-token bilingual substitutions.
- Make every recipe page self-contained. If a page references another recipe for method, restate the needed base method locally.
- Keep ingredient nouns explicit. Never publish placeholder outputs such as Listed ingredient, 1 cheese, or 1 beef.
- Separate subrecipes, sauces, garnish notes, serving notes, seasoning formulas, and variations into labeled subsections or notes instead of pushing them into the main method.
- Normalize English culinary naming where the current title changes the dish identity. Examples include Huevos al plato, Magdalenas, Chicharrón de chancho, Pescado a la menier, and Quequitos de garbanzo.
- Replace generic or irrelevant summaries with one real chef-style sentence that describes the finished dish, its texture, and serving context.
- Add an editorial guardrail pass for obvious corruption signals such as listed ingredient, phantom ingredients, section-header leakage, cross-recipe contamination, and instruction 1 being an ingredient line.
- Preserve source meaning before style. Wrong food identity is a harder failure than awkward prose, so pork should remain pork, vinegar should not disappear, and unsupported ingredients should never be invented.
- When the source is sparse, prefer an honest compact list or a note about source brevity over placeholders.
- For variation-heavy pages, use short subsections so a cook can actually follow them on screen.
