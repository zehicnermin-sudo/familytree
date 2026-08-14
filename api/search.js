const fs = require('fs');
const path = require('path');

module.exports = (req, res) => {
    try {
        const filePath = path.join(process.cwd(), 'data', 'members.json');
        const raw = fs.readFileSync(filePath, 'utf8');
        const members = JSON.parse(raw);

        const { q = '', grana = '', spol = '', gen = '' } = req.query;
        const query = q.toLowerCase().trim();

        let filtered = members.filter(m => {
            if (grana && m.grana !== grana) return false;
            if (spol && m.spol !== spol) return false;
            if (gen && String(m.generacija) !== gen) return false;
            if (query) {
                const matchName = m.ime && m.ime.toLowerCase().includes(query);
                const matchParent = m.ime_roditelja && m.ime_roditelja.toLowerCase().includes(query);
                const matchSpouse = m.supruznik_ime && m.supruznik_ime.toLowerCase().includes(query);
                const matchNotes = m.napomene && m.napomene.toLowerCase().includes(query);
                if (!matchName && !matchParent && !matchSpouse && !matchNotes) return false;
            }
            return true;
        });

        res.setHeader('Content-Type', 'application/json; charset=utf-8');
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.status(200).json({ results: filtered.slice(0, 50), count: filtered.length });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
};
