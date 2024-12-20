<script setup>
import * as d3 from "d3";
// import * as echarts from 'echarts';
import { onMounted, reactive, ref, watch, onUpdated } from "vue";
import { storeToRefs } from "pinia";
import { UserOutlined, UsergroupAddOutlined } from '@ant-design/icons-vue';

// import * as echarts from 'echarts/core';
// import { ParallelComponent } from 'echarts/components';
// import { ParallelChart } from 'echarts/charts';
// import { SVGRenderer } from 'echarts/renderers';
// import { BrushComponent } from "echarts/components";
import { symbolType, colorConfig, chartIsExist } from '../configs/baseConfig'
import { useSelectClassStore } from "../stores/selectClass";
import { reqWeekViewtData } from '../api/index'

import { useStudentStore } from "../stores/Student";

const { totalSelectStudent, lastSelectStudent, lastSelectCluster } = storeToRefs(useStudentStore());

// echarts.use([ParallelComponent, ParallelChart, SVGRenderer, BrushComponent]);

/* ...............................var....................................*/
const { selectTags } = storeToRefs(useSelectClassStore());
let color;
let width;
let height;
let length;
let radius;
let arc_inner;
let arc_border;
let promptBox = d3.select("#tooltip");
let body = d3.select("body");
let myChart;
let weekname = ['week1', 'week2', 'week3', 'week4', 'week5', 'week6', 'week7', 'week8', 'week9', 'week10', 'week11', 'week12', 'week13', 'week14', 'week15', 'week16', 'week17', 'week18', 'week19', 'week20', 'week21', 'week22'];
// let student_list_ref = reactive(["zhx5rxgopln1p5hd10ql", 'b217bae3c84d59dde71f', '4388d48ebff4cf866ecd']);
let student_list_ref = ref([]);
let weekview_data = [
  {
    name: 'Grandpa',
    lr: 0.6,
    children: [
      {
        name: 'Uncle Leo',
        value: 15,
        lr: 0.4,
        // children: [
        //   {
        //     name: 'Cousin Jack',
        //     value: 2
        //   },
        //   {
        //     name: 'Cousin Mary',
        //     value: 5,
        //   },
        //   {
        //     name: 'Cousin Ben',
        //     value: 4
        //   }
        // ]
      },
      {
        name: 'Father',
        value: 10,
        lr: 0.2,
        // children: [
        //   {
        //     name: 'Me',
        //     value: 5
        //   },
        //   {
        //     name: 'Brother Peter',
        //     value: 1
        //   }
        // ]
      }
    ]
  },
  {
    name: 'Nancy',
    value: 5,
    lr: 1,
    // children: [
    //   {
    //     name: 'Uncle Nike',
    //     children: [
    //       {
    //         name: 'Cousin Betty',
    //         value: 1
    //       },
    //       {
    //         name: 'Cousin Jenny',
    //         value: 2
    //       }
    //     ]
    //   }
    // ]
  }
];

let data = {
  name: 'root',
  children: weekview_data
}


const partition = (data) => {
  const root = d3
    .hierarchy(data)
    .sum((d) => d.value)
    .sort((a, b) => b.value - a.value);
  return d3.partition().size([2 * Math.PI, root.height + 1])(root);
};
/* ...............................var....................................*/


watch(totalSelectStudent, async (newVal, oldVal) => {

  // console.log("newVal:", newVal);

  // 获取数据
  let data1 = await reqWeekViewtData(newVal);
  // data = await reqWeekViewtData(["zhx5rxgopln1p5hd10ql", 'b217bae3c84d59dde71f', '4388d48ebff4cf866ecd']);
  data = data1.res_data;
  student_list_ref.value = data1.res_student_list

  console.log("data:", data, "student_list_ref:", data1.res_student_list);
  draw();
},{ immediate: true, deep: true });

