// Load home.html content into #content div
fetch('content/home.html')
  .then(response => response.text())
  .then(data => {
    document.getElementById('content').innerHTML = data;
  })
  .catch(err => {
    console.error('Error loading content:', err);
  });
