<script setup>
import * as d3 from "d3";
import * as echarts from 'echarts';
import { onMounted, reactive, ref, watch, onUpdated } from "vue";
import { storeToRefs } from "pinia";

import { reqProblemViewtData } from '../api/index'
import { symbolType, colorConfig, chartIsExist } from '../configs/baseConfig'
import manageChartList from '../configs/chartConnect'
import { max } from 'd3';
import { useStudentStore } from "../stores/Student";

const { totalSelectStudent, lastSelectStudent, lastSelectCluster } = storeToRefs(useStudentStore());

/* ...............................var....................................*/
let promptBox = d3.select("#tooltip");
let body = d3.select("body");
let data = {
  'knowledgePoint': 'ROOT',
  'children': [{
    "knowledgePoint": "主知识点",
    "children": [
      {
        "knowledgePoint": "一级知识点1",
        "children": [
          { "question": "题目1", "submissions": 150, "score": 0.8 },
          { "question": "题目2", "submissions": 100, "score": 0.6 }
        ]
      },
      {
        "knowledgePoint": "一级知识点2",
        "children": [
          { "question": "题目3", "submissions": 120, "score": 0.75 }
        ]
      }
    ]
  }
    , {
    "knowledgePoint": "主知识点",
    "children": [
      {
        "knowledgePoint": "一级知识点1",
        "children": [
          { "question": "题目1", "submissions": 150, "score": 0.8 },
          { "question": "题目2", "submissions": 100, "score": 0.6 }
        ]
      },
      {
        "knowledgePoint": "一级知识点2",
        "children": [
          { "question": "题目3", "submissions": 120, "score": 0.75 },
          { "question": "题目4", "submissions": 120, "score": 0.75 },
        ]
      }
    ]
  }]
};


/* ...............................var....................................*/

watch(lastSelectCluster, async (newVal, oldVal) => {

console.log("problem newVal:", newVal);

 // 获取数据
data = await reqProblemViewtData(0, newVal, 0, 0);
data = data.res_data;
// color = d3.scaleOrdinal(
//   d3.quantize(d3.interpolateRainbow, data.children.length + 1)
// ).domain(data.children.map(d => d.name));

console.log("problem data:", data);
draw(data);

});

onMounted(async () => {
  promptBox = d3.select("#tooltip");

  let res = await reqProblemViewtData();
  console.log('problem-chart.res_data:',res.res_data);
  data = res.res_data;
  draw(data);

});

function isLeaf(d){ 
  if(d.data.submissions){
    return true
  }
  return false
}

function addEvent(selection) {
  selection
    .on("mouseover.over", function (event, d) {
      let [posX, posY] = d3.pointer(event, body);
      promptBox
        .attr("class", "prompt-show")
        .style("top", posY - 50 + "px")
        .style("left", posX + 15 + "px")
        .html(
          `${d.data.question}:${d.value}<br>
          平均尝试次数：${(d.data.submissions).toFixed(2)}<br>
          平均正确率：${(d.data.score * 100).toFixed(2)}%`
        );
      // console.log("mousemver", d);
    })
    .on("mousemove", function (event) {
      let [posX, posY] = d3.pointer(event, body);
      promptBox.style("top", posY - 50 + "px").style("left", posX + 15 + "px");      
    })
    .on("mouseout.out", function () {
      promptBox.attr("class", "prompt-hide");
    });
}