onMounted(async () => {
  // d3
  width = 2.2 * document.getElementById("weekview-chart").offsetWidth;
  height = 20 * document.getElementById("weekview-chart").offsetHeight;
  console.log("width:", width, "height:", height);

  // length = width > height ? height : width;
  length = 100
  radius = length / 6;
  promptBox = d3.select("#tooltip");

  arc_inner = d3
    .arc()
    // 这里相当于将由partition生成的矩形树图变形成了一个环状树图，以为矩形框对应的宽度是由角度表示的
    .startAngle((d) => d.x0)
    .endAngle((d) => d.x1)
    .padAngle((d) => Math.min((d.x1 - d.x0) / 2, 0.01)) // 限制最大弧间隔为0.005
    .padRadius(radius * 4)
    .innerRadius((d) => d.y0 * radius)
    // .outerRadius((d) => Math.max(d.y0 * radius, d.y1 * radius - 1));
    // .outerRadius((d) => d.y1 * radius - 1);
    .outerRadius((d) => (d.y0 + (d.y1 - d.y0) * d.data.lr) * radius - 1);

  // 获取数据
  // data = await reqWeekViewtData(student_list_ref);
  // data = await reqWeekViewtData(["zhx5rxgopln1p5hd10ql", 'b217bae3c84d59dde71f', '4388d48ebff4cf866ecd']);
  // data = data.res_data;

  // console.log("data:", data);
  // draw();
});

function arcVisible(d) {
  return d.y1 <= 3 && d.y0 >= 1 && d.x1 > d.x0;
}

function labelVisible(d) {
  return false
  return d.y1 <= 3 && d.y0 >= 1 && (d.y1 - d.y0) * (d.x1 - d.x0) > 0.03;
}

function labelTransform(d) {
  const x = (((d.x0 + d.x1) / 2) * 180) / Math.PI;
  const y = ((d.y0 + d.y1) / 2) * radius;
  return `rotate(${x - 90}) translate(${y},0) rotate(${x < 180 ? 0 : 180})`;
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
          `${d.data.name}:${d.value}<br>${(
            d.data.lr * 100
          ).toFixed(2)}%<br>
          ${(d.data.lr * d.data.value).toFixed(2)}`
        );
    })
    .on("mousemove", function (event) {
      let [posX, posY] = d3.pointer(event, body);
      promptBox.style("top", posY - 50 + "px").style("left", posX + 15 + "px");
    })
    .on("mouseout.out", function () {
      promptBox.attr("class", "prompt-hide");
    });
}

