/*!
* Start Bootstrap - Simple Sidebar v6.0.6 (https://startbootstrap.com/template/simple-sidebar)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-simple-sidebar/blob/master/LICENSE)
*/
// 
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});


document.addEventListener('DOMContentLoaded', function () {
            const countries = ["Andorra", "Austria", "Belgium", "Bulgaria", "Bosnia and Herzegovina",
                "Belarus", "Switzerland", "Czech Republic", "Germany", "Denmark", "Estonia",
                "Finland", "United Kingdom", "Greece", "Croatia", "Hungary",
                "Ireland", "Iceland", "Italy", "Liechtenstein", "Lithuania", "Luxembourg",
                "Latvia", "Moldova", "Macedonia", "Montenegro", "Norway", "Poland",
                "Portugal", "Romania", "Serbia", "Slovakia", "Slovenia", "Sweden",
                "Ukraine", "Kosovo", "Netherlands", "Spain", "France", "Cyprus"];

            let targetCountry;
            let guessedCountries = [];
            let startTime;
            let score = 0;
            let gameStarted = false;

            function startTimer() {
                startTime = new Date().getTime();
                updateTimer();
            }

            function updateTimer() {
                const currentTime = new Date().getTime();
                const elapsedTime = currentTime - startTime;
                const minutes = Math.floor((elapsedTime % (1000 * 60 * 60)) / (1000 * 60));
                const seconds = Math.floor((elapsedTime % (1000 * 60)) / 1000);
                document.getElementById('timer').innerText = minutes + "m " + seconds + "s";
                setTimeout(updateTimer, 1000);
            }

            function chooseNextTargetCountry() {
                const remainingCountries = countries.filter(country => !guessedCountries.includes(country));
                if (remainingCountries.length === 0) {
                    console.log("Congratulations! You have guessed all the countries.");
                    return;
                }
                targetCountry = remainingCountries[Math.floor(Math.random() * remainingCountries.length)];
                updateTargetCountry(targetCountry); // Update HTML display
                startTimer(); // Start the timer when a new country is chosen
            }

            function updateTargetCountry(newTargetCountry) {
                document.getElementById('target-country').innerText = newTargetCountry;
            }

            document.getElementById("map-container").addEventListener("click", function (event) {
                if (event.target.classList.contains("country-path")) {
                    const clickedCountry = event.target.getAttribute("data-country");
                    if (clickedCountry === targetCountry) {
                        guessedCountries.push(clickedCountry);
                        const elapsedTimeInSeconds = Math.floor((new Date().getTime() - startTime) / 1000);
                        const points = Math.max(0, 10 - Math.floor(elapsedTimeInSeconds / 5)); // Adjust scoring logic as needed
                        score += points;
                        document.getElementById('score-value').innerText = score;
                        console.log("Congratulations! You guessed correctly in " + elapsedTimeInSeconds + " seconds and earned " + points + " points.");
                        chooseNextTargetCountry();
                    }
                }
            });

            document.getElementById("start-button").addEventListener("click", function () {
                if (!gameStarted) {
                    guessedCountries = []; // Reset guessed countries
                    score = 0; // Reset score
                    document.getElementById('score-value').innerText = score; // Update score display
                    chooseNextTargetCountry(); // Start the game when the button is clicked
                    gameStarted = true;
                    document.getElementById('start-button').innerText = 'Reset Game';
                } else {
                    gameStarted = false;
                    document.getElementById('start-button').innerText = 'Start Game';
                    document.getElementById('timer').innerText = '';
                    document.getElementById('score-value').innerText = '';
                    guessedCountries = [];
                    score = 0;
                }
            });
        });