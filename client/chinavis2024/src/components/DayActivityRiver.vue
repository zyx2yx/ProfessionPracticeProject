<script setup>
// import * as d3 from "d3";
import * as echarts from 'echarts';
import { onMounted, reactive, ref, watch, onUpdated } from "vue";
import { storeToRefs } from "pinia";

import { reqActivitySum } from '../api/index'
import { symbolType, colorConfig, chartIsExist } from '../configs/baseConfig'
import manageChartList from '../configs/chartConnect'

/* ...............................var....................................*/




let myChart;
let option;
// let symbolType = ['circle', 'rect', 'roundRect', 'triangle', 'diamond', 'pin', 'arrow', 'none'];
// let colorConfig = ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc'];
option = {
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'line',
      lineStyle: {
        color: 'rgba(0,0,0,0.2)',
        width: 1,
        type: 'solid'
      }
    }
  },
//   legend: {
//     // data: ['DQ', 'TY', 'SS', 'QG', 'SY', 'DD']
//   },
    // grid: {
    //     top: '0%',
    //     // left: '7%',
    //     // right: '5%',
    //     bottom: '10%',
    // },
//     title: {
//         left: 'left',
//         text: '提交活跃度',
//         // subtext: 'Fake data'
//   },
  singleAxis: {
    top: 0,
    bottom: 20,
    axisTick: {},
    axisLabel: {},
    type: 'time',
    formatter: (value) => value,
    axisPointer: {
      animation: true,
      label: {
        show: true
      }
    },
    splitLine: {
      show: true,
      lineStyle: {
        type: 'dashed',
        opacity: 0.2
      }
    }
  },
  series: [
    {
      type: 'themeRiver',
      emphasis: {
        itemStyle: {
          shadowBlur: 20,
          shadowColor: 'rgba(0, 0, 0, 0.8)'
        }
      },
      data: [
        // ['2015/11/08', 10, 'DQ'],
        // ['2015/11/26', 16, 'DQ'],
        // ['2015/11/27', 22, 'DQ'],
        // ['2015/11/28', 10, 'DQ'],
        // ['2015/11/08', 35, 'TY'],
        // ['2015/11/25', 30, 'TY'],
        // ['2015/11/26', 35, 'TY'],
        // ['2015/11/27', 42, 'TY'],
      ]
    }
  ]
};



/* ...............................var....................................*/

onMounted(async () => {
    const chartDom = document.getElementById('riverflow-chart');
    myChart = echarts.init(chartDom,null,{renderer: 'svg'});
    let res = await reqActivitySum();
    console.log('riverflow-chart.res_data:',res.res_data);
    option.series[0].data = res.res_data;
    option && myChart.setOption(option);
    
});

// watch(selectTags, async (newVal, oldVal) => {


// });
</script>

<template>
  <div id="riverflow-chart" style="display: flex; justify-content: center; align-items: center;">
    <!-- <div>riverflow Chart</div> -->
  </div>
</template>

<style scoped>
#riverflow-chart {
  width: 100%;
  height: 100%;
  font-size: 12px;
}

</style>
