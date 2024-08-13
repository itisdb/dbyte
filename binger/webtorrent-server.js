import WebTorrent from 'webtorrent';
import express from 'express';

const client = new WebTorrent();
const app = express();
const PORT = 3000;

app.get('/stream', (req, res) => {
    const magnetURI = req.query.magnet;
    client.add(magnetURI, torrent => {
        // its not necessary to find the mp4 file, you can stream any file
        const file = torrent.files.find(file => file.name.endsWith('.mp4'));
        if (file) {
            res.setHeader('Content-Type', 'video/mp4');
            const stream = file.createReadStream();
            stream.pipe(res);
        } else {
            res.status(404).send('No MP4 file found in torrent.');
            console.log('No MP4 file found in torrent.');
        }
    });
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
