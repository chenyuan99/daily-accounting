// Initialize charts when the document is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize bar chart
    const monthBarChart = echarts.init(document.getElementById('month-bar-chart'));
    const monthPieChart = echarts.init(document.getElementById('month-pie-chart'));

    // Bar chart options
    const barChartOptions = {
        title: {
            text: 'Monthly Income & Expenses',
            left: 'center'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        legend: {
            data: ['Income', 'Expenses'],
            top: '10%'
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            data: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        },
        yAxis: {
            type: 'value'
        },
        series: [
            {
                name: 'Income',
                type: 'bar',
                data: [],
                itemStyle: {
                    color: '#22c55e'
                }
            },
            {
                name: 'Expenses',
                type: 'bar',
                data: [],
                itemStyle: {
                    color: '#ef4444'
                }
            }
        ]
    };

    // Pie chart options
    const pieChartOptions = {
        title: {
            text: 'Expense Distribution',
            left: 'center'
        },
        tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
            orient: 'vertical',
            left: 10,
            top: 'middle'
        },
        series: [
            {
                name: 'Expenses',
                type: 'pie',
                radius: ['40%', '70%'],
                avoidLabelOverlap: false,
                itemStyle: {
                    borderRadius: 10,
                    borderColor: '#fff',
                    borderWidth: 2
                },
                label: {
                    show: false,
                    position: 'center'
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: '16',
                        fontWeight: 'bold'
                    }
                },
                labelLine: {
                    show: false
                },
                data: []
            }
        ]
    };

    // Set initial options
    monthBarChart.setOption(barChartOptions);
    monthPieChart.setOption(pieChartOptions);

    // Function to update chart data
    function updateCharts() {
        fetch('/api/charts/monthly-data/')
            .then(response => response.json())
            .then(data => {
                // Update bar chart data
                barChartOptions.series[0].data = data.monthly_income;
                barChartOptions.series[1].data = data.monthly_expenses;
                monthBarChart.setOption(barChartOptions);

                // Update pie chart data
                pieChartOptions.series[0].data = data.expense_categories;
                monthPieChart.setOption(pieChartOptions);
            })
            .catch(error => {
                console.error('Error fetching chart data:', error);
                showToast('Error', 'Failed to load chart data', 'error');
            });
    }

    // Update charts initially
    updateCharts();

    // Handle window resize
    window.addEventListener('resize', function() {
        monthBarChart.resize();
        monthPieChart.resize();
    });

    // Handle chart toggle button
    document.getElementById('show-charts').addEventListener('click', function() {
        updateCharts();
    });
});
