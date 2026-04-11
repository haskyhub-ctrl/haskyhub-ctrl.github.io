/**
 * FRAS Firebase Configuration
 * Firebase SDK loaded via CDN in HTML files
 */

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyAErFMFYIBa_fZJZNwhLEfzY6lJMg05VLY",
    authDomain: "fras-85395.firebaseapp.com",
    projectId: "fras-85395",
    storageBucket: "fras-85395.firebasestorage.app",
    messagingSenderId: "262389279505",
    appId: "1:262389279505:web:0742976e6c815c30937ab0",
    measurementId: "G-0Y3CJ7BY2G"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

// Initialize Firebase services
const firebaseAuth = firebase.auth();
const firebaseDb = firebase.firestore();
const firebaseAnalytics = firebase.analytics();

console.log('🔥 Firebase initialized successfully');
