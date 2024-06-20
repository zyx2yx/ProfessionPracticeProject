<script setup>
import * as d3 from "d3";
// import * as echarts from 'echarts';
import { onMounted, reactive, ref, watch, onUpdated } from "vue";
import { storeToRefs } from "pinia";

// import * as echarts from 'echarts/core';
// import { ParallelComponent } from 'echarts/components';
// import { ParallelChart } from 'echarts/charts';
// import { SVGRenderer } from 'echarts/renderers';
// import { BrushComponent } from "echarts/components";

import { useSelectClassStore } from "../stores/selectClass";
import { reqSunburstData } from '../api/index'

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
let sunburst_data = [
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
  name:'root',
  children:sunburst_data
}

let option = {
  tooltip: { // 提示框
    padding: 5,
    backgroundColor: '#fff',
    borderColor: '#fff',
    borderWidth: 1,
    textStyle: {
        color: '#000',
        fontSize: 12,
    },
  },
  series: {
    type: 'sunburst',
    data: sunburst_data,
    radius: [0, '90%'],
    itemStyle: {
      borderRadius: 7,
      borderWidth: 2
    },
    label: {
      show: false
    },
    startAngle:0,
  },
  parallel: {
        top: '20%',
        left: '5%',
        right: '20%',
        bottom: '5%',
    },
};

const partition = (data) => {
  const root = d3
    .hierarchy(data)
    .sum((d) => d.value)
    .sort((a, b) => b.value - a.value);
  return d3.partition().size([2 * Math.PI, root.height + 1])(root);
};
/* ...............................var....................................*/

onMounted(async () => {
  // const chartDom = document.getElementById('sunburst-chart');
  // myChart = echarts.init(chartDom,null,{renderer: 'svg'});
  // let response_data = await reqParallelDataOfStudentOrClass([], selectTags.value, '_starttime','_endtime');
  // option.series.data = response_data.res_list_data;
  // option && myChart.setOption(option);

  // d3
  width = document.getElementById("sunburst-chart").offsetWidth;
  height = document.getElementById("sunburst-chart").offsetHeight;
  length = width > height ? height : width;
  radius = length / 6;
  promptBox = d3.select("#tooltip");

  arc_inner = d3
    .arc()
    // 这里相当于将由partition生成的矩形树图变形成了一个环状树图，以为矩形框对应的宽度是由角度表示的
    .startAngle((d) => d.x0)
    .endAngle((d) => d.x1)
    .padAngle((d) => Math.min((d.x1 - d.x0) / 2, 0.005)) // 限制最大弧间隔为0.005
    .padRadius(radius * 1.5)
    .innerRadius((d) => d.y0 * radius)
    // .outerRadius((d) => Math.max(d.y0 * radius, d.y1 * radius - 1));
    // .outerRadius((d) => d.y1 * radius - 1);
    .outerRadius((d) => (d.y0 + (d.y1-d.y0) * d.data.lr) * radius - 1);

  // console.log('colorname',data.children.map(d => d.name));
  color = d3.scaleOrdinal(
    d3.quantize(d3.interpolateRainbow, data.children.length + 1)
  ).domain(data.children.map(d => d.name));

  arc_border = d3
    .arc()
    // 这里相当于将由partition生成的矩形树图变形成了一个环状树图，以为矩形框对应的宽度是由角度表示的
    .startAngle((d) => d.x0)
    .endAngle((d) => d.x1)
    .padAngle((d) => Math.min((d.x1 - d.x0) / 2, 0.005)) // 限制最大弧间隔为0.005
    .padRadius(radius * 1.5)
    .innerRadius((d) => d.y0 * radius)
    // .outerRadius((d) => Math.max(d.y0 * radius, d.y1 * radius - 1));
    .outerRadius((d) => d.y1 * radius - 1);

  // 获取数据
  data = await reqSunburstData("zhx5rxgopln1p5hd10ql");
  data = data.res_data;
  // console.log('colorname',data.children.map(d => d.name));
  color = d3.scaleOrdinal(
    d3.quantize(d3.interpolateRainbow, data.children.length + 1)
  ).domain(data.children.map(d => d.name));

  console.log("data:", data);
  draw();
});

function arcVisible(d) {
  return d.y1 <= 3 && d.y0 >= 1 && d.x1 > d.x0;
}

