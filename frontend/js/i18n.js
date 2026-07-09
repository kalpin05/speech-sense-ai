const TRANSLATIONS = {
    english: {
        nav_dashboard: "Dashboard",
        nav_exercises: "Exercises",
        nav_progress: "Progress",
        nav_settings: "Settings",
        nav_logout: "Logout",
        dashboard_title: "🎯 Patient Dashboard",
        dashboard_subtitle: "Manage your speech therapy exercises, track progress, and review live corrections.",
        exercises_card_title: "Exercises",
        exercises_card_desc: "Practice speech exercises and improve your pronunciation with interactive lessons.",
        progress_card_title: "Progress & Achievements",
        progress_card_desc: "Track your learning journey with detailed analytics and unlock exciting achievements.",
        settings_card_title: "Settings",
        settings_card_desc: "Customize your learning experience, manage audio preferences, and personalize the app.",
        live_room_title: "Live Speech Room",
        live_room_desc: "Practice speech exercises with live, real-time highlighting and accuracy feedback as you talk.",
        tips_title: "💡 Daily Tips for Success",
        tip_1: "Practice 5-10 minutes daily for maximum progress.",
        tip_2: "Speak slowly and clearly to improve pronunciation accuracy.",
        tip_3: "Review your detailed stats in the Progress tab.",
        logout_confirm: "Are you sure you want to logout?"
    },
    spanish: {
        nav_dashboard: "Tablero",
        nav_exercises: "Ejercicios",
        nav_progress: "Progreso",
        nav_settings: "Ajustes",
        nav_logout: "Cerrar sesión",
        dashboard_title: "🎯 Tablero del Paciente",
        dashboard_subtitle: "Gestione sus ejercicios de terapia del habla, realice un seguimiento de su progreso y revise las correcciones en vivo.",
        exercises_card_title: "Ejercicios",
        exercises_card_desc: "Practique ejercicios de habla y mejore su pronunciación con lecciones interactivas.",
        progress_card_title: "Progreso y Logros",
        progress_card_desc: "Realice un seguimiento de su viaje de aprendizaje con análisis detallados y desbloquee logros.",
        settings_card_title: "Ajustes",
        settings_card_desc: "Personalice su experiencia de aprendizaje, administre sus preferencias de audio y personalice la aplicación.",
        live_room_title: "Sala de habla en vivo",
        live_room_desc: "Practique ejercicios de habla con resaltado en vivo y comentarios de precisión en tiempo real mientras habla.",
        tips_title: "💡 Consejos diarios para el éxito",
        tip_1: "Practique de 5 a 10 minutos al día para obtener el máximo progreso.",
        tip_2: "Hable despacio y con claridad para mejorar la precisión de la pronunciación.",
        tip_3: "Revise sus estadísticas detalladas en la pestaña de Progreso.",
        logout_confirm: "¿Está seguro de que desea cerrar sesión?"
    },
    hindi: {
        nav_dashboard: "डैशबोर्ड",
        nav_exercises: "व्यायाम",
        nav_progress: "प्रगति",
        nav_settings: "सेटिंग्स",
        nav_logout: "लॉगआउट",
        dashboard_title: "🎯 रोगी डैशबोर्ड",
        dashboard_subtitle: "अपने भाषण चिकित्सा अभ्यासों को प्रबंधित करें, प्रगति को ट्रैक करें और लाइव सुधारों की समीक्षा करें।",
        exercises_card_title: "व्यायाम",
        exercises_card_desc: "भाषण अभ्यासों का अभ्यास करें और इंटरैक्टिव पाठों के साथ अपने उच्चारण में सुधार करें।",
        progress_card_title: "प्रगति और उपलब्धियां",
        progress_card_desc: "विस्तृत विश्लेषण के साथ अपनी सीखने की यात्रा को ट्रैक करें और रोमांचक उपलब्धियों को अनलॉक करें।",
        settings_card_title: "सेटिंग्स",
        settings_card_desc: "अपने सीखने के अनुभव को कस्टमाइज़ करें, ऑडियो प्राथमिकताओं को प्रबंधित करें और ऐप को वैयक्तिकृत करें।",
        live_room_title: "लाइव स्पीच रूम",
        live_room_desc: "बोलते समय लाइव, वास्तविक समय की हाइलाइटिंग और सटीकता प्रतिक्रिया के साथ भाषण अभ्यास करें।",
        tips_title: "💡 सफलता के लिए दैनिक टिप्स",
        tip_1: "अधिकतम प्रगति के लिए प्रतिदिन 5-10 मिनट अभ्यास करें।",
        tip_2: "उच्चारण की सटीकता में सुधार के लिए धीरे-धीरे और स्पष्ट रूप से बोलें।",
        tip_3: "प्रगति टैब में अपने विस्तृत आंकड़ों की समीक्षा करें।",
        logout_confirm: "क्या आप निश्चित रूप से लॉगआउट करना चाहते हैं?"
    }
};

// Auto-inject styled language switcher and trigger translation on page load
document.addEventListener("DOMContentLoaded", () => {
    // 1. Inject dropdown language switcher inside navbar
    const navRight = document.querySelector(".nav-right");
    if (navRight) {
        const select = document.createElement("select");
        select.id = "uiLanguageSelect";
        select.style.background = "#1e293b";
        select.style.border = "1px solid rgba(255,255,255,0.15)";
        select.style.color = "white";
        select.style.padding = "6px 12px";
        select.style.borderRadius = "6px";
        select.style.fontSize = "0.85rem";
        select.style.outline = "none";
        select.style.marginRight = "10px";
        select.style.cursor = "pointer";

        const options = [
            { value: "english", label: "🇺🇸 English" },
            { value: "spanish", label: "🇪🇸 Español" },
            { value: "hindi", label: "🇮🇳 हिन्दी" }
        ];

        options.forEach(opt => {
            const o = document.createElement("option");
            o.value = opt.value;
            o.innerText = opt.label;
            select.appendChild(o);
        });

        // Set current value from local storage
        const currentLang = localStorage.getItem("speechai_ui_lang") || "english";
        select.value = currentLang;

        // Add change event listener
        select.addEventListener("change", (e) => {
            const selected = e.target.value;
            localStorage.setItem("speechai_ui_lang", selected);
            translatePage(selected);
        });

        // Prepend to nav-right before the logout button
        navRight.insertBefore(select, navRight.firstChild);
    }

    // 2. Initial Translation
    const currentLang = localStorage.getItem("speechai_ui_lang") || "english";
    translatePage(currentLang);
});

function translatePage(lang) {
    const dictionary = TRANSLATIONS[lang] || TRANSLATIONS.english;
    const elements = document.querySelectorAll("[data-i18n]");
    
    elements.forEach(el => {
        const key = el.getAttribute("data-i18n");
        if (dictionary[key]) {
            // Check if element has a custom attribute to translate (e.g. placeholder)
            if (el.tagName === "INPUT" && el.hasAttribute("placeholder")) {
                el.setAttribute("placeholder", dictionary[key]);
            } else {
                el.innerText = dictionary[key];
            }
        }
    });

    // Update global logout confirm string if requested
    window.I18N_LOGOUT_CONFIRM = dictionary.logout_confirm;
}
