document.addEventListener('DOMContentLoaded', () => {
  const searchForm = document.getElementById('recipe-search-form');
  const searchInput = document.getElementById('recipe-search');
  const searchButton = document.getElementById('recipe-search-button');
  const clearButton = document.getElementById('recipe-search-clear');
  const resultsStatus = document.getElementById('search-results-status');
  const cards = Array.from(document.querySelectorAll('.recipe-card'));
  const sections = Array.from(document.querySelectorAll('.category-section'));
  const noResults = document.getElementById('no-results');
  let previousQuery = '';

  if (!searchInput || cards.length === 0) {
    return;
  }

  function normalizeForSearch(text) {
    return (text || '')
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '');
  }

  function buildCardSearchText(card) {
    const fieldValues = [
      card.dataset.title,
      card.dataset.description,
      card.dataset.category,
      card.dataset.owner,
      card.dataset.titleEs,
      card.dataset.descriptionEs,
      card.dataset.categoryEs,
    ];

    card.querySelectorAll('[data-i18n], [data-i18n-es]').forEach((el) => {
      fieldValues.push(el.getAttribute('data-i18n'));
      fieldValues.push(el.getAttribute('data-i18n-es'));
      fieldValues.push(el.textContent);
    });

    return normalizeForSearch(fieldValues.filter(Boolean).join(' '));
  }

  const searchCorpus = new Map(cards.map((card) => [card, buildCardSearchText(card)]));

  function isSpanishActive() {
    return document.body.classList.contains('lang-es');
  }

  function updateStatusText(visibleCount, query) {
    if (!resultsStatus) {
      return;
    }

    const usingSpanish = isSpanishActive();
    if (!query) {
      resultsStatus.textContent = usingSpanish
        ? `${visibleCount} recetas disponibles.`
        : `${visibleCount} recipes available.`;
      return;
    }

    resultsStatus.textContent = usingSpanish
      ? `${visibleCount} coincidencias para "${searchInput.value.trim()}".`
      : `${visibleCount} matches for "${searchInput.value.trim()}".`;
  }

  function updateResults() {
    const query = normalizeForSearch(searchInput.value.trim());
    let visibleCount = 0;
    let animationOrder = 0;

    cards.forEach((card) => {
      const corpus = searchCorpus.get(card) || '';
      const matches = !query || corpus.includes(query);
      card.style.display = matches ? '' : 'none';
      card.classList.remove('is-visible-result');
      if (matches) visibleCount += 1;

      if (matches && query) {
        card.style.setProperty('--search-order', String(animationOrder));
        animationOrder += 1;
      }
    });

    if (query && query !== previousQuery) {
      cards.forEach((card) => {
        if (card.style.display !== 'none') {
          // Restart animation when the query changes.
          void card.offsetWidth;
          card.classList.add('is-visible-result');
        }
      });
    }

    if (!query) {
      cards.forEach((card) => card.style.removeProperty('--search-order'));
    }

    sections.forEach((section) => {
      const sectionHasVisibleCards = Array.from(section.querySelectorAll('.recipe-card')).some((card) => card.style.display !== 'none');
      section.style.display = sectionHasVisibleCards ? '' : 'none';
    });

    if (noResults) {
      noResults.style.display = visibleCount === 0 ? 'block' : 'none';
    }

    if (clearButton) {
      clearButton.hidden = !query;
    }

    updateStatusText(visibleCount, query);
    previousQuery = query;
  }

  if (searchForm) {
    searchForm.addEventListener('submit', (event) => {
      event.preventDefault();
      updateResults();
      searchInput.focus();
    });
  }

  if (searchButton) {
    searchButton.addEventListener('click', () => {
      updateResults();
      searchInput.focus();
    });
  }

  if (clearButton) {
    clearButton.addEventListener('click', () => {
      searchInput.value = '';
      updateResults();
      searchInput.focus();
    });
  }

  searchInput.addEventListener('input', updateResults);
  const languageObserver = new MutationObserver(() => updateResults());
  languageObserver.observe(document.body, { attributes: true, attributeFilter: ['class'] });
  updateResults();
});
