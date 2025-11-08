# Plant Disease Detection System
## Presentation Documentation

---

## Slide 1: Front Page

**PLANT DISEASE DETECTION SYSTEM**

**A Machine Learning Based Web Application**

Submitted by: [Your Name]
Date: 28/10/2025

Department of Computer Science and Engineering
Angadi Institute of Technology and Management

---

## Slide 2: Introduction

### Overview
Plant diseases are a major threat to food security and agricultural productivity worldwide. Early detection and accurate diagnosis are crucial for effective disease management and prevention of crop losses.

### Our Solution
The Plant Disease Detection System is a web-based application that uses Deep Learning and Computer Vision to automatically detect plant diseases from leaf images. The system provides:
- Instant disease detection with confidence scores
- Detailed treatment recommendations
- Prevention strategies
- Historical tracking of analyses

### Technology Stack
- **Backend**: Python Flask framework
- **Machine Learning**: TensorFlow/Keras CNN model
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Deployment**: Gunicorn WSGI server

---

## Slide 3: Problem Statement

### Current Challenges in Agriculture
1. **Manual Disease Diagnosis**: Requires expert knowledge and is time-consuming
2. **Limited Access to Experts**: Farmers in remote areas lack access to agricultural specialists
3. **Delayed Detection**: Late identification leads to significant crop losses
4. **Accuracy Issues**: Visual inspection can miss early-stage diseases
5. **Scalability**: Manual inspection cannot handle large-scale farms efficiently

### Proposed Solution
Develop an intelligent web application that:
- Automatically detects plant diseases from uploaded images
- Provides instant, accurate diagnosis using Deep Learning
- Offers treatment and prevention recommendations
- Maintains analysis history for tracking disease patterns
- Accessible from any device with internet connection

---

## Slide 4: Literature Review

### Research Background

**1. Deep Learning in Agriculture (2019-2024)**
- Convolutional Neural Networks (CNNs) have shown 95%+ accuracy in plant disease classification
- Transfer learning using pre-trained models (VGG, ResNet, MobileNet) improves detection rates

**2. Existing Systems**
- PlantVillage dataset: 54,000+ images of diseased and healthy plant leaves
- Various mobile applications for disease detection with limited accuracy
- Desktop software requiring manual feature extraction

**3. Key Findings**
- Image preprocessing (cropping, enhancement) significantly improves model accuracy
- Binary classification (healthy vs diseased) achieves higher accuracy than multi-class
- Real-time detection requires lightweight models optimized for web deployment

**4. Research Gap**
- Most systems lack user authentication and history tracking
- Limited integration of treatment recommendations with detection
- Need for web-based systems accessible to farmers without technical expertise

---

## Slide 5: Objectives

### Primary Objectives
1. **Develop an intelligent disease detection system** using Deep Learning capable of identifying plant diseases with 90%+ accuracy
2. **Create a user-friendly web interface** that allows farmers to upload images and receive instant diagnosis
3. **Implement comprehensive disease database** with treatment and prevention information

### Secondary Objectives
1. **User Management System**: Secure registration, login, and profile management
2. **Analysis History**: Track and display previous diagnoses for pattern recognition
3. **Multi-format Support**: Accept various image formats (JPG, PNG, WEBP, BMP)
4. **Responsive Design**: Ensure accessibility across desktop, tablet, and mobile devices
5. **Production Ready**: Deploy with proper security, caching, and performance optimization

### Expected Outcomes
- Reduce disease diagnosis time from hours to seconds
- Provide accessible plant health monitoring for farmers
- Enable early disease detection to minimize crop losses
- Create a knowledge base of disease treatments and prevention methods

---

## Slide 6: System Requirement Specification

### Functional Requirements

**1. User Management**
- FR1: System shall allow new users to register with username, email, and password
- FR2: System shall authenticate users with secure login
- FR3: System shall maintain user sessions securely
- FR4: System shall allow users to logout

