function loadSessionRequestForm(index) {
    var editButton = document.getElementById('editSessionButton'+index);
    var editForm = document.getElementById('editRequest'+index);
    editButton.style.display = 'none';
    editForm.style.display = 'inline';
}

function LightenColor(color, percent) {
    var num = parseInt(color.replace("#",""),16),
    amt = Math.round(2.55 * percent),
    R = (num >> 16) + amt,
    B = (num >> 8 & 0x00FF) + amt,
    G = (num & 0x0000FF) + amt;

    return "#" + (0x1000000 + (R<255?R<1?0:R:255)*0x10000 + (B<255?B<1?0:B:255)*0x100 + (G<255?G<1?0:G:255)).toString(16).slice(1);
}

function create_linechart(datasets, labels, ctx) {
        var datasets = datasets
        var GraphDatasetsArray = [];
        var datasetsLen = datasets.length

        for (i=0; i < datasetsLen; i++)
        {
            var DataArray = datasets[i];
            GraphDatasetsArray[i] = {
                label: DataArray['label'],
                data: DataArray['x_day_average'],
                fill: false,
                borderColor: googleColourPalette[i],
                backgroundColor: googleColourPalette[i],
                pointBackgroundColor: '#ffffff',
                lineTension: 0.4,
            }
        }

        var lineChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: GraphDatasetsArray
            },
            options: {
                responsive: true,
                scales: {
                    y: {beginAtZero:true}
                },
                plugins:{
                    legend:{
                        position: 'right'
                    }
                }
            }
        });
        return lineChart
    }