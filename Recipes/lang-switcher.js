const supportedRecipeLangs = ['en', 'es'];
const STORAGE_KEY = 'publicNotesRecipeLang';

function getSavedLanguage() {
  const saved = localStorage.getItem(STORAGE_KEY);
  if (supportedRecipeLangs.includes(saved)) {
    return saved;
  }
  return null;
}

function detectBrowserLanguage() {
  const languages = navigator.languages || [navigator.language || 'en'];
  for (const lang of languages) {
    if (!lang) {
      continue;
    }
    const code = lang.toLowerCase().slice(0, 2);
    if (supportedRecipeLangs.includes(code)) {
      return code;
    }
  }
  return 'en';
}

function applyRecipeLanguage(lang) {
  if (!supportedRecipeLangs.includes(lang)) {
    lang = 'en';
  }

  document.documentElement.lang = lang;
  document.body.classList.toggle('lang-en', lang === 'en');
  document.body.classList.toggle('lang-es', lang === 'es');
  localStorage.setItem(STORAGE_KEY, lang);

  document.querySelectorAll('[data-i18n]').forEach((el) => {
    if (lang === 'es' && el.dataset.i18nEs) {
      el.textContent = el.dataset.i18nEs;
    } else if (el.dataset.i18n) {
      el.textContent = el.dataset.i18n;
    }
  });

  document.querySelectorAll('[data-i18n-placeholder]').forEach((el) => {
    if (lang === 'es' && el.dataset.i18nPlaceholderEs) {
      el.setAttribute('placeholder', el.dataset.i18nPlaceholderEs);
    } else if (el.dataset.i18nPlaceholder) {
      el.setAttribute('placeholder', el.dataset.i18nPlaceholder);
    }
  });

  const select = document.getElementById('language-select');
  if (select) {
    select.value = lang;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const select = document.getElementById('language-select');
  if (select) {
    select.addEventListener('change', (event) => {
      applyRecipeLanguage(event.target.value);
    });
  }
  const saved = getSavedLanguage();
  const lang = saved || detectBrowserLanguage();
  applyRecipeLanguage(lang);
});
