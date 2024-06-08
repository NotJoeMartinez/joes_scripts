{
    const header = document.querySelector('.header-bar');
    header.innerHTML += `
        <button onclick="copyLinks()">
            Copy Links
        </button>`;

    function copyLinks() {
        const foo = document.querySelectorAll(".item_link");
        const urls = [];
        for (let i = 0; i < foo.length; i++) {
          const yeet = foo[i];
          const bar = yeet.title;
          if (bar.includes(".pdf")) {
            const url = yeet.href;
            urls.push(url);
          }
        }
        const urlsString = urls.join('\n - [ ] ');
    
        console.log(urlsString);
    
        navigator.clipboard.writeText(urlsString)
        .then(() => {
            console.log('URLs copied to clipboard');
            alert('URLs copied to clipboard');
        })
        .catch(err => {
            console.error('Failed to copy URLs to clipboard: ', err);
            alert('Failed to copy URLs to clipboard');
        });

    }

}
  