// Desc: Chart connection configuration
const chartList = []
const manageChartList = {
    getValue: function () {
        return chartList
    },
    appendValue: function (chart) {
        chartList.push(chart)
    },
}

export default manageChartList