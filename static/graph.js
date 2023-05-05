var list_accounts = JSON.parse(document.getElementById('accounts').getAttribute('accounts_list'));
for (var i = 0; i < list_accounts.length; i++){
    var btn = document.createElement("button");
    btn.setAttribute("id", "current-account-btn" + i);
    btn.classList.add("current-account-btn");
    btn.addEventListener("click", function(event) {
        toggleButton(event.target);
        hideOtherButtons(event.target);
    });
    btn.innerHTML = list_accounts[i].name;
    btn.setAttribute("name", list_accounts[i].name);
    document.getElementById("accounts").appendChild(btn);
}

function toggleButton(button) {
    initial_name = button.getAttribute("name");
    if (button.classList.contains("current-account-btn")) {
        button.classList.remove("current-account-btn");
        button.classList.add("close-button");
        var good_account = list_accounts.find(function(account) {
            return account.name === initial_name;
        });
        document.getElementById("show_solde").innerHTML = good_account.solde + " €";
        if (good_account.monthly_saving == null) {
            document.getElementById("show_monthly_saving").innerHTML = "0 €";
        } else {
            document.getElementById("show_monthly_saving").innerHTML = good_account.monthly_saving + " €";
        }
        myChart.data.datasets[0].data[0] = good_account.credits;
        myChart.data.datasets[0].data[1] = good_account.debits;
        myChart.update();

        lineChart.data.datasets[0].data = good_account.credits_for_year;
        lineChart.data.datasets[1].data = good_account.debits_for_year;
        lineChart.update();
        button.innerHTML = "X";
    } else {
        button.classList.remove("close-button");
        button.classList.add("current-account-btn");
        button.innerHTML = initial_name;
    }
}

let card_remove = true;
function hideOtherButtons(clickedButton) {
    const buttons = document.querySelectorAll('.current-account-btn');
    if (card_remove) {
        for (let i = 0; i < buttons.length; i++) {
            if (buttons[i] !== clickedButton) {
                buttons[i].style.display = 'none';
            }
        }
    } else {
        for (let i = 0; i < buttons.length; i++) {
            if (buttons[i] !== clickedButton) {
                buttons[i].style.display = 'inline-block';
            }
        }
    }
}


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


const buttons = document.querySelectorAll('.current-account-btn');
const cards = document.getElementsByClassName('card');

for (let i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener('click', function() {
        if (card_remove) {
            for (let i = 0; i < cards.length; i++) {
                cards[i].style.display = 'block';
            }
            myChart.reset();
            lineChart.reset();
            myChart.update();
            lineChart.update();
            card_remove = false;
        } else {
            for (let i = 0; i < cards.length; i++) {
                cards[i].style.display = 'none';
            }
            myChart.reset();
            lineChart.reset();
            myChart.update();
            lineChart.update();
            card_remove = true;
        }
    });
}
