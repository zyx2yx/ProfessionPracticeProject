<script setup>
// import * as d3 from "d3";
import * as echarts from 'echarts';
import { onMounted, reactive, ref, watch, onUpdated } from "vue";
import { storeToRefs } from "pinia";

// import * as echarts from 'echarts/core';
// import { ParallelComponent } from 'echarts/components';
// import { ParallelChart } from 'echarts/charts';
// import { SVGRenderer } from 'echarts/renderers';
// import { BrushComponent } from "echarts/components";

import { useSelectClassStore } from "../stores/selectClass";
import { ParallelDataOfStudentOrClass } from '../api/index'

// echarts.use([ParallelComponent, ParallelChart, SVGRenderer, BrushComponent]);

/* ...............................var....................................*/
const { selectTags } = storeToRefs(useSelectClassStore());

let option = {
  brush: {
        brushLink: 'all',
        brushMode:'multiple',// ?想要在同一坐标轴刷选多个地方，但是不生效
        toolbox: ['clear'],
        xAxisIndex: 'all,',
        yAxisIndex: 'all,',
        inBrush: {
            opacity: 1,
        },
        throttleType: 'debounce',
        throttleDelay: 500,
        // brushMode:'single',
        // removeOnClick:true,
  },
  tooltip: { // 提示框
    padding: 5,
    backgroundColor: '#fff',
    borderColor: '#fff',
    borderWidth: 1,
    textStyle: {
        color: '#000',
        fontSize: 12,
    },
    formatter: function (params) {
        return 'Price: ' + params.data[0] + '<br/>'
            + 'Net Weight: ' + params.data[1] + '<br/>'
            + 'Amount: ' + params.data[2] + '<br/>'
            + 'Score: ' + params.data[3];
    }
  },
  // toolbox: { // 工具框
  //     top: 10,
  //     right: 10,
  //     itemSize: 20,
  //     feature: {
  //         // mytool1: {
  //         //     show: true,
  //         //     title: "显示核心资产",
  //         //     icon: 'path://M432.45,595.444c0,2.177-4.661,6.82-11.305,6.82c-6.475,0-11.306-4.567-11.306-6.82s4.852-6.812,11.306-6.812C427.841,588.632,432.452,593.191,432.45,595.444L432.45,595.444z M421.155,589.876c-3.009,0-5.448,2.495-5.448,5.572s2.439,5.572,5.448,5.572c3.01,0,5.449-2.495,5.449-5.572C426.604,592.371,424.165,589.876,421.155,589.876L421.155,589.876z M421.146,591.891c-1.916,0-3.47,1.589-3.47,3.549c0,1.959,1.554,3.548,3.47,3.548s3.469-1.589,3.469-3.548C424.614,593.479,423.062,591.891,421.146,591.891L421.146,591.891zM421.146,591.891',
  //         //     onclick: function () {
  //         //         // 获取区域中选中的点，请求这几点构成的连通图，然后存入subGraphStore中
  //         //         // updataPoints(selectedIdArr)
  //         //         console.log('点击显示核心资产');
  //         //     }
  //         // },
  //     }
  // },
  parallelAxis: [
    { dim: 0, name: 'Score' },
    { dim: 1, name: 'Learn Hours' },
    { dim: 2, name: 'Learn Days' },
    { dim: 3, name: 'Avg Complete' },
    { dim: 4, name: 'Avg Correct' },
    { dim: 5, name: 'Avg Attempts' },
    { dim: 6, name: 'Best Time', type: 'category', 
      data: [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]},
    { dim: 7, name: 'Most State', type: 'category', 
      data: ['Absolutely_Correct', 'Absolutely_Error', 'Partially_Correct','Error1', 
      'Error2', 'Error3', 'Error4','Error5', 'Error6','Error7', 'Error8', 'Error9']},
    { dim: 8, name: 'Most Method', type: 'category', 
    data: ['Method_Cj9Ya2R7fZd6xs1q5mNQ', 'Method_gj1NLb4Jn7URf9K2kQPd',
 'Method_5Q4KoXthUuYz3bvrTDFm', 'Method_m8vwGkEZc3TSW2xqYUoR',
 'Method_BXr9AIsPQhwNvyGdZL57']},
  ],
  series: {
    type: 'parallel',
    lineStyle: {
      width: 1
    },
    data: [
      [12.99, 100, 82, 'Good'],
      [9.99, 80, 77, 'OK'],
      [20, 120, 60, 'Excellent']
    ]
  },
  parallel: {
        top: '20%',
        left: '5%',
        right: '20%',
        bottom: '5%',
    },
};

/* ...............................var....................................*/

onMounted(async () => {
  const chartDom = document.getElementById('parallel-chart');
  const myChart = echarts.init(chartDom,null,{renderer: 'svg'});
  let response_data = await ParallelDataOfStudentOrClass([], selectTags.value, '_starttime','_endtime');
  option.series.data = response_data.res_list_data;
  option && myChart.setOption(option);
});

</script>

<template>
  <div id="parallel-chart">
  </div>
</template>

<style scoped>
#parallel-chart {
  width: 100%;
  height: 100%;
  font-size: 12px;
}

</style>
