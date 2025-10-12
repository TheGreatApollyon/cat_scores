# Parichay 2025 - Nirvana

A modern, responsive web application for the Parichay 2025 cultural fest at RNSIT with the theme "Nirvana".

## Features

- **Video Background**: Immersive slowed-down video background with glass morphism effects
- **Dynamic Topbar**: Responsive navigation that transitions on scroll
- **Event Filtering**: Easy-to-use category filters (5-Star, 3-Star, 1-Star events)
- **Interactive Modals**: Detailed event information with registration links
- **Responsive Design**: Perfect viewing experience on desktop and mobile devices
- **Glass Morphism UI**: Modern frosted glass aesthetic throughout

## Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

### Development Mode

```bash
python app.py
```

The application will be available at `http://localhost:5000`

### Production Mode with Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

For production with more workers:

```bash
gunicorn -w 4 -b 0.0.0.0:8000 --timeout 120 app:app
```

## Project Structure

```
parichay_app/
├── app.py                  # Flask application
├── requirements.txt        # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css      # Main stylesheet
│   ├── js/
│   │   ├── events.js      # Event data
│   │   └── main.js        # Main JavaScript functionality
│   ├── images/            # Logo and image assets
│   └── videos/            # Background video
└── templates/
    └── index.html         # Main HTML template
```

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Fonts**: Google Fonts (Cinzel, Playfair Display, Poppins, Cormorant Garamond)
- **Icons**: Material Symbols (Google)
- **Server**: Gunicorn (WSGI HTTP Server)

## Event Categories

- **5-Star Events** (12 events): High-profile competitions like Fashion Show, BGMI, Group Dance, etc.
- **3-Star Events** (10 events): Individual performances including vocals, dance, and quizzes
- **1-Star Events** (14 events): Fun activities and competitions

## Contact

**R.N.S Institute of Technology**
Dr. Vishnuvardhana Road Post, RNS Farms Rd,
Channasandra, Rajarajeshwari Nagar,
Bengaluru, Karnataka 560098

Phone: 080-28611880/1

## License

© 2025 Cultural Activity Team (CAT), RNSIT. All rights reserved.
