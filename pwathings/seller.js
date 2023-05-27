// Service Worker
if ('serviceWorker' in navigator) {
    navigator.serviceWorker
      .register('/storage/seller/sw.js')
      .then(() => { console.log('Service Worker Inscrit'); });
  };