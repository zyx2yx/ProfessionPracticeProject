<script setup>
// import * as d3 from "d3";
import * as echarts from 'echarts';
import dayjs from 'dayjs';
import { onMounted, reactive, ref, watch, onUpdated } from "vue";
import { storeToRefs } from "pinia";

// import * as echarts from 'echarts/core';
// import { ParallelComponent } from 'echarts/components';
// import { ParallelChart } from 'echarts/charts';
// import { SVGRenderer } from 'echarts/renderers';
// import { BrushComponent } from "echarts/components";

import { useSelectClassStore } from "../stores/selectClass";
import { reqParallelDataOfStudentOrClass, reqGetClassStudentList } from '../api/index'
const { resetSelectTags, selectStart, selectEnd, switchClass, updateStudentList, updateStudentListByIndex, addSelectStudent, resetSelectStudents } = useSelectClassStore();

// echarts.use([ParallelComponent, ParallelChart, SVGRenderer, BrushComponent]);

/* ...............................var....................................*/
const { selectTags, selectStudents } = storeToRefs(useSelectClassStore());
/* antd时间组件数据与函数 */
const range = (start, end) => {
  const result = [];
  for (let i = start; i < end; i++) {
    result.push(i);
  }
  return result;
};
let start = dayjs("2023-08-31");
let end = dayjs("2024-01-25")
// console.log("start, end:",start, end);

const disabledDate = current => {
  // Can not select days before today and today

  // console.log(current , dayjs().endOf('day'));
  // return current && current < dayjs().endOf('day');
  return current < start || current > end;
};
const disabledDateTime = () => {
  return {
    disabledHours: () => range(0, 24).splice(4, 20),
    disabledMinutes: () => range(30, 60),
    disabledSeconds: () => [55, 56],
  };
};
const disabledRangeTime = (_, type) => {
  if (type === 'start') {
    return {
      disabledHours: () => range(0, 60).splice(4, 20),
      disabledMinutes: () => range(30, 60),
      disabledSeconds: () => [55, 56],
    };
  }
  return {
    disabledHours: () => range(0, 60).splice(20, 4),
    disabledMinutes: () => range(0, 31),
    disabledSeconds: () => [55, 56],
  };
};
const value3 = ref([start, end]);
const rangePresets = ref([
  // {
  //   label: 'Next 7 Days',
  //   value: [dayjs(value3.value[0].format('YYYY-MM-DD')) ,dayjs(value3.value[0].format('YYYY-MM-DD')).add(7, 'd')],// 有bug，起始时间没有立刻更新
  // },
  // {
  //   label: 'Next 14 Days',
  //   value: [value3.value[0].add(14, 'd'), dayjs()],
  // },
  // {
  //   label: 'Next 30 Days',
  //   value: [value3.value[0].add(30, 'd'), dayjs()],
  // },
  // {
  //   label: 'Next 90 Days',
  //   value: [value3.value[0].add(90, 'd'), dayjs()],
  // },
]);

const handleCalOpenChange = async (status) => {
  // console.log('Calendar Open Status:', v1, v2,v3);
  // console.log("vlaue3:", value3.value, value3.value[0].format('YYYY-MM-DD'), value3.value[1].format('YYYY-MM-DD'));
  if (!status) {
    let response_data = await reqParallelDataOfStudentOrClass(selectStudents.value, selectTags.value, value3.value[0].unix(), value3.value[1].unix());
    option.series.data = response_data.res_list_data;
    option && myChart.setOption(option);
  }
};

/* antd时间组件数据与函数 */


