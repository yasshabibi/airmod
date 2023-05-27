// Le service worker est composé en général de 3 parties :
const cacheName = 'cache-v1';
// DES COMMENTAIRES ICI
const filesToCache = [
    '/storage/seller/index.html',
    '/storage/seller/style.css',
    '/storage/seller/script.js',
    '/storage/seller/commande.html',
    '/storage/seller/parametre_pro.css',
    '/storage/seller/parametre.html',
    '/storage/seller/qrCodeScanner.js',
    '/storage/seller/scan.html',
    '/storage/seller/stylescan.css',
    '/storage/assets/logo.png',
    '/pwathings/icon/AIRMOD PRO.png'
];

// - Un code qui s'exécute à l'installation du service worker
self.addEventListener('install', (event) => {
    console.log('Service Worker: Install', event);
    self.skipWaiting();
    event.waitUntil(
        // On ouvre le cache ("le dossier") avec le nom plus haut
        // Et on y ajoute toutes les adresses de filesToCache
        caches.open(cacheName)
            .then(cache => cache.addAll(filesToCache))
    );
});
// - Un code qui s'exécute à l'activation du service worker
self.addEventListener('activate', (event) => {
    console.log('Service Worker: Activate', event);
    event.waitUntil(
        // Pour tous les caches ("dossiers")
        // S'ils n'ont pas le même nom que cacheName
        // On les supprime
        caches.keys()
            .then(cacheNames => 
                cacheNames
                    .filter(cache => cache !== cacheName)
                    .forEach(cache => {
                        console.log("Delete cache", cache);
                        caches.delete(cache);
                    })
            )
    );
});

// - Un code qui s'exécute quand une requête HTTP est faite
self.addEventListener('fetch', (event) => {
    // Quand il y a une requête faite sur internet...
    // On répond toujours par nous même
    event.respondWith(
        // On cherche d'abord dans le cache, s'il y a un fichier
        // qui correspond à la requête
        caches.match(event.request).then((matchResponse) => {
            // Si c'est le cas, on le renvoie directement
            if(matchResponse !== undefined) return matchResponse;

            // Si c'est pas le cas, on n'a pas le fichier en cache !
            // On fait une vraie requête...
            return fetch(event.request)
                // Si elle passe, on renvoie le fichier
                .then(fetchResponse => fetchResponse)
                // Si elle plante, c'est dommage.
                // Peut être qu'il n'y a pas internet ?
                .catch(() => new Response(null, {
                    status: 501,
                    statusText: 'Service unavailable'
                }));
        })

    );
    console.log('Service Worker: Fetch', event);
});