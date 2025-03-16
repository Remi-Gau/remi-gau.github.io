function updateLanguageElements(lang) {
    // Loop through each element and hide/show based on language
    let languageElements = document.querySelectorAll(".recipe-item");

    languageElements.forEach(function (el) {
        let elementLang = el.classList.contains(lang) ? lang : null;

        if (!elementLang) {
            el.style.display = "none";
        } else {
            el.style.display = "";
        }
    });
}

console.log(localStorage.getItem("siteLanguage"))

document.querySelectorAll("[data-locale]").forEach(el => {
    el.addEventListener("click", function (event) {
        // event.preventDefault();
        let selectedLang = this.getAttribute("data-locale");

        document.documentElement.setAttribute("lang", selectedLang);

        localStorage.setItem("siteLanguage", selectedLang);

        updateLanguageElements(selectedLang);

        initializeI18n();

    });
});

document.addEventListener("DOMContentLoaded", function () {
    let storedLang = localStorage.getItem("siteLanguage");
    if (storedLang) {
        document.documentElement.setAttribute("lang", storedLang);
    }
    updateLanguageElements(storedLang);

    initializeI18n();
});
