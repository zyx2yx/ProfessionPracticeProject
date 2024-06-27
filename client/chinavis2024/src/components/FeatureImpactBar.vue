<script setup>
// import * as d3 from "d3";
import * as echarts from 'echarts';
import { onMounted, reactive, ref, watch, onUpdated } from "vue";
import { storeToRefs } from "pinia";

import { reqFeatureImpact } from '../api/index'
import { symbolType, colorConfig, chartIsExist } from '../configs/baseConfig'
import manageChartList from '../configs/chartConnect'

/* ...............................var....................................*/




let myChart;
let option;
option = {
  title: {
    text: '特征影响力'
  },
//   legend: {
//     data: ['bar', 'bar2']
//   },
//   toolbox: {
//     // y: 'bottom',
//     feature: {
//       magicType: {
//         type: ['stack']
//       },
//       dataView: {},
//       saveAsImage: {
//         pixelRatio: 2
//       }
//     }
//   },
  tooltip: {},
  xAxis: {
    data: [], // 待填充
    splitLine: {
      show: false
    }
  },
  yAxis: {},
  series: [
    {
      name: 'bar',
      type: 'bar',
      data: [], // 待填充
      emphasis: {
        focus: 'series'
      },
      animationDelay: function (idx) {
        return idx * 10;
      }
    },
  ],
  animationEasing: 'elasticOut',
  animationDelayUpdate: function (idx) {
    return idx * 5;
  }
};



/* ...............................var....................................*/

onMounted(async () => {
    const chartDom = document.getElementById('featureimpact-chart');
    myChart = echarts.init(chartDom,null,{renderer: 'svg'});
    let res = await reqFeatureImpact();
    console.log('featureimpact-chart.res_data:',res.res_data);

    option.xAxis.data = res.res_data.xaxislabels; // x轴值
    option.series[0].data = res.res_data.cofficients; // y轴值

    option && myChart.setOption(option);
    
});

// watch(selectTags, async (newVal, oldVal) => {


// });
</script>

<template>
  <div id="featureimpact-chart" style="display: flex; justify-content: center; align-items: center;">
    <!-- <div>riverflow Chart</div> -->
  </div>
</template>

<style scoped>
#featureimpact-chart {
  width: 100%;
  height: 100%;
  font-size: 12px;
}

</style>
