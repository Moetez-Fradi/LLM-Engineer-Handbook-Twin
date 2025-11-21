const fs = require('fs');
const { JSDOM } = require('jsdom');

const html = fs.readFileSync('raw.html', 'utf-8');
const dom = new JSDOM(html);
const document = dom.window.document;

let output = '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Extracted Content</title></head><body>';

const h2s = document.querySelectorAll('h2');

function hasContent(node) {
    // Consider it content if it has text, an image, or a link
    if (node.nodeType === 3) return node.textContent.trim() !== ''; // text node
    if (node.nodeType !== 1) return false; // not an element
    if (node.querySelector('img, a')) return true;
    return node.textContent.trim() !== '';
}

function extractContent(node) {
    if (node.nodeType === 3 && node.textContent.trim() !== '') {
        return node.textContent.trim();
    }
    if (node.nodeType === 1) {
        let children = Array.from(node.childNodes)
            .map(extractContent)
            .filter(Boolean)
            .join(' ');
        if (children) return `<${node.tagName.toLowerCase()}>${children}</${node.tagName.toLowerCase()}>`;
    }
    return '';
}

h2s.forEach(h2 => {
    if (h2.textContent.includes("Feed post number")) {
        output += `<h2>${h2.textContent.trim()}</h2>`;
        let sibling = h2.nextElementSibling;
        while (sibling && sibling.tagName !== 'H2') {
            if (sibling.tagName === 'DIV') {
                let content = extractContent(sibling);
                if (content) output += content;
            }
            sibling = sibling.nextElementSibling;
        }
    }
});

output += '</body></html>';

fs.writeFileSync('output.html', output, 'utf-8');
console.log('Extraction complete. Only meaningful content saved.');
