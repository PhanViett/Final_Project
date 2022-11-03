// Scripts for firebase and firebase messaging
importScripts(
  "https://www.gstatic.com/firebasejs/9.0.0/firebase-app-compat.js"
);
importScripts(
  "https://www.gstatic.com/firebasejs/9.0.0/firebase-messaging-compat.js"
);

// Initialize the Firebase app in the service worker by passing the generated config
var firebaseConfig = {
  apiKey: "AIzaSyBAyZD8XWJo4nl4KcIO-c2KOCdLKchlLb4",
  authDomain: "testnotiappcchndv2.firebaseapp.com",
  projectId: "testnotiappcchndv2",
  storageBucket: "testnotiappcchndv2.appspot.com",
  messagingSenderId: "568106658592",
  appId: "1:568106658592:web:97ae7bbddbf26121c04545",
  measurementId: "G-SE8ET9ZK0K",
};

firebase.initializeApp(firebaseConfig);

// Retrieve firebase messaging
const messaging = firebase.messaging();

messaging.onBackgroundMessage(function (payload) {
  console.log("Received background message ", payload);

  const notificationTitle = payload.notification.title;
  const notificationOptions = {
    body: payload.notification.body,
  };

  self.registration.showNotification(notificationTitle, notificationOptions);
});
