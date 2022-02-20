
import firebase from 'firebase/compat/app';
import 'firebase/compat/auth';
import 'firebase/compat/firestore';
import 'firebase/compat/storage'; 

const firebaseConfig  = firebase.initializeApp({
  "projectId": "saransh-36252",
  "appId": "1:810027509020:web:c38d4b4ce5ea82a202c6d9",
  "databaseURL": "https://saransh-36252-default-rtdb.firebaseio.com",
  "storageBucket": "saransh-36252.appspot.com",
  "locationId": "us-central",
  "apiKey": "AIzaSyAYkvtXrRtT2V6WVtR3vBP4IL7xDVBs2BE",
  "authDomain": "saransh-36252.firebaseapp.com",
  "messagingSenderId": "810027509020",
  "measurementId": "G-B0JCFZ62LK"
});
if (firebase.apps.length === 0) {
  firebase.initializeApp(firebaseConfig);
}else {
  firebase.app(); // if already initialized, use that one
}

var storage = firebase.storage();
export default storage;
