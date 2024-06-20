<script setup>
// import * as d3 from "d3";
import * as echarts from 'echarts';
import { onMounted, reactive, ref, watch, onUpdated } from "vue";
import { storeToRefs } from "pinia";

import { reqAnswerStatus } from '../api/index'

/* ...............................var....................................*/




let myChart;
let option;
option = {
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow'
    }
  },
  legend: {
    type: 'scroll',
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: [
    {
      type: 'value'
    }
  ],
  yAxis: [
    {
      type: 'category',
      data: [], // 待获取
      axisLabel: {
        formatter: function (value, _) {
          if (value === 'Absolutely_Correct') {
            return 'AC';
          } else if (value === 'Absolutely_Error') {
            return 'AE';
          } else if (value === 'Partially_Correct') {
            return 'PC';
          } else {
            // 返回E+最后一个数字
            return 'E'+value[value.length-1];
          }
        }
      }
    }
  ],
  series: [] // 待获取
};


/* ...............................var....................................*/

onMounted(async () => {
    const chartDom = document.getElementById('state-chart');
    myChart = echarts.init(chartDom,null,{renderer: 'svg'});
    let response_data = await reqAnswerStatus('zhx5rxgopln1p5hd10ql', 'm3D1v');
    option.yAxis[0].data = response_data.yAxis;
    option.series = response_data.res_data;
    option && myChart.setOption(option);
});

// watch(selectTags, async (newVal, oldVal) => {


// });
</script>

<template>
  <div id="state-chart" style="display: flex; justify-content: center; align-items: center;">
    <!-- <div>State Chart</div> -->
  </div>
</template>

<style scoped>
#state-chart {
  width: 100%;
  height: 100%;
  font-size: 12px;
}

</style>
