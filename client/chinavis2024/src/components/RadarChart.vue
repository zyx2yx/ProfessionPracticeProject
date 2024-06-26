<script setup>
// import * as d3 from "d3";
import * as echarts from 'echarts';
import { onMounted, reactive, ref, watch, onUpdated } from "vue";
import { storeToRefs } from "pinia";

import { reqCluster } from '../api/index'
import { bin, text } from 'd3';
import { symbolType, colorConfig, chartIsExist } from '../configs/baseConfig'
import manageChartList from '../configs/chartConnect'

/* ...............................var....................................*/




let myChart;
let option;
// let symbolType = ['circle', 'rect', 'roundRect', 'triangle', 'diamond', 'pin', 'arrow', 'none'];
// let colorConfig = ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc'];
   
option = {
  // color: ['#67F9D8', '#FFE434', '#56A3F1', '#FF917C', '#FF5D5D', '#FFC0CB', '#FFA07A' ],
  color: ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc'],
  title: {
    text: '学生行为模式'
  },
  legend: {
    data : [],
    // top: '5%',
    textStyle: {
      fontSize:10,
    },
    itemWidth: 10,
    itemHeight: 10,
    orient: 'vertical',
    itemGap: 25,
    right: '3%',
    top: '30%',
  },
  radar: [
    {
      indicator: [
        { text: 'Indicator1' },
        { text: 'Indicator2' },
        { text: 'Indicator3' },
        { text: 'Indicator4' },
        { text: 'Indicator5' }
      ],
      center: ['45%', '50%'],
      radius: 170,
      startAngle: 90,
      splitNumber: 4,
      shape: 'polygon',
      // axisName: {
      //   formatter: '【{value}】',
      //   color: '#428BD4'
      // },
      axisName: {
        color: '#fff',
        backgroundColor: '#666',
        borderRadius: 3,
        padding: [3, 5]
      }
      // splitArea: {
      //   areaStyle: {
      //     color: ['#77EADF', '#26C3BE', '#64AFE9', '#428BD4'],
      //     shadowColor: 'rgba(0, 0, 0, 0.2)',
      //     shadowBlur: 10
      //   }
      // },
      // axisLine: {
      //   lineStyle: {
      //     color: 'rgba(211, 253, 250, 0.8)'
      //   }
      // },
      // splitLine: {
      //   lineStyle: {
      //     color: 'rgba(211, 253, 250, 0.8)'
      //   }
      // }
    },
  ],
  series: [
    {
      type: 'radar',
      emphasis: {
        lineStyle: {
          width: 5
        },
        focus: 'self'
      },
      data: [
        // {
        //   value: [100, 8, 0.4, -80, 2000],
        //   name: 'Data A',
        //   symbol: 'rect',
        //   symbolSize: 12,
        //   label: {
        //     show: true,
        //     formatter: function (params) {
        //       return params.value;
        //     }
        //   }
        // },
        // {
        //   value: [60, 5, 0.3, -100, 1500],
        //   name: 'Data B',
        //   areaStyle: {
        //     color: 'rgba(255, 228, 52, 0.6)'
        //   },
        //   lineStyle: {
        //     type: 'dashed'
        //   },
        //   areaStyle: {
        //     color: new echarts.graphic.RadialGradient(0.1, 0.6, 1, [
        //       {
        //         color: 'rgba(255, 145, 124, 0.1)',
        //         offset: 0
        //       },
        //       {
        //         color: 'rgba(255, 145, 124, 0.9)',
        //         offset: 1
        //       }
        //     ])
        //   }
        // }
      ]
    },
  ]
};

function bindEvent(myChart) {
  // myChart.on('hihglight', function (params) {
  //   console.log('something light',params);
  // }) // 无效
  // myChart.on('legendselectchanged', function (params) {
  //   console.log('legendselectchanged',params);
  // }) // 点击有效
  // myChart.on('legendselected', function (params) {
  //   console.log('legendselected',params);
  // }) // 点击有效
  let tsnechart
  console.log('mychart:',myChart);
  console.log('tsnechart:',tsnechart);
  myChart.on('mouseover', function (params) { 
    
    tsnechart = manageChartList.getValue().find(chart => chart.id !== myChart.id);
    tsnechart.dispatchAction({
      type: 'highlight',
      // seriesIndex: params.seriesIndex,
      seriesName: params.name,
      // dataIndex: params.dataIndex
    });
    console.log('mouseover:',params);
  })
  .on('mouseout', function (params) {
    tsnechart.dispatchAction({
      type: 'downplay',
      seriesName: params.name,
      // seriesIndex: params.seriesIndex,
      // dataIndex: params.dataIndex
    });
  });
}




/* ...............................var....................................*/

onMounted(async () => {
  const chartDom = document.getElementById('radar-chart');
  myChart = echarts.init(chartDom,null,{renderer: 'svg'});
  let res = await reqCluster();
  // console.log('res.res_data:',res.res_data);
  option.radar[0].indicator = res.res_data.indicator;
  let { cluster_ids, method2code, cluster_data }  = res.res_data;

  for (let i = 0; i < cluster_ids.length; i++) {
    option.series[0].data[i] = {
          value: cluster_data[i],
          name: `Cluster ${cluster_ids[i]}`,
          // symbol: i%2 == 0 ? 'rect' : 'circle',
          symbol: symbolType[cluster_ids[i]],
          itemstyle: {
            color: colorConfig[cluster_ids[i]]
          },
          areaStyle: {
            color: new echarts.graphic.RadialGradient(0.1, 0.7, 1, [
              {
                color: 'rgba(255, 255, 255, 0.1)',
                offset: 0
              },
              {
                color: colorConfig[cluster_ids[i]],
                offset: 1
              }
            ])
          }
          // symbolSize: 12,
          // label: {
          //   show: true,
          //   formatter: function (params) {
          //     return params.value;
          //   }
          // }]
    }
    option.legend.data[i] = {
      name: `Cluster ${cluster_ids[i]}`,
      icon: symbolType[cluster_ids[i]],
      textStyle: {
        color: colorConfig[cluster_ids[i]]
      }
    };
  }

  option && myChart.setOption(option);
  if(!chartIsExist(manageChartList.getValue(), myChart.id)) {
    manageChartList.appendValue(myChart);
  }
  
  // if(manageChartList.getValue().length > 1) {
  //   echarts.connect(manageChartList.getValue());
  // }
  
  bindEvent(myChart);
  console.log("radar chart complete:");

});

// watch(selectTags, async (newVal, oldVal) => {


// });
</script>

<template>
  <div id="radar-chart">
    <!-- <div>Radar Chart</div> -->
  </div>
</template>

<style scoped>
#radar-chart {
  width: 100%;
  height: 100%;
  font-size: 12px;
}

</style>