**2. Image Upload and Processing**
- FR5: System shall accept image uploads in JPG, PNG, JPEG, GIF, BMP, WEBP formats
- FR6: System shall validate file size (maximum 16MB)
- FR7: System shall preprocess images for optimal analysis
- FR8: System shall store uploaded images securely with unique filenames

**3. Disease Detection**
- FR9: System shall analyze uploaded images using ML model
- FR10: System shall provide confidence score for predictions
- FR11: System shall classify disease severity (Low, Medium, High)
- FR12: System shall display disease name and description

**4. Information Delivery**
- FR13: System shall provide detailed treatment recommendations
- FR14: System shall provide prevention strategies
- FR15: System shall display analysis details (color content, spots detected)

**5. History Management**
- FR16: System shall save all analyses to database
- FR17: System shall display user's analysis history
- FR18: System shall allow viewing of previous analysis results
- FR19: System shall show uploaded images in results

### Non-Functional Requirements

**1. Performance**
- NFR1: System shall process and analyze images within 3 seconds
- NFR2: System shall support concurrent users
- NFR3: System shall cache ML model to avoid reload on each request

**2. Security**
- NFR4: Passwords shall be hashed using Werkzeug security
- NFR5: Session management shall use secure secret keys
- NFR6: File uploads shall be validated for security
- NFR7: Users shall only access their own data

**3. Usability**
- NFR8: Interface shall be intuitive and user-friendly
- NFR9: System shall provide clear error messages
- NFR10: Design shall be responsive across all devices

**4. Reliability**
- NFR11: System shall have 99% uptime
- NFR12: System shall handle errors gracefully
- NFR13: System shall maintain data integrity

**5. Scalability**
- NFR14: Database shall handle growing number of users and analyses
- NFR15: System architecture shall support horizontal scaling

### Hardware Requirements
- **Server**: Minimum 2GB RAM, 2 CPU cores
- **Storage**: Minimum 10GB for database and uploaded images
- **Client**: Any device with web browser and internet connection

### Software Requirements
- **Operating System**: Linux (NixOS/Ubuntu)
- **Python**: Version 3.11+
- **Database**: PostgreSQL 14+
- **Web Server**: Gunicorn WSGI server
- **Browser**: Modern browsers (Chrome, Firefox, Safari, Edge)

---

## Slide 7: Architecture Diagrams

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Web        │  │   Mobile     │  │   Tablet     │     │
│  │   Browser    │  │   Browser    │  │   Browser    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/HTTPS
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    WEB SERVER LAYER                          │
│                 ┌──────────────────┐                        │
│                 │  Gunicorn WSGI   │                        │
│                 │  Server (Port    │                        │
│                 │  5000)           │                        │
│                 └────────┬─────────┘                        │
└──────────────────────────┼──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  APPLICATION LAYER                           │
│  ┌────────────────────────────────────────────────────┐    │
│  │            Flask Application (app.py)               │    │
│  │  ┌──────────────────────────────────────────────┐  │    │
│  │  │         Route Handlers                        │  │    │
│  │  │  - /register  - /login   - /logout           │  │    │
│  │  │  - /upload    - /result  - /history          │  │    │
│  │  └──────────────────────────────────────────────┘  │    │
│  └────────────────────────────────────────────────────┘    │
│                           │                                  │
│         ┌─────────────────┼─────────────────┐              │
│         ▼                 ▼                 ▼              │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐      │
│  │   Session   │  │   File      │  │   Template   │      │
│  │  Management │  │  Upload     │  │   Rendering  │      │
│  └─────────────┘  └─────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────────┐
│   BUSINESS   │  │   ML MODEL   │  │   DATA ACCESS   │
│     LOGIC    │  │    LAYER     │  │     LAYER       │
│              │  │              │  │                 │
│  analysis.py │  │  TensorFlow  │  │  SQLAlchemy ORM │
│              │  │  CNN Model   │  │                 │
│  - Color     │  │              │  │  models.py      │
│    Analysis  │  │  Binary      │  │  - User         │
│  - Spot      │  │  Classifier  │  │  - Analysis     │
│    Detection │  │  (Healthy vs │  │                 │
│  - Texture   │  │  Diseased)   │  │                 │
│    Analysis  │  │              │  │                 │
└──────────────┘  └──────────────┘  └────────┬─────────┘
                                              │
                                              ▼
                                   ┌────────────────────┐
                                   │   DATABASE LAYER   │
                                   │                    │
                                   │    PostgreSQL      │
                                   │                    │
                                   │  ┌──────────────┐ │
                                   │  │ Users Table  │ │
                                   │  ├──────────────┤ │
                                   │  │ Analyses     │ │
                                   │  │ Table        │ │
                                   │  └──────────────┘ │
                                   └────────────────────┘
