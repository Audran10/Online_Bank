const circular_graph = document.getElementById('circular-graph').getContext('2d');

let myChart = new Chart(circular_graph, {
    type: 'doughnut',
    data: {
        labels: ["Red", "Blue", "Yellow"],
        datasets: [
            {
            label: "My First dataset",
            data: [12, 19, 3],
            backgroundColor: [
                red, blue, yellow
            ],
            },
        ],
    },
});