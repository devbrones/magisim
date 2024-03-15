function createFullScreenOverlay() {
    // css cuz fuck gradio
    const css = `.lds-ripple {
        display: inline-block;
        position: relative;
        width: 40px;
        height: 40px;
    }
    .lds-ripple div {
        position: absolute;
        border: 4px solid #fff;
        opacity: 1;
        border-radius: 50%;
        animation: lds-ripple 1s cubic-bezier(0, 0.2, 0.8, 1) infinite;
    }
    .lds-ripple div:nth-child(2) {
        animation-delay: -0.5s;
    }
    @keyframes lds-ripple {
        0% {
            top: 18px;
            left: 18px;
            width: 0;
            height: 0;
            opacity: 0;
        }
        4.9% {
            top: 18px;
            left: 18px;
            width: 0;
            height: 0;
            opacity: 0;
        }
        5% {
            top: 18px;
            left: 18px;
            width: 0;
            height: 0;
            opacity: 1;
        }
        100% {
            top: 0px;
            left: 0px;
            width: 36px;
            height: 36px;
            opacity: 0;
        }
    }`
    const style = document.createElement('style');
    style.type = 'text/css';
    style.appendChild(document.createTextNode(css));
    document.head.appendChild(style);
    // Create a new div element for overlay
    const overlay = document.createElement('div');
    // Set styles for overlay
    overlay.style.position = 'fixed';
    overlay.style.top = '0';
    overlay.style.left = '0';
    overlay.style.width = '100vw';
    overlay.style.height = '100vh';
    overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
    overlay.style.backdropFilter = 'blur(25px)';
    overlay.style.zIndex = '10000';
    document.body.appendChild(overlay);

    // Create a new div element for modal
    const modal = document.createElement('div');
    modal.id = 'loadinmodal';
    // Set styles for modal
    modal.style.width = '512px';
    modal.style.height = '360px';
    modal.style.backgroundColor = '#171717';
    modal.style.borderRadius = '10px';
    modal.style.position = 'fixed';
    modal.style.top = '50%';
    modal.style.left = '50%';
    modal.style.transform = 'translate(-50%, -50%)';
    modal.style.zIndex = '10001';
    document.body.appendChild(modal);

    // Create a container for the logo and spinner
    const centerContainer = document.createElement('div');
    centerContainer.style.position = 'absolute';
    centerContainer.style.top = '50%';
    centerContainer.style.left = '50%';
    centerContainer.style.transform = 'translate(-50%, -50%)';
    modal.appendChild(centerContainer);

    // Create an img element for the Magisim logo
    const logo = document.createElement('img');
    logo.src = 'http://magisim.com/resources/magisim_logo256.png';
    logo.style.display = 'block';
    logo.style.width = '128px';
    logo.style.height = '128px';
    logo.style.margin = '0 auto 8px'; // 8px margin at the bottom
    centerContainer.appendChild(logo);

    // Create a div for the ripple spinner
    const spinner = document.createElement('div');
    spinner.className = 'lds-ripple';
    spinner.innerHTML = '<div></div><div></div>';
    spinner.style.display = 'block';
    spinner.style.margin = '0 auto'; // Center spinner in the container
    centerContainer.appendChild(spinner);

    // create loading text
    const loadingText = document.createElement('p');
    loadingText.className = 'md';
    loadingText.style.color = '#ddd';
    loadingText.style.textAlign = 'center';
    loadingText.style.fontSize = '12px';
    loadingText.style.marginTop = '8px';
    loadingText.textContent = 'Loading components';
    centerContainer.appendChild(loadingText);


    // Remove overlay and modal after 5 seconds
    setTimeout(() => {
        overlay.remove();
        modal.remove();
    }, 5000);
}
function waitForElement(selector, callback, interval = 100, timeout = 30000) {
    const startTime = new Date().getTime();

    const check = () => {
        const element = document.querySelector(selector);
        if (element) {
            callback(element);
        } else {
            if (new Date().getTime() - startTime < timeout) {
                setTimeout(check, interval);
            } else {
                console.log(`Element with selector '${selector}' not found within the timeout period.`);
            }
        }
    };

    check();
}

waitForElement('#component-0', (element) => {
    // Code to execute once the specific div is available
    console.log('Element is now available:', element);
    createFullScreenOverlay();
});