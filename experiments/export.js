const fs = require('fs');
const { JSDOM } = require('jsdom');

const html = fs.readFileSync('raw.html', 'utf-8');
const dom = new JSDOM(html);
const document = dom.window.document;

let output = '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Extracted Divs</title></head><body>';

const h2s = document.querySelectorAll('h2');

h2s.forEach(h2 => {
    if (h2.textContent.includes("Feed post number")) {
        output += `<h2>${h2.textContent.trim()}</h2>`;
        let sibling = h2.nextElementSibling;
        while (sibling && sibling.tagName !== 'H2') {
            if (sibling.tagName === 'DIV') {
                output += `<div>${sibling.innerHTML}</div>`;
            }
            sibling = sibling.nextElementSibling;
        }
    }
});

output += '</body></html>';

fs.writeFileSync('output.html', output, 'utf-8');
console.log('Extraction complete. Saved to output.html');
