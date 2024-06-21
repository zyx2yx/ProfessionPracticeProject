<script setup>
// import * as d3 from "d3";
import * as echarts from 'echarts';
import { onMounted, reactive, ref, watch, onUpdated } from "vue";
import { storeToRefs } from "pinia";

import { reqActivity } from '../api/index'

/* ...............................var....................................*/




let myChart;
let option;

function getVirtualData(year) {
  const date = +echarts.time.parse(year + '-08-31');
  const end = +echarts.time.parse(+year + 1 + '-01-25');
  const dayTime = 3600 * 24 * 1000;
  const data = [];
  for (let time = date; time < end; time += dayTime) {
    data.push([
      echarts.time.format(time, '{yyyy}-{MM}-{dd}', false),
      Math.floor(Math.random() * 10000)
    ]);
  }
  return data;
}

option = {
  title: {
    top: 15,
    left: 'center',
    text: '学生活跃度'
  },
  tooltip: {},
  visualMap: {
    min: 0,
    max: 10,
    type: 'continuous',
    orient: 'horizontal',
    left: 'center',
    top: 50,
    inRange:{
      color: ['#ebedf0', '#216e39']
    }
  },
  calendar: {
    top: 120,
    left: 30,
    right: 30,
    cellSize: 15,
    range: ['2023-8-31', '2024-1-25'],
    itemStyle: {
      borderWidth: 0.5
    },
    splitLine:{
      show: true,
      lineStyle: {
        color: '#000',
        width: 1,
        type: 'dashed'
      }
    },
    yearLabel: { show: false },
    monthLabel: { nameMap: 'ZH' },
    dayLabel: { nameMap: 'ZH' }
  },
  series: {
    type: 'heatmap',
    coordinateSystem: 'calendar',
    // data: getVirtualData('2023'),
    data: [],
    // itemStyle: {
    //   color: '#216e39'
    // }
  }
};

/* ...............................var....................................*/

onMounted(async () => {
  const chartDom = document.getElementById('heatmap-chart');
  myChart = echarts.init(chartDom,null,{renderer: 'svg'});
  let response_data = await reqActivity('zhx5rxgopln1p5hd10ql');
  option.series.data = response_data.res_data;
  option && myChart.setOption(option);
});

// watch(selectTags, async (newVal, oldVal) => {


// });
</script>

<template>
  <div id="heatmap-chart">
  </div>
</template>

<style scoped>
#heatmap-chart {
  width: 100%;
  height: 100%;
  font-size: 12px;
}

</style>
