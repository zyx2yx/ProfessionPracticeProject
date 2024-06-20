<script setup>
// import * as d3 from "d3";
// import * as echarts from 'echarts';
import { onMounted, reactive, ref, watch, onUpdated } from "vue";
import { storeToRefs } from "pinia";

import { reqParallelDataOfStudentOrClass } from '../api/index'

/* ...............................var....................................*/




let myChart;
let option;


/* ...............................var....................................*/

onMounted(async () => {
//   const chartDom = document.getElementById('ladar-chart');
//   myChart = echarts.init(chartDom,null,{renderer: 'svg'});
//   option && myChart.setOption(option);
});

// watch(selectTags, async (newVal, oldVal) => {


// });
</script>

<template>
  <div id="radar-chart" style="display: flex; justify-content: center; align-items: center;">
    <div>Radar Chart</div>
  </div>
</template>

<style scoped>
#radar-chart {
  width: 100%;
  height: 100%;
  font-size: 12px;
}

</style>