function draw() {

  const svg = d3
    .select("#weekview-svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", [0, 0, width, height])
    .style("font", "10px sans-serif");

  // 遍历data对象，键为学生id，值为每周学生的学习情况数组，数组的长度为22，每个元素为一个sunburst图的数据
  let row_num = 0;
  console.log('student_list_ref.value:', student_list_ref.value);

  for (let idx in student_list_ref.value) {
    // for (let student_id in data) {
    // console.log('idx:', idx);

    let student_id = student_list_ref.value[idx];
    // console.log('student_id:', student_id);
    for (let week_num in data[student_id]) {
      const root = partition(data[student_id][week_num]);
      let color_index = data[student_id][week_num].cluster;
      // console.log('root,', root);
      // 广度优先遍历
      root.each(function (descendant) {
        descendant.current = descendant;
      });

      // const border_path = svg
      //   .append("g")
      //   .attr("transform", `translate(${width / 2 + (width / 6)},${height / 2})`)
      //   .selectAll("path")
      //   .data(root.descendants().slice(1))
      //   .join("path")
      //   .attr("fill", "#fff")
      //   .attr("d", (d) => arc_border(d.current))
      //   // 增加边框
      //   .attr("stroke", (d) => {
      //     // if (d.data.lr < 0.6) return 'red'
      //     // else {
      //     while (d.depth > 1) d = d.parent;
      //     return colorConfig[color_index];
      //     // }
      //   });

      const g = svg
        .append("g")
        // .attr("transform", `translate(${width / 2 + (width / 6)},${height / 2})`);
        .attr("transform", () => {
          return `translate(${week_num * length + length / 2},${row_num * length + length / 2})`;
        })
      // 在同一个位置添加相同大小的元素，奇偶数行的元素颜色不同
      g.append("rect")
        .attr('width', length)
        .attr('height', length)
        .attr("fill", week_num % 2 == 0 ? "#f0f0f0" : "#ffffff")
        .attr("transform", () => {
          return `translate(${-length / 2},${-length / 2})`;
        })
      if (week_num != 0) {
        let lineHeight = (data[student_id][week_num].score - data[student_id][week_num - 1].score) / 4;
        if (lineHeight < 2) lineHeight = 2;
        g.append("rect")
          .attr('width', length)
          .attr('height', lineHeight)
          .attr("fill", colorConfig[color_index])
          .attr('fill-opacity', 0.2)
          .attr("transform", () => {
            return `translate(${-length},${-lineHeight / 2})`;
          })
      }

      const path = g
        .append("g")
        .selectAll("path")
        .data(root.descendants().slice(1))
        .join("path")
        // 设置为父亲的颜色基调
        .call(addEvent)
        .attr("fill", (d) => {
          while (d.depth > 1) d = d.parent;
          return colorConfig[color_index];
        })
        // 判断可见性，若可见，根据其是否存在后代设置透明度
        .attr("fill-opacity", (d) =>
          // arcVisible(d.current) ? (d.children ? 0.6 : 0.4) : 0
          arcVisible(d.current) ? 0.6 : 0
        )
        // 不可见则取消触发事件
        .attr("pointer-events", (d) => (arcVisible(d.current) ? "auto" : "none"))
        .attr("d", (d) => arc_inner(d.current))
      // 增加边框
      // .attr("stroke", (d) => {
      //   while (d.depth > 1) d = d.parent;
      //   return colorConfig[color_index];
      // })

      path
        // 为存在后代元素的弧形添加点击事件
        .filter((d) => d.children)
        .style("cursor", "pointer")
      // .on("click", clicked);

      path
        // 为不存在后代元素的可见的弧形添加点击事件
        .filter((d) => !d.children)
        .style("cursor", "pointer")
      // .on("click", showOneField);

      // path.append("title").text(
      //   (d) =>
      //     `${d
      //       .ancestors()
      //       .map((d) => d.data.name)
      //       .reverse()
      //       .join("/")}\n${format(d.value)}`
      // );

      // 添加各个扇形的标签：知识点名称
      // const label = g
      //   .append("g")
      //   .attr("pointer-events", "none")
      //   .attr("text-anchor", "middle")
      //   .style("user-select", "none")
      //   .selectAll("text")
      //   .data(root.descendants().slice(1))
      //   .join("text")
      //   .attr("dy", "0.35em")
      //   .attr("fill-opacity", (d) => +labelVisible(d.current))
      //   .attr("transform", (d) => labelTransform(d.current))
      //   .text((d) => {
      //     let kgs = d.data.name.split('_')
      //     return kgs[kgs.length - 1];
      //   })
      //   .attr("fill", (d) => {
      //     if (d.data.lr < 0.6) return 'red'
      //     else return 'black'
      //   });

      // const fillConfig = (selection, d) => {
      //   selection
      //     .attr("fill", () => {
      //       while (d.depth > 1) d = d.parent;
      //       return colorConfig[color_index];
      //     })
      //     .attr("fill-opacity", 0.2);
      // };

      const parent = g
        .append("circle")
        .datum(root)
        .attr("r", radius / 2)
        .attr("fill", colorConfig[color_index])
        .attr("pointer-events", "all")
        .attr("fill-opacity", (d) => {
          // console.log('d:', d);
          return d.data.score / d.value;
        })
      // .call(addEvent)
      // .on("click", clicked);

      const parentText = g
        .append("text")
        .text(data.name)
        .attr("pointer-events", "none")
        .style("dominant-baseline", "middle")
        .style("text-anchor", "middle");

      function clicked(_, p) {
        // 更新领域
        updataFirstField(p)
        updataSelectField(p.data.name);

        // 中心圆的数据为点击元素的父元素，若不存在父元素，则是根节点
        parent.datum(p.parent || root);
        if (p.data.name !== "paperCount") {
          parent.call(fillConfig, p);
        } else {
          parent.attr("fill", "none");
        }
        parentText.text(p.data.name);

        root.each((d) => {
          d.target = {
            x0:
              Math.max(0, Math.min(1, (d.x0 - p.x0) / (p.x1 - p.x0))) * 2 * Math.PI,
            x1:
              Math.max(0, Math.min(1, (d.x1 - p.x0) / (p.x1 - p.x0))) * 2 * Math.PI,
            y0: Math.max(0, d.y0 - p.depth),
            y1: Math.max(0, d.y1 - p.depth),
          };
        });

        const t = g.transition().duration(750);

        path
          .transition(t)
          .tween("data", (d) => {
            const i = d3.interpolate(d.current, d.target);
            return (t) => (d.current = i(t));
          })
          // 过滤当前可见和即将可见的path
          .filter(function (d) {
            return +this.getAttribute("fill-opacity") || arcVisible(d.target);
          })
          .attr("fill-opacity", (d) =>
            arcVisible(d.target) ? (d.children ? 0.6 : 0.4) : 0
          )
          .attr("pointer-events", (d) => (arcVisible(d.target) ? "auto" : "none"))

          .attrTween("d", (d) => () => arc_inner(d.current));

        label
          .filter(function (d) {
            return +this.getAttribute("fill-opacity") || labelVisible(d.target);
          })
          .transition(t)
          .attr("fill-opacity", (d) => +labelVisible(d.target))
          .attrTween("transform", (d) => () => labelTransform(d.current));
      }

      function showOneField(_, p) {

        // 更新领域
        updataFirstField(p)
        updataSelectField(p.data.name);
      }

      function updataFirstField(p) {
        let ancestors = p.ancestors()
        let fieldName = ancestors.length == 1 ? p.data.name : ancestors[ancestors.length - 2].data.name
        updataParentField(fieldName)
      }

      // 画提示信息
      // let tooltips = svg
      //   .append("g")
      //   .selectAll()
      //   .data(root.children)
      //   .join("g")
      // .on('mouseover',)
      // .on('mouseout',)
      // .on('click',clicked) // 2024.6.17
      // .attr("transform",`translate(${-width/2},${-height/2})`);
      // 画图标
      // tooltips
      //   .append('rect')
      //   .attr('x', 10)
      //   .attr('y', (_, i) => i * 25 + 10)
      //   .attr('width', 20)
      //   .attr('height', 10)
      //   .attr("fill", (d) => colorConfig[color_index]);

      // 画文字
      // tooltips
      //   .append('text')
      //   .attr("transform", (_, i) => `translate(30,${i * 25 + 10 + 10})`)
      //   // .attr('width',20)
      //   // .attr('height',10)
      //   .text((d) => d.data.name);
    }
    row_num++;
  }

}