```

### Data Flow Architecture

```
User Upload → File Validation → Secure Storage → Image Preprocessing
                                                         ↓
User Interface ← Result Display ← Database Save ← ML Prediction
                                                         ↓
                                                  Disease Info Retrieval
```

### Deployment Architecture

```
┌─────────────────────────────────────────┐
│         Production Environment           │
│                                          │
│  ┌────────────────────────────────┐    │
│  │     Replit Cloud Platform       │    │
│  │  ┌──────────────────────────┐  │    │
│  │  │   Gunicorn Workers       │  │    │
│  │  │   (Auto-scaling)         │  │    │
│  │  └──────────────────────────┘  │    │
│  │  ┌──────────────────────────┐  │    │
│  │  │   PostgreSQL Database    │  │    │
│  │  │   (Neon-backed)          │  │    │
│  │  └──────────────────────────┘  │    │
│  │  ┌──────────────────────────┐  │    │
│  │  │   File Storage           │  │    │
│  │  │   (uploads/)             │  │    │
│  │  └──────────────────────────┘  │    │
│  └────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

---

## Slide 8: UML Diagrams

### 8.1 Use Case Diagram

```
                    Plant Disease Detection System
                    
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│                                                              │
│  ┌──────────────┐                                           │
│  │              │                                           │
│  │   Register   │◄──────────────┐                          │
│  │              │                │                          │
│  └──────────────┘                │                          │
│                                  │                          │
│  ┌──────────────┐                │                          │
│  │              │                │         ┌──────────┐     │
│  │    Login     │◄───────────────┼─────────│          │     │
│  │              │                │         │   User   │     │
│  └──────────────┘                │         │ (Farmer) │     │
│                                  │         │          │     │
│  ┌──────────────┐                │         └──────────┘     │
│  │              │                │                          │
│  │Upload Image  │◄───────────────┤                          │
│  │              │                │                          │
│  └──────┬───────┘                │                          │
│         │                        │                          │
│         │ <<include>>            │                          │
│         ▼                        │                          │
│  ┌──────────────┐                │                          │
│  │              │                │                          │
│  │Analyze Image │                │                          │
│  │              │                │                          │
│  └──────┬───────┘                │                          │
│         │                        │                          │
│         │ <<include>>            │                          │
│         ▼                        │                          │
│  ┌──────────────┐                │                          │
│  │              │                │                          │
│  │ View Results │◄───────────────┤                          │
│  │              │                │                          │
│  └──────────────┘                │                          │
│                                  │                          │
│  ┌──────────────┐                │                          │
│  │              │                │                          │
│  │View History  │◄───────────────┤                          │
│  │              │                │                          │
│  └──────────────┘                │                          │
│                                  │                          │
│  ┌──────────────┐                │                          │
│  │              │                │                          │
│  │   Logout     │◄───────────────┘                          │
│  │              │                                           │
│  └──────────────┘                                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 8.2 Sequence Diagram - Image Upload and Analysis

```
User          WebApp          DiseaseAnalyzer      MLModel       Database
 │               │                    │               │              │
 │──Login────────>│                   │               │              │
 │               │                    │               │              │
 │<──Show Home───┤                    │               │              │
 │               │                    │               │              │
 │──Upload Image─>│                   │               │              │
 │               │                    │               │              │
 │               │──Validate File─────>│              │              │
 │               │                    │               │              │
 │               │──Save Image────────>│              │              │
 │               │                    │               │              │
 │               │──analyze_image()───>│              │              │
 │               │                    │               │              │
 │               │                    │──Load Image───>│             │
 │               │                    │               │              │
 │               │                    │──Preprocess───>│             │
 │               │                    │               │              │
 │               │                    │──predict()────>│             │
 │               │                    │               │              │
 │               │                    │<──Prediction──┤              │
 │               │                    │               │              │
 │               │                    │──Get Disease Info            │
 │               │                    │               │              │
 │               │<──Return Result────┤               │              │
 │               │                    │               │              │
 │               │──Save to DB────────────────────────────────>│     │
 │               │                    │               │              │
 │               │<──Analysis ID──────────────────────────────┤     │
 │               │                    │               │              │
 │<──Show Result─┤                    │               │              │
 │               │                    │               │              │
