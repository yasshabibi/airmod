// Service Worker
if ('serviceWorker' in navigator) {
    navigator.serviceWorker
      .register('/storage/client/sw.js')
      .then(() => { console.log('Service Worker Inscrit'); });
  };