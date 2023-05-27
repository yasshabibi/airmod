// Service Worker
if ('serviceWorker' in navigator) {
    navigator.serviceWorker
      .register('/storage/delivery/sw.js')
      .then(() => { console.log('Service Worker Inscrit'); });
  };