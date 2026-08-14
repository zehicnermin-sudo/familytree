const fs = require('fs');
const path = require('path');

module.exports = (req, res) => {
    try {
        const filePath = path.join(__dirname, 'members.json');
        const raw = fs.readFileSync(filePath, 'utf8');
        const members = JSON.parse(raw);

        res.setHeader('Content-Type', 'application/json; charset=utf-8');
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.status(200).json({ members: members, total: members.length });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
};