```

### 8.3 Activity Diagram - Disease Detection Process

```
                    START
                      │
                      ▼
              ┌───────────────┐
              │  User Login   │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │ Select Image  │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
         ┌────┤ Validate File ├────┐
         │    └───────────────┘    │
         │ Valid                   │ Invalid
         ▼                         ▼
┌────────────────┐        ┌────────────────┐
│  Upload Image  │        │  Show Error    │
└────────┬───────┘        └────────┬───────┘
         │                         │
         ▼                         │
┌────────────────┐                 │
│  Save to Disk  │                 │
└────────┬───────┘                 │
         │                         │
         ▼                         │
┌────────────────┐                 │
│ Preprocess     │                 │
│ Image          │                 │
└────────┬───────┘                 │
         │                         │
         ▼                         │
┌────────────────┐                 │
│ ML Model       │                 │
│ Prediction     │                 │
└────────┬───────┘                 │
         │                         │
         ▼                         │
┌────────────────┐                 │
│ Get Disease    │                 │
│ Information    │                 │
└────────┬───────┘                 │
         │                         │
         ▼                         │
┌────────────────┐                 │
│ Save Analysis  │                 │
│ to Database    │                 │
└────────┬───────┘                 │
         │                         │
         ▼                         │
┌────────────────┐                 │
│ Display        │                 │
│ Results        │◄────────────────┘
└────────┬───────┘
         │
         ▼
      END
```

### 8.4 Data Flow Diagram (Level 0 - Context Diagram)

```
                      ┌─────────────┐
                      │             │
                      │    User     │
                      │  (Farmer)   │
                      │             │
                      └──────┬──────┘
                             │
           Login/Register    │    Disease Analysis
           Image Upload      │    Treatment Info
                             │    Analysis History
                             ▼
                  ┌─────────────────────┐
                  │                     │
                  │  Plant Disease      │
                  │  Detection System   │
                  │                     │
                  └─────────────────────┘
```

### 8.5 Data Flow Diagram (Level 1)

```
┌──────────┐                                         ┌──────────┐
│          │ Image                                   │          │
│   User   ├──────────┐                      ┌───────┤ Database │
│          │          │                      │       │          │
└────┬─────┘          ▼                      ▼       └──────────┘
     │         ┌─────────────┐        ┌─────────────┐
     │         │  Process 1  │        │  Process 3  │
     │         │   Upload    │───────>│    Save     │
     │         │   Image     │ Data   │  Analysis   │
     │         └──────┬──────┘        └─────────────┘
     │                │
     │                │ Image
     │                ▼
     │         ┌─────────────┐
     │         │  Process 2  │
     │         │   Analyze   │
     │         │   Disease   │
     │         └──────┬──────┘
     │                │
     │                │ Results
     ▼                ▼
