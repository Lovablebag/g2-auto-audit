/* Period Compare worker: stream CSVs, keep needed columns, report progress. */
importScripts('https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js');

const KEEP = ['Created (UTC)','Booking ID','Master City','City','Property','Contract','Source','Check-In','Nights','Lead Time','Status','Cost','Curr','Rate Plan','Offer','Client Name','Source Market','Distribution Type','Non-Refundable'];

self.onmessage = async (e) => {
  const { files } = e.data;
  const cities = new Set();
  const rows = [];
  let minD = '9999', maxD = '0000', total = 0, kept = 0;
  for (let fi = 0; fi < files.length; fi++) {
    const f = files[fi];
    await new Promise((resolve, reject) => {
      Papa.parse(f, {
        header: true,
        skipEmptyLines: true,
        chunk: (res, parser) => {
          for (const r of res.data) {
            total++;
            const mc = (r['Master City'] || '').trim();
            if (!mc) continue;
            cities.add(mc);
            const created = String(r['Created (UTC)'] || '').slice(0, 10);
            if (created.length === 10) { if (created < minD) minD = created; if (created > maxD) maxD = created; }
            const o = {};
            for (const k of KEEP) o[k] = r[k] == null ? '' : String(r[k]);
            rows.push(o);
            kept++;
          }
          if (total % 20000 < 500) self.postMessage({ type: 'progress', file: f.name, total, kept, pct: Math.min(99, Math.round((fi + 0.5) / files.length * 100)) });
        },
        complete: resolve,
        error: reject
      });
    });
  }
  self.postMessage({ type: 'done', cities: [...cities].sort(), rows, minD, maxD, total, kept });
};
