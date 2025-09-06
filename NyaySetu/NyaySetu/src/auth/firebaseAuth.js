import { initializeApp } from "firebase/app";
import { getAuth, createUserWithEmailAndPassword, sendEmailVerification, signInWithPopup, GoogleAuthProvider } from "firebase/auth";

const firebaseConfig = {
  apiKey: "FIREBASE_API_KEY",
  authDomain: "PROJECT.firebaseapp.com",
  // ...other config
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const googleProvider = new GoogleAuthProvider();

export async function signUpWithEmail(email, password) {
  const userCred = await createUserWithEmailAndPassword(auth, email, password);
  await sendEmailVerification(userCred.user); // sends verification to Gmail
  return userCred.user;
}

export function signInWithGoogle() {
  return signInWithPopup(auth, googleProvider);
}