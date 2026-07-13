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
    },
    marathi: {
        nav_dashboard: "डैशबोर्ड",
        nav_exercises: "व्यायाम",
        nav_progress: "प्रगति",
        nav_settings: "सेटिंग्स",
        nav_logout: "लॉगआउट",
        dashboard_title: "🎯 रुग्ण डॅशबोर्ड",
        dashboard_subtitle: "तुमचे भाषण थेरपी व्यायाम व्यवस्थापित करा आणि प्रगतीचा मागोवा घ्या.",
        exercises_card_title: "व्यायाम",
        exercises_card_desc: "उच्चारण सुधारण्यासाठी विविध स्तरांवरील व्यायामांचा सराव करा.",
        progress_card_title: "प्रगती आणि यश",
        progress_card_desc: "तुमच्या शिकण्याच्या प्रवासाचा तपशीलवार मागोवा घ्या.",
        settings_card_title: "सेTINGS",
        settings_card_desc: "ऑडिओ आणि इतर प्राधान्ये व्यवस्थापित करा.",
        live_room_title: "लाइव्ह स्पीच रूम",
        live_room_desc: "बोलत असताना रिअल-टाइम अभिप्राय मिळवा.",
        tips_title: "💡 यशासाठी टिप्स",
        tip_1: "दररोज ५-१० मिनिटे सराव करा.",
        tip_2: "स्पष्ट आणि हळू बोला.",
        tip_3: "प्रगती टॅबमध्ये आकडेवारी तपासा.",
        logout_confirm: "तुम्हाला खरोखर लॉगआउट करायचे आहे का?",
        stats_title: "एकूण प्रगती आकडेवारी",
        today_progress: "आजची प्रगती",
        daily_goal: "दैनिक लक्ष्य",
        avg_score_lbl: "सरासरी स्कोअर",
        current_streak: "चालू स्ट्रीक",
        recent_attempts: "अलीकडील प्रयत्न",
        exercises_title: "🎮 स्पीच एआय खेळ आणि व्यायाम"
    },
    tamil: {
        nav_dashboard: "டேஷ்போர்டு",
        nav_exercises: "பயிற்சிகள்",
        nav_progress: "முன்னேற்றம்",
        nav_settings: "அமைப்புகள்",
        nav_logout: "வெளியேறு",
        dashboard_title: "🎯 நோயாளி டேஷ்போர்டு",
        dashboard_subtitle: "உங்கள் பேச்சு சிகிச்சைப் பயிற்சிகளை நிர்வகித்து முன்னேற்றத்தைக் கண்காணிக்கவும்.",
        exercises_card_title: "பயிற்சிகள்",
        exercises_card_desc: "உச்சரிப்பை மேம்படுத்த பல்வேறு நிலைகளில் பயிற்சி செய்யுங்கள்.",
        progress_card_title: "முன்னேற்றம் மற்றும் சாதனைகள்",
        progress_card_desc: "உங்கள் கற்றல் பயணத்தை விரிவாகக் கண்காணிக்கவும்.",
        settings_card_title: "அமைப்புகள்",
        settings_card_desc: "உங்கள் ஆடியோ மற்றும் சுயவிவர விருப்பங்களை நிர்வகிக்கவும்.",
        live_room_title: "நேரடி பேச்சு அறை",
        live_room_desc: "பேசும்போது நிகழ்நேர கருத்துக்களைப் பெறுங்கள்.",
        tips_title: "💡 வெற்றிக்கான உதவிக்குறிப்புகள்",
        tip_1: "தினமும் 5-10 நிமிடங்கள் பயிற்சி செய்யுங்கள்.",
        tip_2: "தெளிவாகவும் மெதுவாகவும் பேசுங்கள்.",
        tip_3: "முன்னேற்ற தாவலில் புள்ளிவிவரங்களை சரிபார்க்கவும்.",
        logout_confirm: "நீங்கள் நிச்சயமாக வெளியேற விரும்புகிறீர்களா?",
        stats_title: "ஒட்டுமொத்த முன்னேற்ற புள்ளிவிவரங்கள்",
        today_progress: "இன்றைய முன்னேற்றம்",
        daily_goal: "தினசரி இலக்கு",
        avg_score_lbl: "சராசரி மதிப்பெண்",
        current_streak: "தற்போதைய ஸ்ட்ரீக்",
        recent_attempts: "சமீபத்திய முயற்சிகள்",
        exercises_title: "🎮 பேச்சு ஏஐ விளையாட்டு மற்றும் பயிற்சிகள்"
    },
    telugu: {
        nav_dashboard: "డాష్‌బోర్డ్",
        nav_exercises: "వ్యాయామాలు",
        nav_progress: "ప్రగతి",
        nav_settings: "సెట్టింగులు",
        nav_logout: "లాగ్అవుట్",
        dashboard_title: "🎯 రోగి డాష్‌బోర్డ్",
        dashboard_subtitle: "మీ స్పీッチ థెరపీ వ్యాయామాలను నిర్వహించండి మరియు ప్రగతిని ట్రాక్ చేయండి.",
        exercises_card_title: "వ్యాయామాలు",
        exercises_card_desc: "ఉచ్చారణను మెరుగుపరచడానికి विभिन्न స్థాయిలలో ప్రాక్టీస్ చేయండి.",
        progress_card_title: "ప్రగతి మరియు విజయాలు",
        progress_card_desc: "మీ అభ్యాస ప్రయాణాన్ని వివరంగా ట్రాక్ చేయండి.",
        settings_card_title: "సెట్టింగులు",
        settings_card_desc: "ఆడియో మరియు ప్రొఫైల్ ప్రాధాన్యతలను నిర్వహించండి.",
        live_room_title: "లైవ్ స్ピーచ్ రూమ్",
        live_room_desc: "మాట్లాడుతున్నప్పుడు నిజ-సమయ అభిప్రायాన్ని పొందండి.",
        tips_title: "💡 విజయానికి చిట్కాలు",
        tip_1: "రోజుకు 5-10 నిమిషాలు ప్రాక్టీస్ చేయండి.",
        tip_2: "స్పష్టంగా మరియు నెమ్మదిగా మాట్లాడండి.",
        tip_3: "ప్రగతి ట్యాబ్‌లో గణాంకాలను తనిఖీ చేయండి.",
        logout_confirm: "మీరు ఖచ్చితంగా లాగ్అవుట్ చేయాలనుకుంటున్నారా?",
        stats_title: "మొత్తం ప్రగతి గణాంకాలు",
        today_progress: "ఈ రోజు ప్రగతి",
        daily_goal: "దినసరి లక్ష్యం",
        avg_score_lbl: "సగటు స్కోరు",
        current_streak: "ప్రస్తుత స్ట్రీక్",
        recent_attempts: "ఇటీవలి ప్రయత్నాలు",
        exercises_title: "🎮 స్ピーచ్ ఏఐ గేమ్ మరియు వ్యాయామాలు"
    },
    german: {
        nav_dashboard: "Dashboard",
        nav_exercises: "Übungen",
        nav_progress: "Fortschritt",
        nav_settings: "Einstellungen",
        nav_logout: "Abmelden",
        dashboard_title: "🎯 Patienten-Dashboard",
        dashboard_subtitle: "Verwalten Sie Ihre Logopädie-Übungen und verfolgen Sie Ihren Fortschritt.",
        exercises_card_title: "Übungen",
        exercises_card_desc: "Üben Sie Sprechübungen, um Ihre Aussprache mit interaktiven Lektionen zu verbessern.",
        progress_card_title: "Fortschritt & Erfolge",
        progress_card_desc: "Verfolgen Sie Ihre Lernreise mit detaillierten Analysen.",
        settings_card_title: "Einstellungen",
        settings_card_desc: "Passen Sie Ihr Lernerlebnis an.",
        live_room_title: "Live-Sprechzimmer",
        live_room_desc: "Sprechen Sie mit Echtzeit-Hervorhebung und Feedback.",
        tips_title: "💡 Tägliche Tipps für den Erfolg",
        tip_1: "Üben Sie täglich 5-10 Minuten für maximalen Fortschritt.",
        tip_2: "Sprechen Sie langsam und deutlich.",
        tip_3: "Überprüfen Sie Ihre Statistiken im Fortschritts-Tab.",
        logout_confirm: "Möchten Sie sich wirklich abmelden?",
        stats_title: "Gesamtfortschrittsstatistik",
        today_progress: "Heutiger Fortschritt",
        daily_goal: "Tagesziel",
        avg_score_lbl: "Durchschnittliche Punktzahl",
        current_streak: "Aktuelle Strähne",
        recent_attempts: "Letzte Versuche",
        exercises_title: "🎮 Sprech-KI-Spiel & Übungen"
    },
    french: {
        nav_dashboard: "Tableau de bord",
        nav_exercises: "Exercices",
        nav_progress: "Progrès",
        nav_settings: "Paramètres",
        nav_logout: "Se déconnecter",
        dashboard_title: "🎯 Tableau de bord du patient",
        dashboard_subtitle: "Gérez vos exercices d'orthophonie et suivez vos progrès.",
        exercises_card_title: "Exercices",
        exercises_card_desc: "Pratiquez des exercices d'élocution pour améliorer votre prononciation.",
        progress_card_title: "Progrès & Récompenses",
        progress_card_desc: "Suivez votre parcours d'apprentissage en détail.",
        settings_card_title: "Paramètres",
        settings_card_desc: "Personnalisez votre expérience d'apprentissage.",
        live_room_title: "Salle de parole en direct",
        live_room_desc: "Parlez avec rétroaction et surbrillance en temps réel.",
        tips_title: "💡 Conseils quotidiens pour réussir",
        tip_1: "Pratiquez 5 à 10 minutes par jour.",
        tip_2: "Parlez lentement et clairement.",
        tip_3: "Consultez vos statistiques dans l'onglet Progrès.",
        logout_confirm: "Êtes-vous sûr de vouloir vous déconnecter?",
        stats_title: "Statistiques de progression globale",
        today_progress: "Progrès du jour",
        daily_goal: "Objectif quotidien",
        avg_score_lbl: "Score moyen",
        current_streak: "Série actuelle",
        recent_attempts: "Tentatives récentes",
        exercises_title: "🎮 Jeu et Exercices d'IA Vocale"
    },
    japanese: {
        nav_dashboard: "ダッシュボード",
        nav_exercises: "練習問題",
        nav_progress: "学習進捗",
        nav_settings: "設定",
        nav_logout: "ログアウト",
        dashboard_title: "🎯 患者ダッシュボード",
        dashboard_subtitle: "発話練習の管理と進捗の確認ができます。",
        exercises_card_title: "練習問題",
        exercises_card_desc: "インタラクティブなレッスンで発音を改善しましょう。",
        progress_card_title: "進捗と実績",
        progress_card_desc: "詳細な分析で学習の道のりを追跡します。",
        settings_card_title: "設定",
        settings_card_desc: "オーディオ設定やアカウント設定をカスタマイズします。",
        live_room_title: "リアルタイム発話ルーム",
        live_room_desc: "話しながらリアルタイムで発音のフィードバックを受け取ります。",
        tips_title: "💡 毎日の上達のヒント",
        tip_1: "毎日5〜10分練習すると効果的です。",
        tip_2: "ゆっくり、はっきりと発音しましょう。",
        tip_3: "進捗タブで詳細な統計を確認しましょう。",
        logout_confirm: "本当にログアウトしますか？",
        stats_title: "総合的な進捗統計",
        today_progress: "本日の進捗",
        daily_goal: "目標時間",
        avg_score_lbl: "平均スコア",
        current_streak: "継続日数",
        recent_attempts: "最近の練習",
        exercises_title: "🎮 音声AIゲームと練習問題"
    },
    arabic: {
        nav_dashboard: "لوحة التحكم",
        nav_exercises: "التمارين",
        nav_progress: "التقدم",
        nav_settings: "الإعدادات",
        nav_logout: "تسجيل الخروج",
        dashboard_title: "🎯 لوحة تحكم المريض",
        dashboard_subtitle: "إدارة تمارين علاج النطق وتتبع تقدمك المنجز.",
        exercises_card_title: "التمارين",
        exercises_card_desc: "تدرب على تمارين النطق لتحسين مخارج الحروف.",
        progress_card_title: "التقدم والإنجازات",
        progress_card_desc: "تتبع رحلتك التعليمية مع إحصائيات مفصلة.",
        settings_card_title: "الإعدادات",
        settings_card_desc: "تخصيص تفضيلات الصوت والتحكم بالتطبيق.",
        live_room_title: "غرفة النطق المباشر",
        live_room_desc: "تدرب على الكلام مع تصحيح ونطق مباشر في نفس الوقت.",
        tips_title: "💡 نصائح يومية للنجاح",
        tip_1: "تدرب من 5 إلى 10 دقائق يومياً للحصول على أفضل تقدم.",
        tip_2: "تحدث ببطء ووضوح لزيادة الدقة.",
        tip_3: "راجع إحصائياتك المفصلة في تبويب التقدم.",
        logout_confirm: "هل أنت متأكد من رغبتك في تسجيل الخروج؟",
        stats_title: "إحصائيات التقدم الإجمالية",
        today_progress: "تقدم اليوم",
        daily_goal: "الهدف اليومي",
        avg_score_lbl: "متوسط النتيجة",
        current_streak: "الاستمرارية الحالية",
        recent_attempts: "المحاولات الأخيرة",
        exercises_title: "🎮 لعبة وتمارين النطق الذكي"
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
            { value: "english", label: "GB - English" },
            { value: "hindi", label: "IN - हिंदी (Hindi)" },
            { value: "marathi", label: "IN - मराठी (Marathi)" },
            { value: "tamil", label: "IN - தமிழ் (Tamil)" },
            { value: "telugu", label: "IN - తెలుగు (Telugu)" },
            { value: "german", label: "DE - Deutsch (German)" },
            { value: "french", label: "FR - Français (French)" },
            { value: "spanish", label: "ES - Español (Spanish)" },
            { value: "japanese", label: "JP - 日本語 (Japanese)" },
            { value: "arabic", label: "SA - العربية (Arabic)" }
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
