import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword, sendEmailVerification } 
from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyAFjNTEp3VLSfjHvn1R-YQHsv8tml0hIdQ",
  authDomain: "bulkmailpro-login.firebaseapp.com",
  projectId: "bulkmailpro-login",
  storageBucket: "bulkmailpro-login.firebasestorage.app",
  messagingSenderId: "837635632814",
  appId: "1:837635632814:web:b633bd69e3785aac2d873f"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

document.getElementById("signupForm").addEventListener("submit", function(e){
  e.preventDefault();

  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  createUserWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      const user = userCredential.user;

      sendEmailVerification(user).then(() => {
        alert("Verification email sent! Check inbox 📩");
      });
    })
    .catch((error) => {
      alert(error.message);
    });
});

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