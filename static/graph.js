function HideOthersButtons() {
    const currentAccountBtn = document.querySelector('.current-account-btn');
    const epargneAccounts = document.querySelectorAll('.epargne-account');
    const text = document.querySelectorAll('#affichage');
    const cards = document.querySelectorAll('.card');

    // Changer le bouton "Compte Courant" en croix
    currentAccountBtn.innerHTML = '<';
    currentAccountBtn.classList.remove('current-account-btn');
    currentAccountBtn.classList.add('close-button');

    // Cacher les autres boutons
    epargneAccounts.forEach((btn) => {
        btn.style.display = 'none';
    });

    // Cacher les différents textes
    text.forEach((text) => {
        text.style.display = 'none';
    });

    // Afficher les div avec la classe "card"
    cards.forEach((card) => {
        card.style.display = 'inline-block';
    });

    // Ajouter un écouteur d'événement sur le bouton "Compte Courant" pour restaurer l'état initial
    currentAccountBtn.removeEventListener('click', HideOthersButtons);
    currentAccountBtn.addEventListener('click', ShowOthersButtons);
}

function ShowOthersButtons() {
    const currentAccountBtn = document.querySelector('.close-button');
    const epargneAccounts = document.querySelectorAll('.epargne-account');
    const cards = document.querySelectorAll('.card');
    const text = document.querySelectorAll('#affichage');

    // Changer le bouton "Compte Courant" en son état initial
    currentAccountBtn.innerHTML = 'Compte Courant';
    currentAccountBtn.classList.remove('close-button');
    currentAccountBtn.classList.add('current-account-btn');

    // Afficher les autres boutons
    epargneAccounts.forEach((btn) => {
        btn.style.display = 'inline-block';
    });

    // Afficher les différents textes
    text.forEach((text) => {
        text.style.display = 'block';
    });

    // Cacher les div avec la classe "card"
    cards.forEach((card) => {
        card.style.display = 'none';
    });

    // Ajouter un écouteur d'événement sur le bouton "Compte Courant" pour cacher les autres boutons
    currentAccountBtn.removeEventListener('click', ShowOthersButtons);
    currentAccountBtn.addEventListener('click', HideOthersButtons);
}

// Ajouter un écouteur d'événement sur le bouton "Compte Courant" pour cacher les autres boutons
const currentAccountBtn = document.querySelector('.current-account-btn');
currentAccountBtn.addEventListener('click', HideOthersButtons);



const circular_graph = document.getElementById('circular-graph').getContext('2d');
let credits = document.getElementById('circular-graph').getAttribute('credits');
let debits = document.getElementById('circular-graph').getAttribute('debits');
let percentage = (debits / credits) * 100;
console.log(credits)


let myChart = new Chart(circular_graph, {
    type: 'doughnut',
    data: {
        labels: ["Credits", "Debits"],
        datasets: [
            {
            label: "Monthly income spent",
            data: [credits, debits],
            backgroundColor: [
                'rgb(22, 184, 78)',
                'rgb(102, 204, 153)'
            ],
            cutout: '70%',
            },
        ],
    },
});

const line_graph = document.getElementById('line-graph').getContext('2d');
let credits_for_year = JSON.parse(document.getElementById('line-graph').getAttribute('credits_for_year'));
let debits_for_year = JSON.parse(document.getElementById('line-graph').getAttribute('debits_for_year'));

let lineChart = new Chart(line_graph, {
    type: 'line',
    data: {
        labels: ["January", "February", "March", "April", "May", "June", "July", "August", "September","October","November","December"],
        datasets: [
            {
                label: "Monthly income",
                data: credits_for_year,
                borderColor: [
                    'rgb(22, 184, 78)',
                ],
            },
            {
                label: "Monthly expenses",
                data: debits_for_year,
                borderColor: [
                    '#ec644b',
                ],
            },
        ],
    },
});
