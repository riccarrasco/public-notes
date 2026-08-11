document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('recipe-search');
  const cards = Array.from(document.querySelectorAll('.recipe-card'));
  const noResults = document.getElementById('no-results');

  if (!searchInput || cards.length === 0) {
    return;
  }

  function updateResults() {
    const query = searchInput.value.trim().toLowerCase();
    let visibleCount = 0;

    cards.forEach((card) => {
      const title = card.dataset.title?.toLowerCase() || '';
      const description = card.dataset.description?.toLowerCase() || '';
      const category = card.dataset.category?.toLowerCase() || '';
      const owner = card.dataset.owner?.toLowerCase() || '';
      const matches = !query || [title, description, category, owner].some((text) => text.includes(query));
      card.style.display = matches ? '' : 'none';
      if (matches) visibleCount += 1;
    });

    if (noResults) {
      noResults.style.display = visibleCount === 0 ? 'block' : 'none';
    }
  }

  searchInput.addEventListener('input', updateResults);
  updateResults();
});
