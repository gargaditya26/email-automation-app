import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getAuth, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-analytics.js";

const firebaseConfig = {
  apiKey: "AIzaSyAFjNTEp3VLSfjHvn1R-YQHsv8tml0hIdQ",
  authDomain: "bulkmailpro-login.firebaseapp.com",
  projectId: "bulkmailpro-login",
  storageBucket: "bulkmailpro-login.firebasestorage.app",
  messagingSenderId: "837635632814",
  appId: "1:837635632814:web:b633bd69e3785aac2d873f",
  measurementId: "G-0PKHFRM414"
};

const app = initializeApp(firebaseConfig);
getAnalytics(app);
const auth = getAuth(app);

document.getElementById("loginForm").addEventListener("submit", function(e){
  e.preventDefault();

  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  signInWithEmailAndPassword(auth, email, password)
    .then(async (userCredential) => {
      const user = userCredential.user;

      if (!user.emailVerified) {
        alert("Please verify your email first ❌");
        return;
      }

      // ✅ GET TOKEN
      const idToken = await user.getIdToken();

      // ✅ SEND TOKEN TO FLASK
      const response = await fetch('/verify-token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token: idToken })
      });

      const data = await response.json();

      if (data.status === 'success') {
        window.location.href = "/dashboard";
      } else {
        alert("Server verification failed");
      }
    })
    .catch((error) => {
      alert(error.message);
    });
});

// ===========================
// 👁️ SHOW / HIDE PASSWORD
// ===========================
document.getElementById("togglePass").addEventListener("click", function(){
  const pass = document.getElementById("password");
  if(pass.type === "password"){
    pass.type = "text";
    this.innerText = "Hide";
  } else {
    pass.type = "password";
    this.innerText = "Show";
  }
});