<script setup>
// import * as d3 from "d3";
import * as echarts from 'echarts';
import { onMounted, reactive, ref, watch, onUpdated } from "vue";
import { storeToRefs } from "pinia";

import { reqTsnePos } from '../api/index'
import { symbolType, colorConfig, chartIsExist } from '../configs/baseConfig'
import manageChartList from '../configs/chartConnect'
import { brush, select } from 'd3';

import { useStudentStore } from "../stores/Student";

const { totalSelectStudent, lastSelectStudent, lastSelectCluster } = storeToRefs(useStudentStore());
const { updateTotalSelectStudent, updateLastSelectStudent, updateLastSelectCluster } = useStudentStore();

/* ...............................var....................................*/




let myChart;
let option;
// let symbolType = ['circle', 'rect', 'roundRect', 'triangle', 'diamond', 'pin', 'arrow', 'none'];
// let colorConfig = ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc'];
option = {
  // color: ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc'],
  grid: {
    top: '20%',
    left: '7%',
    right: '5%',
    bottom: '10%',
  },
  xAxis: {},
  yAxis: {},
  legend: {
    data: [],
    top: '10%',
    textStyle: {
      fontSize: 10,
    },
    itemWidth: 10,
    itemHeight: 10,
  },
  title: {
    left: 'left',
    text: '学生学习特征嵌入',
    // subtext: 'Fake data'
  },
  tooltip: {},
  brush: {
    toolbox: ['rect', 'polygon', 'clear'],
    seriesIndex: 'all',
    xAxisIndex: 'all',
    yAxisIndex: 'all',
    transformable: true,
    throttleType: 'debounce',
    throttleDelay: 500,
    removeOnClick: true,
    inBrush: {
      opacity: 1,
    }
  },
  toolbox: {
    right: 20,
    feature: {
      dataZoom: {}
    }
  },
  dataZoom: [
    {
      type: 'inside'
    },
    {
      type: 'inside',
      showDataShadow: false,
      handleSize: '80%'
    },
    {
      type: 'inside',
      orient: 'vertical'
    },
    {
      type: 'inside',
      orient: 'vertical',
      showDataShadow: false,
      handleSize: '80%'
    }
  ],
  series: [
    // {
    // //   symbolSize: 20,
    //   data: [],
    //   type: 'scatter'
    // },
    // {
    // //   symbolSize:30,
    //   data:[
    //     ],
    //   type:'scatter'
    // }
  ]
};

function bindEvent(myChart) {
  // let radarchart = manageChartList.getValue().find(chart => chart.id !== myChart.id);
  let radarchart;
  myChart.on('mouseover', function (params) {
    radarchart = manageChartList.getValue().find(chart => chart.id !== myChart.id);
    radarchart.dispatchAction({
      type: 'highlight',
      dataIndex: params.seriesIndex
    });
    // console.log('mouseover:', params); 
  })
    .on('mouseout', function (params) {
      radarchart.dispatchAction({
        type: 'downplay',
        dataIndex: params.seriesIndex
      });
    });
}


/* ...............................var....................................*/

onMounted(async () => {
  const chartDom = document.getElementById('tsnescatter-chart');
  myChart = echarts.init(chartDom, null, { renderer: 'svg' });
  let res = await reqTsnePos();
  console.log('res.res_data:', res.res_data);
  let { pos, cluster_ids, student_ids} = res.res_data;
  for (let i = 0; i < cluster_ids.length; i++) {
    option.series[i] = {
      data: pos[i],
      type: 'scatter',
      name: `Cluster ${cluster_ids[i]}`,
      symbol: symbolType[cluster_ids[i]],
      symbolSize: 7,
      itemStyle: {
        color: colorConfig[cluster_ids]
      },
      emphasis: {
        focus: 'series'
      },
    }
    option.legend.data[i] = {
      name: `Cluster ${cluster_ids[i]}`,
      icon: symbolType[cluster_ids[i]],
      textStyle: {
        color: colorConfig[cluster_ids[i]]
      }
    };
  }
  console.log('scatter option:', option);
  

  option && myChart.setOption(option);
  if (!chartIsExist(manageChartList.getValue(), myChart.id)) {
    manageChartList.appendValue(myChart);
  }

  let idxs = []
  let selectStudentCluster = -1
  myChart.on('brushSelected', function (params) {
    let selectStudentIds =[]
    // 获取被圈选的节点，在左侧列表展示出来
    var brushComponent = params.batch[0]; // 被选择组件
    const selectIndex = brushComponent.selected[0].dataIndex // 数组，值为原数据的数据序号
    console.log('brushComponent',brushComponent, 'selectIndex',selectIndex)
    // const IDs = selectIndex.map(idx => rawData[idx][5])
    // updataPointsID(selectIndex)
    for (let i=0;i<brushComponent.selected.length;i++){
      if(brushComponent.selected[i].dataIndex.length != 0){
        idxs = brushComponent.selected[i].dataIndex
        selectStudentCluster = i
        // 根据idxs在student_ids中找到对应的学生id
        for (let j=0;j<idxs.length;j++){
          selectStudentIds.push(student_ids[i][idxs[j]])
        }
        updateTotalSelectStudent(selectStudentCluster, selectStudentIds)
        updateLastSelectStudent(selectStudentIds)
        updateLastSelectCluster(selectStudentCluster)

        break
      }
    }

    console.log('selectStudentIds:',selectStudentIds, 'selectStudentCluster:',selectStudentCluster);
  });

  // if(manageChartList.getValue().length > 1) {
  //   echarts.connect(manageChartList.getValue());
  // }

  console.log("scatter chart complete:", manageChartList.getValue());

  bindEvent(myChart);
});

// watch(selectTags, async (newVal, oldVal) => {


// });
</script>

<template>
  <div id="tsnescatter-chart" style="display: flex; justify-content: center; align-items: center;">
    <!-- <div v-for="i in lastSelectStudent">{{ i }}</div> -->
    <!-- <div>tsnescatter Chart</div> -->
  </div>
</template>

<style scoped>
#tsnescatter-chart {
  width: 100%;
  height: 100%;
  font-size: 12px;
}
</style>
