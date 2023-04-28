const circular_graph = document.getElementById('circular-graph').getContext('2d');
let credits = document.getElementById('circular-graph').getAttribute('credits');
let debits = document.getElementById('circular-graph').getAttribute('debits');
let percentage = (debits / credits) * 100;


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


var transactions = document.querySelectorAll('.row.justify-content-between');

// Fonction pour afficher toutes les transactions
function showAllTransactions() {
    console.log('show all transactions');
    for (var i = 0; i < transactions.length; i++) {
        transactions[i].style.display = 'flex';
    }
}

// Fonction pour afficher les transactions correspondant au type d'opération spécifié
function showTransactions(operationType) {
    console.log('show transactions of type ' + operationType);
    for (var i = 0; i < transactions.length; i++) {
        if (transactions[i].getAttribute('operation-type') == operationType) {
            transactions[i].style.display = 'flex';
        } else {
            transactions[i].style.display = 'none';
        }
    }
}