let option = {
  brush: {
    brushLink: 'all',
    brushMode: 'multiple',// ?想要在同一坐标轴刷选多个地方，但是不生效
    toolbox: ['clear'],
    // toolbox: [],
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
    { dim: 0, name: '得分' },
    { dim: 1, name: '时长' },
    { dim: 2, name: '天数' },
    { dim: 3, name: '得分率' },
    { dim: 4, name: '正确率' },
    { dim: 5, name: '尝试数' },
    {
      dim: 6, name: '活跃时间', type: 'category',
      data: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
      axisLabel: {
        formatter: function (value, _) {
          if (value % 4 === 0) {
            return value + 'h';
          } else {
            return '';
          }
          // return value + 'h';
        }
      }
    },
    {
      dim: 7,
      name: '常见状态',
      type: 'category',
      data: ['Absolutely_Correct', 'Absolutely_Error', 'Partially_Correct', 'Error1', 'Error2', 'Error3', 'Error4', 'Error5', 'Error6', 'Error7', 'Error8', 'Error9'],
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
            return 'E' + value[value.length - 1];
          }
        }
      }
    },
    {
      dim: 8,
      name: '常用方法',
      type: 'category',
      data: ['Method_Cj9Ya2R7fZd6xs1q5mNQ', 'Method_gj1NLb4Jn7URf9K2kQPd', 'Method_5Q4KoXthUuYz3bvrTDFm', 'Method_m8vwGkEZc3TSW2xqYUoR', 'Method_BXr9AIsPQhwNvyGdZL57'],
      axisLabel: {
        formatter: function (_, index) {
          return "M_" + index;
        }
      }
    },
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
    top: '15%',
    left: '5%',
    right: '10%',
    bottom: '5%',
  },
};
let myChart;
const boxStyle = {
  width: '100%',
  borderRadius: '6px',
  justifyContent: 'space-between',
  alignItems: 'center',
};
const tagsData = ['AllClass', 'Class1', 'Class2', 'Class3', 'Class4', 'Class5', 'Class6'
, 'Class7', 'Class8', 'Class9', 'Class10', 'Class11', 'Class12', 'Class13', 'Class14', 'Class15'
]

const reqStudenListByClassid = async (class_list) => {
  let student_list = await reqGetClassStudentList(class_list)
  console.log(student_list);
  updateStudentList(student_list.res_data)

}

// 输入框选择班级
const handleChange = value => {
  console.log(`selected ${value}`); // value 为[]
  // console.log(value)
  // 发送请求获取班级学生列表
  reqStudenListByClassid(value)
  resetSelectStudents();
  switchClass(value[0])
};

const handleFocus = () => {
  selectStart();
};

const handleResetSelect = () => {
  resetSelectTags();
  resetSelectStudents();
};

const handleCommit = () => {
  selectEnd();
};

/* ...............................var....................................*/

onMounted(async () => {
  const chartDom = document.getElementById('parallel-chart');
  myChart = echarts.init(chartDom, null, { renderer: 'svg' });
  let response_data = await reqParallelDataOfStudentOrClass(selectStudents.value, selectTags.value, value3.value[0].unix(), value3.value[1].unix());
  option.series.data = response_data.res_list_data;
  option && myChart.setOption(option);
});

watch(selectTags, async (newVal, oldVal) => {

  // let response_data = await reqParallelDataOfStudentOrClass(selectStudents.value, newVal,  value3.value[0].unix(), value3.value[1].unix());
  // option.series.data = response_data.res_list_data;
  // option && myChart.setOption(option);
});
</script>

<template>
  <a-flex :style="{ ...boxStyle }">选择班级:
    <a-select v-model:value="selectTags" mode="multiple" style="width: 40%" placeholder="Please select Class"
      :options="tagsData.map((_, i) => ({ value: _ }))" @change="handleChange" @focus="handleFocus"
      size="small"></a-select>

    <!-- <a-space direction="vertical"> -->
      <a-range-picker v-model:value="value3" :disabled-date="disabledDate" size="small" :defaultPickerValue="[start, end]"
        :presets="rangePresets" @openChange="handleCalOpenChange" style="width: 30%;"/>
    <!-- </a-space> -->

    <a-button size="small" @click="handleResetSelect">清除</a-button>

    <a-button type="primary" size="small" @click="handleCommit">确认</a-button>
  </a-flex>
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