function labelVisible(d) {
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
            (d.value * 100) /
            d.parent.value
          ).toFixed(2)}%`
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
  const root = partition(data);
  console.log('root,',root);
  // 广度优先遍历
  root.each(function (descendant) {
    descendant.current = descendant;
  });

  const svg = d3
    .select("#sunburst-svg")
    .attr("viewBox", [0, 0, width, height])
    .style("font", "10px sans-serif");


  const border_path = svg
    .append("g")
    .attr("transform", `translate(${width / 2 + (width/6)},${height / 2})`)
    .selectAll("path")
    .data(root.descendants().slice(1))
    .join("path")
    .attr("fill", "#fff")
    .attr("d", (d) => arc_border(d.current))
    // 增加边框
    .attr("stroke", (d) => {
      // if (d.data.lr < 0.6) return 'red'
      // else {
        while (d.depth > 1) d = d.parent;
        return color(d.data.name);
      // }
    });
  const g = svg
    .append("g")
    .attr("transform", `translate(${width / 2 + (width/6)},${height / 2})`);

  const path = g
    .append("g")
    .selectAll("path")
    .data(root.descendants().slice(1))
    .join("path")
    // 设置为父亲的颜色基调
    .call(addEvent)
    .attr("fill", (d) => {
      while (d.depth > 1) d = d.parent;
      return color(d.data.name);
    })
    // 判断可见性，若可见，根据其是否存在后代设置透明度
    .attr("fill-opacity", (d) =>
      arcVisible(d.current) ? (d.children ? 0.6 : 0.4) : 0
    )
    // 不可见则取消触发事件
    .attr("pointer-events", (d) => (arcVisible(d.current) ? "auto" : "none"))
    .attr("d", (d) => arc_inner(d.current))
    // 增加边框
    // .attr("stroke", (d) => {
    //   while (d.depth > 1) d = d.parent;
    //   return color(d.data.name);
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
    .on("click", showOneField);

  // path.append("title").text(
  //   (d) =>
  //     `${d
  //       .ancestors()
  //       .map((d) => d.data.name)
  //       .reverse()
  //       .join("/")}\n${format(d.value)}`
  // );

  const label = g
    .append("g")
    .attr("pointer-events", "none")
    .attr("text-anchor", "middle")
    .style("user-select", "none")
    .selectAll("text")
    .data(root.descendants().slice(1))
    .join("text")
    .attr("dy", "0.35em")
    .attr("fill-opacity", (d) => +labelVisible(d.current))
    .attr("transform", (d) => labelTransform(d.current))
    .text((d) => {
      let kgs = d.data.name.split('_')
      return kgs[kgs.length-1];
    })
    .attr("fill", (d) => {
      if (d.data.lr < 0.6) return 'red'
      else return 'black'
    });

  const fillConfig = (selection, d) => {
    selection
      .attr("fill", () => {
        while (d.depth > 1) d = d.parent;
        return color(d.data.name);
      })
      .attr("fill-opacity", 0.2);
  };

  const parent = g
    .append("circle")
    .datum(root)
    .attr("r", radius)
    .attr("fill", "none")
    .attr("pointer-events", "all")
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

  function updataFirstField(p){
    let ancestors = p.ancestors()
    let fieldName = ancestors.length == 1 ? p.data.name : ancestors[ancestors.length-2].data.name
    updataParentField(fieldName)
  }

  // 画提示信息
  let tooltips = svg
    .append("g")
    .selectAll()
    .data(root.children)
    .join("g")
    // .on('mouseover',)
    // .on('mouseout',)
    // .on('click',clicked) // 2024.6.17
    // .attr("transform",`translate(${-width/2},${-height/2})`);
  // 画图标
  tooltips
    .append('rect')
    .attr('x',10)
    .attr('y',(_,i) => i*25 + 10)
    .attr('width',20)
    .attr('height',10)
    .attr("fill", (d) => color(d.data.name));

  // 画文字
  tooltips
    .append('text')
    .attr("transform",(_,i) => `translate(30,${i*25 + 10 + 10})`)
    // .attr('width',20)
    // .attr('height',10)
    .text((d) => d.data.name);
}


watch(selectTags, async (newVal, oldVal) => {

  // let response_data = await reqParallelDataOfStudentOrClass([], newVal, '_starttime','_endtime');
  // option.series.data = response_data.res_list_data;
  // option && myChart.setOption(option);
});
</script>

<template>
  <div id="sunburst-chart">
    <svg id="sunburst-svg"></svg>
  </div>
</template>

<style scoped>
#sunburst-chart {
  width: 100%;
  height: 100%;
  font-size: 12px;
}

</style>
