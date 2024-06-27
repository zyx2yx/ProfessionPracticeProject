<script setup>
// import * as d3 from "d3";
import * as echarts from 'echarts';
import { onMounted, reactive, ref, watch, onUpdated } from "vue";
import { storeToRefs } from "pinia";

import { reqKnowledgeLevel } from '../api/index'
import { symbolType, colorConfig, chartIsExist } from '../configs/baseConfig'
import manageChartList from '../configs/chartConnect'
// import ecSimpleTransform from '../configs/ecSimpleTransform.min.js'; // not working
// import * as ecSimpleTransform from '../configs/ecSimpleTransform.min.js'; // not working
// import * as ecSimpleTransform from '../configs/ecSimpleTransform.js'; // not working
import '../configs/ecSimpleTransform.js'; // # working
// import { aggregate } from '../configs/ecSimpleTransform.min.js'; // not working

/* ...............................var....................................*/


// 首先要注册外部数据转换器。
console.log('ecSimpleTransform:', ecSimpleTransform.aggregate);
echarts.registerTransform(ecSimpleTransform.aggregate);

let myChart;
let option;
option = {
  title: [
    {
      text: '知识掌握程度',
      left: 'left',
      fontSize: 10,
    },
    // {
    //   text: 'upper: Q3 + 1.5 * IQR \nlower: Q1 - 1.5 * IQR',
    //   borderColor: '#999',
    //   borderWidth: 1,
    //   textStyle: {
    //     fontWeight: 'normal',
    //     fontSize: 14,
    //     lineHeight: 20
    //   },
    //   left: '10%',
    //   top: '90%'
    // }
  ],
  dataset: [
    {
      // prettier-ignore
      dimensions: [],
      source: [],
      id: 'scatter_data'
    },
    {
        id: 'boxplot_data',
        fromDatasetId: 'scatter_data',
        transform: [
            {
            type: 'ecSimpleTransform:aggregate',
            config: {
                resultDimensions: [
                { name: 'min', from: 'kg_level', method: 'min' },
                { name: 'Q1', from: 'kg_level', method: 'Q1' },
                { name: 'median', from: 'kg_level', method: 'median' },
                { name: 'Q3', from: 'kg_level', method: 'Q3' },
                { name: 'max', from: 'kg_level', method: 'max' },
                { name: 'cluster', from: 'cluster' }
                ],
                groupBy: 'cluster'
            }
            },
            {
            type: 'sort',
            config: {
                dimension: 'Q3',
                order: 'asc'
            }
            }
        ]
    }
  ],
//   tooltip: {
//     trigger: 'item',
//     axisPointer: {
//       type: 'shadow'
//     }
//   },
tooltip: {
      trigger: 'axis',
      confine: true
    },
    xAxis: {
      name: 'kg_level',
      nameLocation: 'middle',
      nameGap: 30,
      scale: true
    },
    yAxis: {
      type: 'category'
    },
    grid: {
      bottom: 20
    },
    legend: {
      selected: { detail: false }
    },
    series: [
      {
        name: 'boxplot',
        type: 'boxplot',
        datasetId: 'boxplot_data',
        itemStyle: {
          color: '#b8c5f2'
        },
        encode: {
          x: ['min', 'Q1', 'median', 'Q3', 'max'],
          y: 'cluster',
          itemName: ['cluster'],
          tooltip: ['min', 'Q1', 'median', 'Q3', 'max']
        }
      },
      {
        name: 'detail',
        type: 'scatter',
        datasetId: 'scatter_data',
        symbolSize: 6,
        tooltip: {
          trigger: 'item'
        },
        label: {
          show: true,
          position: 'top',
          align: 'left',
          verticalAlign: 'middle',
          rotate: 90,
          fontSize: 12
        },
        itemStyle: {
          color: '#d00000'
        },
        encode: {
          x: 'kg_level',
          y: 'cluster',
          label: 'kg_level',
          itemName: 'kg_level',
          tooltip: ['cluster', 'kg_level']
        }
      }
    ]
  };


/* ...............................var....................................*/

onMounted(async () => {
    // // 创建script元素
    // const script = document.createElement("script");
    // // 设置script元素的src属性为外部JS脚本的URL
    // script.src = 'https://fastly.jsdelivr.net/npm/echarts-simple-transform/dist/ecSimpleTransform.min.js';
    // // 将script元素添加到head标签中
    // document.head.appendChild(script);


    const chartDom = document.getElementById('scoreboxplot-chart');
    myChart = echarts.init(chartDom,null,{renderer: 'svg'});
    let res = await reqKnowledgeLevel();
    console.log('scoreboxplot-chart.res_data:',res.res_data);
    option.dataset[0].dimensions = res.res_data.columns;
    option.dataset[0].source = res.res_data.values;
    

    option && myChart.setOption(option);
    
});

// watch(selectTags, async (newVal, oldVal) => {


// });
</script>

<template>
  <div id="scoreboxplot-chart" style="display: flex; justify-content: center; align-items: center;">
    <!-- <div>riverflow Chart</div> -->
  </div>
</template>

<style scoped>
#scoreboxplot-chart {
  width: 100%;
  height: 100%;
  font-size: 12px;
}

</style>
