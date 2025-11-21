const fs = require('fs');
const { JSDOM } = require('jsdom');

const html = fs.readFileSync('raw.html', 'utf-8');
const dom = new JSDOM(html);
const document = dom.window.document;

let output = '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Filtered Content</title></head><body>';
const h2s = document.querySelectorAll('h2');

const spanStringsToRemove = [
    "•",
    "1 week ago • Edited •",
    "Visible to anyone on or off LinkedIn",
    "Computer Science Student | AI & Data Science | Lifelong Learner",
    "Media is loading",
    "Loaded :",
    "00:00",
    "Stream Type LIVE",
    "Remaining time - 14:39",
    "1x",
    "0.5x",
    "0.75x",
    "1x , selected",
    "1.25x",
    "1.5x",
    "1.75x",
    "2x",
    "Media player modal window",
    "Media player modal window This modal can be closed by pressing the Escape key or activating the close button.",
    "Auto captions have been added to your video",
    "View analytics"
];

const buttonStringsToRemove = [
    "Like",
    "Comment",
    "Share",
    "Follow",
    "Repost",
    "Send",
    "more",
    "Speed",
    "Play",
    "Turn",
    "window",
    "Unmute",
    "captions",
    "Love"
];

const divExactRemove = [
    "1x",
    "00:00",
    "Stream Type LIVE",
    ":"
];

const paragraphExactRemove = [
    "Media player modal window",
    "Media player modal window This modal can be closed by pressing the Escape key or activating the close button.",
    "Auto captions have been added to your video"
];

function isBigMedia(node) {
    if (node.tagName === 'IMG') {
        const width = parseInt(node.getAttribute('width')) || 0;
        const height = parseInt(node.getAttribute('height')) || 0;
        return width > 80 && height > 80;
    } else if (node.tagName === 'VIDEO') {
        return true;
    }
    return false;
}

function shouldRemoveButton(node) {
    if (node.tagName !== 'BUTTON') return false;
    const text = (node.textContent || '').trim();
    return buttonStringsToRemove.some(str => text.includes(str));
}

function shouldRemoveDiv(node) {
    if (node.tagName !== 'DIV') return false;
    const text = (node.textContent || '').trim();
    return divExactRemove.includes(text);
}

function shouldRemoveParagraph(node) {
    if (node.tagName !== 'P') return false;
    const text = (node.textContent || '').trim();
    return paragraphExactRemove.includes(text);
}

function extractContent(node) {
    if (node.nodeType === 3 && node.textContent.trim() !== '') return node.textContent.trim();
    if (node.nodeType === 1) {
        if (shouldRemoveDiv(node)) return '';
        if (shouldRemoveParagraph(node)) return '';
        if (isBigMedia(node)) return node.outerHTML;

        if (node.tagName === 'SPAN') {
            const t = (node.textContent || '').trim();
            for (const s of spanStringsToRemove) if (t.includes(s)) return '';
        }

        if (shouldRemoveButton(node)) return '';

        const children = Array.from(node.childNodes)
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
                const content = extractContent(sibling);
                if (content) output += content;
            }
            sibling = sibling.nextElementSibling;
        }
    }
});

output += '</body></html>';
fs.writeFileSync('output.html', output, 'utf-8');
console.log('Extraction complete. Specified spans, buttons, divs, and paragraphs removed.');
