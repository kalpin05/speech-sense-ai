const TRANSLATIONS = {
    english: {
        nav_dashboard: "Dashboard",
        nav_exercises: "Exercises",
        nav_progress: "Progress",
        nav_settings: "Settings",
        nav_logout: "Logout",
        
        // Dashboard
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
        logout_confirm: "Are you sure you want to logout?",
        stats_title: "Overall Progress Stats",
        today_progress: "Today's Progress",
        daily_goal: "Daily Goal",
        avg_accuracy: "Avg Accuracy",
        current_streak: "Current Streak",
        recent_attempts: "Recent Attempts",
        no_recent_attempts: "No recent attempts. Go practice!",
        session_details: "Session Details",
        achievements_title: "Achievements & Badges",
        view_progress_btn: "View Progress Details",
        practice_now_btn: "Practice Now",

        // Exercises Page
        exercises_title: "🎮 Speech AI Game & Exercises",
        select_difficulty: "Select Difficulty",
        diff_beginner: "Beginner",
        diff_intermediate: "Intermediate",
        diff_advanced: "Advanced",
        diff_custom_ai: "Custom AI Exercise",
        practice_phrase_title: "Practice Phrase",
        transcribe_feedback_title: "Realtime Transcription & Feedback",
        listening_hint: "Speak clearly into your microphone...",
        generate_btn: "Generate custom exercise",
        custom_prompt_placeholder: "Enter topic (e.g. restaurant, airport, shopping)",

        // Progress Page
        progress_title: "📊 Progress & Achievements",
        total_attempts_lbl: "Total Attempts",
        avg_score_lbl: "Average Score",
        best_score_lbl: "Best Score",
        current_streak_lbl: "Current Streak",
        confidence_lbl: "Avg Confidence",
        nervousness_lbl: "Avg Nervousness",
        hesitation_lbl: "Avg Hesitation",
        progress_timeline_title: "Progress Timeline",
        performance_breakdown_title: "Performance Breakdown",

        // Settings Page
        settings_title: "⚙️ Settings",
        profile_settings_title: "Profile Settings",
        change_profile_lbl: "Change your profile name",
        voice_speed_lbl: "Choose voice speed",
        daily_goal_title: "Daily Goal",
        daily_goal_desc: "Set your daily target in minutes",
        therapist_linkage_title: "👨‍⚕️ Speech Therapist Linkage",
        therapist_email_lbl: "Enter therapist email",
        theme_accessibility_title: "🎨 Theme & Accessibility",
        save_settings_btn: "Save Settings",
        reset_app_btn: "Reset App Data",

        // Realtime Page
        live_room_title_h1: "⚡ Live Speech practice Room",
        select_exercise_lbl: "Select Exercise to Practice",
        load_std_btn: "Load Standard Exercises",
        visualizer_lbl: "Live Audio Visualizer",
        mic_instruction_lbl: "Speak clearly into your microphone..."
    },
    spanish: {
        nav_dashboard: "Tablero",
        nav_exercises: "Ejercicios",
        nav_progress: "Progreso",
        nav_settings: "Ajustes",
        nav_logout: "Cerrar sesión",
        
        // Dashboard
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
        logout_confirm: "¿Está seguro de que desea cerrar sesión?",
        stats_title: "Estadísticas de Progreso General",
        today_progress: "Progreso de Hoy",
        daily_goal: "Meta Diaria",
        avg_accuracy: "Precisión Promedio",
        current_streak: "Racha Actual",
        recent_attempts: "Intentos Recientes",
        no_recent_attempts: "No hay intentos recientes. ¡A practicar!",
        session_details: "Detalles de la Sesión",
        achievements_title: "Logros y Medallas",
        view_progress_btn: "Ver Detalles del Progreso",
        practice_now_btn: "Practicar Ahora",

        // Exercises Page
        exercises_title: "🎮 Juegos y Ejercicios de Habla",
        select_difficulty: "Seleccionar Dificultad",
        diff_beginner: "Principiante",
        diff_intermediate: "Intermedio",
        diff_advanced: "Avanzado",
        diff_custom_ai: "Ejercicio de IA Personalizado",
        practice_phrase_title: "Frase de Práctica",
        transcribe_feedback_title: "Transcripción y Comentarios en Tiempo Real",
        listening_hint: "Hable claramente en el micrófono...",
        generate_btn: "Generar ejercicio personalizado",
        custom_prompt_placeholder: "Ingrese un tema (ej. restaurante, aeropuerto, compras)",

        // Progress Page
        progress_title: "📊 Progreso y Logros",
        total_attempts_lbl: "Total de Intentos",
        avg_score_lbl: "Puntuación Promedio",
        best_score_lbl: "Mejor Puntuación",
        current_streak_lbl: "Racha Actual",
        confidence_lbl: "Confianza Promedio",
        nervousness_lbl: "Nerviosismo Promedio",
        hesitation_lbl: "Vacilación Promedio",
        progress_timeline_title: "Línea de Tiempo del Progreso",
        performance_breakdown_title: "Desglose del Rendimiento",

        // Settings Page
        settings_title: "⚙️ Ajustes",
        profile_settings_title: "Ajustes de Perfil",
        change_profile_lbl: "Cambiar nombre de perfil",
        voice_speed_lbl: "Elegir velocidad de voz",
        daily_goal_title: "Meta Diaria",
        daily_goal_desc: "Establecer meta diaria en minutos",
        therapist_linkage_title: "👨‍⚕️ Vinculación con Terapeuta",
        therapist_email_lbl: "Correo del terapeuta",
        theme_accessibility_title: "🎨 Tema y Accesibilidad",
        save_settings_btn: "Guardar Ajustes",
        reset_app_btn: "Restablecer Datos de App",

        // Realtime Page
        live_room_title_h1: "⚡ Sala de práctica del Habla en Vivo",
        select_exercise_lbl: "Seleccionar Ejercicio para Practicar",
        load_std_btn: "Cargar Ejercicios Estándar",
        visualizer_lbl: "Visualizador de Audio en Vivo",
        mic_instruction_lbl: "Hable claramente en el micrófono..."
    },
    hindi: {
        nav_dashboard: "डैशबोर्ड",
        nav_exercises: "व्यायाम",
        nav_progress: "प्रगति",
        nav_settings: "सेटिंग्स",
        nav_logout: "लॉगआउट",
        
        // Dashboard
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
        logout_confirm: "क्या आप निश्चित रूप से लॉगआउट करना चाहते हैं?",
        stats_title: "समग्र प्रगति आँकड़े",
        today_progress: "आज की प्रगति",
        daily_goal: "दैनिक लक्ष्य",
        avg_accuracy: "औसत सटीकता",
        current_streak: "वर्तमान स्ट्रीक",
        recent_attempts: "हाल के प्रयास",
        no_recent_attempts: "कोई हालिया प्रयास नहीं। अभ्यास करें!",
        session_details: "सत्र विवरण",
        achievements_title: "उपलब्धियां और बैज",
        view_progress_btn: "प्रगति विवरण देखें",
        practice_now_btn: "अभी अभ्यास करें",

        // Exercises Page
        exercises_title: "🎮 स्पीच एआई गेम और व्यायाम",
        select_difficulty: "कठिनाई चुनें",
        diff_beginner: "शुरुआती",
        diff_intermediate: "मध्यम",
        diff_advanced: "उन्नत",
        diff_custom_ai: "कस्टम एआई व्यायाम",
        practice_phrase_title: "अभ्यास वाक्यांश",
        transcribe_feedback_title: "वास्तविक समय प्रतिलेखन और प्रतिक्रिया",
        listening_hint: "अपने माइक्रोफ़ोन में स्पष्ट रूप से बोलें...",
        generate_btn: "कस्टम व्यायाम उत्पन्न करें",
        custom_prompt_placeholder: "विषय दर्ज करें (जैसे: रेस्तरां, हवाई अड्डा, खरीदारी)",

        // Progress Page
        progress_title: "📊 प्रगति और उपलब्धियां",
        total_attempts_lbl: "कुल प्रयास",
        avg_score_lbl: "औसत स्कोर",
        best_score_lbl: "सर्वश्रेष्ठ स्कोर",
        current_streak_lbl: "वर्तमान स्ट्रीक",
        confidence_lbl: "औसत आत्मविश्वास",
        nervousness_lbl: "औसत घबराहट",
        hesitation_lbl: "औसत हिचकिचाहट",
        progress_timeline_title: "प्रगति की समयरेखा",
        performance_breakdown_title: "प्रदर्शन विश्लेषण",

        // Settings Page
        settings_title: "⚙️ सेटिंग्स",
        profile_settings_title: "प्रोफ़ाइल सेटिंग्स",
        change_profile_lbl: "अपना प्रोफ़ाइल नाम बदलें",
        voice_speed_lbl: "आवाज की गति चुनें",
        daily_goal_title: "दैनिक लक्ष्य",
        daily_goal_desc: "मिनटों में अपना दैनिक लक्ष्य निर्धारित करें",
        therapist_linkage_title: "👨‍⚕️ भाषण चिकित्सक लिंकेज",
        therapist_email_lbl: "चिकित्सक का ईमेल दर्ज करें",
        theme_accessibility_title: "🎨 थीम और पहुंच",
        save_settings_btn: "सेटिंग्स सहेजें",
        reset_app_btn: "ऐप डेटा रीसेट करें",

        // Realtime Page
        live_room_title_h1: "⚡ लाइव स्पीच अभ्यास कक्ष",
        select_exercise_lbl: "अभ्यास के लिए व्यायाम चुनें",
        load_std_btn: "मानक व्यायाम लोड करें",
        visualizer_lbl: "लाइव ऑडियो विज़ुअलाइज़र",
        mic_instruction_lbl: "माइक्रोफ़ोन में स्पष्ट रूप से बोलें..."
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
            window.dispatchEvent(new CustomEvent("uiLanguageChanged", { detail: { language: selected } }));
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
