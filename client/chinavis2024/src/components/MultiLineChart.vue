<script setup>
// import * as d3 from "d3";
import * as echarts from 'echarts';
import { onMounted, reactive, ref, watch, onUpdated } from "vue";
import { storeToRefs } from "pinia";

import { reqAttemptAndCorrect } from '../api/index'
import { symbolType, colorConfig, chartIsExist } from '../configs/baseConfig'
import manageChartList from '../configs/chartConnect'
import { max } from 'd3';

/* ...............................var....................................*/




let myChart;
let option;
option = {
//   title: {
//     text: '尝试次数与正确率',
//     left: 'left'
//   },
//   grid: [{
//     bottom: 20,
//     top: 30,
//     left: 30,
//     right: 30
//   }],
//   toolbox: {
//     feature: {
//       dataZoom: {
//         yAxisIndex: 'none'
//       },
//       restore: {},
//       saveAsImage: {}
//     }
//   },
grid: [
    {
      left: 40,
      right: 15,
      top: 30,
      height: '35%'
    },
    {
      left: 40,
      right: 15,
      top: '55%',
      height: '35%'
    }
  ],
  axisPointer: {
    link: [
      {
        xAxisIndex: 'all'
      }
    ]
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'cross',
      animation: false,
      label: {
        backgroundColor: '#505765'
      }
    }
  },
  legend: {
    // data: ['Flow', 'Rainfall'],
    // left: 10,
    selectedMode: 'single',
    // selectedMode: 'multiple',
    // icon: 'none',
  },
  xAxis: [  
    {
      type: 'category',
      boundaryGap: false,
      axisLine: { onZero: false },
      // prettier-ignore
      data: [], // 待获取
      axisLabel: {
            show: false,
        }
    },
    {
      gridIndex: 1,
      type: 'category',
      boundaryGap: false,
      axisLine: { onZero: true },
      data: [] ,// 待获取,
      position: 'top',
        axisLabel: {
            show: false,
        }
    }
  ],
  yAxis: [
    {
      name: '平均尝试次数',
      type: 'value',
      max: 40,
    },
    {
        gridIndex: 1,
      name: '平均正确率',
      nameLocation: 'start',
      alignTicks: true,
      type: 'value',
      inverse: true,
      min: 0,
      max: 1,
    }
  ],
  series: []
};



/* ...............................var....................................*/

onMounted(async () => {
    const chartDom = document.getElementById('multiline-chart');
    myChart = echarts.init(chartDom,null,{renderer: 'svg'});
    let res = await reqAttemptAndCorrect();
    console.log('multiline-chart.res_data:',res.res_data);

    option.xAxis[0].data = res.res_data.title; // x轴值
    option.xAxis[1].data = res.res_data.title; // x轴值
    let attempts_list = res.res_data.attempts.data;
    let attempts_idx = res.res_data.attempts.index;
    let correct_list = res.res_data.correct.data;
    let correct_idx = res.res_data.correct.index;

    for (let i = 0; i < attempts_idx.length; i++) {
        option.series.push({
            name: `Cluster ${attempts_idx[i]}`,
            type: 'line',
            yAxisIndex: 0,
            lineStyle: {
                width: 1,
            },
            symbol: 'circle',
            emphasis: {
                focus: 'series'
            },
            data: attempts_list[i]
        })
    }
    for(let i = 0; i < correct_idx.length; i++) {
        option.series.push({
            name: `Cluster ${correct_idx[i]}`,
            type: 'line',
            xAxisIndex: 1,
            yAxisIndex: 1,
            lineStyle: {
                width: 1,
                type: 'dashed'
            },
            // symbol: 'none',
            symbol: 'triangle',
            emphasis: {
                focus: 'series'
            },
            data: correct_list[i]
        })
    }
    option && myChart.setOption(option);
    
});

// watch(selectTags, async (newVal, oldVal) => {


// });
</script>

<template>
  <div id="multiline-chart" style="display: flex; justify-content: center; align-items: center;">
    <!-- <div>riverflow Chart</div> -->
  </div>
</template>

<style scoped>
#multiline-chart {
  width: 100%;
  height: 100%;
  font-size: 12px;
}

</style>