</script>

<template>
  <div id="weekview-chart">
    <div style="font-size: 18px; font-weight:bold; margin-bottom: 5px;">学生学习情况周视图</div>
    <div id="weekhead">
      <div id="empty" style="width: 50px ; height: 100%; flex-shrink: 0;"></div>
      <div v-for="(text, idx) in weekname " :class="{ active: idx % 2 != 1 }" class="weekhead-item">{{ text }}</div>
    </div>
    <div id="weekview-body">
      <div id="weekview-body-leftbar">
        <div v-for="(student_id, idx) in student_list_ref" :key="idx"
          style="height: 100px; vertical-align: middle; text-align: center; display: flex; justify-content: space-around; flex-direction: column; ">
          <div style="flex-grow: 0;">
            <UserOutlined :style="`font-size: 20px; color: ${colorConfig[0]};`" /> 
            <div>{{ student_id.slice(0, 5) }}</div>
          </div>
        </div>
      </div>
      <div id="weekview-body-main">
        <svg id="weekview-svg"></svg>
      </div>
    </div>
  </div>
</template>

<style scoped>
#weekview-chart {
  width: 100%;
  height: 100%;
  font-size: 12px;
  overflow: auto;
}

#weekhead {
  width: 100%;
  height: 25px;
  display: flex;
}

#weekview-body {
  width: 100%;
  height: 100%;
  display: flex;
}

#weekview-body-leftbar {
  width: 50px;
  height: 100%;
  flex-grow: 0;
  flex-shrink: 0;
  /* padding-top: 25px; */
}

#weekview-body-main {
  width: 100%;
  height: 100%;
  flex-grow: 0;
  flex-shrink: 0;
}

.weekhead-item {
  width: 100px;
  height: 100%;
  display: flex;
  flex-shrink: 0;
  /* justify-content: center;
  align-items: center; */
  /* 文字居中 */
  text-align: center;
  justify-content: center;
  flex-direction: column;
  line-height: 25px;
}

.active {
  background-color: #f0f0f0;
}
</style>