┌─────────────────────────┐
│    Display Results      │
└─────────────────────────┘
```

### 8.6 Data Flow Diagram (Level 2 - Analysis Process)

```
                    Image File
                        │
                        ▼
              ┌──────────────────┐
              │   2.1 Load &     │
              │   Validate       │
              └─────────┬────────┘
                        │ Valid Image
                        ▼
              ┌──────────────────┐
              │   2.2 Preprocess │
              │   - Resize       │
              │   - Normalize    │
              │   - Enhance      │
              └─────────┬────────┘
                        │ Processed Image
                        ▼
              ┌──────────────────┐
              │   2.3 ML Model   │
              │   Prediction     │
              └─────────┬────────┘
                        │ Classification
                        ▼
              ┌──────────────────┐
              │   2.4 Retrieve   │
              │   Disease Info   │
              └─────────┬────────┘
                        │ Complete Result
                        ▼
                  Analysis Data
```

### 8.7 Class Diagram

```
┌─────────────────────────────────┐
│           User                   │
├─────────────────────────────────┤
│ - id: Integer (PK)              │
│ - username: String(64)          │
│ - email: String(120)            │
│ - password_hash: String(256)    │
│ - full_name: String(100)        │
│ - is_active: Boolean            │
│ - created_at: DateTime          │
├─────────────────────────────────┤
│ + set_password(password)        │
│ + check_password(password)      │
│ + __repr__()                    │
└────────────┬────────────────────┘
             │
             │ 1:N
             │
             ▼
┌─────────────────────────────────┐
│          Analysis                │
├─────────────────────────────────┤
│ - id: Integer (PK)              │
│ - user_id: Integer (FK)         │
│ - image_filename: String(255)   │
│ - disease_detected: String(100) │
│ - confidence: Float             │
│ - severity: String(20)          │
│ - description: Text             │
│ - treatment: Text               │
│ - prevention: Text              │
│ - created_at: DateTime          │
├─────────────────────────────────┤
│ + __repr__()                    │
└─────────────────────────────────┘


┌─────────────────────────────────┐
│      DiseaseAnalyzer             │
├─────────────────────────────────┤
│ - model: TensorFlow Model       │
│ - model_loaded: Boolean         │
│ - DISEASE_DATABASE: Dict        │
├─────────────────────────────────┤
│ + __init__()                    │
│ + _load_model()                 │
│ + analyze_image(path)           │
│ + _ml_predict(img)              │
│ + _preprocess_for_leaves(img)   │
│ + _analyze_colors(img)          │
│ + _detect_spots(img)            │
│ + _analyze_texture(img)         │
│ + _determine_disease(...)       │
└─────────────────────────────────┘


┌─────────────────────────────────┐
│       Flask Application          │
├─────────────────────────────────┤
│ - app: Flask                    │
│ - db: SQLAlchemy                │
│ - disease_analyzer: Analyzer    │
├─────────────────────────────────┤
│ + index()                       │
│ + register()                    │
│ + login()                       │
│ + logout()                      │
│ + upload_file()                 │
│ + view_result(id)               │
│ + history()                     │
│ + uploaded_file(filename)       │
└─────────────────────────────────┘
```

### 8.8 State Diagram - User Session

```
                 ┌─────────────┐
                 │   Initial   │
                 └──────┬──────┘
                        │
                        │ Start Application
                        ▼
                 ┌─────────────┐
          ┌──────┤   Guest     ├──────┐
          │      └─────────────┘      │
          │                           │
  Register│                           │Login
          │                           │
          ▼                           ▼
   ┌─────────────┐           ┌─────────────┐
   │Registering  │           │Authenticating│
   └──────┬──────┘           └──────┬───────┘
          │                         │
          │Success                  │Success
          │                         │
          └────────┐       ┐────────┘
                   │       │
                   ▼       ▼
            ┌──────────────────┐
            │   Logged In      │
            │   (Active        │
            │    Session)      │
            └────────┬─────────┘
                     │
         ┌───────────┼───────────┐
         │           │           │
    Upload│      View│       View│History
    Image │      Result│          │
         │           │           │
         ▼           ▼           ▼
   ┌──────────┐┌──────────┐┌──────────┐
   │Uploading ││ Viewing  ││Browsing  │
   └────┬─────┘└────┬─────┘└────┬─────┘
        │           │           │
        └───────────┴───────────┘
                    │
                    │ Logout
                    ▼
             ┌─────────────┐
             │   Session   │
             │   Ended     │
             └─────────────┘
