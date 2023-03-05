



function logRouteAndIP() {
  // Get the user's IP address
  fetch('https://api.ipify.org?format=json')
    .then(response => response.json())
    .then(data => {
      const ip = data.ip;
      // Get the current route of the website
      const route = window.location.pathname;
      // Send the IP address and route to the server
      fetch(`/log?r=${route}&ip=${ip}`)
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
        })
        .catch(error => console.error(error));
    })
    .catch(error => console.error(error));


};
logRouteAndIP();