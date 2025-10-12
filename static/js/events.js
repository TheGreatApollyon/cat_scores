// Event data structure
const eventsData = {
    "5-star": [
        {
            name: "Street Play",
            icon: "theater_comedy",
            fee: 500,
            category: "5-star",
            description: "Nukkad Natak - Express social themes through powerful street performances",
            details: "A traditional form of street theatre that brings social issues to life. Teams perform in open spaces, engaging with audiences through compelling narratives and powerful performances.",
            regLink: "https://google.com"
        },
        {
            name: "Fashion Show",
            icon: "checkroom",
            fee: 1000,
            category: "5-star",
            description: "Showcase creativity and style on the ramp with themed fashion",
            details: "Display your fashion sense and creativity with unique theme-based designs. Express yourself through attire, makeup, and presentation that embodies the Nirvana spirit.",
            regLink: "https://google.com"
        },
        {
            name: "BGMI",
            icon: "sports_esports",
            fee: 200,
            category: "5-star",
            description: "Warborn: The BGMI Showdown - Battle royale gaming competition",
            details: "Compete in intense Battlegrounds Mobile India matches. Form your squad and prove your tactical prowess in this ultimate mobile gaming showdown.",
            regLink: "https://google.com"
        },
        {
            name: "Valorant",
            icon: "sports_esports",
            fee: 250,
            category: "5-star",
            description: "One Shot to Nirvana - Tactical FPS gaming championship",
            details: "Demonstrate your skills in this competitive tactical shooter. Strategy, teamwork, and precision shooting will determine the champions.",
            regLink: "https://google.com"
        },
        {
            name: "Mock IPL Auction",
            icon: "gavel",
            fee: 500,
            category: "5-star",
            description: "Build your dream cricket team through strategic bidding",
            details: "Experience the thrill of being a team owner. Use strategy, cricket knowledge, and bidding skills to create the ultimate cricket franchise.",
            regLink: "https://google.com"
        },
        {
            name: "Murder Mystery",
            icon: "search",
            fee: 200,
            category: "5-star",
            description: "Solve the mystery through clues, deduction, and teamwork",
            details: "Step into the shoes of a detective. Use your observation skills, logical thinking, and teamwork to unravel a complex murder mystery.",
            regLink: "https://google.com"
        },
        {
            name: "Short Film",
            icon: "movie",
            fee: 500,
            category: "5-star",
            description: "Create and present original short films on the Nirvana theme",
            details: "Showcase your filmmaking talents. From script to screen, present your creative vision through the medium of short film.",
            regLink: "https://google.com"
        },
        {
            name: "Group Dance",
            icon: "groups",
            fee: 500,
            category: "5-star",
            description: "Choreographed team performances with energy and coordination",
            details: "Display synchronization, creativity, and energy through group choreography. Any dance style is welcome - make it spectacular!",
            regLink: "https://google.com"
        },
        {
            name: "Warli Art",
            icon: "palette",
            fee: 0,
            category: "5-star",
            description: "Traditional Indian tribal art on festival theme",
            details: "Create beautiful Warli artwork inspired by the Nirvana theme. Express the festival spirit through this ancient Indian art form.",
            regLink: "https://forms.gle/D6oecEmh8p6kmwix9"
        },
        {
            name: "Banner Painting",
            icon: "brush",
            fee: 0,
            category: "5-star",
            description: "Large-scale artistic expression on canvas",
            details: "Paint your vision on a large banner. Show your artistic skills and creativity in this traditional art competition.",
            regLink: "https://forms.gle/D6oecEmh8p6kmwix9"
        },
        {
            name: "Origami",
            icon: "auto_awesome",
            fee: 0,
            category: "5-star",
            description: "Fold to Nirvana - Japanese paper folding art",
            details: "Create intricate designs through the ancient art of paper folding. Transform simple paper into complex, beautiful structures.",
            regLink: "https://forms.gle/D6oecEmh8p6kmwix9"
        },
        {
            name: "Model Installation",
            icon: "architecture",
            fee: 0,
            category: "5-star",
            description: "3D artistic installations on Nirvana theme",
            details: "Design and create three-dimensional art installations. Bring the Nirvana theme to life through sculptural creativity.",
            regLink: "https://forms.gle/D6oecEmh8p6kmwix9"
        }
    ],
    "3-star": [
        {
            name: "Classical Vocal Solo",
            icon: "music_note",
            fee: 100,
            category: "3-star",
            description: "Indian classical singing performance",
            details: "Showcase your mastery of classical Indian vocal music. Demonstrate your training, technique, and emotional expression through raga-based performance.",
            regLink: "https://google.com"
        },
        {
            name: "Indian Dance Solo",
            icon: "self_improvement",
            fee: 100,
            category: "3-star",
            description: "Classical or folk Indian dance forms",
            details: "Perform traditional Indian dance forms like Bharatanatyam, Kathak, Odissi, or folk dances. Express stories and emotions through mudras and movements.",
            regLink: "https://google.com"
        },
        {
            name: "Indian Cinema Solo",
            icon: "movie_filter",
            fee: 100,
            category: "3-star",
            description: "Bollywood and regional film music performances",
            details: "Sing your favorite songs from Indian cinema. From classic melodies to modern chartbusters, showcase your versatility.",
            regLink: "https://google.com"
        },
        {
            name: "Beg Borrow Steal",
            icon: "shopping_bag",
            fee: 100,
            category: "3-star",
            description: "Fast-paced scavenger hunt challenge",
            details: "Race against time to collect items from the audience and surroundings. Quick thinking and social skills are your best weapons!",
            regLink: "https://google.com"
        },
        {
            name: "Chess 960",
            icon: "chess",
            fee: 100,
            category: "3-star",
            description: "Fischer Random Chess variant competition",
            details: "Test your chess skills with randomized starting positions. Pure strategy and calculation matter more than memorized openings.",
            regLink: "https://google.com"
        },
        {
            name: "Instrumental Solo",
            icon: "piano",
            fee: 100,
            category: "3-star",
            description: "Solo musical instrument performances",
            details: "Display your instrumental prowess. Any instrument is welcome - from traditional to modern, create music that moves souls.",
            regLink: "https://google.com"
        },
        {
            name: "Mono Acting",
            icon: "person",
            fee: 100,
            category: "3-star",
            description: "Solo theatrical performance and character portrayal",
            details: "Bring a character or story to life through solo acting. Use voice modulation, expressions, and body language to captivate the audience.",
            regLink: "https://google.com"
        },
        {
            name: "Anime Quiz",
            icon: "quiz",
            fee: 200,
            category: "3-star",
            description: "Otaku Odyssey - Test your anime knowledge",
            details: "Prove your anime expertise! From classics to recent releases, across genres and eras, show you're a true otaku.",
            regLink: "https://google.com"
        },
        {
            name: "Western Vocal Solo",
            icon: "mic",
            fee: 100,
            category: "3-star",
            description: "English and international music performances",
            details: "Sing your heart out with Western music. From rock to pop, jazz to soul, showcase your vocal range and style.",
            regLink: "https://google.com"
        },
        {
            name: "Western Dance Solo",
            icon: "nightlife",
            fee: 100,
            category: "3-star",
            description: "Contemporary, hip-hop, and western dance styles",
            details: "Express yourself through contemporary Western dance forms. Hip-hop, contemporary, freestyle - show your moves and groove!",
            regLink: "https://google.com"
        }
    ],
    "1-star": [
        {
            name: "Mini Games",
            icon: "casino",
            fee: 200,
            category: "1-star",
            description: "Multiple fun and competitive mini challenges",
            details: "Participate in various quick games and challenges. Test your skills across different fun activities and win points!",
            regLink: "https://google.com"
        },
        {
            name: "Where is Waldo",
            icon: "pageview",
            fee: 200,
            category: "1-star",
            description: "Visual search and observation challenge",
            details: "Find hidden characters and objects in complex illustrations. Sharp eyes and quick observation skills will lead to victory!",
            regLink: "https://google.com"
        },
        {
            name: "The Laugh Lab",
            icon: "sentiment_very_satisfied",
            fee: 200,
            category: "1-star",
            description: "Improv comedy and mad ads challenge",
            details: "Create hilarious improvisations and advertisements on the spot. Think fast, be funny, and make the audience laugh!",
            regLink: "https://google.com"
        },
        {
            name: "Photography",
            icon: "photo_camera",
            fee: 100,
            category: "1-star",
            description: "Capture the essence of Nirvana through lens",
            details: "Submit photographs that embody the Nirvana theme. Show your perspective, technical skills, and artistic vision.",
            regLink: "https://google.com"
        },
        {
            name: "Face Painting",
            icon: "face_retouching_natural",
            fee: 100,
            category: "1-star",
            description: "Ethereal Ink - Artistic face painting",
            details: "Transform faces into canvases. Create beautiful, themed designs that showcase your artistic skills and creativity.",
            regLink: "https://google.com"
        },
        {
            name: "Clay Modelling",
            icon: "cake",
            fee: 100,
            category: "1-star",
            description: "Sculpt creative forms from clay",
            details: "Mold clay into artistic creations. Show your three-dimensional artistic abilities and attention to detail.",
            regLink: "https://google.com"
        },
        {
            name: "Shark Tank",
            icon: "business_center",
            fee: 300,
            category: "1-star",
            description: "Venture Vault - Pitch your business ideas",
            details: "Present your startup idea to our panel of judges. Convince them with your business acumen, pitch, and innovation.",
            regLink: "https://google.com"
        },
        {
            name: "Rap Battle",
            icon: "headphones",
            fee: 100,
            category: "1-star",
            description: "Freestyle rap competition",
            details: "Drop bars and prove your lyrical prowess. Rhythm, wordplay, and flow - show you're the ultimate rapper!",
            regLink: "https://google.com"
        },
        {
            name: "Fitness Witness",
            icon: "fitness_center",
            fee: 100,
            category: "1-star",
            description: "SW3AT T(O) N!RVANA - Physical fitness challenge",
            details: "Test your physical strength, endurance, and fitness. Sweat your way to Nirvana through various fitness challenges!",
            regLink: "https://google.com"
        },
        {
            name: "Elocution",
            icon: "record_voice_over",
            fee: 200,
            category: "1-star",
            description: "Public speaking on given topics",
            details: "Speak eloquently on assigned topics. Show your command over language, expression, and persuasive speaking.",
            regLink: "https://google.com"
        },
        {
            name: "Contemporary Dance",
            icon: "girl",
            fee: 100,
            category: "1-star",
            description: "Modern interpretive dance performance",
            details: "Express emotions and stories through contemporary dance. Blend technique with artistic interpretation.",
            regLink: "https://google.com"
        },
        {
            name: "Debate",
            icon: "forum",
            fee: 150,
            category: "1-star",
            description: "Debate Me! Maybe - Formal debate competition",
            details: "Argue for or against given motions. Logic, research, and persuasive speaking will determine the winner.",
            regLink: "https://google.com"
        },
        {
            name: "Fandom Quiz",
            icon: "live_tv",
            fee: 100,
            category: "1-star",
            description: "Fandom Moksha - Pop culture and entertainment quiz",
            details: "Test your knowledge of TV shows, movies, music, and pop culture. From Game of Thrones to Marvel, prove you're a true fan!",
            regLink: "https://google.com"
        },
        {
            name: "Reels Making",
            icon: "videocam",
            fee: 100,
            category: "1-star",
            description: "Parichay to Nirvana - Create engaging short videos",
            details: "Create creative Instagram reels around the theme. Show your video editing, creativity, and storytelling in short format.",
            regLink: "https://google.com"
        }
    ]
};

// Function to get all events or filtered by category
function getEvents(category = 'all') {
    if (category === 'all') {
        return [...eventsData['5-star'], ...eventsData['3-star'], ...eventsData['1-star']];
    }
    return eventsData[category] || [];
}

// Function to get a specific event by name
function getEventByName(name) {
    const allEvents = getEvents();
    return allEvents.find(event => event.name === name);
}
