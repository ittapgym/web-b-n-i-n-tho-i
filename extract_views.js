const fs = require('fs');
const path = require('path');

const indexHtmlPath = path.join(__dirname, 'peach_admin', 'index.html');
const viewsDir = path.join(__dirname, 'peach_admin', 'src', 'views');

if (!fs.existsSync(viewsDir)) {
  fs.mkdirSync(viewsDir, { recursive: true });
}

let html = fs.readFileSync(indexHtmlPath, 'utf8');

// Regex to match <div v-if="activeTab === 'VIEW_NAME'" ...> ... </div>
// It uses balanced matching conceptually, but since regex can't easily match deeply nested divs reliably,
// we will do it manually.
const extractView = (tabName, filename) => {
  const markerStr = `v-if="activeTab === '${tabName}'"`;
  const startIdx = html.indexOf(markerStr);
  if (startIdx === -1) return;

  // Find the opening <div
  let divStart = html.lastIndexOf('<div', startIdx);
  if (divStart === -1) return;

  let openDivs = 0;
  let endIdx = -1;
  let inString = false;
  let stringChar = '';

  for (let i = divStart; i < html.length; i++) {
    if (!inString) {
      if (html[i] === "'" || html[i] === '"') {
        inString = true;
        stringChar = html[i];
      } else if (html.slice(i, i + 4) === '<div') {
        openDivs++;
        i += 3;
      } else if (html.slice(i, i + 6) === '</div>') {
        openDivs--;
        if (openDivs === 0) {
          endIdx = i + 6;
          break;
        }
        i += 5;
      }
    } else {
      if (html[i] === stringChar && html[i-1] !== '\\') {
        inString = false;
      }
    }
  }

  if (endIdx !== -1) {
    const viewContent = html.substring(divStart, endIdx);
    fs.writeFileSync(path.join(viewsDir, filename), viewContent);
    console.log(`Extracted ${filename}`);
    
    // Replace in main html
    const includeTag = `<include-html src="src/views/${filename}"></include-html>`;
    html = html.substring(0, divStart) + includeTag + html.substring(endIdx);
  }
};

extractView('dashboard', 'Dashboard.html');
extractView('stats', 'Analytics.html');
extractView('products', 'Products.html');
extractView('inventory', 'Inventory.html');
extractView('orders', 'Orders.html');
extractView('customers', 'Customers.html');
extractView('finance', 'Finance.html');
extractView('settings', 'Settings.html');
extractView('promotions', 'Promotions.html');
extractView('reports', 'Reports.html');

fs.writeFileSync(indexHtmlPath, html);
console.log("Extraction complete!");