function draw(data) {
  let width = document.getElementById("problem-chart").offsetWidth;
  let height = document.getElementById("problem-chart").offsetHeight;

  const svg = d3.select("#problem-svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", [0, 0, width, height])
    .style("font", "10px sans-serif");

  // 清除画布
  svg.selectAll("*").remove();

  const treeLayout = d3.tree().size([height, 0.4*width]); // 设置树的宽高，宽为叶子节点层宽度，高为树的高度，我们是横向树，所以宽高互换

  // Generate tree hierarchy
  const root = d3.hierarchy(data, d => d.children);
  treeLayout(root);
  console.log('tree root:', root);
  console.log('tree root.links:', root.links());
  

  // Draw links (edges)
  svg.selectAll(".link")
    .data(root.links())
    .enter().append("path")
    .attr("class", "link")
    .attr("d", d3.linkHorizontal()// 向x,y两个函数传递d中source和target对象
      .x(d => d.y)
      .y(d => d.x)
    )
    .classed("rootlevel", (d) => {
      // console.log('d:', d, d.x, d.y);
      return d.source.data.knowledgePoint === 'ROOT'
    })
    .attr("fill", colorConfig[lastSelectCluster.value])

  // Draw nodes (knowledge points)
  const nodes = svg.selectAll(".node")
    .data(root.descendants())
    .enter().append("g")
    .attr("class", "node")
    .attr("transform", d => `translate(${d.y},${d.x})`)

  let treenode_r = 5
  nodes.append("circle")
    .attr("r", d => isLeaf(d) ? treenode_r : 0)
    // .attr("fill", colorConfig[lastSelectCluster.value])
    .attr("fill", '#c6dbec')

  nodes.append("text")
    .attr("dy", 5)
    .attr("dx", -60)
    .text(d => {
      if (d.depth == 1){
        return d.data.knowledgePoint || d.data.question
      }
    })
    

    
  // 以下配置提交次数和得分率的可视化
  // Add additional visualization for submissions and scores
  let rect_max_length = 150;
  let rect_h = 5;
  let rect_pad = 20
  let circle_r = 5
  const submissionsScale = d3.scaleLinear()
    .domain([0, d3.max(root.descendants(), d => d.data.submissions || 0)]) // 定义域：提交次数
    .range([0, rect_max_length]); // 值域：实际长度

  const scoresScale = d3.scaleLinear()
    .domain([0, 1])
    .range([0, rect_max_length]);

  let submission_gs = nodes.append('g')
  submission_gs.append("rect")
    .attr("x", rect_pad)
    .attr("y", -rect_h/2)
    // .attr("width", d => submissionsScale(d.data.submissions || 0))
    .attr("width", d => isLeaf(d) ? rect_max_length : 0)
    // .attr("width",rect_max_length)
    .attr("height", rect_h)
    // .attr("fill", "lightgreen");
    .attr("fill", colorConfig[lastSelectCluster.value])
    .attr('fill-opacity', 0.6)
    .call(addEvent)

  submission_gs.append('circle')
    .attr("cx", d => submissionsScale(d.data.submissions || 0))
    .attr("cy", 0)
    .attr("r", d => isLeaf(d) ? circle_r : 0)
    // .attr("fill", "green");
    .attr("fill", colorConfig[lastSelectCluster.value])
    


  let score_gs = nodes.append('g').attr("transform", `translate(${2 * rect_pad + rect_max_length},${-rect_h/2})`)
  score_gs.append("rect")
    // .attr("width", d => scoresScale(d.data.score || 0))
    .attr("width", d => isLeaf(d) ? rect_max_length : 0)
    // .attr("width", rect_max_length)
    .attr("height", rect_h)
    // .attr("fill", "lightblue");
    .attr("fill", colorConfig[lastSelectCluster.value])
    .attr('fill-opacity', 0.6)
    .call(addEvent)

  score_gs.append('circle')
    .attr("cx", d => scoresScale(d.data.score || 0))
    .attr("cy", rect_h/2)
    .attr("r", d => isLeaf(d) ? circle_r : 0)
    // .attr("fill", "green");
    .attr("fill", colorConfig[lastSelectCluster.value])
    

}


</script>

<template>
  <div id="problem-chart" style="display: flex; justify-content: center; align-items: center;">
    <!-- <div>riverflow Chart</div> -->
    <svg id="problem-svg"></svg>
  </div>
</template>

<style scoped>
#problem-chart {
  width: 100%;
  height: 100%;
  font-size: 12px;
}

.node rect {
  fill: steelblue;
  stroke: white;
  stroke-width: 1.5px;
}

.node text {
  font-size: 12px;
  fill: black;
}
/* 添加deep才会在SVG中更新，不然可能找不到样式配置 */
:deep(.link) {
  fill: #c6dbec;
  stroke: #ccc;
  stroke-width: 1;
}
:deep(.rootlevel) {
  display: none;
}

.axis {
  font-size: 10px;
  fill: black;
}
</style>