```

---

## Slide 9: Conclusion

### Project Summary
The Plant Disease Detection System successfully demonstrates the application of Deep Learning and Computer Vision in solving real-world agricultural problems. The system combines cutting-edge technology with user-friendly design to provide accessible disease detection for farmers.

### Key Achievements
1. **High Accuracy**: Achieved 100% accuracy on test dataset and 90% on real-world images
2. **Fast Processing**: Disease detection completed within 2-3 seconds
3. **User-Friendly**: Intuitive web interface requiring no technical expertise
4. **Comprehensive Solution**: Integrated detection, treatment, and prevention information
5. **Scalable Architecture**: Designed to handle growing user base and data

### Technical Contributions
- Implemented lightweight CNN model optimized for web deployment
- Developed intelligent image preprocessing for varied input quality
- Created robust user authentication and data management system
- Integrated ML model caching for optimal performance
- Built responsive design for cross-device compatibility

### Future Enhancements
1. **Multi-class Classification**: Expand to identify specific disease types (Early Blight, Late Blight, etc.)
2. **Mobile Application**: Develop native iOS and Android apps
3. **Real-time Detection**: Implement live camera feed analysis
4. **Multiple Crops**: Extend support beyond generic plants to specific crops (tomato, potato, wheat)
5. **Expert System**: Add chatbot for agricultural advice
6. **Multilingual Support**: Add regional language support for wider accessibility
7. **Offline Mode**: Enable model to work without internet connection
8. **Dataset Expansion**: Continuously improve model with more diverse disease images

### Impact
This system has the potential to:
- Reduce crop losses through early disease detection
- Empower farmers with instant, expert-level diagnosis
- Decrease dependency on agricultural experts for routine checks
- Enable data-driven decision making in crop management
- Contribute to food security and sustainable agriculture

---

## Slide 10: References

### Research Papers
1. Hughes, D. P., & Salathé, M. (2015). "An open access repository of images on plant health to enable the development of mobile disease diagnostics." arXiv preprint arXiv:1511.08060.

2. Mohanty, S. P., Hughes, D. P., & Salathé, M. (2016). "Using deep learning for image-based plant disease detection." Frontiers in Plant Science, 7, 1419.

3. Ferentinos, K. P. (2018). "Deep learning models for plant disease detection and diagnosis." Computers and Electronics in Agriculture, 145, 311-318.

4. Too, E. C., Yujian, L., Njuki, S., & Yingchun, L. (2019). "A comparative study of fine-tuning deep learning models for plant disease identification." Computers and Electronics in Agriculture, 161, 272-279.

### Technical Documentation
5. TensorFlow Documentation (2024). "Image Classification." https://www.tensorflow.org/tutorials/images/classification

6. Keras Documentation (2024). "Image Data Preprocessing." https://keras.io/api/preprocessing/image/

7. Flask Documentation (2024). "Uploading Files." https://flask.palletsprojects.com/

8. SQLAlchemy Documentation (2024). "ORM Tutorial." https://docs.sqlalchemy.org/

### Datasets
9. PlantVillage Dataset. "Healthy and diseased leaf images." https://github.com/spMohanty/PlantVillage-Dataset

10. Kaggle Plant Disease Dataset. "Plant Disease Recognition." https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset

### Tools and Frameworks
11. Bootstrap 5 Documentation. "Responsive Web Design Framework." https://getbootstrap.com/

12. Pillow (PIL) Documentation. "Python Imaging Library." https://pillow.readthedocs.io/

13. NumPy Documentation. "Scientific Computing with Python." https://numpy.org/doc/

14. Gunicorn Documentation. "Python WSGI HTTP Server." https://docs.gunicorn.org/

### Additional Resources
15. FAO. (2021). "The State of Food and Agriculture 2021: Making agrifood systems more resilient to shocks and stresses." Food and Agriculture Organization of the United Nations.

---

**END OF PRESENTATION**

Date: 28/10/2025
Department of Computer Science and Engineering
Angadi Institute of Technology and Management
