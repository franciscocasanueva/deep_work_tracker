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

function movingAvg(array, count, qualifier){

        // calculate average for subarray
        var avg = function(array, qualifier){

            var sum = 0, count = 0, val;
            for (var i in array){
                val = array[i];
                if (!qualifier || qualifier(val)){
                    sum += val;
                    count++;
                }
            }

            return sum / count;
        };

        var result = [], val;

        // pad beginning of result with 0 values
        for (var i=0; i < count-1; i++)
            result.push(0);

        // calculate average for each subarray and add to result
        for (var i=0, len=array.length - count; i <= len; i++){

            val = avg(array.slice(i, i + count), qualifier);
            if (isNaN(val))
                result.push(0);
            else
                result.push(val);
        }

        return result;
    }

function roll_sum_series(series, window) {
    var series = series
    var window = window
    var datasetsLen = series.length
    var rolled_series = [];

    // Roll all the different user series
    for (i=0; i < datasetsLen; i++)
        {
            var DataArray = series[i];
            rolled_series[i] = {
                label: DataArray['label'],
                dw_minutes: DataArray['dw_minutes'],
                x_day_average: movingAvg(DataArray['dw_minutes'], window, function(val){ return val != -1; }),
                x_labels: DataArray['x_labels']
            }
        }
    return rolled_series

}

function create_linechart(datasets, timeframe, ctx) {
        var datasets = datasets
        var GraphDatasetsArray = [];
        var datasetsLen = datasets.length

        for (i=0; i < datasetsLen; i++)
        {
            var DataArray = datasets[i];
            GraphDatasetsArray[i] = {
                label: DataArray['label'].slice(-timeframe),
                data: DataArray['x_day_average'].slice(-timeframe),
                fill: false,
                borderColor: googleColourPalette[i],
                backgroundColor: googleColourPalette[i],
                pointBackgroundColor: '#ffffff',
                lineTension: 0.4,
                pointRadius: 0,
            }
        }
        var lineChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: DataArray['x_labels'].slice(-timeframe),
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