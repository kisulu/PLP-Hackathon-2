# 🧠 AI Study Buddy - Flashcard Generator

**Vibe Coding 3.0 Hackathon Project**  
**SDG 4: Quality Education**

Transform your study notes into interactive flashcards with AI. Built specifically for African students who want to study smarter, not harder.

## 🚀 Features

### 🤖 AI-Powered Flashcard Generation
- Paste study notes or textbook content
- Hugging Face Question-Answering API creates smart flashcards
- Automatic difficulty assessment
- Personalized question-answer pairs

### 📚 Interactive Study Mode
- Beautiful 3D flip card animations
- Progress tracking and analytics
- Keyboard shortcuts for efficient studying
- Self-assessment with correct/incorrect marking

### 🔐 User Authentication
- Secure signup/login system
- Session management with Flask-Login
- Personalized flashcard libraries
- User progress tracking

### 💡 Community Feedback System
- Student suggestion box
- Bulk email confirmations for all users
- Admin panel for community management
- Feedback-driven development

### 💳 Payment Integration (IntaSend)
- M-Pesa payment support
- Credit/Debit card processing
- Bank transfer options
- Premium subscription tiers

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Python Flask
- **Database**: MySQL with SQLAlchemy ORM
- **AI**: Hugging Face Question-Answering API
- **Email**: Flask-Mail for bulk confirmations
- **Payments**: IntaSend API (African payment gateway)
- **Authentication**: Flask-Login with bcrypt

## 📁 Project Structure

```
ai-study-buddy/
├── app.py                  # Main Flask application
├── config.py               # Configuration settings
├── models.py               # SQLAlchemy database models
├── requirements.txt        # Python dependencies
├── migrate_db.py          # Database migration script
├── .env.example           # Environment variables template
├── README.md              # Project documentation
├── templates/             # Jinja2 HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Homepage (paste notes)
│   ├── flashcards.html   # Flashcards display & study mode
│   ├── login.html        # Login page
│   ├── signup.html       # Registration page
│   ├── suggestions.html  # Feedback system
│   └── premium.html      # Premium plans
├── static/               # Static assets
│   ├── style.css        # Main stylesheet
│   └── flashcards.js    # Frontend JavaScript
├── routes/              # Flask blueprints
│   ├── auth_routes.py   # Authentication routes
│   ├── flashcard_routes.py # Flashcard CRUD operations
│   └── suggestion_routes.py # Suggestion system
└── utils/               # Utility modules
    ├── ai_utils.py      # Hugging Face API integration
    └── email_utils.py   # Bulk email functionality
```

## 🔧 Setup Instructions

### 1. Prerequisites
- Python 3.8+
- MySQL 5.7+ or MariaDB 10.3+
- Git

### 2. Installation

```bash
# Clone the repository
git clone <repository-url>
cd ai-study-buddy

# Install Python dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your credentials
```

### 3. Database Setup

```bash
# Run the migration script
python migrate_db.py
```

### 4. API Keys Setup

#### Hugging Face API
1. Visit: https://huggingface.co/settings/tokens
2. Create a new token
3. Add to `.env`: `HUGGINGFACE_API_KEY=your_token_here`

#### IntaSend Payment Gateway
1. Sign up at: https://intasend.com
2. Get your API keys from the dashboard
3. Add to `.env`:
   ```
   INTASEND_PUBLISHABLE_KEY=your_publishable_key
   INTASEND_SECRET_KEY=your_secret_key
   INTASEND_TEST_MODE=true
   ```

#### Email Configuration (Gmail example)
1. Enable 2-factor authentication on Gmail
2. Generate an app password
3. Add to `.env`:
   ```
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   ```

### 5. Run the Application

```bash
python app.py
```

Visit: http://localhost:5000

## 🌍 Built for African Students

### 🎯 Target Market
- University and high school students across Africa
- Focus on affordable, accessible education technology
- Mobile-first design for smartphone users
- Support for local payment methods (M-Pesa, Airtel Money)

### 💰 Monetization Strategy
- **Free Tier**: 10 flashcards per day
- **Student Plan**: KES 300/month - 100 flashcards daily
- **Premium Plan**: KES 500/month - Unlimited flashcards + advanced features

### 🔄 Scalability Features
- Modular Flask architecture
- Database indexing for performance
- Caching strategies ready for implementation
- API rate limiting preparation
- Multi-language support framework

## 🏆 Hackathon Alignment

### SDG 4: Quality Education
- **Accessible Learning**: Free tier ensures basic access for all students
- **Technology Integration**: AI makes studying more efficient
- **Inclusive Design**: Built for diverse African educational contexts
- **Skill Development**: Promotes active learning and retention

### Technical Innovation
- **AI Integration**: Novel use of Question-Answering models for education
- **User Experience**: Intuitive card-flip animations and study flow
- **Community Features**: Feedback system builds user engagement
- **Payment Integration**: Local payment methods for African market

## 🚀 Future Enhancements

### Phase 1 (Post-Hackathon)
- [ ] Advanced AI models for better question generation
- [ ] Offline study mode with PWA
- [ ] Spaced repetition algorithm
- [ ] Multi-language support (Swahili, French, Arabic)

### Phase 2 (Market Expansion)
- [ ] Mobile app (React Native)
- [ ] Collaborative study groups
- [ ] Teacher dashboard for classroom use
- [ ] Integration with African universities

### Phase 3 (Scale)
- [ ] AI tutoring chatbot
- [ ] Video content flashcard generation
- [ ] Marketplace for shared flashcard decks
- [ ] Analytics dashboard for institutions

## 🤝 Contributing

We welcome contributions from the African developer community! Please read our contributing guidelines and submit pull requests.

## 📧 Contact

- **Email**: support@aistudybuddy.com
- **Website**: https://aistudybuddy.com
- **Twitter**: @AIStudyBuddy

## 📄 License

MIT License - Built with ❤️ for African education

---

**Vibe Coding 3.0 Hackathon**  
*Empowering African students through AI-powered education technology*