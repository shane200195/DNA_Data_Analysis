function graphs(choice, data, y_label){
    if (choice == 'ACTG Count') {
        var set = 'DNA_Count';
        create_bar_graph(Object.keys(data[set]), Object.values(data[set]), y_label);
    }
    if (choice == 'DNA Motif') {
        var set = 'DNA_motif_combo';
        create_bar_graph(Object.keys(data[set]), Object.values(data[set]), y_label);
    }
}

function create_bar_graph(graph_x_labels, graph_data, graph_y_label){
    var ctx = document.getElementById('myChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: graph_x_labels,
            datasets: [{
                label: graph_y_label,
                data: graph_data,
                backgroundColor:'rgb(0,0,0)',
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}